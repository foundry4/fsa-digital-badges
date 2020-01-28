from flask import Blueprint, Markup, request, redirect, render_template
from werkzeug import secure_filename
import markdown
import os
import tempfile
from .wiki import wiki_title, nav, style
from .github import commit, pull

upload = Blueprint('upload', __name__)


# Wiki file uploads

@upload.route('/', methods=['GET'])
def redirect_to_upload():
    return redirect("/upload")

@upload.route('/upload', methods=['GET'])
@upload.route('/Upload', methods=['GET'])
def upload_form():
    """ Form to upload images and other files to the wiki. """
    repo = os.getenv('GITHUB_REPO')
    return render_template('upload.html', 
        wiki_title=wiki_title(),
        title="Upload", 
        path="Upload", 
        nav=Markup(nav()),
        repo=repo
        )

@upload.route('/upload', methods=['POST'])
def upload_post():
    """ Process an uploaded file, then render a page that contains just the markdown and displays the file. """

    # Process the uploaded file
    upload = request.files.get('file')
    if upload:
        username = request.form.get("username")
        password = request.form.get("password")
        filename = secure_filename(upload.filename)
        with tempfile.NamedTemporaryFile(delete=False) as t:
            t.write(upload.read())
            temp = t.name

        # Commit to Github and, if successful, save locally:
        path = os.path.join('uploads', filename)
        print(f'attempting to commit {path} to Github')
        if commit(path, temp, username, password):
            # Render a page to show the upload
            extension = os.path.splitext(filename)[1].lower()
            md_filename = "upload_image.md" if extension in [".jpg", ".jpeg", ".gif", ".png"] else "upload_file.md"
            with open(f"default-pages/{md_filename}") as f:
                content = f.read()
            content = content.replace("{filename}", filename)
            md = markdown.markdown(content)
            html = style(md)
            
            return render_template('page.html', 
                wiki_title=wiki_title(),
                title="Upload", 
                path="Upload",
                content=Markup(html), 
                nav=Markup(nav()))
        else:
            print('Commit failed?')
    
    # Fallback
    return redirect(request.url)


import urllib 
import os
from git import Repo
from github import Github
from github.GithubException import UnknownObjectException, BadCredentialsException

def pull(username, password):

    if os.path.isdir(os.path.join('wiki', '.git')):
        # pull
        Repo('wiki').remotes.origin.pull(rebase=True)
    else:
        # clone
        repo = os.getenv('GITHUB_REPO')
        print(f"Repo: {repo}")
        url = f'https://{username}:{password}@github.com/{repo}.wiki.git'
        print(f"Cloning {url}")
        Repo.clone_from(url, 'wiki')
    
    # Wiki title - we may have set a custom one, so don't overwrite
    title = os.getenv('WIKI_TITLE')
    if title and not os.path.isfile(os.path.join('wiki', 'title.txt')):
        with open(os.path.join('wiki', 'title.txt'), 'w+') as f:
            f.write(title)

def commit(path, content, username, password, comment="Update"):

    # Check we have the latest version of the repo
    pull(username, password)
    if not os.path.isdir(os.path.join('wiki', 'uploads')):
        os.mkdir(os.path.join('wiki', 'uploads'))

    # Copy the content into the repo at path
    repo_path = os.path.join('wiki', path)
    with open(content, 'rb') as c, open(repo_path, 'wb') as p:
        p.write(c.read())

    # Add the path to the repo
    repo = Repo('wiki')
    repo.index.add(path)
    repo.index.commit(comment)

    # Push the change
    repo.remotes.origin.push()

    return True

# def gh_commit(path, content, username, password):

#     result = False
#     print(f'Committing path {path} to Github')
#     if os.path.isfile(content):
        
#         gh_username = urllib.parse.quote(username, safe='')
#         gh_password = urllib.parse.quote(password, safe='')
#         url = f'https://{gh_username}:{gh_password}@github.com/{repo}.wiki.git'
#         print(f"Github repo: {repo}, wiki url: https://{gh_username}:[{'yes' if gh_password else 'no'}]@github.com/{repo}.wiki.git.")

#         g = Github(password)
#         try:
#             print(f'Getting repo {repo}')
#             repository=g.get_repo(repo)
#         except UnknownObjectException:
#             print(f'Getting organisation repo {username}/{repo}')
#             repository=g.get_organization(username).get_repo(repo)
#         except BadCredentialsException:
#             print("Bad credentials for Github")
#         with open(content, 'rb') as t:
#             try:
#                 gh_contents = repository.get_contents(path, ref='master')
#                 print(f"Updating {path}")
#                 repository.update_file(path, "Wiki file update", t.read(), gh_contents.sha, branch='master')
#                 result = True
#             except UnknownObjectException:
#                 print(f"Creating {path}")
#                 repository.create_file(path, "Wiki file upload", t.read(), branch='master')
#                 result = True
#     return result
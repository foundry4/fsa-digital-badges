#!/usr/bin/env bash

export GITHUB_USERNAME=davidcarboni
export GITHUB_REPO=notbinary/fsa-digital-badges

# Run as a container for local test/development
docker build --tag fsa-digital-badges . && \
docker run -it --rm -p 5000:5000 \
    -e NOSSL=true \
    -e GITHUB_USERNAME \
    -e GITHUB_REPO \
    fsa-digital-badges

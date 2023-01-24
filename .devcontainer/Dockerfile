# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
# https://github.com/microsoft/vscode-dev-containers/tree/main/containers/python-3
ARG VARIANT=3-bullseye
FROM python:${VARIANT}
LABEL org.opencontainers.image.source https://github.com/oleksis/youtube-dl-gui
LABEL org.opencontainers.image.description="A cross platform front-end GUI of the popular youtube-dl written in wxPython."

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

ARG vscode
RUN if [[ -z "$devcontainercli" ]] ; then printf "\nERROR: This Dockerfile needs to be built with VS Code !" && exit 1; else printf "VS Code is detected: $devcontainercli"; fi

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends libgtk-3-dev libjpeg-dev libtiff-dev \
    libsdl2-dev libgstreamer-plugins-base1.0-dev libnotify-dev freeglut3 freeglut3-dev libsm-dev \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

CMD ["/bin/bash", "-l"]

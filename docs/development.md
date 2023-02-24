# Development notes

## Winget tools
- 7Zip
```pwsh
➜ winget install -e  --id 7zip.7zip
```

- Git
```pwsh
➜ winget install -e  --id Git.Git
```

- AzureCLI
```pwsh
# https://learn.microsoft.com/en-us/azure/devops/repos/git/share-your-code-in-git-cmdline?view=azure-devops#download-and-install-azure-cli-and-add-azure-devops-extension
➜ winget install -e  --id Microsoft.AzureCLI
➜ az --version
# set environment variable for current process
➜ $env:AZURE_DEVOPS_EXT_PAT = 'xxxxxxxxxx'
➜ az devops login --organization https://dev.azure.com/oleksis
➜ az devops configure --defaults organization=https://dev.azure.com/oleksis project=yt-dlg
➜ git remote add azure https://dev.azure.com/oleksis/yt-dlg/_git/yt-dlg
➜ git push azure master
```

- RealVNC.VNCViewer
```pwsh
➜ winget install -e --id RealVNC.VNCViewer
```

- Advanced Installer
```pwsh
➜ winget install -e --id Caphyon.AdvancedInstaller
```

### Winget Packages
- Update package manifest

```pwsh
➜ wingetcreate update --urls "https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.4/yt-dlg-20221113.1.msi|x64" --version 1.8.4 -s -t ghp_PERSONAL_TOKEN yt-dlg.yt-dlg
```

## Windows Development Environment
See
- [Notes](../README.md#Notes)
- [Python Launcher for Windows)](https://gist.github.com/oleksis/c22ed90daa922c1a072d2593a7f8d5b4)
```pwsh
➜ py -3.11 -m venv venv
➜ .\venv\Scripts\Activate.ps1
➜ py -c "import sys; print(sys.version, sys.executable, sep='\n')"
➜ py -m pip install -U pip wheel setuptools
# See Notes: [wxPython Windows artifacts for Python 3.7 to 3.11]
➜ iwr -Uri "<https://artprodcca1.artifacts.visualstudio.com-artifact-wxPython-4.2.1a1-cp311-cp311-win_amd64.whl>" -OutFile wxPython-4.2.1a1-cp311-cp311-win_amd64.whl
➜ py -m pip install wxPython-4.2.1a1-cp311-cp311-win_amd64.whl
➜ py -m pip install polib -r requirements/requirements.in
➜ py setup.py build_trans
➜ py -m youtube_dl_gui
```

### Tox
Use `pip install tox>=4.1.2` for test diferents Python versions from Microsoft Store (3.7, 3.8, 3.9, 3.10)

### Pyenv, Tox and py Launcher
See [Pyenv and Py Launcher](https://gist.github.com/oleksis/7cab1772862df71f73ce22b7515f6af3#environment-variable)
```pwsh
➜ pyenv install 3.7.9 3.8.10 3.9.13 3.10.10 3.11.1
➜ pyenv local 3.7.9 3.8.10 3.9.13 3.10.10 3.11.1
➜ python310 -m venv venv
➜ $env:VIRTUAL_ENV="${PWD}/venv"
➜ py -m pip install -e .[binaries]
➜ py -m pip install -r .\requirements\requirements-dev.in
➜ pyenv exec py -m tox
```

## Docker
- PyInstaller one dir
```pwsh
➜ pyinstaller -w -D --icon=youtube_dl_gui/data/pixmaps/youtube-dl-gui.ico --add-data="youtube_dl_gui/data;youtube_dl_gui/data" --add-data="youtube_dl_gui/locale;youtube_dl_gui/locale" --exclude-module=tests --version-file=file_version_info.txt --noconfirm --name=yt-dlg youtube_dl_gui/__main__.py
```
### ManyLinux
- [ PyInstaller on ManyLinux 2.28](https://github.com/oleksis/pyinstaller-manylinux)
```pwsh
➜ docker run --name yt-dlg -it -d --workdir /src -v ${pwd}:/src pyinstaller-manylinux -w -F --add-data=youtube_dl_gui/data:youtube_dl_gui/data --add-data=youtube_dl_gui/locale:youtube_dl_gui/locale --exclude-module=tests --name=yt-dlg youtube_dl_gui/__main__.py
```

- Interactive terminal typing (tty)
```pwsh
➜ docker run --name ytdlg-pyenv -it --entrypoint bash --workdir /src -v ${pwd}:/src pyinstaller-manylinux
```

## Dev Containers
Use `devcontainer` with dev container Features: [Light-weight Desktop (desktop-lite)](https://github.com/devcontainers/features/tree/main/src/desktop-lite#light-weight-desktop-desktop-lite)

VNC Sever
  - user: vscode
  - password: vscode

- Public devcontainer to Packages (GHCR)
Install `devcontainer`
```pwsh
npm install -g @devcontainers/cli
$env:PATH="$env:APPDATA\npm;$env:PATH"
devcontainer --version
```

[Example of building and publishing an image](https://code.visualstudio.com/docs/remote/devcontainer-cli#_prebuilding)
```bash
export CR_PAT='YOUR_TOKEN'
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
devcontainer build --workspace-folder . --push true --image-name ghcr.io/USERNAME/IMAGE-NAME:latest
devcontainer up --workspace-folder .
```

## Releases
Create a resume

- Compare from the lastest release
`https://github.com/oleksis/youtube-dl-gui/compare/v1.8.4...HEAD`

### Check
See all the Python base version from [`version-manifest.json`](https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json)
- Select the [Python](https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md#python) base
  - Python 3.10.y

### Python base
- 3.10.10
- Actions Setup-Python
	- GitHub Actions and [Azure UsePythonVersion](https://github.com/microsoft/azure-pipelines-tasks/blob/1be088a422530fbaa1a9ed7b5073ee665dcb8f53/Tasks/UsePythonVersionV0/installpythonversion.ts#LL11C23-L11C108)
	- [3.8.15, 3.9.9-win32-x64, 3.10.10-win32-x64](#check)

Search for 3.10.y in files like:
- Review 
  - `.github/workflows/release.yml` for Python base
  - `.azure/azure-pipelines-build.yml`
  - .python-version
  - setup.sh
  - file_version_info.txt
- Build
  - Build MSI from azure-pipelines
  - Build binary (pyinstaller) using [Windows embeddable package (64-bit)](https://www.python.org/ftp/python/3.10.10/python-3.10.10-embed-amd64.zip)
  - Build using [ManyLinux](#manylinux)


## Install Open Build Service in openSUSE Tumbleweed
- [Build RPMs in local from PyPI](https://gist.github.com/oleksis/cf45143457cb31f52ebfdcad77a895fe#build-rpms-in-local-from-pypi)

## Distros GNU/Linux with glibc 2.31
[Manylinux Timeline](https://mayeut.github.io/manylinux-timeline/)

- Fedora 32
- openSUSE Leap 15.3
- Debian 11 Bullseye
- Ubuntu 20.04 LTS (Focal Fossa)

## Extras
- wxPython using Wayland
```bash
GDK_BACKEND=x11 ./dist/yt-dlg
```

- [GitHub Actions: Deprecating save-state and set-output commands](https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/)

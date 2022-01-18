# Development notes

## PyInstaller one dir
```pwsh
pyinstaller -w -D --icon=youtube_dl_gui/data/pixmaps/youtube-dl-gui.ico --add-data="youtube_dl_gui/data;youtube_dl_gui/data" --add-data="youtube_dl_gui/locale;youtube_dl_gui/locale" --exclude-module=tests --version-file=file_version_info.txt --noconfirm --name=yt-dlg youtube_dl_gui/__main__.py
```

## Docker
- [ PyInstaller on ManyLinux 2.24](https://github.com/oleksis/pyinstaller-manylinux)
```pwsh
docker run --name yt-dlg -it -d --workdir /src -v ${pwd}:/src pyinstaller-manylinux -w -F --add-data=youtube_dl_gui/data:youtube_dl_gui/data --add-data=youtube_dl_gui/locale:youtube_dl_gui/locale --add-binary=libcrypt.so.2:. --exclude-module=tests --name=yt-dlg youtube_dl_gui/__main__.py
```

- Interactive terminal typing (tty)
```pwsh
docker run --name ytdlg-pyenv -it --entrypoint bash --workdir /src -v ${pwd}:/src pyinstaller-manylinux
```

## Winget tools
- RealVNC.VNCViewer
```pwsh
winget install -e --id RealVNC.VNCViewer
```

## Dev Containers
- Run desktop lite debian ENTRYPOINT for use VNC Sever

  - user: vscode
  - password: vscode

```bash
/usr/local/share/desktop-init.sh
```

## Tox
Use `pip install tox==4.0.0a8` for test diferents Python versions from Microsoft Store (3.7, 3.8, 3.9, 3.10)

## Install Open Build Service in openSUSE Tumbleweed
- [Build RPMs in local from PyPI](https://gist.github.com/oleksis/cf45143457cb31f52ebfdcad77a895fe#build-rpms-in-local-from-pypi)

## Distros GNU/Linux with glibc 2.31
[Manylinux Timeline](https://mayeut.github.io/manylinux-timeline/)

- Fedora 32
- openSUSE Leap 15.3
- Debian 11 Bullseye
- Ubuntu 20.04 LTS (Focal Fossa)

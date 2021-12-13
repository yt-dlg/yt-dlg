# Development notes

## PyInstaller one dir
```pwsh
pyinstaller -w -D --icon=youtube_dl_gui/data/pixmaps/youtube-dl-gui.ico --add-data="youtube_dl_gui/data;youtube_dl_gui/data" --add-data="youtube_dl_gui/locale;youtube_dl_gui/locale" --exclude-module=tests --name=yt-dlg youtube_dl_gui/__main__.py
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

## Install Open Build Service in openSUSE Tumbleweed
- [Build RPMs in local from PyPI](https://gist.github.com/oleksis/cf45143457cb31f52ebfdcad77a895fe#build-rpms-in-local-from-pypi)

---
permalink: /
redirect_from:
  - /Home
---
# yt-dlg
yt-dlg is a cross platform front-end GUI of the popular youtube-dl media downloader written in wxPython[¹][1]. It supports many sites[²][2] and allows you to download videos and audio from them. You can install it from PyPI[³][3], GitHub, [Microsoft Store](https://apps.microsoft.com/store/detail/ytdlg/XP9CCFSWS911F5), Winget or [Snap Store](https://snapcraft.io/yt-dlg).


## Screenshots
![yt-dlg UI Gif](https://raw.githubusercontent.com/oleksis/youtube-dl-gui/master/docs/img/yt-dlg_ui.gif)

## Downloads
* [Source (zip)](https://github.com/oleksis/youtube-dl-gui/archive/refs/tags/v1.8.5.zip)
* [Source (tar.gz)](https://github.com/oleksis/youtube-dl-gui/archive/refs/tags/v1.8.5.tar.gz)
* [Windows](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.5/yt-dlg-20230224.1.msi)
* [GNU/Linux](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.5/yt-dlg)
* [PyPI](https://pypi.org/project/yt-dlg/)

## Requirements
* [Python 3.7+](https://www.python.org/downloads/)
* [wxPython 4 Phoenix](https://wxpython.org/download.php)
* [PyPubSub](https://pypi.org/project/PyPubSub)
* [FFmpeg](https://ffmpeg.org/download.html) optional; to postprocess video files
* [polib](https://pypi.org/project/polib) optional; manipulate, create, modify gettext files (pot, po and mo)
* [PyInstaller](https://www.pyinstaller.org/) optional; to build binaries/executables
* [GNU gettext](https://www.gnu.org/software/gettext/) optional; to translations

## Installation
Source
```bash
python setup.py build_tran
python setup.py install
```

PyPI
```bash
pip install yt-dlg
```

[1]: <https://pypi.org/project/yt-dlg/> "yt-dlg · PyPI. Accessed 2/12/2023."
[2]: <http://ytdl-org.github.io/youtube-dl/supportedsites.html> "Supported sites. Accessed 2/17/2023."
[3]: <https://github.com/yt-dlg/yt-dlg> "GitHub - yt-dlg/yt-dlg: A cross platform front-end GUI of the popular .... Accessed 2/12/2023."

# yt-dlg
A cross platform front-end GUI of the popular [youtube-dl](https://rg3.github.io/youtube-dl/) media downloader written in wxPython. [Supported sites](https://rg3.github.io/youtube-dl/supportedsites.html)

## Screenshots
![youtube-dl-gui main window](https://raw.githubusercontent.com/MrS0m30n3/youtube-dl-gui/gh-pages/images/ydlg_ui.gif)

## Requirements
* [Python 3](https://www.python.org/downloads)
* [wxPython 4 Phoenix](https://wxpython.org/download.php)
* [TwoDict](https://pypi.org/project/twodict)
* [PyPubSub](https://pypi.org/project/PyPubSub)
* [polib](https://pypi.org/project/polib)
* [FFmpeg](https://ffmpeg.org/download.html) (optional, to postprocess video files)

### Requirement for build Binaries/Executables
* [PyInstaller](https://www.pyinstaller.org/)

### Optionals
* [GNU gettext](https://www.gnu.org/software/gettext/)

## Downloads
* [SHA2-256SUMS](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.2.0/SHA2-256SUMS)
* [youtube-dlg](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.2.0/youtube-dlg)
* [youtube-dlg.exe](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.2.0/youtube-dlg.exe)
* [Source (.zip)](https://github.com/oleksis/youtube-dl-gui/archive/v1.2.0.zip)
* [Source (.tar.gz)](https://github.com/oleksis/youtube-dl-gui/archive/v1.2.0.tar.gz)

## Installation

### Install From Source
* Download & extract the source
* Change directory into *yt-dlg-1.2.2*
* Create virtual environment 
```bash
make venv
```
* Activate virtual environment
```bash
source venv/bin/activate
```
* Install requirements, build translations and install
```bash
make install
```

## Binaries
Create binaries using [PyInstaller](https://www.pyinstaller.org/)
* Create virtual environment
```bash
make venv
```
* Activate virtual environment
```bash
source venv/bin/activate
```
* Install requirements, build translations and create binaries
```bash
make pyinstaller
```

## Run yt-dlg
* Activate virtual environment and run
```bash
source venv/bin/activate
yt-dlg
```

## Using pip3 on Debian 10:

Install the following packages and their dependences:

```bash
sudo apt-get install -y build-essential dpkg-dev \
             libgtk-3-dev libjpeg-dev libtiff-dev \
             libsdl2-dev libgstreamer-plugins-base1.0-dev \
             libnotify-dev freeglut3 freeglut3-dev \
             libsm-dev 
```

### Setting the virtual environment and activate

```bash
sudo apt-get install -y python3-venv
python3 -m pip install --upgrade pip setuptools wheel
python3 -m venv venv
source venv/bin/activate
```

### Install wxPython , requirements and yt-dlg
> See [Notes](#notes) for install wxPython on Ubuntu

```bash
pip3 install wxPython-4.1.1-cp37-cp37m-linux_x86_64.whl
pip3 install -r requirements.in
pip3 install --no-deps yt-dlg
yt-dlg 
```

### Comprobar wxPython 4

```bash
python3 -c "import wx ; print(wx.__version__)"
```

### List and configure Locales

```bash
locale -a
sudo dpkg-reconfigure locales
```

## Notes
An alternative to install wxPython 4 **Phoenix** from the Extras section

For Ubuntu 20.04

```bash
wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04/wxPython-4.1.0-cp38-cp38-linux_x86_64.whl
pip3 install wxPython-4.1.0-cp38-cp38-linux_x86_64.whl 
```

* [wxPython 4 builds on various linux distros with Vagrant](https://github.com/wxWidgets/Phoenix/blob/wxPy-4.0.x/vagrant/debian-9/bootstrap.sh)

* [Building wxPython for Linux via Pip](https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html)

## Contributing
* **Add support for new language:** See [localization howto](docs/localization_howto.md)
* **Report a bug:** See [issues](https://github.com/oleksis/yt-dlg/issues)

## Authors
See [AUTHORS](AUTHORS) file

## License
The [Public Domain License](LICENSE)

## Frequently Asked Questions
See [FAQs](docs/faqs.md) file

## Thanks
Thanks to everyone who contributed to this project and to [@philipzae](https://github.com/philipzae) for designing the new UI layout.

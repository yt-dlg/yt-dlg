[![Build Status](https://dev.azure.com/oleksis/yt-dlg/_apis/build/status/yt-dlg?repoName=yt-dlg&branchName=master)](https://dev.azure.com/oleksis/yt-dlg/_build/latest?definitionId=1&repoName=yt-dlg&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/oleksis/yt-dlg/1/master.svg)](https://dev.azure.com/oleksis/yt-dlg/_build/latest?definitionId=1&branchName=master)

# yt-dlg
A cross platform front-end GUI of the popular [youtube-dl](https://github.com/ytdl-org/youtube-dl/) media downloader written in wxPython. [Supported sites](https://github.com/ytdl-org/youtube-dl/supportedsites.html)

## Screenshots
![youtube-dl-gui main window](https://raw.githubusercontent.com/MrS0m30n3/youtube-dl-gui/gh-pages/images/ydlg_ui.gif)

## Requirements
* [Python 3](https://www.python.org/downloads)
* [wxPython 4 Phoenix](https://wxpython.org/download.php)
* [PyPubSub](https://pypi.org/project/PyPubSub)
* [FFmpeg](https://ffmpeg.org/download.html) (optional, to postprocess video files)

### Requirement for build Binaries/Executables
* [polib](https://pypi.org/project/polib)
* [PyInstaller](https://www.pyinstaller.org/)

### Optionals
* [GNU gettext](https://www.gnu.org/software/gettext/)

## Downloads
* [SHA2-256SUMS](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.3/SHA2-256SUMS)
* [yt-dlg](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.3/yt-dlg)
* [yt-dlg.exe](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.3/yt-dlg.exe)
* [yt-dlg-20220118.2.msi](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.3/yt-dlg-20220118.2.msi)
* [Source (.zip)](https://github.com/oleksis/youtube-dl-gui/archive/v1.8.3.zip)
* [Source (.tar.gz)](https://github.com/oleksis/youtube-dl-gui/archive/v1.8.3.tar.gz)

## Installation
In Windows install `make` using `winget`
```pwsh
winget install GnuWin32.Make
```

In GNU/Linux install `make`. Ubuntu:
```bash
sudo apt install make
```

### Install From Source
> ℹ️ The latest version compatible with Python 3.6.1 is [yt-dlg v1.8.2](https://github.com/oleksis/youtube-dl-gui/releases/tag/v1.8.2)
* Download & extract the source
* Change directory into *yt-dlg-1.8.3*
* Create virtual environment
```bash
make clean-requirements
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
make clean-requirements
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

> ℹ️ The default CLI Backend is `youtube-dl` if you have any issue you can change to `yt-dlp` CLI Backend in:
>
>   Settings -> Options -> Extra and change/select `yt-dlp`

## Windows 10 / 11
Install using `winget`
```pwsh
winget install -e --id yt-dlg.yt-dlg
```

## Debian 10
Install the following packages and their dependences:

```bash
sudo apt-get install -y build-essential dpkg-dev \
             libgtk-3-dev libjpeg-dev libtiff-dev \
             libsdl2-dev libgstreamer-plugins-base1.0-dev \
             libnotify-dev freeglut3 freeglut3-dev \
             libsm-dev python3-dev
```

### Setting the virtual environment and activate
```bash
sudo apt-get install -y python3-venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
```

### Install wxPython , requirements and yt-dlg
> * See [Notes](#notes) for install wxPython on Ubuntu
>
> * For install **wxPython on Debian 11 "bullseye"** download the wheel from the release:
>
>   [wxPython-4.1.1-cp39-cp39-linux_x86_64.whl](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.7.1/wxPython-4.1.1-cp39-cp39-linux_x86_64.whl)

```bash
pip3 install wxPython-4.1.1-cp37-cp37m-linux_x86_64.whl
pip3 install -r requirements/requirements.in
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

## openSUSE Tumbleweed
Install using `zypper`

### Open Build Service
```bash
sudo zypper ar -cfp 90 https://download.opensuse.org/repositories/home:oleksis.fraga/openSUSE_Tumbleweed/home:oleksis.fraga.repo
sudo zypper install python38-yt-dlg
yt-dlg
```

### With Python 3.8
The following steps can be executed if you use the Python version of the system (3.6, 3.8, 3.9)

```bash
sudo zypper dup  # Distribition Upgrade
sudo zypper -n update  # Non Interactive
sudo zypper -n install yum-utils
```

### Add openSUSE Factory repository for wxPython 4
```bash
sudo zypper addrepo -f http://download.opensuse.org/tumbleweed/repo/oss/ openSUSE-Factory
```

### Install wxPython 4 global (system level)
Need at least one font installed

```bash
sudo zypper -n install python38-wxPython google-opensans-fonts
```

### Install other dev packages/tools for Python 3.8
```bash
sudo zypper -n install python38-pip python38-setuptools python38-devel python38-tools python38-virtualenv python38-requests
```

### Install `yt-dlg` global from PyPI
```bash
pip3 install yt-dlg
```

### Add `yt-dlg` executable to the PATH and run
```bash
PATH=$HOME/.local/bin:$PATH
yt-dlg
```

## openSUSE 15.3
We need build **wxPython 4.1.1** for **Python 3.6**

> * For install **wxPython on openSUSE 15.3** download the wheel from the release:
>
>   [wxPython-4.1.1-cp36-cp36m-linux_x86_64.whl](https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.1/wxPython-4.1.1-cp36-cp36m-linux_x86_64.whl)

### Dev Tools
```bash
sudo zypper -n install -t pattern devel_basis
sudo zypper -n install gcc-c++
sudo zypper -n install git wget
```

### Requirement for install Python from source (Build dependencies)
```bash
sudo zypper -n install \
    readline-devel sqlite3-devel libbz2-devel \
    zlib-devel libopenssl-devel libffi-devel \
    ncurses-devel tk-devel libgdbm4 \
    ca-certificates gcc
```

### Install wxPython 4 Dependencies
```bash
sudo zypper -n install \
    gtk3-devel gtk3-tools webkit2gtk3-devel \
    libjbig2 libjbig-devel libjpeg8 libjpeg8-devel \
    libpng16-16 libpng16-devel libtiff-devel \
    libSDL2-2_0-0 libSDL2-devel libSM6 libSM-devel\
    gstreamer gstreamer-devel gstreamer-plugins-base-devel \
    freeglut-devel libnotify4 libnotify-devel \
    libSM6 libSM-devel liblzma5 libXtst6 libXv1 \
    gdk-pixbuf-loader-rsvg gdk-pixbuf-query-loaders \
```

### Install Pyenv
```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $HOME/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> $HOME/.bashrc
echo 'eval "$(pyenv init -)"' >> $HOME/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bashrc
source $HOME/.bashrc
```

### Custom Python build with `--enable-shared`
```bash
PYTHON_CONFIGURE_OPTS="--enable-shared" \
    pyenv install 3.6.13

pyenv shell 3.6.13
```

### Add python-config to the PATH
```bash
PATH=$(pyenv root)/versions/${PYENV_VERSION}/bin:$PATH
```

### Install requirements and run `yt-dlg`
```bash
python -m pip install --upgrade pip six setuptools wheel
python -m pip install -r requirements/requirements.in
pip install yt-dlg
yt-dlg
```

### List locales
```bash
locale  -av
```

### Windows Subsystem for Linux
Some issues is possible. Can read more in: [Troubleshooting GUI Linux apps on openSUSE on WSLg](https://boxofcables.dev/why-do-apps-look-weird-on-wslg-on-opensuse/)

```bash
sudo zypper -n install --no-recommends -t pattern gnome
sudo /usr/bin/gdk-pixbuf-query-loaders-64 --update-cache
```

## Mageia 8
Exists a third-party repository for Mageia 8 that have a rpm package for youtube-dl-gui.
The repository comes from [BlogDrake](https://blogdrake.net/) The Official Community for Spanish Talking Users

### Instructions
First you have to configure the Official Mageia repositories then

For i586 - 32bit systems
```
su -
urpmi.addmedia --wget --distrib https://ftp.blogdrake.net/mageia/mageia8/i586
urpmi yt-dlg
exit
```
For x86_64 - 64bit systems
```
su -
urpmi.addmedia --wget --distrib https://ftp.blogdrake.net/mageia/mageia8/x86_64
urpmi yt-dlg
exit
```

### Source and RPM on Mageia 8
* [SRC](https://ftp.blogdrake.net/mageia/mageia8/free/SRPMS/yt-dlg-1.8.2-1bdk_mga8.src.rpm)
* [RPM](https://ftp.blogdrake.net/mageia/mageia8/free/noarch/yt-dlg-1.8.2-1bdk_mga8.noarch.rpm)

## Notes
An alternative to install wxPython 4 **Phoenix** from the Extras section

For Ubuntu 20.04

```bash
wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04/wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
pip3 install wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
```

* [wxPython 4 builds on various linux distros with Vagrant](https://github.com/wxWidgets/Phoenix/blob/wxPy-4.0.x/vagrant/debian-9/bootstrap.sh)

* [Building wxPython for Linux via Pip](https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html)

* [Building wxPython4 with Docker](https://github.com/wxWidgets/Phoenix/blob/master/docker/build/debian-10/Dockerfile#L25)

* [Compile wxPython 4.1.2a1 using Microsoft C++ Build Tools 2019](https://gist.github.com/oleksis/8637f096b97e18e00786e46465e97b34)

## Contributing
* **Add support for new language:** See [localization howto](docs/localization_howto.md)
* **Report a bug:** See [issues](https://github.com/oleksis/youtube-dl-gui/issues)

<a href="https://www.buymeacoffee.com/oleksis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## Authors
See [AUTHORS](AUTHORS) file

## License
The [Public Domain License](LICENSE)

## Frequently Asked Questions
See [FAQs](docs/faqs.md) file

## Thanks
Thanks to everyone who contributed to this project and to [@philipzae](https://github.com/philipzae) for designing the new UI layout.

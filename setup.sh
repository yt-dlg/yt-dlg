#!/bin/bash
# Setup for PyInstaller ManyLinux 2.28 Docker Action
# https://github.com/oleksis/pyinstaller-manylinux

# Fail on errors.
set -e

PYTHON_VERSION=3.10
PYINSTALLER_VERSION=5.13.0

# libpng16
curl -L -O -C - https://newcontinuum.dl.sourceforge.net/project/libpng/libpng16/1.6.40/libpng-1.6.40.tar.gz
tar -xzf libpng-1.6.40.tar.gz
pushd libpng-1.6.40
./configure
make
make install
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib/
popd
rm -rf libpng-1.6.40 libpng-1.6.40.tar.gz

# libjpeg8
dnf -y install --allowerasing cmake nasm

curl -L -O -C - https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/3.0.0.tar.gz
tar -xzf 3.0.0.tar.gz
pushd libjpeg-turbo-3.0.0
cmake -G"Unix Makefiles" -DWITH_JPEG8=1 .
make
make install
LD_LIBRARY_PATH=/opt/libjpeg-turbo/lib64/:${LD_LIBRARY_PATH}
popd
rm -rf libjpeg-turbo-3.0.0 3.0.0.tar.gz

echo "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}" >> ${HOME}/.bashrc

# Install wxPython 4 Dependencies
dnf -y update

dnf install -y \
	freeglut-devel \
	gstreamer1-devel \
	gstreamer1-plugins-base-devel \
	gtk3-devel \
	libjpeg-turbo-devel \
	libnotify-devel \
	libpng-devel \
	libSM-devel \
	libtiff-devel \
	libXtst-devel \
	SDL-devel \
	webkit2gtk3-devel \
	which

# Simple DirectMedia Layer 2
dnf install -y SDL2-devel

# Perl-compatible regular expression library 2
dnf install -y pcre2 pcre2-devel

dnf clean all
rm -rf /var/cache/yum

pyenv virtualenv ${PYTHON_VERSION}.12 venv310
pyenv local venv310
pyenv exec python -m pip install --upgrade pip six setuptools wheel

curl -L -O -C - https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04/wxPython-4.2.1-cp310-cp310-linux_x86_64.whl
pyenv exec pip install wxPython-4.2.1-cp310-cp310-linux_x86_64.whl
# Install requirements here
pyenv exec pip install --upgrade pyinstaller==$PYINSTALLER_VERSION
pyenv exec pip install polib -r requirements/requirements.in
# Build Translations
pyenv exec python setup.py build_trans

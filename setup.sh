#!/bin/bash
# Setup for PyInstaller ManyLinux 2.28 Docker Action
# https://github.com/oleksis/pyinstaller-manylinux

# Fail on errors.
set -e

PYTHON_VERSION=3.8
PYINSTALLER_VERSION=5.6.2

# libpng12
curl -L -O -C - https://sourceforge.net/projects/libpng/files/libpng12/1.2.59/libpng-1.2.59.tar.gz
tar -xzf libpng-1.2.59.tar.gz
pushd libpng-1.2.59
./configure
make
make install
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib/
popd
rm -rf libpng-1.2.59 libpng-1.2.59.tar.gz

# libjpeg8
dnf -y install --allowerasing cmake nasm

curl -L -O -C - https://sourceforge.net/projects/libjpeg-turbo/files/2.1.1/libjpeg-turbo-2.1.1.tar.gz
tar -xzf libjpeg-turbo-2.1.1.tar.gz
pushd libjpeg-turbo-2.1.1
cmake -G"Unix Makefiles" -DWITH_JPEG8=1 .
make
make install
LD_LIBRARY_PATH=/opt/libjpeg-turbo/lib64/:${LD_LIBRARY_PATH}
popd
rm -rf libjpeg-turbo-2.1.1 libjpeg-turbo-2.1.1.tar.gz

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

dnf clean all
rm -rf /var/cache/yum

pyenv virtualenv ${PYTHON_VERSION}.15 venv38
pyenv local venv38
pyenv exec python -m pip install --upgrade pip six setuptools wheel

curl -L -O -C - https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04/wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
pyenv exec pip install wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
# Install requirements here
pyenv exec pip install --upgrade pyinstaller==$PYINSTALLER_VERSION
pyenv exec pip install -r requirements/requirements.in
# Build Translations
pyenv exec python setup.py build_trans

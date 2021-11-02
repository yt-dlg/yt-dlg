#!/bin/bash -i
# Fail on errors.
set -e

# Setup on Centos 7 ManyLinux 2014
PYTHON_VERSION=3.8
PYINSTALLER_VERSION=4.6

# Work in venv
python$PYTHON_VERSION -m venv venv
. venv/bin/activate
python$PYTHON_VERSION -m pip install --upgrade pip six setuptools wheel

# Requirement for install Python from source
yum -y install gcc openssl-devel bzip2-devel libffi-devel

# Devtoolset 10
yum -y install devtoolset-10-gcc devtoolset-10-gcc-c++ devtoolset-10-dyninst-devel

# libpng16
wget --no-check-certificate https://sourceforge.net/projects/libpng/files/libpng16/1.6.37/libpng-1.6.37.tar.gz
tar xvf libpng-1.6.37.tar.gz
cd libpng-1.6.37
./configure
make
make install
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
cd ..

## Instal GNU/GCC 10
#yum -y install gmp-devel mpfr-devel libmpc-devel

#wget --no-check-certificate https://ftp.gnu.org/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.gz
#tar xvf gcc-10.2.0.tar.gz
#cd gcc-10.2.0
#./configure --disable-multilib --enable-languages=c,c++ --prefix=$HOME/local
#make
#make install
#PATH=/root/local/bin:$PATH
#LD_LIBRARY_PATH=/root/local/lib64/:$LD_LIBRARY_PATH:/usr/local/lib/
#cd ..

## Devtoolset 8
#yum -y install devtoolset-8-gcc devtoolset-8-gcc-c++

## Install GLIBC 2.28
#wget --no-check-certificate https://ftp.gnu.org/gnu/glibc/glibc-2.28.tar.gz
#tar xvf glibc-2.28.tar.gz
#cd glibc-2.28
#mkdir build
#cd build
#../configure --prefix=/opt/glibc-2.28
#make
#make install

# Install wxPython 4 Dependencies
yum -y install gtk3 gtk3-devel \
    webkitgtk3 webkitgtk3-devel \
    libjpeg-turbo-devel libpng-devel libtiff-devel \
    SDL SDL-devel gstreamer gstreamer-devel gstreamer-plugins-base-devel \
    freeglut freeglut-devel libnotify libnotify-devel libSM-devel

# Install wget in Centos 7
yum install -y wget

# Install pre-requirements like wxPython (Python 3.8)
# on PyInstaller ManyLinux 2014 Docker Action
wget --no-check-certificate https://extras.wxpython.org/wxPython4/extras/linux/gtk3/centos-8/wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
pip$PYTHON_VERSION install wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
# Install requirements here
pip$PYTHON_VERSION install --upgrade pyinstaller==$PYINSTALLER_VERSION
pip$PYTHON_VERSION install -r requirements/requirements.in
# Build Translations
python$PYTHON_VERSION setup.py build_trans

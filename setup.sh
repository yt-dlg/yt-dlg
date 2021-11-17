#!/bin/bash
# Setup for PyInstaller ManyLinux 2.24 Docker Action
# https://github.com/oleksis/pyinstaller-manylinux

# Fail on errors.
set -e

PYTHON_VERSION=3.8
PYINSTALLER_VERSION=4.6

LD_LIBRARY_PATH=${OPENSSL_DIR}/lib
PATH="${OPENSSL_DIR}:$PATH"

# libpng12
wget https://sourceforge.net/projects/libpng/files/libpng12/1.2.59/libpng-1.2.59.tar.gz
tar -xzf libpng-1.2.59.tar.gz
pushd libpng-1.2.59
./configure
make
make install
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib/
popd
rm -rf libpng-1.2.59 libpng-1.2.59.tar.gz

# libjpeg8
apt-get install -y nasm cmake

wget https://sourceforge.net/projects/libjpeg-turbo/files/2.1.1/libjpeg-turbo-2.1.1.tar.gz
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
apt-get update

apt-get install -y libgtk2.0-dev libgtk-3-dev
apt-get install -y libjpeg-dev libtiff-dev \
	libsdl1.2-dev libgstreamer-plugins-base1.0-dev \
	libnotify-dev freeglut3 freeglut3-dev libsm-dev \
	libwebkitgtk-dev libwebkitgtk-3.0-dev

# Simple DirectMedia Layer 2
apt-get install -y libsdl2-dev

CPPFLAGS="-O2 -I${OPENSSL_DIR}/include" CFLAGS="-I${OPENSSL_DIR}/include" \
	LD_FLAGS="-L${OPENSSL_DIR}/lib -Wl,-rpath,${OPENSSL_DIR}/lib" LD_RUN_PATH="${OPENSSL_DIR}/lib" \
	CONFIGURE_OPTS="--with-openssl=${OPENSSL_DIR}" PYTHON_CONFIGURE_OPTS="--enable-shared" \
	pyenv install $PYTHON_VERSION.3

pyenv virtualenv ${PYTHON_VERSION}.3 venv38
pyenv local venv38
pyenv exec python -m pip install --upgrade pip six setuptools wheel

# Install pre-requirements like wxPython (Python 3.8)
# on PyInstaller ManyLinux 2.24 Docker Action
wget -c https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04/wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
pyenv exec pip install wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
# Install requirements here
pyenv exec pip install --upgrade pyinstaller==$PYINSTALLER_VERSION
pyenv exec pip install -r requirements/requirements.in
# Build Translations
pyenv exec python setup.py build_trans
# Copy libcrypt.so.2 required by libpython3.8.so.1.0
cp -f /usr/local/lib/libcrypt.so.2 .

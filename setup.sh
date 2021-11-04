#!/bin/bash -i
# Fail on errors.
set -e

# Setup on Debian 9 ManyLinux 2.24
PYTHON_VERSION=3.8
PYINSTALLER_VERSION=4.6

MANYLINUX_CPPFLAGS="-Wdate-time -D_FORTIFY_SOURCE=2"
MANYLINUX_CFLAGS="-g -O2 -Wall -fdebug-prefix-map=/=. -fstack-protector-strong -Wformat -Werror=format-security"
MANYLINUX_CXXFLAGS="-g -O2 -Wall -fdebug-prefix-map=/=. -fstack-protector-strong -Wformat -Werror=format-security"
MANYLINUX_LDFLAGS="-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,z,now"

# Install wget in Debian 9
apt-get install -y wget

# Requirement for install Python from source (Build dependencies)
apt-get install -y make checkinstall build-essential \
	libreadline-dev libncursesw5-dev libbz2-dev \
	libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
	libffi-dev zlib1g-dev curl llvm xz-utils \
	libxml2-dev libxmlsec1-dev liblzma-dev \
	git upx ca-certificates

# Install Python
#wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
#tar xzf Python-3.8.12.tgz
#cd Python-3.8.12
#./configure --enable-optimizations
#make altinstall
#cd ..

# openssl 1.1.1
apt-get -y remove libssl-dev
export OPENSSL_DIR=/usr/local/ssl
wget https://www.openssl.org/source/openssl-1.1.1.tar.gz
tar -xzf openssl-1.1.1.tar.gz
cd openssl-1.1.1
./config --prefix=$OPENSSL_DIR --openssldir=$OPENSSL_DIR shared zlib
make
make install
LD_LIBRARY_PATH=$OPENSSL_DIR/lib
PATH="$OPENSSL_DIR:$PATH"
cd ..

# libpng12
wget https://sourceforge.net/projects/libpng/files/libpng12/1.2.59/libpng-1.2.59.tar.gz
tar -xzf libpng-1.2.59.tar.gz
cd libpng-1.2.59
./configure
make
make install
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
cd ..

# libjpeg8
apt-get install -y nasm cmake

wget https://sourceforge.net/projects/libjpeg-turbo/files/2.1.1/libjpeg-turbo-2.1.1.tar.gz
tar -xzf libjpeg-turbo-2.1.1.tar.gz
cd libjpeg-turbo-2.1.1
cmake -G"Unix Makefiles" -DWITH_JPEG8=1 .
make
make install
LD_LIBRARY_PATH=/opt/libjpeg-turbo/lib64/:$LD_LIBRARY_PATH
cd ..

# Install wxPython 4 Dependencies
apt-get update

apt-get install -y libgtk2.0-dev libgtk-3-dev
apt-get install -y libjpeg-dev libtiff-dev \
	libsdl1.2-dev libgstreamer-plugins-base1.0-dev \
	libnotify-dev freeglut3 freeglut3-dev libsm-dev \
	libwebkitgtk-dev libwebkitgtk-3.0-dev

# Simple DirectMedia Layer 2
apt-get install -y libsdl2-dev

# Pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
. ~/.bashrc
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
CPPFLAGS="-O2 -I$OPENSSL_DIR/include" CFLAGS="-I$OPENSSL_DIR/include" \
	LD_FLAGS="-L$OPENSSL_DIR/lib -Wl,-rpath,$OPENSSL_DIR/lib" LD_RUN_PATH="$OPENSSL_DIR/lib" \
	CONFIGURE_OPTS="--with-openssl=$OPENSSL_DIR" PYTHON_CONFIGURE_OPTS="--enable-shared" \
	pyenv install $PYTHON_VERSION.3
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# Work in venv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
. ~/.bashrc

# Reload the shell (NO in GitHub Actions)
# exec "$SHELL"

PYTHON_VERSION=3.8
PYINSTALLER_VERSION=4.6

pyenv virtualenv $PYTHON_VERSION.3 venv38
pyenv local venv38
pyenv exec python$PYTHON_VERSION -m pip install --upgrade pip six setuptools wheel

# Install pre-requirements like wxPython (Python 3.8)
# on PyInstaller ManyLinux 2.24 Docker Action
wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04/wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
pyenv exec pip$PYTHON_VERSION install wxPython-4.1.1-cp38-cp38-linux_x86_64.whl
# Install requirements here
pyenv exec pip$PYTHON_VERSION install --upgrade pyinstaller==$PYINSTALLER_VERSION
pyenv exec pip$PYTHON_VERSION install -r requirements/requirements.in
# Build Translations
pyenv exec python$PYTHON_VERSION setup.py build_trans
# Copy libcrypt.so.2 required by libpython3.8.so.1.0
cp /usr/local/lib/libcrypt.so.2 .
alias pyinstaller="pyenv exec pyinstaller"

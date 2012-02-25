#!/bin/zsh
# Extracts the Chrome PDF viewer and copies it so Chromium uses it
# Adapt this if your chromium is located e.g. at /usr/lib/chromium-browser
CHROMIUMPATH=/usr/lib/chromium
# Choose one: unstable, beta, stable
CRELEASE=beta

ARCHSTRING=$(uname -m)
if [[ $ARCHSTRING == "x86_64" ]]; then
	ARCH=amd64
elif [[ $ARCHSTRING == "i686" ]]; then
	ARCH=i386
else
	echo "could not determine platform"
	return 1
fi

TEMPDIR=`mktemp -d`
pushd $TEMPDIR
echo "Downloading current chrome ${CRELEASE} for ${ARCH}..."
wget "http://dl.google.com/linux/direct/google-chrome-${CRELEASE}_current_${ARCH}.deb"
echo "Extracting..."
# If you're not using a system with Debian package management, you might want to use ar xv and lzma -df and tar xvf instead
dpkg -x google-chrome-${CRELEASE}_current_${ARCH}.deb .
echo "Installing libpdf.so to ${CHROMIUMPATH}..."
sudo install -Dm 755 ./opt/google/chrome/libpdf.so ${CHROMIUMPATH}/libpdf.so
popd
rm -r $TEMPDIR

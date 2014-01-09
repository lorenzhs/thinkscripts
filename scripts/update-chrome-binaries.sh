#!/bin/zsh
# Extracts the Chrome PDF viewer and copies it so Chromium uses it
# Adapt this if your chromium is located e.g. at /usr/lib/chromium-browser
CHROMIUMPATH=/usr/lib/chromium
# Choose one: unstable, beta, stable
CRELEASE=stable

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
wget "https://dl-ssl.google.com/linux/direct/google-chrome-${CRELEASE}_current_${ARCH}.deb"
echo "Extracting..."
# If you're not using a system with Debian package management, you might want to use ar xv and lzma -df and tar xvf instead
dpkg -x google-chrome-${CRELEASE}_current_${ARCH}.deb .
echo "Backing up current libpdf.so..."
sudo mv ${CHROMIUMPATH}/libpdf.so ${CHROMIUMPATH}/libpdf.so.old
echo "Installing libpdf.so to ${CHROMIUMPATH}..."
sudo install -Dm 755 ./opt/google/chrome/libpdf.so ${CHROMIUMPATH}/libpdf.so
echo "Backing up current Pepper Flash..."
if [[ -d ${CHROMIUMPATH}/PepperFlash_old ]]; then
	sudo rm -r ${CHROMIUMPATH}/PepperFlash_old
fi
sudo mv ${CHROMIUMPATH}/PepperFlash ${CHROMIUMPATH}/PepperFlash_old
echo "Installing new Pepper Flash to ${CHROMIUMPATH}/PepperFlash..."
sudo install -d ${CHROMIUMPATH}/PepperFlash
sudo install -m644 ./opt/google/chrome/PepperFlash/* ${CHROMIUMPATH}/PepperFlash
popd
rm -r $TEMPDIR

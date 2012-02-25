#!/bin/zsh
# Extracts the Chrome PDF viewer and copies it so Chromium uses it
# Adapt this if your chromium is located e.g. at /usr/lib/chromium-browser
CHROMIUMPATH=/usr/lib/chromium

TEMPDIR=`mktemp -d`
pushd $TEMPDIR
echo "Downloading current chrome amd64 beta..."
wget "http://dl.google.com/linux/direct/google-chrome-beta_current_amd64.deb"
echo "Extracting..."
dpkg -x google-chrome-beta_current_amd64.deb .
echo "Copying libpdf.so to $CHROMIUMPATH..."
sudo cp opt/google/chrome/libpdf.so $CHROMIUMPATH
popd
rm -r $TEMPDIR

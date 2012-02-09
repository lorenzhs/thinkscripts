#!/bin/zsh
# Extracts the Chrome PDF viewer and copies it so Chromium uses it

TEMPDIR=`mktemp -d`
pushd $TEMPDIR
echo "Downloading current chrome amd64 beta..."
wget "http://dl.google.com/linux/direct/google-chrome-beta_current_amd64.deb"
echo "Extracting..."
dpkg -x google-chrome-beta_current_amd64.deb .
echo "Copying libpdf.so to /usr/lib/chromium-browser..."
sudo cp opt/google/chrome/libpdf.so /usr/lib/chromium-browser/
popd
rm -r $TEMPDIR

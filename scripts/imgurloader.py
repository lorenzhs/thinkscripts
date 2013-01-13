#!/usr/bin/env python
# encoding: utf-8
"""
imguralbum.py - Download a whole imgur album or account in one go.

MIT License
Copyright Alex Gisby <alex@solution10.com>, Lorenz H-S <thinkscripts@4z2.de>
"""

import sys
import re
import urllib
import os
import math

help_message = '''
Quickly and easily download an album or account from Imgur.

Format:
    $ python imguralbum.py [album or account URL] [destination folder]

Example:
    $ python imguralbum.py http://imgur.com/a/uOOju#6 ~/album
    $ python imguralbum.py http://username.imgur.com ~/my_account

If you omit the dest folder name, the utility will use the album ID or account name and create it in the cwd.

The albums in an account will be saved into individual folders with the album title as folder name.

'''


class ImgurException(Exception):
    def __init__(self, msg=False):
        self.msg = msg

class ImgurAccountDownloader:
    def __init__(self, account_url, output_messages=False, skip_existing=False):
        """
        Constructor. Pass in the account_url. Seeing as this is mostly a shell tool, you can have
        the class output messages too.
        """
        self.account_url = account_url
        self.output_messages = output_messages
        self.skip_existing = skip_existing
        match = re.match('http\:\/\/([a-zA-Z0-9]+)\.imgur.com/?', account_url)
        if not match:
            raise ImgurException("URL must be a valid Imgur User Account")
        self.username = match.group(1)

        self.response = urllib.urlopen(account_url)
        if self.response.getcode() != 200:
            raise ImgurException("Error reading Imgur: Error Code %d" % self.response.getcode())

    def save_albums(self, base_folder=None):
        """
        Downloads the albums of the given user into a base folder
        """
        html = self.response.read()
        #self.albums = re.findall('<a href="//imgur.com/a/([a-zA-Z0-9]+)">',html)
        self.albums = re.findall('<div id="album-([a-zA-Z0-9]+)" data-title="(.+)" data-cover="[a-zA-Z0-9]+.jpg" data-layout="[a-z]*" data-privacy="[0-9]*" data-description=".*" class="album ">', html)

        if self.output_messages:
            print "Found %d albums in user %s" % (len(self.albums), self.username)

        # Try and create the base folder:
        base_folder = base_folder or self.username

        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        # And finally loop through and save the albums:
        for (counter, (albumid, desc)) in enumerate(self.albums, start=1):
            if self.output_messages:
                print "Fetching Album %i: %s (%s)..." % (counter, desc, albumid),

            album_url = "http://imgur.com/a/%s" % albumid
            album_folder = os.path.join(base_folder, desc)

            if self.skip_existing and os.path.exists(album_folder):
                if self.output_messages:
                    print "Album has already been downloaded, skipping!"
                continue
            loader = ImgurAlbumDownloader(album_url, False, True)
            loader.save_images(album_folder)

        if self.output_messages:
            print ""
            print "Done!"


class ImgurAlbumDownloader:
    def __init__(self, album_url, output_messages=False, few_messages=False):
        """
        Constructor. Pass in the album_url. Seeing as this is mostly a shell tool, you can have the
        class output messages too.
        """
        self.album_url = album_url
        self.output_messages = output_messages
        self.few_messages = few_messages

        # Check the URL is actually imgur:
        match = re.match('http\:\/\/(www\.)?imgur\.com/a/([a-zA-Z0-9]+)(#[0-9]+)?', album_url)
        if not match:
            raise ImgurException("URL must be a valid Imgur Album")

        self.album_key = match.group(2)

        # Read the no-script version of the page for all the images:
        noscriptURL = 'http://imgur.com/a/' + match.group(2) + '/noscript'
        self.response = urllib.urlopen(noscriptURL)

        if self.response.getcode() != 200:
            raise ImgurException("Error reading Imgur: Error Code %d" % self.response.getcode())

    def save_images(self, foldername=None):
        """
        Saves the images from the album into a folder given by foldername.
        If no foldername is given, it'll use the album key from the URL.
        """
        html = self.response.read()
        matches = re.findall('<img src="http\:\/\/i\.imgur\.com\/([a-zA-Z0-9]{5})h?\.(jpg|jpeg|png|gif)"', html)
        self.images = [('http://i.imgur.com/%s.%s' % (img[0], img[1]), '%s.%s' % (img[0], img[1]), img[1]) for img in matches]

        if self.output_messages or self.few_messages:
            print "Found %d images in album, downloading" % len(self.images),

        # Try and create the album folder:
        albumFolder = foldername or self.album_key
        if not os.path.exists(albumFolder):
            os.makedirs(albumFolder)

        # And finally loop through and save the images:
        digits = int(math.ceil(math.log(len(self.images) + 1, 10)))
        for (counter, image) in enumerate(self.images, start=1):
            if self.output_messages:
                print "Fetching Image: " + image[0]
            elif self.few_messages:
                sys.stdout.write( ".")
                sys.stdout.flush()
            prefix = "%0*d-" % (digits, counter)
            path = os.path.join(albumFolder, prefix + image[1])

            attempt = 1
            while attempt < 3:
                try:
                    urllib.urlretrieve(image[0], path)
                    break
                except IOError as e:
                    print "Error downloading image %i: Failed to save %s to %s, attempt %i" % (counter, image[0], path, attempt)
                    attempt += 1
            else:
                print "Failed to download image"

        if self.output_messages:
            print ""
            print "Done!"
        elif self.few_messages:
            print " done"


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        # Print help message and exit
        print help_message
        exit()

    try:
        if re.match('http\:\/\/([a-zA-Z0-9]+)\.imgur.com/?', args[1]):
            # Download a whole account
            downloader = ImgurAccountDownloader(args[1], True, True)
            folder = args[2] if len(args) == 3 else None
            downloader.save_albums(folder)
        else:
            # Download an album
            downloader = ImgurAlbumDownloader(args[1], output_messages=True)
            folder = args[2] if len(args) == 3 else None
            downloader.save_images(folder)
    except ImgurException as e:
        print "Error:", e.msg, "\n\n", help_message
        exit(1)

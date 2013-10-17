#!/usr/bin/env python

import os
import HTMLParser
import argparse

from anonbrowser import AnonBrowser


parser = argparse.ArgumentParser(
    description='Download all images from an url')
parser.add_argument('-u', '--url', dest='target_url', help='URL we are going to fetch images from',
                    default='http://xkcd.com/')
parser.add_argument('-d', '--directory', dest='dir', help='directory images will be downloaded to',
                    default='images')


class ImageParser(HTMLParser.HTMLParser):
    def __init__(self):
        self.images = set()
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.images.add(attr[1])

    @staticmethod
    def get_images_from_html(data):
        parser = ImageParser()
        parser.feed(data)
        return list(parser.images)


def mirror_images(url, dir):
    if not os.path.isdir(dir):
        print "No such directory: %s" % dir
        return

    ab = AnonBrowser()
    page = ab.open(url)
    html = page.read()
    image_links = ImageParser.get_images_from_html(html)
    for image_link in image_links:
        filename = image_link.lstrip('http://')
        filename = filename.replace('/', '_')
        filename = os.path.join(dir, filename)
        data = ab.open(image_link).read()
        print '[*] Saving %s' % filename
        with open(filename, 'wb') as f:
            f.write(data)


def main():
    args = parser.parse_args()
    url = args.target_url
    dir = args.dir
    print 'Saving all images found on %s in directory %s' % (url, dir)
    mirror_images(url, dir)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import argparse
import HTMLParser

from anonbrowser import AnonBrowser


parser = argparse.ArgumentParser(
    description='Parse links present on a given url')
parser.add_argument('-u', '--url', dest='target_url', help='URL we are going to fetch links from',
                    default='https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs')


class LinkParser(HTMLParser.HTMLParser):
    def __init__(self):
        self.links = set()
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.add(attr[1])

    @staticmethod
    def get_links_from_html(data):
        parser = LinkParser()
        parser.feed(data)
        return list(parser.links)


def parse_link_from_tag(tag):
    html_link = str(tag)
    if 'href=' not in html_link:
        return None
    parsed_link = html_link[html_link.index('href=') + len('href='):]
    parsed_link = parsed_link.lstrip('"')
    parsed_link = parsed_link[:parsed_link.index('"')]
    return parsed_link


def parse_links(url):
    ab = AnonBrowser()
    ab.anonymize()
    page = ab.open(url)
    html = page.read()
    return LinkParser.get_links_from_html(html)


def main():
    args = parser.parse_args()
    url = args.target_url
    links = parse_links(url)
    links = '\n'.join(links)

    print 'Links fetched from %s:' % url
    print links


if __name__ == '__main__':
    main()

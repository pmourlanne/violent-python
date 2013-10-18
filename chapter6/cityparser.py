import HTMLParser
import re
import argparse

from anonbrowser import AnonBrowser


parser = argparse.ArgumentParser(
    description='Tries to parse cities present on a given wikipedia page and saves the output in a file')
parser.add_argument('-u', '--url', dest='target_url', help='URL we are going to fetch links from',
                    default='https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')
parser.add_argument('-f', '--file', dest='target_file', help='file the cities\' names will be saved to',
                    default='cities')


link_city_regexp = re.compile('/wiki/[a-zA-Z_]+,_[a-zA-Z_]+')


def is_link_city(url):
    return re.match(link_city_regexp, url)


def get_city_name_from_title(title):
    city_name = title.split(',')[0]
    return city_name.lstrip()


class CityParser(HTMLParser.HTMLParser):
    def __init__(self):
        self.cities = set()
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) == 2 and attrs[0][0] == 'href' and attrs[1][0] == 'title':
                url = attrs[0][1]
                title = attrs[1][1]
                if is_link_city(url):
                    self.cities.add(get_city_name_from_title(title))

    @staticmethod
    def get_cities_from_wikipedia(url='https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'):
        ab = AnonBrowser()
        ab.anonymize()
        page = ab.open(url)
        html = page.read()
        parser = CityParser()
        parser.feed(html)
        return sorted(parser.cities)


def main():
    args = parser.parse_args()
    url = args.target_url
    cities = CityParser.get_cities_from_wikipedia(url)
    print 'Found %d cities on %s' % (len(cities), url)

    file_location = args.target_file
    with open(file_location, 'w') as f:
        f.write('\n'.join(cities))
        f.write('\n')

    print 'Successfully saved cities\' names in %s' % file_location


if __name__ == '__main__':
    main()

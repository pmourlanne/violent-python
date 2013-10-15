import time
import random
import urllib2
import cookielib
import mechanize

UA_file = "user_agent_strings"


class AnonBrowser(mechanize.Browser):
    def __init__(self, proxies=[], user_agents=[]):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)  # To ignore robots.txt

        self.proxies = proxies + AnonBrowser.get_proxies()
        self.user_agents = user_agents + AnonBrowser.get_user_agents()
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()

    def clear_cookies(self):
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)

    def change_user_agent(self):
        self.addheaders = [('User-agent', (self.user_agents[random.randint(1, len(self.user_agents))]))]

    def change_proxy(self):
        self.set_proxies({'http': self.proxies[random.randint(1, len(self.proxies))]})

    def anonymize(self, sleep=False):
        self.clear_cookies()
        self.change_proxy()
        self.change_user_agent()
        if sleep:
            time.sleep(60)

    @staticmethod
    def get_proxies():
        response = urllib2.urlopen("http://rmccurdy.com/scripts/proxy/good.txt")
        page_source = response.read()
        proxy_urls = page_source.lstrip(":\n").rstrip("\n").split("\n")
        return proxy_urls

    @staticmethod
    def get_user_agents():
        with open(UA_file) as f:
            return map(lambda s: s.rstrip('\n'), f.readlines())

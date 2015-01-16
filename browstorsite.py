import re
import socks
import socket
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from stem.control import Controller
from mimetypes import guess_type, guess_extension


class ScrapeMethod():

    def __init__(self):
        self.set_driver()
        self.allhrefDict = {}
        self.downloadable_link = []
        self.get_contenttype = [
            'application/x-tar', 'application/java-archive', 'application/rar',
            'application/x-debian-package', 'application/x-lzh',
            'application/x-cbz', 'application/x-redhat-package-manager',
            'application/octet-stream', 'application/zip', 'application/x-lha',
            'application/x-7z-compressed']

    def create_connection(self, address, timeout=None, source_address=None):
        sock = socks.socksocket()
        sock.connect(address)
        return sock

    def set_proxy(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        socket.create_connection = self.create_connection

    def ip_changer(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate('download')
                controller.signal(Signal.NEWNYM)
        except Exception as ex:
            raise Exception('Tor is not running or configuration missing')

    def soap_get_alllinks(self, soapcontent):
        allurl = soapcontent.find_all('a')
        return allurl

    def set_driver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks_version", 5)
        profile.set_preference("network.proxy.socks", '127.0.0.1')
        profile.set_preference("network.proxy.socks_port", 9050)
        profile.set_preference("network.proxy.socks_remote_dns", True)
        self.driver = webdriver.Firefox(profile)

    def browse_url(url):
        self.driver.get(url)

    def get_alldata(self, url=None, soup_obj=True):
        if url:
            self.driver.get(url)
        pagesource = self.driver.page_source
        if soup_obj:
            return BeautifulSoup(pagesource)
        else:
            return pagesource

    def close_driver(self):
        self.driver.close()

    def get_type(self, typeurl):
        types, encoding = guess_type(typeurl, strict=True)
        if types in self.get_contenttype:
            self.downloadable_link.append(typeurl)

    def driver_all_href(self, linklist):
        return map(lambda link: link.get_attribute('href'), linklist)

    def driver_get_all_link(self):
        return self.driver.find_elements_by_tag_name('a')

    def driver_get_all_downloadable_link(self, check_type_link):
        for check in check_type_link:
            if check:
                self.get_type(check)

    def get_all_external_link(self, soap):
        pattern = "(?:http[s]?:[/][/]|www.)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\s]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:.zip|.rar|.gz|.7z|.tar)"
        try:
            fordata = re.findall(pattern, soap)
        except Exception, e:
            fordata = []
        for i in fordata:
            print i
            self.get_type(i)

    def anom(self):
        url = 'http://doxbinrqbk7lcslw.onion/archive.php'
        soup = self.get_alldata(url, soup_obj=False)
        linklist = self.driver.find_elements_by_tag_name('a')
        return self.driver_all_href(linklist)

    def get_all_downloadable_link(self):
        for i in self.anom():
            soap = self.get_alldata(i, soup_obj=False)
            patten = '(?:http[s]?:[/][/]|www.)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\s]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:.zip|.rar|.gz|.7z|.tar)'
            fordata = re.findall(patten, soap)
            for i in fordata:
                self.get_type(i)
            print self.type_dict

    def onionweb(self, NUM=1900):
        while NUM < 2850:
            url = "http://3fnhfsfc2bpzdste.onion/index.php?a=download&q=%s" % NUM
            soap = self.get_alldata(url, soup_obj=False)
            lst = self.driver_all_href(self.driver_get_all_link())
            for i in lst:
                if i not in self.allhrefDict.keys():
                    with open('somefile.txt', 'a') as the_file:
                        the_file.write('%s \n' % i)
                self.allhrefDict[i] = ''

            return self.onionweb(NUM+1)

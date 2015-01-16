from bs4 import BeautifulSoup
from selenium import webdriver
import subprocess


class ScrapeMethod():

    def __init__(self):
        self.SetDriver()
        self.AllContentList = []

    def SetDriver(self):
        ff_prof = webdriver.Firefox()
        ff_prof.set_preference("places.history.enabled", False)
        ff_prof.set_preference("privacy.clearOnShutdown.offlineApps", True)
        ff_prof.set_preference("privacy.clearOnShutdown.passwords", True)
        ff_prof.set_preference("privacy.clearOnShutdown.siteSettings", True)
        ff_prof.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        ff_prof.set_preference("signon.rememberSignons", False)
        ff_prof.set_preference("network.cookie.lifetimePolicy", 2)
        ff_prof.set_preference("network.dns.disablePrefetch", True)
        ff_prof.set_preference("network.http.sendRefererHeader", 0)

        # set socks proxy
        ff_prof.set_preference("network.proxy.type", 1)
        ff_prof.set_preference("network.proxy.socks_version", 5)
        ff_prof.set_preference("network.proxy.socks", '127.0.0.1')
        ff_prof.set_preference("network.proxy.socks_port", 9050)
        ff_prof.set_preference("network.proxy.socks_remote_dns", True)

        # if you're really hardcore about your security
        # js can be used to reveal your true i.p.
        ff_prof.set_preference("javascript.enabled", False)

        # get a huge speed increase by not downloading images
        ff_prof.set_preference("permissions.default.image", 2)

        self.driver = ff_prof

    def GetAlldata(self, url):
        self.driver.get(url)
        pagesource = self.driver.page_source
        soup = BeautifulSoup(pagesource)
        return soup

    def Pastebin(self):
        url = 'http://abc.ca'
        soupData = self.GetAlldata(url)
        recentPost = soupData.find(id="idmenurecent").find_all("a")
        allLinks = []
        for recent in recentPost:
            allLinks.append(url + recent.attrs['href'])
        return allLinks

    def Quickleak(self):
        url = 'https://abc.org/last-pastes.html'
        puturl = '/'.join(url.split('/')[:-1])
        soupData = self.GetAlldata(url)
        table = soupData.find("table", {"id": "example"})
        allLinks = []
        for row in table.findAll("tr"):
            if row.td:
                link = row.td.find('a').attrs['href']
                allLinks.append(puturl + '/' + link)
        return allLinks

    def CloseDriver(self):
        self.driver.close()

    def AllLinks(self):
        self.AllLinksList = self.Pastebin() + self.Quickleak()
        return 'self.Quickleak() + self.Pastebin()'

    def ContentData(self):
        self.AllLinks()
        for content in self.AllLinksList:
            soupData = self.GetAlldata(content)

            if 'pastebin' in content:
                self.PastebinContent(content, soupData)

            if 'quickleak' in content:
                self.QuickleakContent(content, soupData)
        return self.AllContentList

    def PastebinContent(self, url, getData):

        contentdata = getData.select("div > #idsec0 > .ccontent li")
        headingdata = getData.select("div #idsec0 h2 dt")

        tempDict = {
            'url': url,
            'heading': self.GetString(headingdata),
            'content': self.GetString(contentdata),
        }

        self.AllContentList.append(tempDict)

    def QuickleakContent(self, url, getData):

        contentdata = getData.select("div > .content li")
        headingdata = getData.select("div .page-title .titlebar h2")

        tempDict = {
            'url': url,
            'heading': self.GetString(headingdata),
            'content': self.GetString(contentdata),
        }

        self.AllContentList.append(tempDict)

    def GetString(self, contentdata):
        string = ''
        for content in contentdata:
            txt = content.text
            string = string + txt + '\n '
        return string

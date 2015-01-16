from bs4 import BeautifulSoup
from selenium import webdriver
import re


class ScrapeMethod():

    def __init__(self):
        self.SetDriver()
        self.AllContentList = []

    def SetDriver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks_version", 5)
        profile.set_preference("network.proxy.socks", '127.0.0.1')
        profile.set_preference("network.proxy.socks_port", 9050)
        profile.set_preference("network.proxy.socks_remote_dns", True)
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', '/tmp')
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/rar')
        self.driver = webdriver.Firefox(profile)


    def GetAlldata(self, url, soup_obj=True):
        self.driver.get(url)
        pagesource = self.driver.page_source
        if soup_obj:
            soup = BeautifulSoup(pagesource)
        else:
            soup = pagesource
        return soup

    def CloseDriver(self):
        self.driver.close()

    def AllLinks(self):
        self.AllLinksList = self.Pastebin() + self.Quickleak()
        return 'self.Quickleak() + self.Pastebin()'

    def make_lambda(self, url):
        return lambda link: url + link.attrs['href']

    def BlackMarket(self):
        url = 'http://jppcxclcwvkbh3xi.onion/messages/'
        soupData = self.GetAlldata(url)
        self.driver.find_element_by_xpath("//div[@class='quarterContent']//a").click()
        allLinks = soupData.find_all('a', text=re.compile(".html"))

        return map(self.make_lambda(url), allLinks)

    def BlackMarketContent(self):
        links = self.BlackMarket()
        allMail = []
        for i in links[500:700]:
            soupData = self.GetAlldata(i, soup_obj=False)
            li = re.findall(r'[\w\.-]+@[\w\.-]+', soupData)
            allMail.extend(list(set(li)))
        print list(set(allMail))

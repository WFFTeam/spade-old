### - spade_bs4.py
### - Beautiful Soup functions

import re, requests, errno, unidecode, string, urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlsplit
from requests_html import HTMLSession

# Unified BeautifulSoup SCRAPING FUNCTION
def bs4UnifiedScrape(url):
    errorUrl = ""
    errorCount = 0
    try:
        hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 5)
        html = page.read()
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), "html.parser")
        urlSplit = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(urlSplit)
        
        if '/' in urlSplit.path:
            path = url[:url.rfind('/')+1]
        else:
            path = url

        titleText = str(soup.title.text)
        foundMail = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', soup.text)
        resultList = ([titleText, soup, foundMail])
        return resultList

    except Exception as error:
        errorUrl = url
        errorNotice = str(error)
        errorInfo = ([errorNotice, errorUrl, "!!ERROR!!"])
        return errorInfo
"""
New Request-HTML crawler and scraper
def requestsHtmlScrape(url):
    errorUrl = ""
    errorCount = 0
    try:
      session = HTMLSession()
      r = session.get(url)
      r.html.render()

      foundMail = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', r.html.full_text)
      absoluteLinks = r.html.absolute_links

      htmlResultsList = [ foundMail, absoluteLinks, ]
      return htmlResultsList
      about = r.html.find('#about', first=True)

  except Exception as error:
        errorUrl = url
        errorNotice = str(error)
        errorInfo = [errorNotice,errorUrl,"!!ERROR!!"]
        return errorInfo
"""
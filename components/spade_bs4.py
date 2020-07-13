### - spade_bs4.py
### - Beautiful Soup functions

import re, requests, errno, unidecode, string, urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# BeautifulSoup GET TITLE
def ScrapeTitle(url):
    errorUrl = ""
    errorCount = 0
    try:
        hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 5)
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
        return str(soup.title.text)

    except Exception as error:
        errorUrl = url
        errorNotice = str(error)
        errorInfo = [errorNotice,errorUrl,'ERROR']
        return errorInfo

# BeautifulSoup GET HTML
def ScrapeHTML(url):
    errorUrl = ""
    errorCount = 0
    try:
        hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 5)
        html = page.read()
        return html

    except Exception as error:
        errorUrl = url
        errorNotice = str(error)
        errorInfo = [errorNotice,errorUrl,'ERROR']
        return errorInfo
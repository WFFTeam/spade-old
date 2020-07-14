### - spade_bs4.py
### - Beautiful Soup functions

import re, requests, errno, unidecode, string, urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlsplit

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

        titleText = str(soup.title.text)                                                ### TITLE VARIABLE
        parsedHtml = soup                                                               ### HTML VARIABLE
        foundMail = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", soup.text, re.I) ### EMAIL VARIABLE
        resultList = [ titleText, parsedHtml, foundMail]                                ### LISTA OD RESULTATA VARIABLA IZNAD
        return resultList

    except Exception as error:
        errorUrl = url
        errorNotice = str(error)
        errorInfo = [errorNotice,errorUrl,"!!ERROR!!"]
        return errorInfo

# # BeautifulSoup GET TITLE
# def ScrapeTitle(url):
#     errorUrl = ""
#     errorCount = 0
#     try:
#         hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
#         req = Request(url,headers=hdr)
#         page = urlopen(req, timeout = 5)
#         soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
#         return str(soup.title.text)

#     except Exception as error:
#         errorUrl = url
#         errorNotice = str(error)
#         errorInfo = [errorNotice,errorUrl,"!!ERROR!!"]
#         return errorInfo

# # BeautifulSoup GET HTML
# def ScrapeHTML(url):
#     errorUrl = ""
#     errorCount = 0
#     try:
#         hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
#         req = Request(url,headers=hdr)
#         page = urlopen(req, timeout = 5)
#         html = page.read()
#         parsedHtml = BeautifulSoup(html.decode('utf-8', 'ignore'), "html.parser")
#         return parsedHtml

#     except Exception as error:
#         errorUrl = url
#         errorNotice = str(error)
#         errorInfo = [errorNotice,errorUrl,"!!ERROR!!"]
#         return errorInfo

# # BeautifulSoup EMAIL REGEX SEARCH IN HTML
# def ScrapeMail(url):
#     errorUrl = ""
#     errorCount = 0

#     urlSplit = urlsplit(url)
#     base_url = "{0.scheme}://{0.netloc}".format(urlSplit)
#     if '/' in urlSplit.path:
#       path = url[:url.rfind('/')+1]
#     else:
#       path = url

#     try:
#         hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
#         req = Request(url,headers=hdr)
#         page = urlopen(req, timeout = 5)
#         soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
#         foundMail = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", soup.text, re.I)
#        ###ALT FUNKCIJA za mail scrape: # #foundMail = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", (BeautifulSoup(urlopen(Request(url,headers=hdr), timeout = 5).read().decode('utf-8', 'ignore'), "html.parser")).text, re.I)
#        #foundMail.sort(key=len)
#        #print(foundMail) #DEBUG#
#        #print(foundMail[0].replace("\n","")) #DEBUG#
#         return str(foundMail)
#     except Exception as error:
#         errorUrl = url
#         errorNotice = str(error)
#         errorInfo = [errorNotice,errorUrl,"!!ERROR!!"]
#         return errorInfo
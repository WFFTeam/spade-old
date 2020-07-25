### - spade_requesthtml.py
### - Request-html JS parsing and scraping

import re, requests, errno, unidecode, string, urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlsplit
from requests_html import HTMLSession

def requestsHtmlScrape(url):
    errorUrl = ""
    errorCount_htmlreq = 0
    absoluteLinks = relativeLinks = foundMail = linkList = []
    try:
        session = HTMLSession()
        r = session.get(url)
        r.html.render()

        foundMail = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', r.html.full_text)
        if foundMail == '':
            foundMail = 'NONE'
        absoluteLinks = r.html.absolute_links
        relativeLinks = r.html.links
        linkList.append(absoluteLinks)
        linkList.append(relativeLinks)
        if linkList == '':
            linkList = 'NONE'
    #   U listi rezultata treba da bude:    
    #   htmlResultList = [ altTitle, altHtml, altMail, siteSections, linkList ]
        htmlResultsList = [foundMail, linkList, "OK"]
        return htmlResultsList

    #   Ideja za internu navigaciju bota ka kontakt stranici/sekciji
    #   about = r.html.find('#about', first=True)

    except Exception as error:
        errorUrl = url
        errorNotice = str(error)
        errorInfo = [errorNotice,errorUrl,"!!ERROR!!"]
        return errorInfo
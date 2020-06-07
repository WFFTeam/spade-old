#SPADE v0.3a

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from googlesearch import search
import csv
import string
import re
import sys
import os
import time
from datetime import datetime
import requests
from urllib.error import HTTPError
import argparse
import time

def clear():
    os.system( 'clear')

def countdown(p,q):
    i=p
    j=q
    k=0
    while True:
        if(j==-1):
            j=59
            i -=1
        if(j > 9):  
            print(str(k)+str(i)+":"+str(j), end="\r")
        else:
            print(str(k)+str(i)+":"+str(k)+str(j), end="\r")
        time.sleep(1)
        j -= 1
        if(i==0 and j==-1):
            break
    if(i==0 and j==-1):
        print("Goodbye!", end="\r")
        time.sleep(1)


def DateTimePrint():
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
    return(dt_string);

def QueryProgress(queryInput):
    print(" ")
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print(DateTimePrint())
    print("Fetching results for string: " + queryInput)

def ScrapeTitle(url):
    errorUrlList = []
    errorCount = 0
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 5)
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
        return soup.title.text
    except Exception as e:
        errorUrlList.append(url)
        errorCount += 1
        print(e.code)
        return e.code
#       return "ERROR: " + str(error)

def FileOutput(result_list, csvPath, logPath, queryInput, count):
    
    for i in result_list:
        data = [i]
        wr = open(csvPath, 'a', newline='')
        with wr:
            write = csv.writer(wr)
            write.writerows(data)
    
    with open(logPath, "w") as text_file:
        print("SPADE v0.3a", file=text_file)
        print("Search string: " + queryInput, file=text_file)
        print("Results saved to: " + csvPath, file=text_file)
        print("Total number of results found: " + str(count), file=text_file)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print("Saved results to: " + csvPath)
    print("Saved log to: " + logPath)

def SprungeUpload(csvPath, logPath):
    files = {
        'sprunge': (None, open(csvPath, 'rb')),
    }
    r = requests.post('http://sprunge.us/', files=files)
    sprungeUsURL = r.text
    print("| File uploaded to sprunge.us; access URL: " + sprungeUsURL)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print(" ")
    with open(logPath, "a+") as text_file:
        print("CSV URL: " + sprungeUsURL, file=text_file)

def main():
    QueryListArg = sys.argv[1]
    if QueryListArg == "":
        print("Query list file not specified in argument; aborting.")
        sys.exit()
        
    with open(QueryListArg, 'r') as QueryList:
        lines = []
        for line in QueryList:
            result_list = []
            url_list =[]
            queryInput = re.sub(r'[\n\r\t]*', '', line)
            csvFilename = re.sub('[\W_]', '.', queryInput) + '.csv'
            logFilename = re.sub('[\W_]', '.', queryInput) + '.log'
            csvPath = './RESULTS/' + csvFilename
            logPath = './RESULTS/' + logFilename
            i = 0
            progBarMult = i
            emptyBarMult = 70
            progSign = 1
            try:
                for url in search(queryInput,   # The query you want to run
#                           tld = 'com',  # The top level domain
#                           lang = 'en',  # The language
#                           start = 0,    # First result to retrieve
#                           stop = 20,    # Last result to retrieve
                            num = 10,     # Number of results per page
                            pause = 4.0,  # Lapse between HTTP requests
                            ):
                    time.sleep(0.5)
                    i += 1
                    result = []
                    result = ([i, url])
                    url_list.append(result)
                    clear()
                    print("SPADE v0.3a")
                    QueryProgress(queryInput)
                    print(f'No. {i} --- {result[1]}')
                    if progBarMult == 100:
                        progSign = -1
                    if progBarMult == 0:
                        progSign = 1
                    progBarMult = progBarMult + 2 * progSign
                    emptyBarMult = emptyBarMult - progSign
                    emptyBar = " " * emptyBarMult
                    print(emptyBar + '<=' + "=" * progBarMult + '=>')
                    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
                    
                    
            except IndexError as e:
                print('Index error occured: ' + str(e.code))
            except HTTPError as err:
                print(err)
                countdown(0,5)
#               break
            print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            for i in url_list:
                count = i[0]
                url = i[1]
                title = re.sub(r'[\n\r\t]*', '', ScrapeTitle(url))
                result = ([url, title])
                result_list.append(result)
                print("#: " + str(count) + " | " + DateTimePrint())
                print("URL: " + result[0])
                print("Title: " + result[1])
                print(" ")
            FileOutput(result_list, csvPath, logPath, queryInput, count)
            SprungeUpload(csvPath, logPath)

            
if __name__ == "__main__":
    main()

#SPADE v0.6a

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
from termcolor import colored

def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])

def green(text):
    return colored(text, 'green', attrs=['bold'])

def red(text):
    return colored(text, 'red', attrs=['bold'])

def cyan(text):
    return colored(text, 'cyan', attrs=['bold'])

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

def QueryProgress(currentLine, numOfLines, queryInput):
    print(" ")
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(green(DateTimePrint()))
    print(green(f'Working string {currentLine} of {numOfLines}'))
    print(green(f'Fetching results for string: {queryInput}'))

def ScrapeTitle(url):
    errorUrl = ""
    errorCount = 0
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 5)
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
        return soup.title.text
    except Exception as error:
        errorUrl = url
        errorNotice = error
        errorInfo = [errorNotice,errorUrl,'ERROR']
        return errorInfo

def FileOutput(result_list, csvPath, logPath, queryInput, count, errorCount):
    os.mkdir('RESULTS')
    for i in result_list:
        data = [i]
        wr = open(csvPath, 'a', newline='')
        with wr:
            write = csv.writer(wr)
            write.writerows(data)
    
    with open(logPath, "w") as text_file:
        print("SPADE v0.6a", file=text_file)
        print("Search string: " + queryInput, file=text_file)
        print("Results saved to: " + csvPath, file=text_file)
        print("Total number of results found: " + str(count), file=text_file)
        print("Number of errors:" + str(errorCount), file=text_file)
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(green("Saved results to: " + csvPath))
    print(green("Saved log to: " + logPath))
    print(red("Number of errors:" + str(errorCount)))
    
def SprungeUpload(csvPath, logPath):
    files = {
        'sprunge': (None, open(csvPath, 'rb')),
    }
    r = requests.post('http://sprunge.us/', files=files)
    sprungeUsURL = r.text
    print(yellow("File uploaded to sprunge.us; access URL: " + sprungeUsURL))
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(" ")
    with open(logPath, "a+") as text_file:
        print("CSV URL: " + sprungeUsURL, file=text_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", "-l", help="Set file to read URLs from")
    parser.add_argument("--query", "-q", help="Set Google search query")
    args = parser.parse_args()
### LOAD LIST OF QUERUES
    if args.list:
        QueryListArg = args.list
        numOfLines = sum(1 for line in open(QueryListArg, 'r'))
        with open(QueryListArg, 'r') as QueryList:
            lines = []
            currentLine = 0
            for line in QueryList:
                currentLine += 1
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
#                               tld = 'com',  # The top level domain
#                               lang = 'en',  # The language
#                               start = 0,    # First result to retrieve
#                               stop = 10,    # Last result to retrieve
                                num = 10,     # Number of results per page
                                pause = 4.0,  # Lapse between HTTP requests
                                ):
                        time.sleep(0.5)
                        i += 1
                        result = []
                        result = ([i, url])
                        url_list.append(result)
                        clear()
                        print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                        print(green("SPADE v0.6a"))
                        print(cyan("Searching google and collecting URL addresses"))
                        QueryProgress(currentLine, numOfLines, queryInput)
                        print(yellow(f'No. {i} --- {result[1]}'))
                        if progBarMult == 100:
                            progSign = -1
                        if progBarMult == 0:
                            progSign = 1
                        progBarMult = progBarMult + 2 * progSign
                        emptyBarMult = emptyBarMult - progSign
                        emptyBar = " " * emptyBarMult
                        print(" ")
                        print(cyan(emptyBar + '<=' + "=" * progBarMult + '=>'))
                        print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                        
                        
                except IndexError as e:
                    print(red('Index error occured: ' + str(e.code)))
                except HTTPError as err:
                    print(red(err))
                    countdown(0,5)
                print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                errorCount = 0
                for i in url_list:
                    numOfURL = len(url_list)
                    count = i[0]
                    url = i[1]
                    if 'ERROR' in ScrapeTitle(url):

                        title = ScrapeTitle(url)[0]
                        errorUrl = ScrapeTitle(url)[1]
                        errorCount += 1
                        titleColor = red(f'Error: {title}')
                    else:
                        title = re.sub(r'[\n\r\t]*', '', str(ScrapeTitle(url)))
                        titleColor = yellow(f'Title: {title}')
                    result = ([url, title])
                    print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
                    print(yellow("URL: " + result[0]))
                    print(titleColor)
                    print(" ")
                    result_list.append(result)
                FileOutput(result_list, csvPath, logPath, queryInput, count, errorCount)
                SprungeUpload(csvPath, logPath)
### DIRECT QUERY
    elif args.query:
        line = args.query
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
#                       stop = 50,    # Last result to retrieve
                        num = 10,     # Number of results per page
                        pause = 4.0,  # Lapse between HTTP requests
                        ):
                time.sleep(0.5)
                i += 1
                result = []
                result = ([i, url])
                url_list.append(result)
                clear()
                print(green("SPADE v0.6a"))
                print(" ")
                print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                print(green(DateTimePrint()))
                print(green(f'Fetching results for string: {queryInput}'))
                print(yellow(f'No. {i} --- {result[1]}'))
                if progBarMult == 100:
                    progSign = -1
                if progBarMult == 0:
                    progSign = 1
                progBarMult = progBarMult + 2 * progSign
                emptyBarMult = emptyBarMult - progSign
                emptyBar = " " * emptyBarMult
                print(" ")
                print(cyan(emptyBar + '<=' + "=" * progBarMult + '=>'))
                print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                
                
        except IndexError as e:
            print(red('Index error occured: ' + str(e.code)))
        except HTTPError as err:
            print(red(err))
            countdown(0,5)
        print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
        errorCount = 0
        for i in url_list:
            numOfURL = len(url_list)
            count = i[0]
            url = i[1]
            if 'ERROR' in ScrapeTitle(url):

                title = ScrapeTitle(url)[0]
                errorUrl = ScrapeTitle(url)[1]
                errorCount += 1
                titleColor = red(f'Error: {title}')
            else:
                title = re.sub(r'[\n\r\t]*', '', str(ScrapeTitle(url)))
                titleColor = yellow(f'Title: {title}')
            result = ([url, title])
            print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
            print(yellow("URL: " + result[0]))
            print(titleColor)
            print(" ")
            result_list.append(result)
        FileOutput(result_list, csvPath, logPath, queryInput, count, errorCount)
        SprungeUpload(csvPath, logPath)

            
if __name__ == "__main__":
    main()

#SPADE v0.1a

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

result_list =[]
def DateTimePrint():
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
    return(dt_string);
    
def ScrapeTitle(url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 3)
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
        return soup.title.text
    except Exception as error:
        return "ERROR: " + str(error);

def main():
    QueryListArg = sys.argv[1]
#   QueryListArg = 'test2.txt'
    if QueryListArg == "":
        print("Query list file not specified in argument; aborting.")
        sys.exit()
    with open(QueryListArg, 'r') as QueryList:
        lines = []
        for line in QueryList:
            i = 1
            QueryInput = re.sub(r'[\n\r\t]*', '', line)
            print(" ")
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
            print(DateTimePrint())
            print("Fetching results for string: " + QueryInput)
            csvFilename = re.sub('[\W_]', '.', QueryInput) + '.csv'
            logFilename = re.sub('[\W_]', '.', QueryInput) + '.log'
            csvPath = './RESULTS/' + csvFilename
            logPath = './RESULTS/' + logFilename
            print("Saving results to: " + csvPath)
            print("Saving log to: " + logPath)
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
            print(" ")

            while True:
                try:
                    for url in search(QueryInput,        # The query you want to run
        #                               tld = 'com',  # The top level domain
        #                               lang = 'en',  # The language
        #                               start = 0,    # First result to retrieve
        #                               stop = 10,  # Last result to retrieve
                                num = 10,     # Number of results per page
                                pause = 10.0,  # Lapse between HTTP requests
                                ):
                        result = []
                        title = re.sub(r'[\n\r\t]*', '', ScrapeTitle(url))
                        if "ERROR: " in title:
                            errorMsg = title
                            title = ""
                            result = ([url, title, i, errorMsg])
                        else:
                            result = ([url, title, i])

                        result_list.append(result)
                        data = [result]
                        wr = open(csvPath, 'a', newline ='')
                        with wr:
                            write = csv.writer(wr)
                            write.writerows(data)
                        print("#: " + str(result[2]) + " | " + DateTimePrint())
                        if result[1] == "":
                            print("!!!" + result[3])
                        else:
                            print("Title: " + result[1])
                        print("URL: " + result[0])
                        print(" ")
                        i += 1
                        continue
                    
                    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
                    files = {
                        'sprunge': (None, open(csvPath, 'rb')),
                    }
                    r = requests.post('http://sprunge.us/', files=files)
                    sprungeUsURL = r.text
                    print("| File uploaded to sprunge.us; access URL: " + sprungeUsURL)
                    with open(logPath, "w") as text_file:
                        print("Search string: " + QueryInput, file=text_file)
                        print("Results saved to: " + csvFilename, file=text_file)
                        print("Total number of results found: " + str(i), file=text_file)
                        print("CSV URL: " + sprungeUsURL, file=text_file)
                    break
                except IndexError as indexerror:
                    print('Index error occured: ' + str(indexerror))
                    break
                except Exception as exception:
                    print('Unknown error occured: ' + str(exception))
                    break
                
                
                
    
if __name__ == "__main__":
    main()

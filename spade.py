#SPADE v0.8a
spadeVersion = "v0.83a"

import string, argparse, re, unidecode, time, os, sys
from googlesearch import search
from urllib.error import HTTPError
from datetime import datetime as dt
from components import *
from components.config_db import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", "-l", help="Set file to read queries from")
    parser.add_argument("--start", "-s", help="Set the starting line")
    args = parser.parse_args()

    # LOAD LIST OF QUERUES FROM FILE
    if args.list:
        queryListArg = args.list
        numOfLines = sum(1 for line in open(queryListArg, 'r'))
        if args.start:
            queryListStart = int(args.start) - 1
        else:
            queryListStart = 0

        with open(queryListArg, 'r') as queryList:
            lines = []
            sL = int(queryListStart)
            currentLine = 0 + sL
            queryList = queryList.readlines()[sL:]
            for line in queryList:
                currentLine += 1
                result_list = []
                resultDict_list = []
                url_list =[]

                #Filename & Filepath generaton                
                queryInput = re.sub(r'[\n\r\t]*', '', line)
                sanInput = unidecode.unidecode(re.sub(r'\.+', ".", re.sub('[\W_]', '.', queryInput)))
                baseFilename = '.'.join(sanInput.split(".")[:8])
                csvFilename = baseFilename + '.csv'
                jsonFilename = baseFilename + '.json'
                logFilename = baseFilename + '.log'

                csvPath = './RESULTS/' + csvFilename
                jsonPath = './RESULTS/' + jsonFilename
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
                        time.sleep(0.2)
                        i += 1
                        result = []
                        result = ([i, url])
                        url_list.append(result)
                        clear()
                        print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                        print(green("SPADE " + spadeVersion))
                        if sL != 0:
                            print(yellow(f'Skipping first {queryListStart} of {numOfLines} lines'))

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
                    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                    print(green("SPADE " + spadeVersion))
                    print(red('Index error occured: ' + str(e.code)))
                except HTTPError as err:
                    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                    print(green("SPADE " + spadeVersion))
                    print(red(err))
                    if err.code == 429:
                        try:
                            q += 600
                            sL = sL + int(i)
                            print(cyan("Increasing retry delay by 600 seconds"))
                            print(yellow("Current delay is: ") + red(str(q)))
                        except Exception as exceptionError:
                            q = 600
                        print(red('Too many requests; temporarily blocked by Google'))
                        countdown(0,q)
                        main() ### OBRATITI PAZNJU NA OVO                        
                        return
                    
                print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                errorCount = 0
                for i in url_list:
                    numOfURL = len(url_list)
                    count = i[0]
                    url = i[1]

                    scrapeResults = bs4UnifiedScrape(url)
                    if "!!ERROR!!" in scrapeResults[2]:
                        title = html = foundMail = foundMailFormatted = 'BeautifulSoup error'
                        errorTitle = errorHtml = errorMail = scrapeResults[0]
                        errorUrl = scrapeResults[1]
                        errorCount += 1
                        titleColor = red(f'Error: {errorTitle}')
                        htmlColor = red(f'Error: {errorHtml}')
                        foundMailColor = red(f'Error: {errorMail}')

                    else:
                        title = re.sub(r'[\n\r\t]*', '', str(scrapeResults[0]))
                        WhiteSpaceComb = re.compile(r"\s+")
                        title = WhiteSpaceComb.sub(" ", title).strip()
                        titleColor = green(f'Title: {title}')
                        errorTitle = 'NONE'
                        if title == '':
                            title = 'NONE'
                        html = scrapeResults[1]
                        htmlColor = green(f'HTML sucessfully extracted')
                        errorHtml = 'NONE'

                        if scrapeResults[2] == []:
                            foundMail = errorMail = foundMailFormatted  = 'NONE'
                            foundMailColor = yellow(f'No E-Mail found')
                        else:
                            foundMail = bs4UnifiedScrape(url)[2]
                            foundMailFormatted = str(foundMail).replace("', '"," ").replace("['", "").replace("']", "")
                            foundMailColor = cyan("E-Mail addresses found: " + foundMailFormatted)
                            errorMail = 'NONE'

                    jsonTimestamp = json.dumps(dt.now().isoformat())
                    result = ([title, foundMailFormatted, url, queryInput, errorTitle, errorMail, DateTimePrint()])
                    resultDict = ({"timestamp": jsonTimestamp, "url": url, "title": title, "query": queryInput, "email": foundMail, "html": str(html), "titleError": str(errorTitle), "htmlError": str(errorHtml), "emailError": str(errorMail)})

                    print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
                    print(green("URL: " + result[2]))
                        print(titleColor)
                        print(htmlColor)
                        print(foundMailColor)
                    else:
                        print(titleColor)
                    print(" ")
                    result_list.append(result)
                    resultDict_list.append(resultDict)
                print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))
                print(red("|| ") + yellow(" Number of errors: ") + red(str(errorCount) + " ||"))
                print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))

                FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount, resultDict_list)
                Json2PyMongo(jsonPath, logPath, baseFilename, resultDict_list)
                SprungeUpload(csvPath, jsonPath, logPath)

    else:
        sys.exit("Argument -l not provided or valid, exiting.") 
''' 
    ################################################################################################################################################################################################################################################            
    # SPECIFY QUERY IN COMMAND !!! VERY OUTDATED
    elif args.query:
        line = args.query
        result_list = []
        url_list =[]
        resultDict_list = []
        foundMail_list = []

        #Filename & Filepath generaton
        queryInput = re.sub(r'[\n\r\t]*', '', line)
        sanInput = unidecode.unidecode(re.sub(r'\.+', ".", re.sub('[\W_]', '.', queryInput)))
        baseFilename = '.'.join(sanInput.split(".")[:8])
        csvFilename = baseFilename + '.csv'
        jsonFilename = baseFilename + '.json'
        logFilename = baseFilename + '.log'
        
        csvPath = './RESULTS/' + csvFilename
        jsonPath = './RESULTS/' + jsonFilename
        logPath = './RESULTS/' + logFilename
        i = 0
        progBarMult = i
        emptyBarMult = 70
        progSign = 1
        try:
            for url in search(queryInput,   # The query you want to run
#                       tld = 'com',  # The top level domain
#                       lang = 'en',  # The language
#                       start = 0,    # First result to retrieve
                        stop = 10,    # Last result to retrieve
                        num = 10,     # Number of results per page
                        pause = 4.0,  # Lapse between HTTP requests
                        ):
                time.sleep(0.2)
                i += 1
                result = []
                result = ([i, url])
                url_list.append(result)
                clear()
                print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                print(green("SPADE " + spadeVersion))
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
            print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
            print(green("SPADE " + spadeVersion))
            print(red('Index error occured: ' + str(e.code)))
        except HTTPError as err:
            print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
            print(green("SPADE " + spadeVersion))
            print(red(err))
            if err.code == 429:
                try:
                    print(cyan("Increasing retry delay by 600 seconds"))
                    q += 600
                    print(yellow("Current delay is: ") + red(str(q)))
                except Exception as exceptionError:
                    q = 600    
                countdown(0,q)
                main() ### OBRATITI PAZNJU NA OVO 
                return
            
            
        print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
        errorCount = 0
        for i in url_list:
            numOfURL = len(url_list)
            count = i[0]
            url = i[1]

            if "!!ERROR!!" in bs4UnifiedScrape(url):
                title = 'ScrapeTitleError'
                html = 'ScrapeHtmlError'
                foundMail = 'ScrapeMailError'
                foundMailFormatted = 'ScrapeMailError'

                errorTitle = bs4UnifiedScrape(url)[0]
                errorHtml = bs4UnifiedScrape(url)[0]
                errorMail = bs4UnifiedScrape(url)[0]
                errorUrl = bs4UnifiedScrape(url)[1]

                errorCount += 1
                titleColor = red(f'Error: {errorTitle}')
                htmlColor = red(f'Error: {errorHtml}')
                foundMailColor = red(f'Error: {errorMail}')

            else:
                title = re.sub(r'[\n\r\t]*', '', str(bs4UnifiedScrape(url)[0]))
                WhiteSpaceComb = re.compile(r"\s+")
                title = WhiteSpaceComb.sub(" ", title).strip()
                titleColor = green(f'Title: {title}')
                errorTitle = 'NONE'

                html = bs4UnifiedScrape(url)[1]
                htmlColor = green(f'HTML sucessfully extracted')
                errorHtml = 'NONE'

                if bs4UnifiedScrape(url)[2] == []:
                    foundMail = 'NONE'
                    errorMail = 'NONE'
                    foundMailFormatted = 'NONE'
                    foundMailColor = yellow(f'No E-Mails found')
                else:
                    foundMail = bs4UnifiedScrape(url)[2]
                    foundMailFormatted = str(foundMail).replace("', '"," ").replace("['", "").replace("']", "")
                    foundMailColor = cyan("E-Mail addresses found: " + foundMailFormatted)
                    errorMail = 'NONE'

            jsonTimestamp = json.dumps(dt.now().isoformat())
            result = ([title, foundMailFormatted, url, queryInput, errorTitle, errorMail, DateTimePrint()])
            resultDict = ({"timestamp": jsonTimestamp, "url": url, "title": title, "query": queryInput, "email": foundMail, "html": str(html), "titleError": str(errorTitle), "htmlError": str(errorHtml), "emailError": str(errorMail)})
            
            print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
            print(green("URL: " + result[2]))
            print(titleColor)
            print(htmlColor)
            print(foundMailColor)
            print(" ")
            result_list.append(result)
            resultDict_list.append(resultDict)
        print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))
        print(red("|| ") + yellow(" Number of errors: ") + red(str(errorCount) + " ||"))
        print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))

        FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount, resultDict_list)
        Json2PyMongo(jsonPath, logPath, baseFilename, resultDict_list)
        SprungeUpload(csvPath, jsonPath, logPath)
'''
if __name__ == "__main__":
    main()
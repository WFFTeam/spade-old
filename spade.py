#SPADE v0.8a
spadeVersion = "v0.81a"

import string, argparse, re, unidecode, time, os, sys
from googlesearch import search
from urllib.error import HTTPError
from datetime import datetime as dt

from components import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", "-l", help="Set file to read queries from")
    parser.add_argument("--start", "-s", help="Set the starting line")
    parser.add_argument("--query", "-q", help="Set Google search query")
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
                baseFilename = unidecode.unidecode(re.sub(r'\.+', ".", re.sub('[\W_]', '.', queryInput)))[:100]
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
#                               stop = 5,    # Last result to retrieve
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
                    if "!ERROR!" in ScrapeTitle(url):
                        title = 'ScrapeTitleError'
                        errorTitle = ScrapeTitle(url)[0] # FORMAT TITLE
                        errorUrl = ScrapeTitle(url)[1]
                        errorCount += 1
                        titleColor = red(f'Error: {errorTitle}')
                    else:
                        title = re.sub(r'[\n\r\t]*', '', str(ScrapeTitle(url)))
                        WhiteSpaceComb = re.compile(r"\s+")
                        title = WhiteSpaceComb.sub(" ", title).strip()
                        titleColor = yellow(f'Title: {title}')
                        errorTitle = "NONE"

                    if "!ERROR!" in str(ScrapeHTML(url)):
                        html = 'ScrapeHtmlError'
                        errorHtml = ScrapeHTML(url)[0]
                        htmlColor = red(f'Error: {errorHtml}')
                    else:
                        html = ScrapeHTML(url)
                        errorHtml = "NONE"
                        htmlColor = green("HTML sucessfully extracted")

                    jsonTimestamp = json.dumps(dt.now().isoformat())
                    result = ([url, title, queryInput, errorTitle, jsonTimestamp])
                    resultDict = ({"timestamp": jsonTimestamp, "url": str(url), "title": str(title), "query": str(queryInput), "html": str(html), "titleError": str(errorTitle), "htmlError": str(errorHtml)})

                    print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
                    print(yellow("URL: " + result[0]))
                    print(titleColor)
                    print(htmlColor)
                    print(" ")
                    result_list.append(result)
                    resultDict_list.append(resultDict)
                print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))
                print(red("|| ") + yellow(" Number of errors: ") + red(str(errorCount) + " ||"))
                print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))
                print(" ")

                FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount, resultDict_list)
                Json2PyMongo(jsonPath, logPath, baseFilename, resultDict_list)
                SprungeUpload(csvPath, jsonPath, logPath)
                
    # SPECIFY QUERY IN COMMAND
    elif args.query:
        line = args.query
        result_list = []
        url_list =[]
        resultDict_list = []

        #Filename & Filepath generaton
        queryInput = re.sub(r'[\n\r\t]*', '', line)
        baseFilename = unidecode.unidecode(re.sub(r'\.+', ".", re.sub('[\W_]', '.', queryInput)))[:100]
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
#                       stop = 5,    # Last result to retrieve
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
            if "!ERROR!" in ScrapeTitle(url):
                title = 'ScrapeTitleError'
                errorTitle = ScrapeTitle(url)[0] # FORMAT TITLE
                errorUrl = ScrapeTitle(url)[1]
                errorCount += 1
                titleColor = red(f'Error: {errorTitle}')
            else:
                title = re.sub(r'[\n\r\t]*', '', str(ScrapeTitle(url)))
                WhiteSpaceComb = re.compile(r"\s+")
                title = WhiteSpaceComb.sub(" ", title).strip()
                titleColor = yellow(f'Title: {title}')
                errorTitle = "NONE"

            if "!ERROR!" in str(ScrapeHTML(url)):
                html = 'ScrapeHtmlError'
                errorHtml = ScrapeHTML(url)[0]
                htmlColor = red(f'Error: {errorHtml}')
            else:
                html = ScrapeHTML(url)
                htmlColor = green(f'HTML sucessfully extracted')
                errorHtml = "NONE"

            jsonTimestamp = json.dumps(dt.now().isoformat())
            result = ([url, title, queryInput, errorTitle, jsonTimestamp])
            resultDict = ({"timestamp": jsonTimestamp, "url": str(url), "title": str(title), "query": str(queryInput), "html": str(html), "titleError": str(errorTitle), "htmlError": str(errorHtml)})
            
            print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
            print(yellow("URL: " + result[0]))
            print(titleColor)
            print(htmlColor)
            print(" ")
            result_list.append(result)
            resultDict_list.append(resultDict)
        print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))
        print(red("|| ") + yellow(" Number of errors: ") + red(str(errorCount) + " ||"))
        print(red("~~~~~~~~~~~~~~~~~~~~~~~~~~"))

        FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount, resultDict_list)
        Json2PyMongo(jsonPath, logPath, baseFilename, resultDict_list)
        SprungeUpload(csvPath, jsonPath, logPath)

if __name__ == "__main__":
    main()
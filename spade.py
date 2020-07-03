#SPADE v0.7a
spadeVersion = "v0.7a"

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from googlesearch import search
import csv, json, string, re, sys, os, time, requests, argparse, errno, mpu.io
from datetime import datetime
from urllib.error import HTTPError
from termcolor import colored
import warnings # pymongo warning ingore
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pymongo

# TERMCOLOR FUNCTIONS
def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])
def green(text):
    return colored(text, 'green', attrs=['bold'])
def red(text):
    return colored(text, 'red', attrs=['bold'])
def cyan(text):
    return colored(text, 'cyan', attrs=['bold'])

# SCREEN CLEAN FUNCTION
def clear():
    os.system( 'clear')

# COUNTDOWN FUNCTION *NEED TESTING
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

# CURRENT DATE&TIME FUNCTION
def DateTimePrint():
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
    return(dt_string);

# QUERYPROGRESS FUNCTION
def QueryProgress(currentLine, numOfLines, queryInput):
    print(" ")
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(green(DateTimePrint()))
    print(green(f"Working string {currentLine} of {numOfLines}"))
    print(green(f"Fetching results for string: {queryInput}"))

# BS4 TITLE PARSE FUNCTION
def ScrapeTitle(url):
    errorUrl = ""
    errorCount = 0
    try:
#       hdr = {'User-Agent': 'Mozilla/5.0'}
        hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
        req = Request(url,headers=hdr)
        page = urlopen(req, timeout = 5)
        soup = BeautifulSoup(page.read().decode('utf-8', 'ignore'), "html.parser")
        return str(soup.title.text)

    except Exception as error:
        errorUrl = url
        errorNotice = error
        errorInfo = [errorNotice,errorUrl,'ERROR']
        return errorInfo

# WRITE RESULTS TO FILES
def FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount):    
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(yellow("SAVING RESULTS"))
    try:
        os.mkdir('RESULTS')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    # HEADERS
    with open(csvPath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Url", "Title"])
    # CSV
    for i in result_list:
        data = [i]
        wr = open(csvPath, 'a', newline='')
        with wr:
            writer = csv.writer(wr)
            writer.writerows(data)
    # LOG
    with open(logPath, "w") as text_file:
        print("SPADE v0.7a", file=text_file)
        print("Search string: " + queryInput, file=text_file)
        print("Results saved to: " + csvPath, file=text_file)
        print("Total number of results found: " + str(count), file=text_file)
        print("Number of errors:" + str(errorCount), file=text_file)
    # JSON
    dataJson = {}
    with open(csvPath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            title = re.sub(r'[.]*', '', csvRow["Title"])
            dataJson[title] = csvRow
    with open(jsonPath, 'w') as jsonFile:
        jsonFile.write(json.dumps(dataJson, sort_keys=True, indent=4, ensure_ascii=False))            

    print(green("Saved results to: ") + yellow(csvPath))
    print(green("Saved json file to: ") + yellow(jsonPath))
    print(green("Saved log to: ") + yellow(logPath))

# UPLOAD JSON TO MONGODB
def Json2PyMongo(jsonPath, logPath, queryInput):
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(yellow("UPLOADING JSON FILE TO MONGODB"))
    databaseName = "spadeDB" # DB Name
    collectionName = re.sub('[\W_]', '_', queryInput)
    dbhost = 'localhost' # DB host
    dbport = 27017 # DB port
    
    mng_client = pymongo.MongoClient(dbhost, dbport)
    mng_db = mng_client[databaseName]
    db_cm = mng_db[collectionName]

    with open(jsonPath, 'r') as data_file: # Get the data from JSON file
        data_json = json.load(data_file)
    try:
        db_cm.insert(data_json) # Insert Data
    except Exception as error:
        return

    # Print report
    mongoDBstring = "mongodb://" + dbhost.replace("'", "") + ":" + str(dbport)
    print(green("Input json file: ") + yellow(jsonPath))
    print(green("Uploading to host: ") + yellow(dbhost))
    print(green("Database name: ") + yellow(databaseName))
    print(green("Collection name: ") + yellow(collectionName))
    print(green("MongoDB connection string: ") + cyan(mongoDBstring))
    
    # Save to log file
    with open(logPath, "a+") as text_file:
        print("JSON file uploaded to MongoDB host: " + mongoDBstring, file=text_file)
        print("Database name: " + databaseName, file=text_file)
        print("Collection name: " + collectionName, file=text_file)

# SPRUNGE UPLOAD
def SprungeUpload(csvPath, jsonPath, logPath):
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(yellow("UPLOADING FILES TO SPRUNGE.US"))
    # CSV UPLOAD
    files = {
        'sprunge': (None, open(csvPath, 'rb')),
    }
    r = requests.post('http://sprunge.us/', files=files)
    sprungeUsURL_csv = r.text
    # JSON UPLOAD
    files = {
        'sprunge': (None, open(jsonPath, 'rb')),
    }
    r = requests.post('http://sprunge.us/', files=files)
    sprungeUsURL_json = r.text
    # PRINT URLS    
    print(yellow("Files uploaded to sprunge.us; access URL:"))
    print(green("CSV URL: ") + cyan(sprungeUsURL_csv), end = '')
    print(green("JSON URL: ") + cyan(sprungeUsURL_json), end = '')
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    # WRITE TO LOG
    with open(logPath, "a+") as text_file:
        print("CSV URL: " + sprungeUsURL_csv, end = '', file=text_file)
        print("JSON URL: " + sprungeUsURL_json, end = '', file=text_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", "-l", help="Set file to read URLs from")
    parser.add_argument("--query", "-q", help="Set Google search query")
    args = parser.parse_args()
    # LOAD LIST OF QUERUES FROM FILE
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
                baseFilename = re.sub(r'\.+', ".", re.sub('[\W_]', '.', queryInput))
                
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
                        time.sleep(0.5)
                        i += 1
                        result = []
                        result = ([i, url])
                        url_list.append(result)
                        clear()
                        print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
                        print(green("SPADE " + spadeVersion))
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
                        WhiteSpaceComb = re.compile(r"\s+")
                        title = WhiteSpaceComb.sub(" ", title).strip()
                        titleColor = yellow(f'Title: {title}')
                    result = ([url, title])
                    print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
                    print(yellow("URL: " + result[0]))
                    print(titleColor)
                    print(" ")
                    result_list.append(result)
                
                print(red("Number of errors:" + str(errorCount)))
                
                FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount)
                Json2PyMongo(jsonPath, logPath, queryInput)
                SprungeUpload(csvPath, jsonPath, logPath)
                
    # SPECIFY QUERY IN COMMAND
    elif args.query:
        line = args.query
        result_list = []
        url_list =[]
        queryInput = re.sub(r'[\n\r\t]*', '', line)
        baseFilename = re.sub(r'\.+', ".", re.sub('[\W_]', '.', queryInput))
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
                time.sleep(0.5)
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
                WhiteSpaceComb = re.compile(r"\s+")
                title = WhiteSpaceComb.sub(" ", title).strip()
                titleColor = yellow(f'Title: {title}')
            result = ([url, title])
            print(yellow(str(count) + " of " + str(numOfURL) + " URLs | " + DateTimePrint()))
            print(yellow("URL: " + result[0]))
            print(titleColor)
            print(" ")
            result_list.append(result)

        print(red("Number of errors:" + str(errorCount)))
        
        FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount)
        Json2PyMongo(jsonPath, logPath, queryInput)
        SprungeUpload(csvPath, jsonPath, logPath)
            
if __name__ == "__main__":
    main()

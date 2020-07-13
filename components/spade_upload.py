### - spade_upload.py
### - Upload json result to MongoDB and upload result .csv and .json to sprunge.us

import pymongo, string, re, urllib.parse, csv, json, mpu.io, requests
from .spade_interface import yellow, green, red, cyan 
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import warnings # pymongo warning ingore
warnings.filterwarnings("ignore", category=DeprecationWarning)


#JSON TO MONGODB UPLOAD
def Json2PyMongo(jsonPath, logPath, baseFilename, resultDict_list):
    print(green("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="))
    print(yellow("UPLOADING JSON FILE TO MONGODB"))
    collectionName = re.sub('[\W_]', '_', baseFilename)
    databaseName = "spadeDB" # DB Name
    userDB = 'admin' # Admin DB
    dbhost = '127.0.0.1' # DB host
    dbport = 27017 # DB port
    dbuser = 'spadeUser' #DB Username
    dbpass = "S1EdE9xxxxAuIII@#!22Dandjop" # DB Password

    username = urllib.parse.quote_plus(dbuser)
    password = urllib.parse.quote_plus(dbpass)
    
    mng_client = pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s' % (username, password, dbhost, dbport, userDB))
    mng_db = mng_client[databaseName]
    db_cm = mng_db[collectionName]

    with open(jsonPath, 'r') as data_file: # Get the data from JSON file
        data_json = json.load(data_file)
    try:
        db_cm.insert(data_json) # Insert Data
        db_cm.insert(resultDict_list)
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
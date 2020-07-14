### - spade_fileoutput.py
### - Write results to csv and json file and log operations

import string, re, csv, json, mpu.io, os, errno
from urllib.error import HTTPError
from .spade_interface import yellow, green, red, cyan


def FileOutput(result_list, csvPath, jsonPath, logPath, queryInput, count, errorCount, resultDict_list):    
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
        writer.writerow([ "Url", "Title", "Query", "Error", "Timestamp" ])
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
    # outputJson = json.dumps(resultDict_list, sort_keys=True, indent=4, ensure_ascii=False)
    outputJson = json.dumps(resultDict_list, indent=4, ensure_ascii=False)
    # with open(jsonPath, 'w', encoding='utf8') as jsonFile:
    with open(jsonPath, 'w') as jsonFile:
        jsonFile.write(outputJson)

    print(green("Saved results to: ") + yellow(csvPath))
    print(green("Saved json file to: ") + yellow(jsonPath))
    print(green("Saved log to: ") + yellow(logPath))
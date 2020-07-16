### - spade_interface.py
### - Terminal and output functions

import os, string, sys, time
from datetime import datetime
from termcolor import colored

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

# COUNTDOWN FUNCTION
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
        print(red("RESTARTING"), end="\r")
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
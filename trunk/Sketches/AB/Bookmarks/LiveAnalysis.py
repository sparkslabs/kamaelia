#! /usr/bin/python

# Analyses saved data in DB to give something more useful. Saves to output DB ready for display in web interface
# Need word freq analysis, tweet rate analysis etc
# Any looking at natural language engines / subtitles should be done here or in components following this
# Need to ensure one rogue user can't cause a trend - things must be mentioned by several

import MySQLdb
import _mysql_exceptions
import cjson
import os
import time
from dateutil.parser import parse
from datetime import timedelta
import math

exclusions = ["a","able","about","across","after","all","almost","also","am",\
            "among","an","and","any","are","as","at","be","because","been","but",\
            "by","can","cannot","could","dear","did","do","does","either","else",\
            "ever","every","for","from","get","got","had","has","have","he","her",\
            "hers","him","his","how","however","i","if","in","into","is","it",\
            "its","just","least","let","like","likely","may","me","might","most",\
            "must","my","neither","no","nor","not","of","off","often","on","only",\
            "or","other","our","own","rather","said","say","says","she","should",\
            "since","so","some","than","that","the","their","them","then","there",\
            "these","they","this","tis","to","too","twas","us","wants","was","we",\
            "were","what","when","where","which","while","who","whom","why","will",\
            "with","would","yet","you","your"]


def dbConnect(dbuser,dbpass):
    db = MySQLdb.connect(user=dbuser,passwd=dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
    cursor = db.cursor()
    return cursor

if __name__ == "__main__":
    # Live analysis on ALL statistics - tweets in each minute etc until imported = 1
    # Only analyse each minute when a later minute's tweets have started to come in???
    # Calculate running total and mean etc

    # Load Config
    try:
        homedir = os.path.expanduser("~")
        file = open(homedir + "/twitter-login.conf")
    except IOError, e:
        print ("Failed to load login data - exiting")
        sys.exit(0)

    raw_config = file.read()
    file.close()

    # Read Config
    config = cjson.decode(raw_config)
    dbuser = config['dbuser']
    dbpass = config['dbpass']

    cursor = dbConnect(dbuser,dbpass)

    while 1:
        # The below does LIVE and FINAL analysis - do NOT run DataAnalyser at the same time
        # Check if analysed = 0

        print "Checking for unanalysed data..."
        
        
        # Sleep here until more data is available to analyse
        print "Sleeping for 1 second..."
        time.sleep(1)
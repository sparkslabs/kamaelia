#! /usr/bin/python

# Analyses saved data in DB to give something more useful. Saves to output DB ready for display in web interface
# Need word freq analysis, tweet rate analysis etc
# Any looking at natural language engines / subtitles should be done here or in components following this
# This component probably needs the original keywords etc too as it needs to separate both programmes and channels
# TODO: Ability to analyse multiple channels at once should be achieved automatically here, but still needs implementing at earlier stages.
# When analysing, look for mentions of just first names used with #programme etc, as people are unlikely to describe presenters etc with full names (could actually modify the original search to do this) TODO
# Watch out for repeated tweets - could be user or Twitter error
# Need to ensure one rogue user can't cause a trend - things must be mentioned by several

import MySQLdb
import cjson
import os
from dateutil.parser import parse
#from datetime import datetime

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
    # TODO: Do live analysis on ALL statistics - tweets in each minute etc until imported = 1
    # Only analyse each minute when a later minute's tweets have started to come in
    # Calculate running total and mean etc
    # TODO: Check if imported is 1 or not and if so do final analysis of all before setting analysed to 1
    # Final analysis involves redoing all earlier analysis to make sure nothing was missed
    # Calculate total, mean, median, mode, etc - anything needed

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
        # Check if imported = 1 and analysed = 0
        cursor.execute("""SELECT pid,title FROM programmes WHERE imported = 1 AND analysed = 0""")
        data = cursor.fetchall()

        for result in data:
            # If so, calculate total tweets and gather all keywords into a list
            pid = result[0]
            title = result[1]
            print "Currently processing " + title + ": " + pid
            cursor.execute("""SELECT keyword FROM keywords WHERE pid = %s""",(pid))
            kwdata = cursor.fetchall()
            keywords = list()
            for word in kwdata:
                keywords.append(str(word[0]))
            print "Keywords are: " + str(keywords)
            cursor.execute("""SELECT tid,datetime,text,user FROM rawdata WHERE pid = %s ORDER BY datetime ASC""",(pid))
            tweets = cursor.fetchall()
            numtweets = len(tweets)
            print "Total tweets: " + str(numtweets)

            # Then group tweets by minute and create db entries in 'analysed' for each minute
            tweetminutes = dict()
            for tweet in tweets:
                tid = tweet[0]
                tweettime = parse(tweet[1])
                tweettime = tweettime.replace(tzinfo=None)
                # Need to bear in mind that everything here is in GMT - if UK is in BST on a particular date bookmarks will need an offset
                tweettime = tweettime.replace(second=0)
                text = tweet[2]
                user = tweet[3]
                if not tweetminutes.has_key(str(tweettime)):
                    tweetminutes[str(tweettime)] = 1
                else:
                    tweetminutes[str(tweettime)] += 1

            print tweetminutes


            # Calculate average (mean) tweets per minute and store alongside programme (with total tweets)


            # Do word freq analysis on each minute and store top 20 words???? - expected and unexpected


        break


        

        

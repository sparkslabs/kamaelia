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
    # TODO: Do live analysis on ALL statistics - tweets in each minute etc until imported = 1
    # Only analyse each minute when a later minute's tweets have started to come in
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
        # The below does FINAL analysis only - live analysis still needs adding. This will likely need modifying once that's done
        # Check if imported = 1 and analysed = 0

        print "Checking for unanalysed data..."
        
        cursor.execute("""SELECT pid,title,duration FROM programmes WHERE imported = 1 AND analysed = 0""")
        data = cursor.fetchall()

        for result in data:
            # If so, calculate total tweets and gather all keywords into a list
            pid = result[0]
            title = result[1]
            duration = result[2]
            print "Currently processing " + title + ": " + pid
            cursor.execute("""SELECT keyword FROM keywords WHERE pid = %s""",(pid))
            kwdata = cursor.fetchall()
            keywords = list()
            for word in kwdata:
                keywords.append(str(word[0]))
            print "Keywords are: ", keywords
            cursor.execute("""SELECT tid,datetime,text,user FROM rawdata WHERE pid = %s ORDER BY datetime ASC""",(pid))
            tweets = cursor.fetchall()
            numtweets = len(tweets)
            print "Total tweets: ", numtweets

            if numtweets > 0:
                # Then group tweets by minute and create db entries in 'analysed' for each minute
                tweetminutes = dict()
                lasttime = None
                for tweet in tweets:
                    tid = tweet[0]
                    tweettime = parse(tweet[1])
                    tweettime = tweettime.replace(tzinfo=None)
                    # Need to bear in mind that everything here is in GMT - if UK is in BST on a particular date bookmarks will need an offset
                    tweettime = tweettime.replace(second=0)
                    if lasttime != None:
                        while tweettime > (lasttime + timedelta(seconds=60)):
                            lasttime += timedelta(seconds=60)
                            tweetminutes[str(lasttime)] = 0
                    text = tweet[2]
                    user = tweet[3]
                    if not tweetminutes.has_key(str(tweettime)):
                        tweetminutes[str(tweettime)] = 1
                    else:
                        tweetminutes[str(tweettime)] += 1
                    lasttime = tweettime

                print "Tweets per minute: ", tweetminutes


                # Calculate average (mean) tweets per minute and store alongside programme (with total tweets)
                duration = duration/60
                if numtweets > 0 and duration > 0:
                    meantweets = float(numtweets)/float(duration)
                else:
                    meantweets = 0

                print "Mean tweets per minute: ", meantweets

                # Calculate median
                if len(tweetminutes) < duration:
                    extrazeros = duration - len(tweetminutes)
                else:
                    extrazeros = 0

                midpoint = int((len(tweetminutes) + extrazeros) / 2)

                # Order the list!
                items = [[v, k] for k, v in tweetminutes.items()]
                items.sort()

                if midpoint <= extrazeros:
                    mediantweets = 0
                else:
                    midpoint -= (extrazeros + 1)
                    mediantweets = items[midpoint][0]

                print "Median tweets per minute: ", mediantweets

                # Calculate mode
                numcheck = dict({extrazeros : 0})
                for pair in items:
                    if numcheck.has_key(pair[0]):
                        numcheck[pair[0]] += 1
                    else:
                        numcheck[pair[0]] = 1

                ncitems = [[v, k] for k, v in numcheck.items()]
                ncitems.sort(reverse=True)
                modetweets = ncitems[0][1]

                print "Mode tweets per minute: ", modetweets

                # Calculate standard deviation / quartiles
                stdevsum = (0-meantweets)*(0-meantweets)*extrazeros
                for tweet in tweetminutes:
                  stdevsum += (tweetminutes[tweet]-meantweets)*(tweetminutes[tweet]-meantweets)
                stdevtweets = math.sqrt(stdevsum/(len(tweetminutes)+extrazeros))

                print "Standard deviation: ", stdevtweets

            else:
                meantweets = 0
                mediantweets = 0
                modetweets = 0
                stdevtweets = 0
                tweetminutes = dict()
            

            # Do word freq analysis on each minute and store top 20 words???? - expected and unexpected
            # TODO

            try:
                for minute in sorted(tweetminutes, reverse=True):
                    if tweetminutes[minute] > 0:
                        cursor.execute("""INSERT INTO analyseddata (pid,datetime,wordfreqexpected,wordfrequnexpected,totaltweets) VALUES (%s,%s,%s,%s,%s)""", (pid,minute,0,0,tweetminutes[minute]))

                cursor.execute("""UPDATE programmes SET analysed = 1, totaltweets = %s, meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s WHERE pid = %s""",(numtweets,meantweets,mediantweets,modetweets,stdevtweets,pid))
            except _mysql_exceptions.IntegrityError, e:
                print "Data has already been analysed. Clear DB tables to redo: ", e

        # Sleep here until more data is available to analyse
        print "Sleeping for 5 minutes..."
        time.sleep(60*5)
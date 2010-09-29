#! /usr/bin/python

# Analyses saved data in DB to give something more useful. Saves to output DB ready for display in web interface
# Need word freq analysis, tweet rate analysis etc
# Any looking at natural language engines / subtitles should be done here or in components following this
# Need to ensure one rogue user can't cause a trend - things must be mentioned by several

import MySQLdb
import cjson
import os
import time
from dateutil.parser import parse
from datetime import timedelta, datetime
import math
import sys


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
        # Bookmarks could be made more accurate by applying the timediff offset to the tweettime here

        print "Checking for new data..."

        # Stage 1: Live analysis - could do with a better way to do the first query - rather resource killing for SQL it seems
        # Could move this into the main app to take a copy of tweets on arrival, but would rather solve separately if poss
        cursor.execute("""SELECT tid,pid,datetime,text,user FROM rawdata WHERE analysed = 0 ORDER BY tid LIMIT 5000""")
        data = cursor.fetchall()

        for result in data:
            tid = result[0]
            pid = result[1]
            tweettime = result[2]
            tweettext = result[3]
            tweetuser = result[4]
            dbtime = parse(tweettime)
            dbtime = dbtime.replace(tzinfo=None)
            dbtime = dbtime.replace(second=0)
            print "Analysing new tweet for pid", pid, "(" + str(dbtime) + "):"
            print "'" + tweettext + "'"
            cursor.execute("""SELECT duration,totaltweets,meantweets,mediantweets,modetweets,stdevtweets,timediff,expectedstart FROM programmes WHERE pid = %s""",(pid))
            progdata = cursor.fetchone()
            duration = progdata[0]
            totaltweets = progdata[1]
            totaltweets += 1
            meantweets = progdata[2]
            mediantweets = progdata[3]
            modetweets = progdata[4]
            stdevtweets = progdata[5]
            timediff = progdata[6]
            expectedstart = progdata[7]
            cursor.execute("""SELECT did,totaltweets FROM analyseddata WHERE pid = %s AND datetime = %s""",(pid,dbtime))
            analyseddata = cursor.fetchone()
            if analyseddata == None: # No tweets yet recorded for this minute
                minutetweets = 1
                cursor.execute("""INSERT INTO analyseddata (pid,datetime,wordfreqexpected,wordfrequnexpected,totaltweets) VALUES (%s,%s,%s,%s,%s)""", (pid,dbtime,0,0,minutetweets))
            else:
                did = analyseddata[0]
                minutetweets = analyseddata[1] # Get current number of tweets for this minute
                minutetweets += 1 # Add one to it for this tweet
                cursor.execute("""UPDATE analyseddata SET totaltweets = %s WHERE did = %s""",(minutetweets,did))

            # Averages / stdev are calculated roughly based on the programme's running time at this point
            progdate = parse(expectedstart)
            tz = progdate.tzinfo
            progdate = progdate.replace(tzinfo=None)
            actualstart = progdate - timedelta(seconds=timediff)

            offset = datetime.strptime(str(tz.utcoffset(parse(tweettime))),"%H:%M:%S")
            offset = timedelta(hours=offset.hour)
            actualtweettime = parse(tweettime) + offset
            actualtweettime = actualtweettime.replace(tzinfo=None)

            # Calculate how far through the programme this tweet occurred
            runningtime = actualtweettime - actualstart
            runningtime = runningtime.seconds

            if runningtime < 0:
                runningtime = 0
            else:
                runningtime = float(runningtime) / 60

            try:
                meantweets = totaltweets / runningtime
            except ZeroDivisionError, e:
                meantweets = 0
                
            cursor.execute("""SELECT totaltweets FROM analyseddata WHERE pid = %s""",(pid))
            analyseddata = cursor.fetchall()

            runningtime = int(runningtime)

            tweetlist = list()
            for result in analyseddata:
                totaltweetsmin = result[0]
                tweetlist.append(int(totaltweetsmin))

            # Ensure tweetlist has enough entries
            if len(tweetlist) < runningtime:
                additions = runningtime - len(tweetlist)
                while additions > 0:
                    tweetlist.append(0)
                    additions -= 1

            tweetlist.sort()

            mediantweets = tweetlist[int(len(tweetlist)/2)]

            modes = dict()
            stdevlist = list()
            for tweet in tweetlist:
                modes[tweet] = tweetlist.count(tweet)
                stdevlist.append((tweet - meantweets)*(tweet - meantweets))

            modeitems = [[v, k] for k, v in modes.items()]
            modeitems.sort(reverse=True)
            modetweets = int(modeitems[0][1])

            stdevtweets = 0
            for val in stdevlist:
                stdevtweets += val

            try:
                stdevtweets = math.sqrt(stdevtweets / runningtime)
            except ZeroDivisionError, e:
                stdevtweets = 0

            # Finished analysis
            cursor.execute("""UPDATE programmes SET totaltweets = %s, meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s WHERE pid = %s""",(totaltweets,meantweets,mediantweets,modetweets,stdevtweets,pid))
            cursor.execute("""UPDATE rawdata SET analysed = 1 WHERE tid = %s""",(tid))
            print "Done!"
        
        # Stage 2: If all raw tweets analysed and imported = 1, finalise the analysis - could do bookmark identification here too?
        cursor.execute("""SELECT pid,duration,totaltweets,meantweets,mediantweets,modetweets,stdevtweets,title FROM programmes WHERE imported = 1 AND analysed = 0 LIMIT 5000""")
        data = cursor.fetchall()
        for result in data:
            pid = result[0]
            duration = result[1]
            totaltweets = result[2]
            meantweets = result[3]
            mediantweets = result[4]
            modetweets = result[5]
            stdevtweets = result[6]
            title = result[7]
            # Cycle through checking if all tweets for this programme have been analysed - if so finalise the stats
            cursor.execute("""SELECT tid FROM rawdata WHERE analysed = 0 AND pid = %s""", (pid))
            if cursor.fetchone() == None:
                # OK to finalise stats here
                print "Finalising stats for pid:", pid, "(" + title + ")"

                meantweets = float(totaltweets) / (duration / 60) # Mean tweets per minute

                cursor.execute("""SELECT totaltweets FROM analyseddata WHERE pid = %s""",(pid))
                analyseddata = cursor.fetchall()

                runningtime = duration / 60

                tweetlist = list()
                for result in analyseddata:
                    totaltweetsmin = result[0]
                    tweetlist.append(int(totaltweetsmin))

                # Ensure tweetlist has enough entries
                if len(tweetlist) < runningtime:
                    additions = runningtime - len(tweetlist)
                    while additions > 0:
                        tweetlist.append(0)
                        additions -= 1

                tweetlist.sort()

                mediantweets = tweetlist[int(len(tweetlist)/2)]

                modes = dict()
                stdevlist = list()
                for tweet in tweetlist:
                    modes[tweet] = tweetlist.count(tweet)
                    stdevlist.append((tweet - meantweets)*(tweet - meantweets))

                modeitems = [[v, k] for k, v in modes.items()]
                modeitems.sort(reverse=True)
                modetweets = int(modeitems[0][1])

                stdevtweets = 0
                for val in stdevlist:
                    stdevtweets += val
                try:
                    stdevtweets = math.sqrt(stdevtweets / runningtime)
                except ZeroDivisionError, e:
                    stdevtweets = 0
                
                cursor.execute("""UPDATE programmes SET meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s, analysed = 1 WHERE pid = %s""",(meantweets,mediantweets,modetweets,stdevtweets,pid))
                print "Done!"
                
        # Sleep here until more data is available to analyse
        print "Sleeping for 1 second..."
        time.sleep(1)
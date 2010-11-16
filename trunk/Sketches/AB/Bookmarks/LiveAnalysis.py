#! /usr/bin/python

# NB: It is recommended that this file is used for analysis as opposed to DataAnalyser.py

# Analyses saved data in DB to give something more useful. Saves to output DB ready for display in web interface
# Need word freq analysis, tweet rate analysis etc
# Any looking at natural language engines / subtitles should be done here or in components following this
# Need to ensure one rogue user can't cause a trend - things must be mentioned by several

# Having added this as a component, the printed output is a bit confusing, so 'Analysis component: ' has been added to everything.

import MySQLdb
import time
from datetime import timedelta, datetime
import math
import cjson
import string

from Axon.ThreadedComponent import threadedcomponent

class LiveAnalysis(threadedcomponent):
    Inboxes = {
        "inbox" : "",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "signal" : ""
    }

    def __init__(self, dbuser, dbpass):
        super(LiveAnalysis, self).__init__()
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.exclusions = ["a","able","about","across","after","all","almost","also","am",\
                    "among","an","and","any","are","as","at","be","because","been","but",\
                    "by","can","cannot","could","dear","did","do","does","either","else",\
                    "ever","every","for","from","get","got","had","has","have","he","her",\
                    "hers","him","his","how","however","i","if","in","into","is","it",\
                    "its","just","least","let","like","likely","may","me","might","most",\
                    "must","my","neither","no","nor","not","of","off","often","on","only",\
                    "or","other","our","own","rather","said","say","says","she","should",\
                    "since","so","some","than","that","the","their","them","then","there",\
                    "these","they","this","tis","to","too","twas","up","us","wants","was","we",\
                    "were","what","when","where","which","while","who","whom","why","will",\
                    "with","would","yet","you","your","via","rt"]

    def dbConnect(self,dbuser,dbpass):
        db = MySQLdb.connect(user=dbuser,passwd=dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
        cursor = db.cursor()
        return cursor

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def analyseTweet(self,cursor,pid,tweettext):
        # Do word frequency analysis at this point
        # Inefficient at the mo as if a tweet comes in at 48 or 59 secs etc, all previous tweets for that minute will be re-alanysed
        keywords = dict()
        cursor.execute("""SELECT uid,keyword,type FROM keywords WHERE pid = %s""",(pid))
        keyworddata = cursor.fetchall()
        for word in keyworddata:
            wordname = word[1]
            for items in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                wordname = string.replace(wordname,items,"")
                wordname = string.lower(wordname)
            keywords[wordname] = word[2]

        wordfreqexpected = dict()
        wordfrequnexpected = dict()
        words = list()
        filteredwords = list()

        for keyword in keywords:
            keyword = string.lower(keyword)
            if keyword in string.lower(tweettext):
                # Direct match (expected)
                if wordfreqexpected.has_key(keyword):
                    wordfreqexpected[keyword] = wordfreqexpected[keyword] + 1
                else:
                    wordfreqexpected[keyword] = 1
            elif "^" in keyword:
                splitter = keyword.split("^")
                if splitter[0] in string.lower(tweettext):
                    # Direct match (expected)
                    if wordfreqexpected.has_key(splitter[0]):
                        wordfreqexpected[splitter[0]] = wordfreqexpected[splitter[0]] + 1
                    else:
                        wordfreqexpected[splitter[0]] = 1

        splittweet = tweettext.split()
        newsplitlist = list()
        for word in splittweet:
            if not "http://" in word:
                wordnew = word
                for items in """*+-/<=>.\\_""":
                    wordnew = string.replace(wordnew,items," ")
                if wordnew != word:
                    for item in wordnew.split():
                        newsplitlist.append(item)
                else:
                    newsplitlist.append(word)
            else:
                newsplitlist.append(word)

        for word in newsplitlist:
            for items in """!"#$%&(),:;?@~[]'`{|}""":
                word = string.replace(word,items,"")
            if word != "":
                words.append(string.lower(word))
                if string.lower(word) not in self.exclusions:
                    filteredwords.append(word)

        for word in filteredwords:
            word = string.lower(word)
            if wordfrequnexpected.has_key(word) and not wordfreqexpected.has_key(word):
                wordfrequnexpected[word] = wordfrequnexpected[word] + 1
            elif not wordfreqexpected.has_key(word):
                wordfrequnexpected[word] = 1

        expecteditems = [(v,k) for k, v in wordfreqexpected.items()]
        expecteditems.sort(reverse=True)
        itemdict = dict()
        index = 0
        for item in expecteditems:
            itemdict[item[1]] = item[0]
            if index == 9:
                break
            index += 1
        #itemdict = cjson.encode(itemdict)
        unexpecteditems = [(v,k) for k, v in wordfrequnexpected.items()]
        unexpecteditems.sort(reverse=True)
        itemdict2 = dict()
        index = 0
        for item in unexpecteditems:
            itemdict2[item[1]] = item[0]
            if index == 9:
                break
            index += 1
        #itemdict2 = cjson.encode(itemdict2)

        return [itemdict,itemdict2]

    def main(self):
        # Calculate running total and mean etc

        cursor = self.dbConnect(self.dbuser,self.dbpass)

        while not self.finished():
            # The below does LIVE and FINAL analysis - do NOT run DataAnalyser at the same time
            # Bookmarks could be made more accurate by applying the timediff offset to the tweettime here

            print "Analysis component: Checking for new data..."

            # Stage 1: Live analysis - could do with a better way to do the first query (indexed field 'analsed' to speed up for now)
            # Could move this into the main app to take a copy of tweets on arrival, but would rather solve separately if poss
            cursor.execute("""SELECT tid,pid,timestamp,text,user FROM rawdata WHERE analysed = 0 ORDER BY tid LIMIT 5000""")
            data = cursor.fetchall()

            for result in data:
                tid = result[0]
                pid = result[1]
                tweettime = result[2]
                tweettext = result[3]
                tweetuser = result[4]
                dbtime = datetime.utcfromtimestamp(tweettime)
                dbtime = dbtime.replace(second=0)
                print "Analysis component: Analysing new tweet for pid", pid, "(" + str(dbtime) + "):"
                print "Analysis component: '" + tweettext + "'"
                cursor.execute("""SELECT duration,totaltweets,meantweets,mediantweets,modetweets,stdevtweets,timediff,timestamp,utcoffset FROM programmes WHERE pid = %s ORDER BY timestamp DESC""",(pid))
                progdata = cursor.fetchone()
                duration = progdata[0]
                totaltweets = progdata[1]
                totaltweets += 1
                meantweets = progdata[2]
                mediantweets = progdata[3]
                modetweets = progdata[4]
                stdevtweets = progdata[5]
                timediff = progdata[6]
                timestamp = progdata[7]
                utcoffset = progdata[8]
                dbtimestamp = time.mktime(dbtime.timetuple()) + utcoffset
                cursor.execute("""SELECT did,totaltweets,wordfreqexpected,wordfrequnexpected FROM analyseddata WHERE pid = %s AND timestamp = %s""",(pid,dbtimestamp))
                analyseddata = cursor.fetchone()
                if analyseddata == None: # No tweets yet recorded for this minute
                    minutetweets = 1
                    itemdicts = self.analyseTweet(cursor,pid,tweettext)
                    wfdict = cjson.encode(itemdicts[0])
                    wfudict = cjson.encode(itemdicts[1])
                    cursor.execute("""INSERT INTO analyseddata (pid,wordfreqexpected,wordfrequnexpected,totaltweets,timestamp) VALUES (%s,%s,%s,%s,%s)""", (pid,wfdict,wfudict,minutetweets,dbtimestamp))
                else:
                    did = analyseddata[0]
                    minutetweets = analyseddata[1] # Get current number of tweets for this minute
                    minutetweets += 1 # Add one to it for this tweet
                    wfexpected = cjson.decode(analyseddata[2])
                    wfunexpected = cjson.decode(analyseddata[3])
                    itemdicts = self.analyseTweet(cursor,pid,tweettext)
                    wfdict = itemdicts[0]
                    wfudict = itemdicts[1]
                    for entry in wfdict:
                        if wfexpected.has_key(entry):
                            wfexpected[entry] = wfexpected[entry] + wfdict[entry]
                        else:
                            wfexpected[entry] = wfdict[entry]
                    for entry in wfudict:
                        if wfunexpected.has_key(entry):
                            wfunexpected[entry] = wfunexpected[entry] + wfudict[entry]
                        else:
                            wfunexpected[entry] = wfudict[entry]
                    wfexpected = cjson.encode(wfexpected)
                    wfunexpected = cjson.encode(wfunexpected)


                    # Ensure we're not exceeding DB limits
                    # for now, if this happens we won't update the affected field
                    if len(wfunexpected) > 2000 and len(wfexpected) > 2000:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s WHERE did = %s""",(minutetweets,did))
                    elif len(wfexpected) > 2000:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s, wordfrequnexpected = %s WHERE did = %s""",(minutetweets,wfunexpected,did))
                    elif len(wfunexpected) > 2000:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s, wordfreqexpected = %s WHERE did = %s""",(minutetweets,wfexpected,did))
                    else:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s, wordfreqexpected = %s, wordfrequnexpected = %s WHERE did = %s""",(minutetweets,wfexpected,wfunexpected,did))

                # Averages / stdev are calculated roughly based on the programme's running time at this point
                progdate = datetime.utcfromtimestamp(timestamp) + timedelta(seconds=utcoffset)
                actualstart = progdate - timedelta(seconds=timediff)
                actualtweettime = datetime.utcfromtimestamp(tweettime + utcoffset)

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

                cursor.execute("""SELECT totaltweets FROM analyseddata WHERE pid = %s AND timestamp >= %s AND timestamp < %s""",(pid,timestamp,timestamp+duration))
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
                cursor.execute("""UPDATE programmes SET totaltweets = %s, meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s WHERE pid = %s AND timestamp = %s""",(totaltweets,meantweets,mediantweets,modetweets,stdevtweets,pid,timestamp))
                cursor.execute("""UPDATE rawdata SET analysed = 1 WHERE tid = %s""",(tid))
                print "Analysis component: Done!"

            # Stage 2: If all raw tweets analysed and imported = 1, finalise the analysis - could do bookmark identification here too?
            cursor.execute("""SELECT pid,duration,totaltweets,meantweets,mediantweets,modetweets,stdevtweets,title,timestamp,timediff FROM programmes WHERE imported = 1 AND analysed = 0 LIMIT 5000""")
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
                timestamp = result[8]
                timediff = result[9]
                # Cycle through checking if all tweets for this programme have been analysed - if so finalise the stats
                cursor.execute("""SELECT tid FROM rawdata WHERE analysed = 0 AND pid = %s""", (pid))
                if cursor.fetchone() == None:
                    # OK to finalise stats here
                    print "Analysis component: Finalising stats for pid:", pid, "(" + title + ")"

                    meantweets = float(totaltweets) / (duration / 60) # Mean tweets per minute

                    cursor.execute("""SELECT totaltweets FROM analyseddata WHERE pid = %s AND timestamp >= %s AND timestamp < %s""",(pid,timestamp,timestamp+duration))
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

                    cursor.execute("""UPDATE programmes SET meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s, analysed = 1 WHERE pid = %s AND timestamp = %s""",(meantweets,mediantweets,modetweets,stdevtweets,pid,timestamp))
                    print "Analysis component: Done!"

            # Sleep here until more data is available to analyse
            print "Analysis component: Sleeping for 10 seconds..."
            time.sleep(10)


class LiveAnalysisNLTK(threadedcomponent):
    Inboxes = {
        "inbox" : "",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "signal" : ""
    }

    def __init__(self, dbuser, dbpass):
        super(LiveAnalysisNLTK, self).__init__()
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.exclusions = ["a","able","about","across","after","all","almost","also","am",\
                    "among","an","and","any","are","as","at","be","because","been","but",\
                    "by","can","cannot","could","dear","did","do","does","either","else",\
                    "ever","every","for","from","get","got","had","has","have","he","her",\
                    "hers","him","his","how","however","i","if","in","into","is","it",\
                    "its","just","least","let","like","likely","may","me","might","most",\
                    "must","my","neither","no","nor","not","of","off","often","on","only",\
                    "or","other","our","own","rather","said","say","says","she","should",\
                    "since","so","some","than","that","the","their","them","then","there",\
                    "these","they","this","tis","to","too","twas","up","us","wants","was","we",\
                    "were","what","when","where","which","while","who","whom","why","will",\
                    "with","would","yet","you","your","via","rt"]

    def dbConnect(self,dbuser,dbpass):
        db = MySQLdb.connect(user=dbuser,passwd=dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
        cursor = db.cursor()
        return cursor

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def analyseTweet(self,cursor,pid,tweettext):
        # Do word frequency analysis at this point
        # Inefficient at the mo as if a tweet comes in at 48 or 59 secs etc, all previous tweets for that minute will be re-alanysed
        keywords = dict()
        cursor.execute("""SELECT uid,keyword,type FROM keywords WHERE pid = %s""",(pid))
        keyworddata = cursor.fetchall()
        for word in keyworddata:
            wordname = word[1]
            for items in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                wordname = string.replace(wordname,items,"")
                wordname = string.lower(wordname)
            keywords[wordname] = word[2]

        wordfreqexpected = dict()
        wordfrequnexpected = dict()
        words = list()
        filteredwords = list()

        for keyword in keywords:
            keyword = string.lower(keyword)
            if keyword in string.lower(tweettext):
                # Direct match (expected)
                if wordfreqexpected.has_key(keyword):
                    wordfreqexpected[keyword] = wordfreqexpected[keyword] + 1
                else:
                    wordfreqexpected[keyword] = 1
            elif "^" in keyword:
                splitter = keyword.split("^")
                if splitter[0] in string.lower(tweettext):
                    # Direct match (expected)
                    if wordfreqexpected.has_key(splitter[0]):
                        wordfreqexpected[splitter[0]] = wordfreqexpected[splitter[0]] + 1
                    else:
                        wordfreqexpected[splitter[0]] = 1

        splittweet = tweettext.split()
        newsplitlist = list()
        for word in splittweet:
            if not "http://" in word:
                wordnew = word
                for items in """*+-/<=>.\\_""":
                    wordnew = string.replace(wordnew,items," ")
                if wordnew != word:
                    for item in wordnew.split():
                        newsplitlist.append(item)
                else:
                    newsplitlist.append(word)
            else:
                newsplitlist.append(word)

        for word in newsplitlist:
            for items in """!"#$%&(),:;?@~[]'`{|}""":
                word = string.replace(word,items,"")
            if word != "":
                words.append(string.lower(word))
                if string.lower(word) not in self.exclusions:
                    filteredwords.append(word)

        for word in filteredwords:
            word = string.lower(word)
            if wordfrequnexpected.has_key(word) and not wordfreqexpected.has_key(word):
                wordfrequnexpected[word] = wordfrequnexpected[word] + 1
            elif not wordfreqexpected.has_key(word):
                wordfrequnexpected[word] = 1

        expecteditems = [(v,k) for k, v in wordfreqexpected.items()]
        expecteditems.sort(reverse=True)
        itemdict = dict()
        index = 0
        for item in expecteditems:
            itemdict[item[1]] = item[0]
            if index == 9:
                break
            index += 1
        #itemdict = cjson.encode(itemdict)
        unexpecteditems = [(v,k) for k, v in wordfrequnexpected.items()]
        unexpecteditems.sort(reverse=True)
        itemdict2 = dict()
        index = 0
        for item in unexpecteditems:
            itemdict2[item[1]] = item[0]
            if index == 9:
                break
            index += 1
        #itemdict2 = cjson.encode(itemdict2)

        return [itemdict,itemdict2]

    def main(self):
        # Calculate running total and mean etc

        cursor = self.dbConnect(self.dbuser,self.dbpass)

        while not self.finished():
            # The below does LIVE and FINAL analysis - do NOT run DataAnalyser at the same time
            # Bookmarks could be made more accurate by applying the timediff offset to the tweettime here

            print "Analysis component: Checking for new data..."

            # Stage 1: Live analysis - could do with a better way to do the first query (indexed field 'analsed' to speed up for now)
            # Could move this into the main app to take a copy of tweets on arrival, but would rather solve separately if poss
            cursor.execute("""SELECT tid,pid,timestamp,text,user FROM rawdata WHERE analysed = 0 ORDER BY tid LIMIT 5000""")
            data = cursor.fetchall()

            for result in data:
                tid = result[0]
                pid = result[1]
                tweettime = result[2]
                tweettext = result[3]
                tweetuser = result[4]
                dbtime = datetime.utcfromtimestamp(tweettime)
                dbtime = dbtime.replace(second=0)
                print "Analysis component: Analysing new tweet for pid", pid, "(" + str(dbtime) + "):"
                print "Analysis component: '" + tweettext + "'"
                cursor.execute("""SELECT duration,totaltweets,meantweets,mediantweets,modetweets,stdevtweets,timediff,timestamp,utcoffset FROM programmes WHERE pid = %s""",(pid))
                progdata = cursor.fetchone()
                duration = progdata[0]
                totaltweets = progdata[1]
                totaltweets += 1
                meantweets = progdata[2]
                mediantweets = progdata[3]
                modetweets = progdata[4]
                stdevtweets = progdata[5]
                timediff = progdata[6]
                timestamp = progdata[7]
                utcoffset = progdata[8]
                dbtimestamp = time.mktime(dbtime.timetuple()) + utcoffset
                cursor.execute("""SELECT did,totaltweets,wordfreqexpected,wordfrequnexpected FROM analyseddata WHERE pid = %s AND timestamp = %s""",(pid,dbtimestamp))
                analyseddata = cursor.fetchone()
                if analyseddata == None: # No tweets yet recorded for this minute
                    minutetweets = 1
                    itemdicts = self.analyseTweet(cursor,pid,tweettext)
                    wfdict = cjson.encode(itemdicts[0])
                    wfudict = cjson.encode(itemdicts[1])
                    cursor.execute("""INSERT INTO analyseddata (pid,wordfreqexpected,wordfrequnexpected,totaltweets,timestamp) VALUES (%s,%s,%s,%s,%s)""", (pid,wfdict,wfudict,minutetweets,dbtimestamp))
                else:
                    did = analyseddata[0]
                    minutetweets = analyseddata[1] # Get current number of tweets for this minute
                    minutetweets += 1 # Add one to it for this tweet
                    wfexpected = cjson.decode(analyseddata[2])
                    wfunexpected = cjson.decode(analyseddata[3])
                    itemdicts = self.analyseTweet(cursor,pid,tweettext)
                    wfdict = itemdicts[0]
                    wfudict = itemdicts[1]
                    for entry in wfdict:
                        if wfexpected.has_key(entry):
                            wfexpected[entry] = wfexpected[entry] + wfdict[entry]
                        else:
                            wfexpected[entry] = wfdict[entry]
                    for entry in wfudict:
                        if wfunexpected.has_key(entry):
                            wfunexpected[entry] = wfunexpected[entry] + wfudict[entry]
                        else:
                            wfunexpected[entry] = wfudict[entry]
                    wfexpected = cjson.encode(wfexpected)
                    wfunexpected = cjson.encode(wfunexpected)


                    # Ensure we're not exceeding DB limits
                    # for now, if this happens we won't update the affected field
                    if len(wfunexpected) > 2000 and len(wfexpected) > 2000:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s WHERE did = %s""",(minutetweets,did))
                    elif len(wfexpected) > 2000:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s, wordfrequnexpected = %s WHERE did = %s""",(minutetweets,wfunexpected,did))
                    elif len(wfunexpected) > 2000:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s, wordfreqexpected = %s WHERE did = %s""",(minutetweets,wfexpected,did))
                    else:
                        cursor.execute("""UPDATE analyseddata SET totaltweets = %s, wordfreqexpected = %s, wordfrequnexpected = %s WHERE did = %s""",(minutetweets,wfexpected,wfunexpected,did))

                # Averages / stdev are calculated roughly based on the programme's running time at this point
                progdate = datetime.utcfromtimestamp(timestamp) + timedelta(seconds=utcoffset)
                actualstart = progdate - timedelta(seconds=timediff)
                actualtweettime = datetime.utcfromtimestamp(tweettime + utcoffset)

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
                print "Analysis component: Done!"

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
                    print "Analysis component: Finalising stats for pid:", pid, "(" + title + ")"

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
                    print "Analysis component: Done!"

            # Sleep here until more data is available to analyse
            print "Analysis component: Sleeping for 10 seconds..."
            time.sleep(10)
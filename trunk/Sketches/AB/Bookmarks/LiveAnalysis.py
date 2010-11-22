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
import nltk
from nltk import FreqDist
import re

from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component

class LiveAnalysis(threadedcomponent):
    Inboxes = {
        "inbox" : "",
        "nltk" : "Receives data back from the NLTK component",
        "nltkfinal" : "Receives data back from the final NLTK analysis component",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "nltk" : "Sends data out to the NLTK component",
        "nltkfinal" : "Sends data out to the final NLTK analysis component",
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
            cursor.execute("""SELECT tid,pid,timestamp,text,user,tweet_id FROM rawdata WHERE analysed = 0 ORDER BY tid LIMIT 5000""")
            data = cursor.fetchall()

            for result in data:
                tid = result[0]
                pid = result[1]
                tweettime = result[2]
                tweettext = result[3]
                tweetuser = result[4]
                tweetid = result[5]
                dbtime = datetime.utcfromtimestamp(tweettime)
                dbtime = dbtime.replace(second=0)
                print "Analysis component: Analysing new tweet for pid", pid, "(" + str(dbtime) + "):"
                print "Analysis component: '" + tweettext + "'"
                cursor.execute("""SELECT duration FROM programmes_unique WHERE pid = %s""",(pid))
                progdata = cursor.fetchone()
                cursor.execute("""SELECT totaltweets,meantweets,mediantweets,modetweets,stdevtweets,timediff,timestamp,utcoffset FROM programmes WHERE pid = %s ORDER BY timestamp DESC""",(pid))
                progdata2 = cursor.fetchone()
                duration = progdata[0]
                totaltweets = progdata2[0]
                totaltweets += 1
                meantweets = progdata2[1]
                mediantweets = progdata2[2]
                modetweets = progdata2[3]
                stdevtweets = progdata2[4]
                timediff = progdata2[5]
                timestamp = progdata2[6]
                utcoffset = progdata2[7]
                dbtimestamp = time.mktime(dbtime.timetuple()) + utcoffset
                cursor.execute("""SELECT did,totaltweets,wordfreqexpected,wordfrequnexpected FROM analyseddata WHERE pid = %s AND timestamp = %s""",(pid,dbtimestamp))
                analyseddata = cursor.fetchone()
                self.send([pid,tweetid],"nltk")
                while not self.dataReady("nltk"):
                    time.sleep(0.01)
                nltkdata = self.recv("nltk")
                if analyseddata == None: # No tweets yet recorded for this minute
                    minutetweets = 1
                    cursor.execute("""INSERT INTO analyseddata (pid,totaltweets,timestamp) VALUES (%s,%s,%s)""", (pid,minutetweets,dbtimestamp))
                    for word in nltkdata:
                        if nltkdata[word][0] == 1:
                            cursor.execute("""INSERT INTO wordanalysis (pid,timestamp,phrase,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,dbtimestamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                        else:
                            cursor.execute("""INSERT INTO wordanalysis (pid,timestamp,word,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,dbtimestamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                else:
                    did = analyseddata[0]
                    minutetweets = analyseddata[1] # Get current number of tweets for this minute
                    minutetweets += 1 # Add one to it for this tweet

                    cursor.execute("""UPDATE analyseddata SET totaltweets = %s WHERE did = %s""",(minutetweets,did))

                    for word in nltkdata:
                        if nltkdata[word][0] == 1:
                            cursor.execute("""SELECT wid,count FROM wordanalysis WHERE pid = %s AND timestamp = %s AND phrase LIKE %s""",(pid,dbtimestamp,word))
                            wordcheck = cursor.fetchone()
                            if wordcheck == None:
                                cursor.execute("""INSERT INTO wordanalysis (pid,timestamp,phrase,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,dbtimestamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                            else:
                                cursor.execute("""UPDATE wordanalysis SET count = %s WHERE wid = %s""",(nltkdata[word][1] + wordcheck[1],wordcheck[0]))
                        else:
                            cursor.execute("""SELECT wid,count FROM wordanalysis WHERE pid = %s AND timestamp = %s AND word LIKE %s""",(pid,dbtimestamp,word))
                            wordcheck = cursor.fetchone()
                            if wordcheck == None:
                                cursor.execute("""INSERT INTO wordanalysis (pid,timestamp,word,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,dbtimestamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                            else:
                                cursor.execute("""UPDATE wordanalysis SET count = %s WHERE wid = %s""",(nltkdata[word][1] + wordcheck[1],wordcheck[0]))
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

                sqltimestamp1 = timestamp + timediff
                if dbtimestamp < sqltimestamp1:
                    sqltimestamp1 = dbtimestamp
                sqltimestamp2 = timestamp + duration - timediff
                if dbtimestamp > sqltimestamp2:
                    sqltimestamp2 = dbtimestamp
                # This isn't great - needs redoing TODO
                cursor.execute("""SELECT totaltweets FROM analyseddata WHERE pid = %s AND timestamp >= %s AND timestamp < %s""",(pid,sqltimestamp1,sqltimestamp2))
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
            cursor.execute("""SELECT pid,totaltweets,meantweets,mediantweets,modetweets,stdevtweets,timestamp,timediff FROM programmes WHERE imported = 1 AND analysed = 0 LIMIT 5000""")
            data = cursor.fetchall()
            for result in data:
                pid = result[0]
                cursor.execute("""SELECT duration,title FROM programmes_unique WHERE pid = %s""",(pid))
                data2 = cursor.fetchone()
                duration = data2[0]
                totaltweets = result[1]
                meantweets = result[2]
                mediantweets = result[3]
                modetweets = result[4]
                stdevtweets = result[5]
                title = data2[1]
                timestamp = result[6]
                timediff = result[7]
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

                    if 1:
                        sqltimestamp1 = timestamp - timediff
                        sqltimestamp2 = timestamp + duration - timediff
                        cursor.execute("""SELECT tweet_id FROM rawdata WHERE pid = %s AND timestamp >= %s AND timestamp < %s""", (pid,sqltimestamp1,sqltimestamp2))
                        rawtweetids = cursor.fetchall()
                        tweetids = list()
                        for tweet in rawtweetids:
                            tweetids.append(tweet[0])

                        if len(tweetids) > 0:
                            self.send([pid,tweetids],"nltkfinal")
                            while not self.dataReady("nltkfinal"):
                                time.sleep(0.01)
                            nltkdata = self.recv("nltkfinal")

                    cursor.execute("""UPDATE programmes SET meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s, analysed = 1 WHERE pid = %s AND timestamp = %s""",(meantweets,mediantweets,modetweets,stdevtweets,pid,timestamp))
                    print "Analysis component: Done!"

            # Sleep here until more data is available to analyse
            print "Analysis component: Sleeping for 10 seconds..."
            time.sleep(10)


class LiveAnalysisNLTK(component):
    Inboxes = {
        "inbox" : "",
        "tweetfixer" : "",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "tweetfixer" : "",
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

    def spellingFixer(self,text):
	# Fix ahahahahahaha and hahahahaha
        # Doesn't catch bahahahaha TODO
        # Also seem to be missing HAHAHAHA - case issue? TODO
        # Some sort of issue with Nooooooo too - it's just getting erased? #TODO
	text = re.sub("\S{0,}(ha){2,}\S{0,}","haha",text,re.I)
	# fix looooooool and haaaaaaaaaaa - fails for some words at the mo, for example welllll will be converted to wel, and hmmm to hm etc
	# Perhaps we could define both 'lol' and 'lool' as words, then avoid the above problem by reducing repeats to a max of 2
	x = re.findall(r'((\D)\2*)',text,re.I)
	for entry in sorted(x,reverse=True):
            if len(entry[0])>2:
                text = text.replace(entry[0],entry[1]).strip()
            if len(text) == 1:
                text += text
	return text

    def main(self):
        # Calculate running total and mean etc

        cursor = self.dbConnect(self.dbuser,self.dbpass)

        while not self.finished():

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                pid = data[0]
                tweetid = data[1]

                # There is a possibility at this point that the tweet won't yet be in the DB.
                # We'll have to stall for now if that happens but eventually it should be ensured tweets will be in the DB first

                # Issue #TODO - Words that appear as part of a keyword but not the whole thing won't get marked as being a keyword (e.g. Blue Peter - two diff words)
                # Need to check for each word if it forms part of a phrase which is also a keyword
                # If so, don't count is as a word, count the whole thing as a phrase and remember not to count it more than once
                # May actually store phrases AS WELL AS keywords

                tweetdata = None
                while tweetdata == None:
                    cursor.execute("""SELECT tweet_json FROM rawtweets WHERE tweet_id = %s""",(tweetid))
                    tweetdata = cursor.fetchone()
                    if tweetdata == None:
                        self.pause()
                        yield 1

                tweetjson = cjson.decode(tweetdata[0])

                keywords = dict()
                cursor.execute("""SELECT keyword,type FROM keywords WHERE pid = %s""",(pid))
                keyworddata = cursor.fetchall()
                for word in keyworddata:
                    wordname = word[0].lower()
                    keywords[wordname] = word[1]

                self.send(tweetjson,"tweetfixer")
                while not self.dataReady("tweetfixer"):
                    self.pause()
                    yield 1
                tweetjson = self.recv("tweetfixer")

                # Format: {"word" : [is_phrase,count,is_keyword,is_entity,is_common]}
                # Need to change this for retweets as they should include all the text content if truncated - need some clever merging FIXME TODO
                wordfreqdata = dict()
                for item in tweetjson['entities']['user_mentions']:
                    if wordfreqdata.has_key("@" + item['screen_name']):
                        wordfreqdata["@" + item['screen_name']][1] += 1
                    else:
                        if item['screen_name'].lower() in keywords or "@" + item['screen_name'].lower() in keywords:
                            wordfreqdata["@" + item['screen_name']] = [0,1,1,1,0]
                        else:
                            wordfreqdata["@" + item['screen_name']] = [0,1,0,1,0]
                for item in tweetjson['entities']['urls']:
                    if wordfreqdata.has_key(item['url']):
                        wordfreqdata[item['url']][1] += 1
                    else:
                        wordfreqdata[item['url']] = [0,1,0,1,0]
                for item in tweetjson['entities']['hashtags']:
                    if wordfreqdata.has_key("#" + item['text']):
                        wordfreqdata["#" + item['text']][1] += 1
                    else:
                        if item['text'].lower() in keywords or "#" + item['text'].lower() in keywords:
                            wordfreqdata["#" + item['text']] = [0,1,1,1,0]
                        else:
                            wordfreqdata["#" + item['text']] = [0,1,0,1,0]

                tweettext = self.spellingFixer(tweetjson['filtered_text']).split()
                for word in tweettext:
                    if word[0] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                        word = word[1:]
                    if word != "":
                        # Done twice to capture things like 'this is a "quote".'
                        if len(word) >= 2:
                            if word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and word[len(word)-2:len(word)] != "s'" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                word = word[:len(word)-1]
                                if word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and word[len(word)-2:len(word)] != "s'" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                    word = word[:len(word)-1]
                        elif word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                            word = word[:len(word)-1]
                            if word != "":
                                if word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                    word = word[:len(word)-1]
                    if word != "":
                        if word in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                            word = ""

                    if word != "":
                        if wordfreqdata.has_key(word):
                            wordfreqdata[word][1] += 1
                        else:
                            if word.lower() in self.exclusions:
                                exclude = 1
                            else:
                                exclude = 0
                            if word.lower() in keywords:
                                wordfreqdata[word] = [0,1,1,0,exclude]
                            else:
                                wordfreqdata[word] = [0,1,0,0,exclude]

                self.send(wordfreqdata,"outbox")

            self.pause()
            yield 1

class FinalAnalysisNLTK(component):
    Inboxes = {
        "inbox" : "",
        "tweetfixer" : "",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "tweetfixer" : "",
        "signal" : ""
    }

    def __init__(self, dbuser, dbpass):
        super(FinalAnalysisNLTK, self).__init__()
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

    def spellingFixer(self,text):
	# Fix ahahahahahaha and hahahahaha
	text = re.sub("\S{0,}(ha){2,}\S{0,}","haha",text,re.I)
        # E-mail filter
        text = re.sub("\S{1,}@\S{1,}.\S{1,}","",text,re.I)
	# fix looooooool and haaaaaaaaaaa - fails for some words at the mo, for example welllll will be converted to wel, and hmmm to hm etc
	# Perhaps we could define both 'lol' and 'lool' as words, then avoid the above problem by reducing repeats to a max of 2
	x = re.findall(r'((\D)\2*)',text,re.I)
	for entry in sorted(x,reverse=True):
            if len(entry[0])>2:
                text = text.replace(entry[0],entry[1]).strip()
            if len(text) == 1:
                text += text
	return text

    def main(self):
        # Calculate running total and mean etc

        cursor = self.dbConnect(self.dbuser,self.dbpass)

        while not self.finished():

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                pid = data[0]
                tweetids = data[1]

                # Issue #TODO - Words that appear as part of a keyword but not the whole thing won't get marked as being a keyword (e.g. Blue Peter - two diff words)
                # Need to check for each word if it forms part of a phrase which is also a keyword
                # If so, don't count is as a word, count the whole thing as a phrase and remember not to count it more than once
                # May actually store phrases AS WELL AS keywords

                keywords = dict()
                cursor.execute("""SELECT keyword,type FROM keywords WHERE pid = %s""",(pid))
                keyworddata = cursor.fetchall()
                for word in keyworddata:
                    wordname = word[0].lower()
                    if "^" in wordname:
                        wordbits = wordname.split("^")
                        wordname = wordbits[0]
                    wordbits = wordname.split()
                    # Only looking at phrases here (more than one word)
                    if len(wordbits) > 1:
                        keywords[wordname] = word[1]

                filteredtext = list()
                for tweetid in tweetids:

                    tweetdata = None
                    while tweetdata == None:
                        cursor.execute("""SELECT tweet_json FROM rawtweets WHERE tweet_id = %s""",(tweetid))
                        tweetdata = cursor.fetchone()
                        if tweetdata != None:

                            tweetjson = cjson.decode(tweetdata[0])

                            self.send(tweetjson,"tweetfixer")
                            while not self.dataReady("tweetfixer"):
                                self.pause()
                                yield 1
                            tweetjson = self.recv("tweetfixer")

                            tweettext = self.spellingFixer(tweetjson['filtered_text']).split()
                            
                            for word in tweettext:
                                if word[0] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                    word = word[1:]
                                if word != "":
                                    # Done twice to capture things like 'this is a "quote".'
                                    if len(word) >= 2:
                                        if word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and word[len(word)-2:len(word)] != "s'" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                            word = word[:len(word)-1]
                                            if word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and word[len(word)-2:len(word)] != "s'" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                                word = word[:len(word)-1]
                                    elif word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                        word = word[:len(word)-1]
                                        if word != "":
                                            if word[len(word)-1] in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and not (len(word) <= 3 and (word[0] == ":" or word[0] == ";")):
                                                word = word[:len(word)-1]
                                if word != "":
                                    if word in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                                        word = ""

                                if word != "":
                                    filteredtext.append(word)

                # Format: {"word" : [is_phrase,count,is_keyword,is_entity,is_common]}
                # Need to change this for retweets as they should include all the text content if truncated - need some clever merging FIXME TODO
                wordfreqdata = dict()

                bigram_fd = FreqDist(nltk.bigrams(filteredtext))

                print bigram_fd

                for entry in bigram_fd:
                    if entry[0] not in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and entry[1] not in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                        if entry[0] not in self.exclusions and entry[1] not in self.exclusions:
                            for word in keywords:
                                print word
                                if entry[0] in word and entry[1] in word:
                                    print "Keyword Match! " + str([entry[0],entry[1]])
                                    break
                            else:
                                print [entry[0],entry[1]]

                self.send(None,"outbox")

            self.pause()
            yield 1
#! /usr/bin/python

'''
Analyses saved data in DB to give something more useful. Saves to output DB ready for display in web interface
Any looking at natural language engines / subtitles should be done here or in components following this
Need to ensure one rogue user can't cause a trend - things must be mentioned by several
'''

# Having added this as a component, the Printed output is a bit confusing, so 'Analysis component: ' has been added to everything.

raise NotImplementedError("Needs fixing due to MySQLdb  -- python 2.0 based -- dependency")
import json as cjson
import math
import re
import time
import MySQLdb
import nltk
from nltk import FreqDist
from datetime import datetime, timedelta

from Axon.Component import component
from Axon.Ipc import producerFinished
from Axon.Ipc import shutdownMicroprocess
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Apps.SocialBookmarks.Print import Print
from Kamaelia.Apps.SocialBookmarks.DBWrapper import DBWrapper

class LiveAnalysis(DBWrapper,threadedcomponent):
    Inboxes = {
        "inbox" : "Unused",
        "nltk" : "Receives data back from the NLTK component",
        "nltkfinal" : "Receives data back from the final NLTK analysis component",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Unused",
        "nltk" : "Sends data out to the NLTK component",
        "nltkfinal" : "Sends data out to the final NLTK analysis component",
        "signal" : ""
    }

    def __init__(self, dbuser, dbpass):
        super(LiveAnalysis, self).__init__(dbuser=dbuser, dbpass=dbpass)
        # List of 'common' words so they can be labelled as such when the data is stored
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

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):
        # Calculate running total and mean etc
            self.dbConnect()
            while not self.finished():
                # The below does LIVE and FINAL analysis - do NOT run DataAnalyser at the same time

                Print("Analysis component: Checking for new data...")

                # Stage 1: Live analysis - could do with a better way to do the first query (indexed field 'analsed' to speed up for now)
                # Could move this into the main app to take a copy of tweets on arrival, but would rather solve separately if poss
                self.db_select("""SELECT tid,pid,timestamp,text,tweet_id,programme_position FROM rawdata WHERE analysed = 0 ORDER BY tid LIMIT 5000""")
                data = self.db_fetchall()

                # Cycle through all the as yet unanalysed tweets
                for result in data:
                    tid = result[0]
                    pid = result[1]
                    tweettime = result[2] # Timestamp based on the tweet's created_at field
                    tweettext = result[3]
                    tweetid = result[4] # This is the real tweet ID, tid just makes a unique identifier as each tweet can be stored against several pids
                    progpos = result[5] # Position through the programme that the tweet was made
                    dbtime = datetime.utcfromtimestamp(tweettime)
                    # Each tweet will be grouped into chunks of one minute to make display better, so set the seconds to zero
                    # This particular time is only used for console display now as a more accurate one calculated from programme position is found later
                    dbtime = dbtime.replace(second=0)
                    Print("Analysis component: Analysing new tweet for pid", pid, "(" , dbtime ,"):")
                    try:
                        Print("Analysis component: '" , tweettext , "'")
                    except UnicodeEncodeError:
                        e = sys.exc_info()[1]
                        Print ("UnicodeEncodeError", e)
                    self.db_select("""SELECT duration FROM programmes_unique WHERE pid = %s""",(pid))
                    progdata = self.db_fetchone()
                    duration = progdata[0]
                    self.db_select("""SELECT totaltweets,meantweets,mediantweets,modetweets,stdevtweets,timediff,timestamp,utcoffset FROM programmes WHERE pid = %s ORDER BY timestamp DESC""",(pid))
                    progdata2 = self.db_fetchone()
                    totaltweets = progdata2[0]
                    # Increment the total tweets recorded for this programme's broadcast
                    totaltweets += 1
                    meantweets = progdata2[1]
                    mediantweets = progdata2[2]
                    modetweets = progdata2[3]
                    stdevtweets = progdata2[4]
                    timediff = progdata2[5]
                    timestamp = progdata2[6]
                    utcoffset = progdata2[7]

                    # Need to work out the timestamp to assign to the entry in analysed data
                    progstart = timestamp - timediff
                    progmins = int(progpos / 60)
                    analysedstamp = int(progstart + (progmins * 60))
                    # Ensure that this tweet occurs within the length of the programme, otherwise for the purposes of this program it's useless

                    if progpos > 0 and progpos <= duration:
                        self.db_select("""SELECT did,totaltweets,wordfreqexpected,wordfrequnexpected FROM analyseddata WHERE pid = %s AND timestamp = %s""",(pid,analysedstamp))
                        analyseddata = self.db_fetchone()
                        # Just in case of a missing raw json object (ie. programme terminated before it was stored - allow it to be skipped if not found after 30 secs)
                        #failcounter = 0
                        # Pass this tweet to the NLTK analysis component
                        self.send([pid,tweetid],"nltk")
#                        print "BUM", 1
                        while not self.dataReady("nltk"):
                        #    if failcounter >= 3000:
                        #        nltkdata = list()
                        #        break
                            time.sleep(0.01)
                        #    failcounter += 1
                        #if failcounter < 3000:
#                        print "BUM", 2
                        if 1:
                            # Receive back a list of words and their frequency for this tweet, including whether or not they are common, an entity etc
                            nltkdata = self.recv("nltk")
                        if analyseddata == None: # No tweets yet recorded for this minute
                            minutetweets = 1
                            self.db_insert("""INSERT INTO analyseddata (pid,totaltweets,timestamp) VALUES (%s,%s,%s)""", (pid,minutetweets,analysedstamp))
                            for word in nltkdata:
                                # Check if we're storing a word or phrase here
                                if nltkdata[word][0] == 1:
                                    self.db_insert("""INSERT INTO wordanalysis (pid,timestamp,phrase,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,analysedstamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                                else:
                                    self.db_insert("""INSERT INTO wordanalysis (pid,timestamp,word,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,analysedstamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                        else:
                            did = analyseddata[0]
                            minutetweets = analyseddata[1] # Get current number of tweets for this minute
                            minutetweets += 1 # Add one to it for this tweet

                            self.db_update("""UPDATE analyseddata SET totaltweets = %s WHERE did = %s""",(minutetweets,did))

                            for word in nltkdata:
                                # Check if we're storing a word or phrase
                                if nltkdata[word][0] == 1:
                                    self.db_select("""SELECT wid,count FROM wordanalysis WHERE pid = %s AND timestamp = %s AND phrase LIKE %s""",(pid,analysedstamp,word))
                                    # Check if this phrase has already been stored for this minute - if so, increment the count
                                    wordcheck = self.db_fetchone()
                                    if wordcheck == None:
                                        self.db_insert("""INSERT INTO wordanalysis (pid,timestamp,phrase,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,analysedstamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                                    else:
                                        self.db_update("""UPDATE wordanalysis SET count = %s WHERE wid = %s""",(nltkdata[word][1] + wordcheck[1],wordcheck[0]))
                                else:
                                    self.db_select("""SELECT wid,count FROM wordanalysis WHERE pid = %s AND timestamp = %s AND word LIKE %s""",(pid,analysedstamp,word))
                                    # Check if this word has already been stored for this minute - if so, increment the count
                                    wordcheck = self.db_fetchone()
                                    if wordcheck == None:
                                        self.db_insert("""INSERT INTO wordanalysis (pid,timestamp,word,count,is_keyword,is_entity,is_common) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (pid,analysedstamp,word,nltkdata[word][1],nltkdata[word][2],nltkdata[word][3],nltkdata[word][4]))
                                    else:
                                        self.db_update("""UPDATE wordanalysis SET count = %s WHERE wid = %s""",(nltkdata[word][1] + wordcheck[1],wordcheck[0]))
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
                        except ZeroDivisionError:
                            meantweets = 0

                        self.db_select("""SELECT totaltweets FROM analyseddata WHERE pid = %s AND timestamp >= %s AND timestamp < %s""",(pid,progstart,analysedstamp+duration))
                        analyseddata = self.db_fetchall()

                        runningtime = int(runningtime)

                        tweetlist = list()
                        for result in analyseddata:
                            totaltweetsmin = result[0]
                            # Create a list of each minute and the total tweets for that minute in the programme
                            tweetlist.append(int(totaltweetsmin))

                        # Ensure tweetlist has enough entries
                        # If a minute has no tweets, it won't have a database record, so this has to be added
                        if len(tweetlist) < runningtime:
                            additions = runningtime - len(tweetlist)
                            while additions > 0:
                                tweetlist.append(0)
                                additions -= 1

                        # Order by programme position 0,1,2, mins etc
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
                        except ZeroDivisionError:
                            stdevtweets = 0

                        # Finished analysis - update DB
                        self.db_update("""UPDATE programmes SET totaltweets = %s, meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s WHERE pid = %s AND timestamp = %s""",(totaltweets,meantweets,mediantweets,modetweets,stdevtweets,pid,timestamp))

                    else:
                        pass
                        # Print("Analysis component: Skipping tweet - falls outside the programme's running time")

                    # Mark the tweet as analysed
                    self.db_update("""UPDATE rawdata SET analysed = 1 WHERE tid = %s""",(tid))
                    Print("Analysis component: Done!")

                # Stage 2: If all raw tweets analysed and imported = 1 (all data for this programme stored and programme finished), finalise the analysis - could do bookmark identification here too?
                self.db_select("""SELECT pid,totaltweets,meantweets,mediantweets,modetweets,stdevtweets,timestamp,timediff FROM programmes WHERE imported = 1 AND analysed = 0 LIMIT 5000""")
                data = self.db_fetchall()
                # Cycle through each programme that's ready for final analysis
                for result in data:
                    pid = result[0]
                    self.db_select("""SELECT duration,title FROM programmes_unique WHERE pid = %s""",(pid))
                    data2 = self.db_fetchone()
                    if not data2:
                        Print("Getting data for duration,title, etc failed - pid", pid)
                        Print("Let's try skipping this pid")
                        continue
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
                    self.db_select("""SELECT tid FROM rawdata WHERE analysed = 0 AND pid = %s""", (pid))
                    if self.db_fetchone() == None:
                        # OK to finalise stats here
                        Print("Analysis component: Finalising stats for pid:", pid, "(" , title , ")")
                        meantweets = float(totaltweets) / (duration / 60) # Mean tweets per minute
                        self.db_select("""SELECT totaltweets FROM analyseddata WHERE pid = %s AND timestamp >= %s AND timestamp < %s""",(pid,timestamp-timediff,timestamp+duration-timediff))
                        analyseddata = self.db_fetchall()

                        runningtime = duration / 60

                        tweetlist = list()
                        for result in analyseddata:
                            totaltweetsmin = result[0]
                            tweetlist.append(int(totaltweetsmin))

                        # Ensure tweetlist has enough entries - as above, if no tweets are recorded for a minute it won't be present in the DB
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
                        except ZeroDivisionError:
                            stdevtweets = 0

                        if 1: # This data is purely a readout to the terminal at the moment associated with word and phrase frequency, and retweets
                            sqltimestamp1 = timestamp - timediff
                            sqltimestamp2 = timestamp + duration - timediff
                            self.db_select("""SELECT tweet_id FROM rawdata WHERE pid = %s AND timestamp >= %s AND timestamp < %s""", (pid,sqltimestamp1,sqltimestamp2))
                            rawtweetids = self.db_fetchall()
                            tweetids = list()
                            for tweet in rawtweetids:
                                tweetids.append(tweet[0])

                            if len(tweetids) > 0:
                                # Just in case of a missing raw json object (ie. programme terminated before it was stored - allow it to be skipped if not found after 10 secs)
                                failcounter = 0
                                self.send([pid,tweetids],"nltkfinal")
                                while not self.dataReady("nltkfinal"):
                                    if failcounter >= 1000:
                                        Print("Timed out waiting for NTLKFINAL")
                                        nltkdata = list()
                                        break
                                    time.sleep(0.01)

                                    failcounter += 1
                                    if failcounter %100 == 0:
                                        Print( "Hanging waiting for NLTKFINAL" )

                                Print("failcounter (<1000 is success)", failcounter)
                                if failcounter < 1000:
#                                if 1:
                                    nltkdata = self.recv("nltkfinal")

                        self.db_update("""UPDATE programmes SET meantweets = %s, mediantweets = %s, modetweets = %s, stdevtweets = %s, analysed = 1 WHERE pid = %s AND timestamp = %s""",(meantweets,mediantweets,modetweets,stdevtweets,pid,timestamp))
                        Print("Analysis component: Done!")

                # Sleep here until more data is available to analyse
                Print("Analysis component: Sleeping for 10 seconds...")
                time.sleep(10)


class LiveAnalysisNLTK(DBWrapper, component):
    Inboxes = {
        "inbox" : "Receives a tweet ID and its related PID for NLTK analysis [pid,tweetid]",
        "tweetfixer" : "Received data back from the tweet fixing components (tweet json)",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Sends out analysed words/phrases in the format {'word/phrase' : [is_phrase,count,is_keyword,is_entity,is_common]}",
        "tweetfixer" : "Sends out data to the tweet fixing components (tweet json)",
        "signal" : ""
    }

    def __init__(self, dbuser, dbpass):
        super(LiveAnalysisNLTK, self).__init__(dbuser=dbuser, dbpass=dbpass)
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

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def spellingFixer(self,text):
        # This function attempts to normalise some common Twitter mis-spellings and accentuations
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
        self.dbConnect()

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
                twnc = 0
                while tweetdata == None:
                    # Retrieve the tweet json corresponding to the ID receieved
                    self.db_select("""SELECT tweet_json FROM rawtweets WHERE tweet_id = %s""",(tweetid))
                    tweetdata = self.db_fetchone()
                    if tweetdata == None:
                        twnc += 1
                        # self.pause()
                        yield 1
                    if twnc == 100:
                        break

#                print "NLTK", 2
                if tweetdata == None:
                    self.send({},"outbox")
                else:
                    tweetjson = cjson.decode(tweetdata[0])

                    keywords = dict()
                    # Find the keywords relating to the PID received
                    self.db_select("""SELECT keyword,type FROM keywords WHERE pid = %s""",(pid))
                    keyworddata = self.db_fetchall()
                    for word in keyworddata:
                        wordname = word[0].lower()
                        keywords[wordname] = word[1]

                    # Send the tweet off to have retweets fixed, links analysed etc
                    self.send(tweetjson,"tweetfixer")
                    while not self.dataReady("tweetfixer"):
                        self.pause()
                        yield 1
                    tweetjson = self.recv("tweetfixer")

                    # Format: {"word" : [is_phrase,count,is_keyword,is_entity,is_common]}
                    wordfreqdata = dict()
                    for item in tweetjson['entities']['user_mentions']:
                        if ( ("@" + item['screen_name']) in wordfreqdata):
                            wordfreqdata["@" + item['screen_name']][1] += 1
                        else:
                            if item['screen_name'].lower() in keywords or "@" + item['screen_name'].lower() in keywords:
                                wordfreqdata["@" + item['screen_name']] = [0,1,1,1,0]
                            else:
                                wordfreqdata["@" + item['screen_name']] = [0,1,0,1,0]
                    for item in tweetjson['entities']['urls']:
                        if ( item['url'] in wordfreqdata):
                            wordfreqdata[item['url']][1] += 1
                        else:
                            wordfreqdata[item['url']] = [0,1,0,1,0]
                    for item in tweetjson['entities']['hashtags']:
                        if ( ("#" + item['text']) in wordfreqdata):
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
                            if ( word in wordfreqdata):
                                wordfreqdata[word][1] += 1
                            else:
                                if word.lower() in self.exclusions:
                                    exclude = 1
                                else:
                                    exclude = 0
                                for row in keywords:
                                    if word.lower() in row:
                                        wordfreqdata[word] = [0,1,1,0,exclude]
                                        break
                                else:
                                    wordfreqdata[word] = [0,1,0,0,exclude]

                    self.send(wordfreqdata,"outbox")

            self.pause()
            yield 1


class FinalAnalysisNLTK(DBWrapper,component):
    Inboxes = {
        "inbox" : "Receives a list of tweet IDs and their related PID for NLTK analysis [pid,[tweetid,tweetid]]",
        "tweetfixer" : "Received data back from the tweet fixing components (tweet json)",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "urrently sends nothing out, just Prints to screen - needs work", #TODO
        "tweetfixer" : "Sends out data to the tweet fixing components (tweet json)",
        "signal" : ""
    }

    def __init__(self, dbuser, dbpass):
        super(FinalAnalysisNLTK, self).__init__(dbuser=dbuser, dbpass=dbpass)
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

        self.dbConnect()
        Print("FinalAnalysisNLTK: Initialised")
        while not self.finished():
            Print("FinalAnalysisNLTK: Waiting for data")
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                Print("FinalAnalysisNLTK: got data")
                Print("FinalAnalysisNLTK: ... and ignoring it (Since didn't store results of final analysis anyway...")

                if False:
                    pid = data[0]
                    tweetids = data[1]

                    retweetcache = dict()

                    # Issue #TODO - Words that appear as part of a keyword but not the whole thing won't get marked as being a keyword (e.g. Blue Peter - two diff words)
                    # Need to check for each word if it forms part of a phrase which is also a keyword
                    # If so, don't count is as a word, count the whole thing as a phrase and remember not to count it more than once
                    # May actually store phrases AS WELL AS keywords

                    keywords = dict()
                    # Find keywords for this PID
                    self.db_select("""SELECT keyword,type FROM keywords WHERE pid = %s""",(pid))
                    keyworddata = self.db_fetchall()
                    Print("FinalAnalysisNLTK: len(keyworddata)", len(keyworddata))
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
                    
                    Print("FinalAnalysisNLTK: about to loop through tweet ids - count -", len(tweetids))

                    for tweetid in tweetids:
                        # Cycle through each tweet and find its JSON
                        tweetdata = None
                        Print("FinalAnalysisNLTK: getting tweet data", len(tweetids))
                        tweetdatafailcount = 0
                        tweetfixfailcount = 0
                        failed_tweet = False
                        while tweetdata == None:
                            Print("FinalAnalysisNLTK: Trying to get tweetdata")
                            self.db_select("""SELECT tweet_json FROM rawtweets WHERE tweet_id = %s""",(tweetid))
                            tweetdata = self.db_fetchone()
                            if tweetdata == None:
                                tweetdatafailcount += 1
                                Print("FinalAnalysisNLTK: failed to tweetdata - count, id:", tweetdatafailcount, tweetid)
                                if tweetdatafailcount >1000:
                                    failed_tweet = True
                                    # FIXME: Without the following break, this goes into a busy wait loop, which locks
                                    # FIXME: up the scheduler because this component does not yield command back to the caller
                                    # FIXME: This results in starvation of the system because it does not allow any other
                                    # FIXME: process/component to progress. Since this has happened remarkably rarely, this
                                    # FIXME: means the collection & storage has been remarkably reliable.
                                    # FIXME: Should be able to actually fix this, and the mystery hangs now too.
                                    # FIXME: This "break" is actually sufficient in the short term, but means there's a hang
                                    # FIXME: of 1000 cycles -- if this entire block is uncommented.
                                    # FIXME: Since this problem happens rarely, bt catastrophically, fixing this really matters.
                                    # FIXME: Means it's especially surprising that *any* data was collected during this period,
                                    # FIXME: since this would cause the entire system - except other threads - to hang.
                                    # FIXME: Crucially, this is also something the zombie killer can't kill, but can (and did)
                                    # FIXME: draw attention to.
                                    break
                            else:
                                Print("FinalAnalysisNLTK: got tweetdata")
                                tweetjson = cjson.decode(tweetdata[0])

                                self.send(tweetjson,"tweetfixer")
                                twnc_count = 0
                                while not self.dataReady("tweetfixer"):
                                    if twnc_count > 10:
                                        # Empirically, twnc_count gets there within 2 or 3 loops
                                        break
                                    twnc_count += 1
                                    self.pause()
                                    yield 1

                                if not self.dataReady("tweetfixer"):
                                    tweetfixfailcount += 1
                                    Print("FinalAnalysisNLTK: Tweet Fixer Failed - twnc_count, tweetfixfailcount", twnc_count, tweetfixfailcount, tweetid )
                                else:
                                    tweetjson = self.recv("tweetfixer")

                                    # Identify retweets
                                    if ("retweeted_status" in tweetjson):
                                        if "id" in tweetjson['retweeted_status']:
                                            statusid = tweetjson['retweeted_status']['id']
                                            if statusid in retweetcache:
                                                retweetcache[statusid][0] += 1
                                            else:
                                                retweetcache[statusid] = [1,tweetjson['retweeted_status']['text']]


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

                    # Look for phrases - very limited
                    bigram_fd = FreqDist(nltk.bigrams(filteredtext))

                    # Print(bigram_fd)
                    for entry in bigram_fd:
                        if entry[0] not in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""" and entry[1] not in """!"#$%&()*+,-./:;<=>?@~[\\]?_'`{|}?""":
                            if entry[0] not in self.exclusions and entry[1] not in self.exclusions:
                                for word in keywords:
                                    # Print(word)
                                    if entry[0] in word and entry[1] in word:
                                        # Print("Keyword Match! " , entry[0],entry[1] )
                                        break
                                else:
                                    pass
                                    #Print( entry[0],entry[1])

                    # Print("Retweet data: " , retweetcache)

                self.send(None,"outbox")  ## FIXME: AAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHHHHHHHHHHHHHHHH

            if not self.anyReady():
                Print("FinalAnalysisNLTK: about to pause")
                self.pause()
            yield 1

#! /usr/bin/python

'''
Saves relevant data fed back from TwitterStream etc next to its PID and timestamp ready for analysis
Needs to do limited analysis to work out which keywords in the tweet stream correspond to which programme
'''

from datetime import datetime
import os
import string
import time as time2
from time import time

from Axon.Ipc import producerFinished
from Axon.Ipc import shutdownMicroprocess
from Axon.ThreadedComponent import threadedcomponent
import MySQLdb
import _mysql_exceptions
import cjson
from dateutil.parser import parse

class DataCollector(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives data in the format [tweetjson,[pid,pid]]",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "signal" : ""
    }

    def __init__(self,dbuser,dbpass):
        super(DataCollector, self).__init__()
        self.dbuser = dbuser
        self.dbpass = dbpass

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def dbConnect(self):
        db = MySQLdb.connect(user=self.dbuser,passwd=self.dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
        cursor = db.cursor()
        return cursor

    def main(self):
        cursor = self.dbConnect()
        while not self.finished():
            twitdata = list()
            # Collect all current received tweet JSON and their related PIDs into a twitdata list
            while self.dataReady("inbox"):
                pids = list()
                data = self.recv("inbox")
                for pid in data[1]:
                    pids.append(pid)
                twitdata.append([data[0],pids])
            if len(twitdata) > 0:
                # Process the received twitdata
                for tweet in twitdata:
                    tweet[0] = tweet[0].replace("\\/","/") # Fix slashes in links: This may need moving further down the line - ideally it would be handled by cjson
                    if tweet[0] != "\r\n": # If \r\n is received, this is just a keep alive signal from Twitter every 30 secs
                        # At this point, each 'tweet' contains tweetdata, and a list of possible pids
                        newdata = cjson.decode(tweet[0])
                        if newdata.has_key('delete') or newdata.has_key('scrub_geo') or newdata.has_key('limit'):
                            # Keep a record of all requests from Twitter for deletions, location removal etc
                            # As yet none of these have been received, but this code will store them if they are received to enable debugging
                            filepath = "contentDebug.txt"
                            if os.path.exists(filepath):
                                file = open(filepath, 'r')
                                filecontents = file.read()
                            else:
                                filecontents = ""
                            file = open(filepath, 'w')
                            file.write(filecontents + "\n" + str(datetime.utcnow()) + " " + cjson.encode(newdata))
                            file.close()
                        else:
                            # This is a real tweet
                            tweetid = newdata['id']
                            print "New tweet! @" + newdata['user']['screen_name'] + ": " + newdata['text']
                            for pid in tweet[1]:
                                # Cycle through possible pids, grabbing that pid's keywords from the DB
                                # Then, check this tweet against the keywords and save to DB where appropriate (there may be more than one location)
                                cursor.execute("""SELECT keyword,type FROM keywords WHERE pid = %s""",(pid))
                                data = cursor.fetchall()
                                for row in data:
                                    # Some keywords are stored with a ^. These must be split, and the tweet checked to see if it has both keywords, but not necessarily next to each other
                                    keywords = row[0].split("^")
                                    if len(keywords) == 2:
                                        if string.lower(keywords[0]) in string.lower(newdata['text']) and string.lower(keywords[1]) in string.lower(newdata['text']):
                                            cursor.execute("""SELECT timestamp,timediff FROM programmes WHERE pid = %s ORDER BY timestamp DESC""",(pid))
                                            progdata = cursor.fetchone()
                                            if progdata != None:
                                                # Ensure the user hasn't already tweeted the same text
                                                # Also ensure they haven't tweeted in the past 10 seconds
                                                timestamp = time2.mktime(parse(newdata['created_at']).timetuple())
                                                cursor.execute("""SELECT * FROM rawdata WHERE (pid = %s AND text = %s AND user = %s) OR (pid = %s AND user = %s AND timestamp >= %s AND timestamp < %s)""",(pid,newdata['text'],newdata['user']['screen_name'],pid,newdata['user']['screen_name'],timestamp-10,timestamp+10))
                                                if cursor.fetchone() == None:
                                                    print ("Storing tweet for pid " + pid)
                                                    # Work out where this tweet really occurred in the programme using timestamps and DVB bridge data
                                                    progposition = timestamp - (progdata[0] - progdata[1])
                                                    cursor.execute("""INSERT INTO rawdata (tweet_id,pid,timestamp,text,user,programme_position) VALUES (%s,%s,%s,%s,%s,%s)""", (tweetid,pid,timestamp,newdata['text'],newdata['user']['screen_name'],progposition))
                                                    break # Break out of this loop and back to check the same tweet against the next programme
                                                else:
                                                    print ("Duplicate tweet from user - ignoring")
                                    if string.lower(row[0]) in string.lower(newdata['text']):
                                        cursor.execute("""SELECT timestamp,timediff FROM programmes WHERE pid = %s ORDER BY timestamp DESC""",(pid))
                                        progdata = cursor.fetchone()
                                        if progdata != None:
                                            # Ensure the user hasn't already tweeted the same text for this programme
                                            # Also ensure they haven't tweeted in the past 10 seconds
                                            timestamp = time2.mktime(parse(newdata['created_at']).timetuple())
                                            cursor.execute("""SELECT * FROM rawdata WHERE (pid = %s AND text = %s AND user = %s) OR (pid = %s AND user = %s AND timestamp >= %s AND timestamp < %s)""",(pid,newdata['text'],newdata['user']['screen_name'],pid,newdata['user']['screen_name'],timestamp-10,timestamp+10))
                                            if cursor.fetchone() == None:
                                                print ("Storing tweet for pid " + pid)
                                                # Work out where this tweet really occurred in the programme using timestamps and DVB bridge data
                                                progposition = timestamp - (progdata[0] - progdata[1])
                                                cursor.execute("""INSERT INTO rawdata (tweet_id,pid,timestamp,text,user,programme_position) VALUES (%s,%s,%s,%s,%s,%s)""", (tweetid,pid,timestamp,newdata['text'],newdata['user']['screen_name'],progposition))
                                                break # Break out of this loop and back to check the same tweet against the next programme
                                            else:
                                                print ("Duplicate tweet from user - ignoring")
                    else:
                        print "Blank line received from Twitter - no new data"
                    
                    print ("Done!") # new line to break up display
            else:
                time2.sleep(0.1)

'''
The raw data collector differs from the plain data collector in that it stores the raw JSON containers for tweets next to their unique IDs, but with no relation to PIDs
This is run concurrent to the other data collector, so the two won't necessarily run at the same rate and could be out of sync
This possible lack of sync must be handled later
'''

class RawDataCollector(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives data in the format [tweetjson,[pid,pid]]",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "signal" : ""
    }

    def __init__(self,dbuser,dbpass):
        super(RawDataCollector, self).__init__()
        self.dbuser = dbuser
        self.dbpass = dbpass

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def dbConnect(self):
        db = MySQLdb.connect(user=self.dbuser,passwd=self.dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
        cursor = db.cursor()
        return cursor

    def main(self):
        cursor = self.dbConnect()
        while not self.finished():
            twitdata = list()
            # As in the data collector, create a list of all tweets currently received
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                twitdata.append(data[0])
            if len(twitdata) > 0:
                # Cycle through the tweets, fixing their URLs as before, and storing them if they aren't a status message
                for tweet in twitdata:
                    tweet = tweet.replace("\\/","/") # This may need moving further down the line - ideally it would be handled by cjson
                    if tweet != "\r\n":
                        newdata = cjson.decode(tweet)
                        if newdata.has_key('delete') or newdata.has_key('scrub_geo') or newdata.has_key('limit'):
                            # It is assumed here that the original data collector has handled the Twitter status message
                            print "Discarding tweet instruction - captured by other component"
                        else:
                            tweetid = newdata['id']
                            # Capture exactly when this tweet was stored
                            tweetstamp = time()
                            tweetsecs = int(tweetstamp)
                            # Include the fractions of seconds portion of the timestamp in a separate field
                            tweetfrac = tweetstamp - tweetsecs
                            # We only have a 16000 VARCHAR field to use in MySQL (through choice) - this should be enough, but if not, the tweet will be written out to file
                            if len(tweet) < 16000:
                                try:
                                    cursor.execute("""INSERT INTO rawtweets (tweet_id,tweet_json,tweet_stored_seconds,tweet_stored_fraction) VALUES (%s,%s,%s,%s)""", (tweetid,tweet,tweetsecs,tweetfrac))
                                except _mysql_exceptions.IntegrityError, e:
                                    # Handle the possibility for Twitter having sent us a duplicate
                                    print "Duplicate tweet ID:", str(e)
                            else:
                                print "Discarding tweet - length limit exceeded"
                                tweetcontents = ""
                                homedir = os.path.expanduser("~")
                                if os.path.exists(homedir + "/oversizedtweets.conf"):
                                    try:
                                        file = open(homedir + "/oversizedtweets.conf",'r')
                                        tweetcontents = file.read()
                                        file.close()
                                    except IOError, e:
                                        print ("Failed to load oversized tweet cache - it will be overwritten")
                                try:
                                    file = open(homedir + "/oversizedtweets.conf",'w')
                                    tweetcontents = tweetcontents + tweet
                                    file.write(tweetcontents)
                                    file.close()
                                except IOError, e:
                                    print ("Failed to save oversized tweet cache")
            else:
                time2.sleep(0.1)

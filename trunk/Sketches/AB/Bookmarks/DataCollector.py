#! /usr/bin/python

# Saves relevant data fed back from TwitterStream etc next to its PID and timestamp (TODO) ready for analysis
# Needs to do limited analysis to work out which keywords in the tweet stream correspond to which programme
# Keywords, and possibly PIDs and channels will most likely have to be passed here as well as to the TwitterStream from Requester

import time
import MySQLdb
import cjson
import string

from Axon.ThreadedComponent import threadedcomponent

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
            while self.dataReady("inbox"):
                pids = list()
                data = self.recv("inbox")
                for pid in data[1]:
                    pids.append(pid)
                twitdata.append([data[0],pids])
            if len(twitdata) > 0:
                # TODO: Looking for \n characters, divide tweets, then check them against original keywords and add to table against the correct pid
                print twitdata

                
                for tweet in twitdata:
                    if tweet[0] != "\r\n":
                        # At this point, each 'tweet' contains tweetdata, and a list of possible pids
                        newdata = cjson.decode(tweet[0]) # Won't work - need keywords to be related to their pids - let's requery
                        for pid in tweet[1]:
                            # Cycle through possible pids, grabbing that pid's keywords from the DB
                            # Then, check this tweet against the keywords and save to DB where appropriate (there may be more than one location)
                            cursor.execute("""SELECT keyword,type FROM keywords WHERE pid = %s""",(pid))
                            data = cursor.fetchall()
                            for row in data:
                                if row[1] == "Character":
                                    keywords = row[0].split("^")
                                    if len(keywords) == 2:
                                        if string.lower(keywords[0]) in string.lower(newdata['text']) and string.lower(keywords[1]) in string.lower(newdata['text']):
                                            cursor.execute("""SELECT * FROM programmes WHERE pid = %s""",(pid))
                                            if cursor.fetchone() != None:
                                                cursor.execute("""INSERT INTO rawdata (pid,datetime,text,user) VALUES (%s,%s,%s,%s)""", (pid,newdata['created_at'],newdata['text'],newdata['user']['screen_name']))
                                                break # Break out of this loop and back to check the same tweet against the next programme
                                elif string.lower(row[0]) in string.lower(newdata['text']):
                                    cursor.execute("""SELECT * FROM programmes WHERE pid = %s""",(pid))
                                    if cursor.fetchone() != None:
                                        cursor.execute("""INSERT INTO rawdata (pid,datetime,text,user) VALUES (%s,%s,%s,%s)""", (pid,newdata['created_at'],newdata['text'],newdata['user']['screen_name']))
                                        break # Break out of this loop and back to check the same tweet against the next programme                        

                # Still need to re-search through received data using original keywords to ensure those keywords separated by spaces appear correctly and not split
            else:
                time.sleep(0.1)
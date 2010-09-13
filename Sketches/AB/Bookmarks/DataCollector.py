#! /usr/bin/python

# Saves relevant data fed back from TwitterStream etc next to its PID and timestamp (TODO) ready for analysis
# Needs to do limited analysis to work out which keywords in the tweet stream correspond to which programme
# Keywords, and possibly PIDs and channels will most likely have to be passed here as well as to the TwitterStream from Requester

import time
import os
import MySQLdb
import cjson

from Axon.ThreadedComponent import threadedcomponent

class DataCollector(threadedcomponent):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self,dbuser,dbpass):
        super(DataCollector, self).__init__()
        self.dbuser = dbuser
        self.dbpass = dbpass

    def dbConnect(self):
        db = MySQLdb.connect(user=self.dbuser,passwd=self.dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
        cursor = db.cursor()
        return cursor

    def main(self):
        cursor = self.dbConnect()
        while 1:
            twitdata = list()
            pids = list()
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                twitdata.append(data[0])
                pids.append(data[1])
            if len(twitdata) > 0:
                # TODO: Looking for \n characters, divide tweets, then check them against original keywords and add to table against the correct pid
                print twitdata

                currentnum = 0
                for pid in pids:
                    if twitdata[currentnum] != "\r\n":
                        newdata = cjson.decode(twitdata[currentnum])
                        cursor.execute("""SELECT * FROM programmes WHERE pid = %s""",(pids[currentnum]))
                        if cursor.fetchone() != None:
                            cursor.execute("""INSERT INTO rawdata (pid,datetime,text,user) VALUES (%s,%s,%s,%s)""", (pids[currentnum],newdata['created_at'],newdata['text'],newdata['user']['screen_name']))
                    

                        olddata = ""
                        try:
                            homedir = os.path.expanduser("~")
                            file = open(homedir + "/twitstream.txt",'r')
                            olddata = file.read()
                            file.close()
                        except IOError, e:
                            pass
                        try:
                            # Need better storage method to keep pid and keywords etc (DB)
                            file = open(homedir + "/twitstream.txt",'w')
                            file.write(olddata + "\n" + twitdata[currentnum])
                            file.close()
                        except IOError, e:
                            print ("Writing of data to file failed: " + str(e))
                        

                    currentnum += 1
                # Still need to re-search through received data using original keywords to ensure those keywords separated by spaces appear correctly and not split
            else:
                time.sleep(0.1)
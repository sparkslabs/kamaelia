#! /usr/bin/python

# Saves relevant data fed back from TwitterStream etc next to its PID and timestamp (TODO) ready for analysis
# Needs to do limited analysis to work out which keywords in the tweet stream correspond to which programme
# Keywords, and possibly PIDs and channels will most likely have to be passed here as well as to the TwitterStream from Requester

import time
import os

from Axon.ThreadedComponent import threadedcomponent

class DataCollector(threadedcomponent):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self):
        super(DataCollector, self).__init__()

    def main(self):
        while 1:
            twitdata = ""
            while self.dataReady("inbox"):
                twitdata += self.recv("inbox")
            if twitdata != "":
                print twitdata
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
                    file.write(olddata + "\n" + twitdata)
                    file.close()
                except IOError, e:
                    print ("Writing of data to file failed: " + str(e))
                # Still need to re-search through received data using original keywords to ensure those keywords separated by spaces appear correctly and not split
            else:
                time.sleep(0.1)
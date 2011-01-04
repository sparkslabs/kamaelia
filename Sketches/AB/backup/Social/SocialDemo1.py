#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
#

import cjson
#import feedparser
import os
import rdfxml
import re
import sys
import time
import urllib
import urllib2

from datetime import datetime
from dateutil.parser import parse

#
# Initial Demo
# - Pulls in BBC schedule json
# - Compares current time to schedule to find out what's on
# - Identifies /programmes RDF URL for current prog
# - Identifies the programme title and any extra keywords like people's names - echoes all to console
# - Receives an input from Twitter, filtered based upon the keywords
# - Echos all tweets to the console (more to be added later)
#
# Note: Must keep an eye on the time to switch to new programmes when relevant
#

def getSchedule(scheduleurl):
    # Grab BBC data
    try:
        conn1 = urllib2.urlopen(scheduleurl)
        print ("Connected to requested schedule. Awaiting data...")
    except URLError, e:
        print ("BBC connection failed - aborting")
        print (e.reason)
        sys.exit(0)

    # Print data to the screen
    if conn1:
        content = conn1.read()
        conn1.close()
        try:
            decodedcontent = cjson.decode(content)
            print("Data for " + decodedcontent['schedule']['service']['title'] + " loaded, just need to work out what's on now...")
            return decodedcontent
        except cjson.DecodeError, e:
            print ("Decoding schedule failed - aborting")
            print (e.message)
            sys.exit(0)

def getCurrentProg(decodedcontent):
    # Work out what's on NOW here
    utcdatetime = datetime.now()
    print("Current time is: " + str(utcdatetime))
    for programme in decodedcontent['schedule']['day']['broadcasts']:
        starttime = parse(programme['start'])
        starttime = starttime.replace(tzinfo=None)
        endtime = parse(programme['end'])
        endtime = endtime.replace(tzinfo=None)
        if (utcdatetime >= starttime) & (utcdatetime < endtime):
            print("The current programme is '" + programme['programme']['display_titles']['title'] + "'")
            pid = programme['programme']['pid']
            #return pid
            break

    # TEMPORARY - Set Twitter filter
    prog = re.sub(",","",programme['programme']['display_titles']['title'])
    chan = decodedcontent['schedule']['service']['title']
    prognospace = re.sub("\s+","",prog)
    channospace = re.sub("\s+","",chan)
    #totrack = {'track' : prog + "," + prognospace + "," + channospace + "," + '#' + channospace}
    totrack = {'track' : "#" + prognospace + "," + '#' + channospace}
    data = urllib.urlencode(totrack)
    print("Ready to track '" + totrack['track'] + "'")
    return [data,endtime]

def getKeywords(pid):
    progurl = rdfurl + "/" + pid + ".rdf"
    print("Ready to download info for pid " + pid)
    print(progurl)
    # Grab BBC data
    try:
        rdfconn = urllib2.urlopen(progurl)
        print ("Connected to requested programme. Awaiting data...")
    except URLError, e:
        print ("BBC connection failed - aborting")
        print (e.reason)
        sys.exit(0)

    # Print data to the screen
    if rdfconn:
        content = rdfconn.read()
        rdfconn.close()
        data = rdfxml.parseRDF(content).result
        print(data)
        print("Unfortunately I haven't a clue what to do with this, so let's send twitter the show title instead")


if __name__=="__main__":
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
    username = config['username']
    password = config['password']

    # Set up URLs
    twitterurl = "http://stream.twitter.com/1/statuses/filter.json"
    #scheduleurl = "http://www.bbc.co.uk/radio1/programmes/schedules/england.json"
    scheduleurl = "http://www.bbc.co.uk/bbcone/programmes/schedules/north_west/today.json"
    #scheduleurl = "http://www.bbc.co.uk/bbctwo/programmes/schedules/england/today.json"
    rdfurl = "http://www.bbc.co.uk/programmes"
    if config['proxy']:
        proxy = config['proxy']

    # Configure authentication for Twitter
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, twitterurl, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)

    # Configure proxy and opener
    if proxy:
        proxyhandler = urllib2.ProxyHandler({"http" : proxy})
        twitopener = urllib2.build_opener(proxyhandler, authhandler)
        bbcopener = urllib2.build_opener(proxyhandler)
    else:
        twitopener = urllib2.build_opener(authhandler)
        bbcopener = urllib2.build_opener()

    # Get ready to grab BBC data
    urllib2.install_opener(bbcopener)
    
    decodedcontent = getSchedule(scheduleurl)
    #currentprog = getCurrentProg(decodedcontent)
    #keywords = getKeywords(currentprog)
    data = getCurrentProg(decodedcontent)
    
    # Get ready to grab Twitter data
    urllib2.install_opener(twitopener)

    # Grab twitter data
    try:
        conn2 = urllib2.urlopen(twitterurl, data[0])
        print ("Connected to twitter stream. Awaiting data...")
    except URLError, e:
        print ("Twitter connection failed - aborting")
        print (e.reason)
        sys.exit(0)

    # Print data to the screen
    if conn2:
        i = 1
        
        while 1:
            if datetime.now() >= data[1]:
                conn2.close()
                print("Programme changed - sleeping for 10")
                time.sleep(10)
                data = getCurrentProg(decodedcontent)
                # Grab twitter data
                try:
                    conn2 = urllib2.urlopen(twitterurl, data[0])
                    print ("Connected to twitter stream. Awaiting data...")
                except URLError, e:
                    print ("Twitter connection failed - aborting")
                    print (e.reason)
                    sys.exit(0)
            
            try:
                content = conn2.readline()
                try:
                    content = cjson.decode(content)
                    #for entry in totrack['track']:
                    #    if content['text'].find(entry) != -1:
                    #        goodsearch = entry
                    #        break
                    #    else:
                    #        print(entry)
                    #        goodsearch = False

                    #if (goodsearch):
                    #    print(str(datetime.now()) + ": Matched occurrence of " + entry + " in '" + content['text'] + "'")
                    #else:
                    #    print("False positive: '" + content['text'] + "'")
                    print(content['created_at'] + ": @" + content['user']['screen_name'] + ": " + content['text'])
                except cjson.DecodeError, e:
                    # This was an empty line, meaning no data has arrived for a while
                    pass
            except Exception, e: # Something's not right here, tried socket.error but didn't work
                print("Peer disconnected - reconnecting in 10...")
                time.sleep(10)
                try: # This bit doesn't appear to work
                    conn2 = urllib2.urlopen(twitterurl, data)
                    print ("Connected to twitter stream. Awaiting data...")
                except URLError, e:
                    print ("Twitter connection failed - aborting")
                    print (e.reason)
                    sys.exit(0)
            i += 1
        conn2.close()


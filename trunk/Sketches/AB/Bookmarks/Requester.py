#! /usr/bin/python

# Requests current BBC prog, gets relevant keywords, sends off relevant Twitter searches
# One requester for ALL channels - avoids creating multiple Twitter streams
# Only sends keywords to Twitter once per programme, then monitors for the next programme

import re
import time
from rdflib.Graph import Graph
import rdflib
import cjson
import os
import string
import MySQLdb
from datetime import date

from Axon.ThreadedComponent import threadedcomponent

class Requester(threadedcomponent):
    Inboxes = {
        "inbox" : "",
        "control" : "",
        "whatson" : "Receives back what's currently on a channel - [pid,title,timeoffset,duration,expectedstarttime]",
        "proginfo" : "Receives back raw RDF data for a PID",
        "search" : "Receives back raw Twitter people search JSON"
    }
    Outboxes = {
        "outbox" : "Sends out keywords and pid(s) for streaming API connections - [[keyword,keyword],[pid,pid,pid]]",
        "signal" : "",
        "whatson" : "Requests current programmes by sending a channel name",
        "proginfo" : "Requests RDF format data for a pid - [pid, 'rdf']",
        "search" : "Sends people's names for Twitter username identification"
    }

    def __init__(self, channel,dbuser,dbpass):
        super(Requester, self).__init__()
        self.channel = channel
        self.dbuser = dbuser
        self.dbpass = dbpass
        # Modify this to construct the dictionary based on the channel names passed in?
        self.channels = {
            "bbcone" : "",
            "bbctwo" : "",
            "bbcthree" : "",
            "bbcfour" : "",
            "cbbc" : "",
            "cbeebies" : "",
            "bbcnews" : "",
            "radio1" : "",
            "radio2" : "",
            "radio3" : "",
            "radio4" : "",
            "5live" : "",
            "worldservice" : "",
            "6music" : "",
            "radio7" : "",
            "1xtra" : "",
            "bbcparliament" : "",
            "asiannetwork" : "",
            "sportsextra" : ""
        }

        # Brand PIDs associated with programmes. New progs don't always have brands, but it's a start
        # Ideally this would be replaced by the BBC Buzz database, but that's not yet accessible AFAIK and doesn't always store tags for new programmes.
        # This doesn't help in the channel case where for example radio 1 uses @bbcr1
        self.officialbrandtags = {
            "b00vc3rz" : ["#genius","bbcgenius"], # Genius with Dave Gorman
            "b006t1q9" : ["#bbcqt","bbcquestiontime"], # Question Time
            "b009w2w3" : ["#laterjools", "bbclater"], # Later with Jools Holland
            "b00lwxj1" : ["bbcbang"], # Bang goes the theory
            "b006m8dq" : ["#scd", "bbcstrictly"], # Strictly come dancing
            "b006ml0g" : ["qikipedia", "#qi"], # QI
            "b00j4j7g" : ["#f1"], # Formula 1
            "b006wkqb" : ["chrisdjmoyles","chrismoylesshow"], # Chris Moyles Breakfast Show
            "b0071b63" : ["bbcapprentice"], # The Apprentice
            "b006mg74" : ["bbcwatchdog"] # Watchdog
        }
        # Series PIDs associated with programmes. ONLY used where prog doesn't have a brand
        self.officialseriestags = {
            "b00v2z3s" : ["#askrhod"] # Ask Rhod Gilbert
        }

        self.firstrun = True

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def doStuff(self, channel):
        self.send(channel, "whatson")
        while not self.dataReady("whatson"):
            pass
        data = self.recv("whatson")
        if data == None:
            pid = None
        else:
            pid = data[0]
            title = str(data[1])
            offset = data[2]
            duration = data[3]
            expectedstart = data[4]
        if pid != self.channels[channel]:
            # Perhaps just do a duplicate scan before creating Twitter stream
            if pid == None:
                self.channels[channel] = None
                print (channel + ": Off Air")
            else:
                self.channels[channel] = pid
                self.send([pid, "rdf"], "proginfo")
                while not self.dataReady("proginfo"):
                     pass
                programmedata = self.recv("proginfo")

                filepath = "tempRDF.txt"
                file = open(filepath, 'w')
                file.write(programmedata)
                file.close()

                g = Graph()
                # This is a temporary proxy fix. A URL could be put here instead
                g.parse("tempRDF.txt")

                # Identify the brand and whether there are any official hashtags
                twittags = list()
                for bid in g.subjects(object = rdflib.URIRef('http://purl.org/ontology/po/Brand')):
                    # bid is Brand ID
                    bidmod = bid.replace("#programme","")
                    bidmod = str(bidmod.replace("file:///programmes/",""))
                    if self.officialbrandtags.has_key(bidmod):
                        twittags = self.officialbrandtags[bidmod]
                        break

                # Identify the series and whether there are any official hashtags
                if len(twittags) == 0:
                    # Identify the brand and whether there are any official hashtags
                    for sid in g.subjects(object = rdflib.URIRef('http://purl.org/ontology/po/Series')):
                        # sid is Series ID
                        sidmod = sid.replace("#programme","")
                        sidmod = str(sidmod.replace("file:///programmes/",""))
                        if self.officialseriestags.has_key(sidmod):
                            twittags = self.officialseriestags[sidmod]
                            break

                so = g.subject_objects(predicate=rdflib.URIRef('http://purl.org/ontology/po/version'))
                # Pick a version, any version - for this which one doesn't matter
                for x in so:
                    # vid is version id
                    vid = x[1]
                    vidmod = vid.replace("#programme","")
                    vidmod = vidmod.replace("file:///programmes/","")
                    break

                # Got version, now get people

                self.send([vidmod, "rdf"], "proginfo")
                while not self.dataReady("proginfo"):
                    pass
                versiondata = self.recv("proginfo")

                filepath = "tempRDF.txt"
                file = open(filepath, 'w')
                file.write(versiondata)
                file.close()

                g = Graph()
                g.parse("tempRDF.txt")

                if self.firstrun:
                    print (channel + ": " + title)
                else:
                    print (channel + ": Changed to - " + title)

                # Minor alterations
                title = title.replace("&","and")

                if ":" in title:
                    titlebits = title.split(":")
                    title = titlebits[0]

                # Saving a copy here so apostrophes etc can be used in the Twitter people search
                titlesave = title

                # Remove punctuation
                for item in """!"#$%()*+,-./;<=>?@[\\]?_'`{|}?""":
                    title = title.replace(item,"")

                keywords = dict()

                # Add official hashtags to the list
                for tag in twittags:
                    keywords[tag] = "Twitter"

                # Duplicates will be removed later
                if string.find(title,"The",0,3) != -1:
                    newtitle = string.replace(re.sub("\s+","",title),"The ","",1)
                    keywords[channel] = "Channel"
                    keywords["#" + string.lower(re.sub("\s+","",title))] = "Title"
                    # Check for and remove year too
                    keywords["#" + string.replace(string.lower(re.sub("\s+","",title))," " + str(date.today().year),"",1)] = "Title"
                    keywords['#' + string.lower(re.sub("\s+","",newtitle))] = "Title"
                    # Check for and remove year too
                    keywords['#' + string.replace(string.lower(re.sub("\s+","",newtitle))," " + str(date.today().year),"",1)] = "Title"
                else:
                    keywords[channel] = "Channel"
                    keywords["#" + string.lower(re.sub("\s+","",title))] = "Title"
                    keywords["#" + string.replace(string.lower(re.sub("\s+","",title))," " + str(date.today().year),"",1)] = "Title"

                allwordtitle = string.replace(title,"The ","",1)
                allwordtitle = allwordtitle.lower()
                # Remove current year from events
                allwordtitle = allwordtitle.replace(" " + str(date.today().year),"",1)
                titlewords = allwordtitle.split()
                if len(titlewords) > 1:
                    keywords[allwordtitle] = "Title"
                else:
                    # Trial fix for issue of one word titles producing huge amounts of data
                    keywords[allwordtitle + "^" + "bbc"] = "Title"

                numwords = dict({"one" : 1, "two" : 2, "three": 3, "four" : 4, "five": 5, "six" : 6, "seven": 7})
                for word in numwords:
                    if word in channel.lower() and channel != "asiannetwork": # Bug fix! asianne2rk
                        numchannel = string.replace(channel.lower(),word,str(numwords[word]))
                        keywords[numchannel] = "Channel"
                        break
                    if str(numwords[word]) in channel.lower():
                        numchannel = string.replace(channel.lower(),str(numwords[word]),word)
                        keywords[numchannel] = "Channel"
                        break

                # Load NameCache
                save = False
                try:
                    homedir = os.path.expanduser("~")
                    file = open(homedir + "/namecache.conf",'r')
                    save = True
                except IOError, e:
                    print ("Failed to load name cache - will attempt to create a new file: " + str(e))

                if save:
                    raw_config = file.read()
                    file.close()
                    try:
                        config = cjson.decode(raw_config)
                    except cjson.DecodeError, e:
                        config = dict()
                else:
                    config = dict()

                s = g.subjects(predicate=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),object=rdflib.URIRef('http://purl.org/ontology/po/Role'))

                for x in s:
                    rid = g.value(predicate=rdflib.URIRef('http://purl.org/ontology/po/role'),object=rdflib.BNode(x))
                    pid = g.value(subject=rdflib.BNode(rid),predicate=rdflib.URIRef('http://purl.org/ontology/po/participant'))
                    firstname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/givenName')))
                    lastname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/familyName')))

                    if config.has_key(firstname + " " + lastname):
                        # Found a cached value
                        if config[firstname + " " + lastname] != "":
                            keywords[config[firstname + " " + lastname]] = "Twitter"
                    else:
                        # Not cached yet - new request
                        self.send(firstname + " " + lastname, "search")
                        while not self.dataReady("search"):
                            pass
                        twitdata = self.recv("search")
                        screenname = ""
                        try:
                            for user in twitdata:
                                if user.has_key('verified'):
                                    if (user['verified'] == True or user['followers_count'] > 10000) and string.lower(user['name']) == string.lower(firstname + " " + lastname):
                                        screenname = user['screen_name']
                                        keywords[screenname] = "Twitter"
                                        break
                        except AttributeError, e:
                            pass
                        config[firstname + " " + lastname] = screenname
                    keywords[firstname + " " + lastname] = "Participant"

                s = g.subjects(predicate=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),object=rdflib.URIRef('http://purl.org/ontology/po/Character'))

                for x in s:
                    character = str(g.value(subject=rdflib.BNode(x),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/name')))
                    # TODO: Character names would probably work best as just first names, but watch out for Dr. etc appearing first
                    rid = g.value(predicate=rdflib.URIRef('http://purl.org/ontology/po/role'),object=rdflib.BNode(x))
                    pid = g.value(subject=rdflib.BNode(rid),predicate=rdflib.URIRef('http://purl.org/ontology/po/participant'))
                    firstname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/givenName')))
                    lastname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/familyName')))
                    # This ^ is a temporary fix until I work out a better DB structure
                    keywords[character + "^" + channel] = "Character"
                    keywords[character + "^" + title] = "Character"
                    if " " in character:
                        # Looks like we have a firstname + surname situation
                        charwords = character.split()
                        if charwords[0] != "Dr" and charwords[0] != "Miss" and charwords[0] != "Mr" and charwords[0] != "Mrs" and charwords[0] != "Ms" and charwords[0] != "The":
                            # As long as the first word isn't a title, add it as a first name
                            # This ^ is a temporary fix until I work out a better DB structure
                            keywords[charwords[0] + "^" + channel] = "Character"
                            keywords[charwords[0] + "^" + title] = "Character"
                        elif len(charwords) > 2:
                            # If the first word was a title, and the second word isn't a surname (checked by > 2) add the first name
                            # This ^ is a temporary fix until I work out a better DB structure
                            keywords[charwords[1] + "^" + channel] = "Character"
                            keywords[charwords[1] + "^" + title] = "Character"
                    if config.has_key(firstname + " " + lastname):
                        # Found a cached value
                        if config[firstname + " " + lastname] != "":
                            keywords[config[firstname + " " + lastname]] = "Actor"
                    else:
                        # Not cached yet - new request
                        self.send(firstname + " " + lastname, "search")
                        while not self.dataReady("search"):
                            pass
                        twitdata = self.recv("search")
                        screenname = ""
                        try:
                            for user in twitdata:
                                if user.has_key('verified'):
                                    if (user['verified'] == True or user['followers_count'] > 10000) and string.lower(user['name']) == string.lower(firstname + " " + lastname):
                                        screenname = user['screen_name']
                                        keywords[screenname] = "Twitter"
                                        break
                        except AttributeError, e:
                            pass
                        config[firstname + " " + lastname] = screenname
                    keywords[firstname + " " + lastname] = "Actor"

                # Radio appears to have been forgotten about a bit in RDF / scheduling at the mo
                if "radio" in channel or "6music" in channel or "asiannetwork" in channel or "sportsextra" in channel or "worldservice" in channel:
                    # However, radio shows are often named using the DJ - The cases where this isn't true will cause problems however as they'll be saved in json - DOH! TODO
                    if config.has_key(titlesave):
                        # Found a cached value
                        if config[titlesave] != "":
                            keywords[config[titlesave]] = "Twitter"
                    elif len(titlesave.split()) < 4: # Prevent some shows getting through at least - restricts people's names to three words
                        self.send(titlesave, "search")
                        while not self.dataReady("search"):
                            pass
                        twitdata = self.recv("search")
                        screenname = ""
                        try:
                            for user in twitdata:
                                if user.has_key('verified'):
                                    if (user['verified'] == True or user['followers_count'] > 10000) and  string.lower(user['name']) == titlesave.lower():
                                        screenname = user['screen_name']
                                        keywords[screenname] = "Twitter"
                                        break
                        except AttributeError, e:
                            pass
                        config[titlesave] = screenname

                try:
                    file = open(homedir + "/namecache.conf",'w')
                    raw_config = cjson.encode(config)
                    file.write(raw_config)
                    file.close()
                except IOError, e:
                    print ("Failed to save name cache - could cause rate limit problems")


                return [keywords,data]
            
        else:
            if pid == None:
                print(channel + ": No change - Off Air")
            else:
                print (channel + ": No change - " + title)

    def dbConnect(self):
        db = MySQLdb.connect(user=self.dbuser,passwd=self.dbpass,db="twitter_bookmarks")
        cursor = db.cursor()
        return cursor

    def main(self):
        cursor = self.dbConnect()
        oldkeywords = None
        while not self.finished():
            print ("### Checking current programmes ###")
            if self.channel != "all":
                oldpid = self.channels[self.channel]
                if oldpid == None:
                    cursor.execute("""UPDATE programmes SET imported = 1 WHERE channel = %s""",(self.channel))
                data = self.doStuff(self.channel)
                if data != None:
                    keywords = data[0]
                    pid = data[1][0]
                    title = data[1][1]
                    offset = data[1][2]
                    duration = data[1][3]
                    expectedstart = data[1][4]
                    cursor.execute("""UPDATE programmes SET imported = 1 WHERE pid != %s AND channel = %s""",(pid,self.channel))
                    cursor.execute("""SELECT * FROM programmes WHERE pid = %s""",(pid))
                    if cursor.fetchone() == None:
                        cursor.execute("""INSERT INTO programmes (pid,title,timediff,duration,expectedstart,channel) VALUES (%s,%s,%s,%s,%s,%s)""", (pid,title,offset,duration,expectedstart,self.channel))
                        for word in keywords:
                            cursor.execute("""INSERT INTO keywords (pid,keyword,type) VALUES (%s,%s,%s)""", (pid,word,keywords[word]))
                    keywords = list()
                else:
                    keywords = None

                cursor.execute("""SELECT keyword FROM keywords WHERE pid = %s""",(pid))
                keywordquery = cursor.fetchall()
                for keyword in keywordquery:
                    # This ^ is a temporary fix until I work out a better DB structure
                    if "^" in keyword[0]:
                        keywords.append(string.replace(keyword[0],"^"," "))
                    else:
                        keywords.append(keyword[0])

                if (keywords != oldkeywords) & (keywords != None):
                    print keywords
                    self.send([keywords,[pid]],"outbox")
                    pass
                
            else:
                # Still need to fix the 'changed to - off air' problem, but it isn't causing twitter keyword redos thankfully (purely a printing error)
                # Possible issue will start to occur if programmes change too often - tweet stream will miss too much
                keywords = list()
                for channel in self.channels:
                    oldpid = self.channels[channel]
                    if oldpid == None:
                        cursor.execute("""UPDATE programmes SET imported = 1 WHERE channel = %s""",(channel))
                    data = self.doStuff(channel)
                    if data != None:
                        keywordappender = data[0]
                        pid = data[1][0]
                        title = data[1][1]
                        offset = data[1][2]
                        duration = data[1][3]
                        expectedstart = data[1][4]
                        cursor.execute("""UPDATE programmes SET imported = 1 WHERE pid != %s AND channel = %s""",(pid,channel))
                        cursor.execute("""SELECT * FROM programmes WHERE pid = %s""",(pid))
                        if cursor.fetchone() == None:
                            cursor.execute("""INSERT INTO programmes (pid,title,timediff,duration,expectedstart,channel) VALUES (%s,%s,%s,%s,%s,%s)""", (pid,title,offset,duration,expectedstart,channel))
                            for word in keywordappender:
                                cursor.execute("""INSERT INTO keywords (pid,keyword,type) VALUES (%s,%s,%s)""", (pid,word,keywordappender[word]))

                currentpids = list()
                for channel in self.channels:
                    if self.channels[channel] != "" and self.channels[channel] != None:
                        currentpids.append(self.channels[channel])

                for pid in currentpids:
                    cursor.execute("""SELECT keyword FROM keywords WHERE pid = %s""",(pid))
                    keywordquery = cursor.fetchall()
                    for keyword in keywordquery:
                        # This ^ is a temporary fix until I work out a better DB structure
                        if "^" in keyword[0]:
                            keywords.append(string.replace(keyword[0],"^"," "))
                        else:
                            keywords.append(keyword[0])

                # Remove repeated keywords here
                if len(keywords) != 0:
                    keywords = list(set(keywords))

                if (keywords != oldkeywords) & (len(keywords) != 0):
                    print keywords
                    self.send([keywords,currentpids],"outbox") #epicfail: now need to send all pids, and search through them further down the line
                    pass


            if self.dataReady("inbox"):
                print self.recv("inbox")
            oldkeywords = keywords
            # At this point, find the version tags to allow further info finding
            # Then, pass keywords to TwitterStream. DataCollector will pick up the data
            # Must deal with errors passed back from TwitterStream here
            self.firstrun = False
            time.sleep(30) # Wait for 30 secs - don't need as much given the wait time between /programmes requests
            # Could always get this to wait until the programme is due to change, but this *may* miss last minute schedule changes
            
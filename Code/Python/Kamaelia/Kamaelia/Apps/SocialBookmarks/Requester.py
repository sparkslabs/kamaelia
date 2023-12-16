#! /usr/bin/python

# Requests current BBC prog, gets relevant keywords, sends off relevant Twitter searches
# One requester for ALL channels - avoids creating multiple Twitter streams
# Only sends keywords to Twitter once per programme, then monitors for the next programme

raise NotImplementedError("Needs fixing due to MySQLdb  -- python 2.0 based -- rdflib")
import json as cjson
import os
import re
import string
import time
import rdflib
from rdflib.Graph import Graph

from datetime import date

from Axon.Ipc import producerFinished
from Axon.Ipc import shutdownMicroprocess
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Apps.SocialBookmarks.Print import Print
from Kamaelia.Apps.SocialBookmarks.DBWrapper import DBWrapper

class Requester(DBWrapper,threadedcomponent):
    Inboxes = {
        "inbox" : "",
        "control" : "",
        "whatson" : "Receives back what's currently on a channel - [pid,title,timeoffset,duration,expectedstarttime]",
        "proginfo" : "Receives back raw RDF data for a PID",
        "search" : "Receives back raw Twitter people search JSON",
        "datain" : "URL contents returns from getter component",
    }
    Outboxes = {
        "outbox" : "Sends out keywords and pid(s) for streaming API connections - [[keyword,keyword],[pid,pid,pid]]",
        "signal" : "",
        "whatson" : "Requests current programmes by sending a channel name",
        "proginfo" : "Requests RDF format data for a pid - [pid, 'rdf']",
        "search" : "Sends people's names for Twitter username identification",
        "dataout" : "URL requests to getter component",
    }

    def __init__(self, channel,dbuser,dbpass):
        super(Requester, self).__init__(dbuser=dbuser,dbpass=dbpass)
        self.channel = channel
        # Keep a record of the current PID for each channel here
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
            "b006mg74" : ["bbcwatchdog"], # Watchdog
            "b006v5tb" : ['bbcbreakfast'], # Breakfast
            "b006mkw3" : ["hignfy","bbchignfy"], # Have I Got News For You
            "b008dk4b" : ["childreninneed","bbccin","#cin","#pudsey","pudseybear"], # Children in Need
        }
        # Series PIDs associated with programmes. ONLY used where prog doesn't have a brand
        self.officialseriestags = {
            "b00v2z3s" : ["#askrhod"], # Ask Rhod Gilbert
            "b00vd7qz" : ['film2010'], # Film 2010
            "b00vsw36" : ['manlab'] # James May's Man Lab
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
        # Check what's on for each channel
        self.send(channel, "whatson")
        while not self.dataReady("whatson"):
            pass
        data = self.recv("whatson")
        if data == None:
            pid = None
        else:
            pid = data[0]
            title = data[1]
            offset = data[2]
            duration = data[3]
            expectedstart = data[4]
        if pid != self.channels[channel]:
            # Perhaps just do a duplicate scan before creating Twitter stream
            if pid == None:
                self.channels[channel] = None
                Print (channel, ": Off Air")
            else:
                self.channels[channel] = pid
                self.send(["http://www.bbc.co.uk/programmes/" + pid + ".rdf"], "dataout")
                while not self.dataReady("datain"):
                    pass
                recvdata = self.recv("datain")
                
                if recvdata[0] == "OK":
                    programmedata = recvdata[1]
                else:
                    # Fake programme data to prevent crash - not ideal
                    programmedata = '<?xml version="1.0" encoding="utf-8"?> \
                                    <rdf:RDF xmlns:rdf      = "http://www.w3.org/1999/02/22-rdf-syntax-ns#" \
                                             xmlns:rdfs     = "http://www.w3.org/2000/01/rdf-schema#" \
                                             xmlns:owl      = "http://www.w3.org/2002/07/owl#" \
                                             xmlns:foaf     = "http://xmlns.com/foaf/0.1/" \
                                             xmlns:po       = "http://purl.org/ontology/po/" \
                                             xmlns:mo       = "http://purl.org/ontology/mo/" \
                                             xmlns:skos     = "http://www.w3.org/2008/05/skos#" \
                                             xmlns:time     = "http://www.w3.org/2006/time#" \
                                             xmlns:dc       = "http://purl.org/dc/elements/1.1/" \
                                             xmlns:dcterms  = "http://purl.org/dc/terms/" \
                                             xmlns:wgs84_pos= "http://www.w3.org/2003/01/geo/wgs84_pos#" \
                                             xmlns:timeline = "http://purl.org/NET/c4dm/timeline.owl#" \
                                             xmlns:event    = "http://purl.org/NET/c4dm/event.owl#"> \
                                    </rdf:RDF>'

                # RDF reader needs to read from a file so write out first
                # Alternative is to read from a URL, but this lacks proper proxy support
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
                    if (bidmod in self.officialbrandtags):
                        twittags = self.officialbrandtags[bidmod]
                        break

                # Identify the series and whether there are any official hashtags
                if len(twittags) == 0:
                    # Identify the brand and whether there are any official hashtags
                    for sid in g.subjects(object = rdflib.URIRef('http://purl.org/ontology/po/Series')):
                        # sid is Series ID
                        sidmod = sid.replace("#programme","")
                        sidmod = str(sidmod.replace("file:///programmes/",""))
                        if (sidmod in self.officialseriestags):
                            twittags = self.officialseriestags[sidmod]
                            break

                vidmod = ""
                so = g.subject_objects(predicate=rdflib.URIRef('http://purl.org/ontology/po/version'))
                # Pick a version, any version - for this which one doesn't matter
                for x in so:
                    # vid is version id
                    vid = x[1]
                    vidmod = vid.replace("#programme","")
                    vidmod = vidmod.replace("file:///programmes/","")
                    break

                # Got version, now get people

                self.send(["http://www.bbc.co.uk/programmes/" + vidmod + ".rdf"], "dataout")
                while not self.dataReady("datain"):
                    pass
                recvdata = self.recv("datain")
                if recvdata[0] == "OK":
                    versiondata = recvdata[1]
                else:
                    versiondata = '<?xml version="1.0" encoding="utf-8"?> \
                                    <rdf:RDF xmlns:rdf      = "http://www.w3.org/1999/02/22-rdf-syntax-ns#" \
                                             xmlns:rdfs     = "http://www.w3.org/2000/01/rdf-schema#" \
                                             xmlns:owl      = "http://www.w3.org/2002/07/owl#" \
                                             xmlns:foaf     = "http://xmlns.com/foaf/0.1/" \
                                             xmlns:po       = "http://purl.org/ontology/po/" \
                                             xmlns:mo       = "http://purl.org/ontology/mo/" \
                                             xmlns:skos     = "http://www.w3.org/2008/05/skos#" \
                                             xmlns:time     = "http://www.w3.org/2006/time#" \
                                             xmlns:dc       = "http://purl.org/dc/elements/1.1/" \
                                             xmlns:dcterms  = "http://purl.org/dc/terms/" \
                                             xmlns:wgs84_pos= "http://www.w3.org/2003/01/geo/wgs84_pos#" \
                                             xmlns:timeline = "http://purl.org/NET/c4dm/timeline.owl#" \
                                             xmlns:event    = "http://purl.org/NET/c4dm/event.owl#"> \
                                    </rdf:RDF>'

                filepath = "tempRDF.txt"
                file = open(filepath, 'w')
                file.write(versiondata)
                file.close()

                g = Graph()
                g.parse("tempRDF.txt")

                # Identify if this is a change of programme, or the first time we've checked what's on for Print clarity
                if self.firstrun:
                    Print (channel , ": " + title)
                else:
                    Print (channel , ": Changed to - " , title)

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
                # Save keywords next to a descriptor of what they are
                keywords[pid] = "PID"

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
                keywords["#" + re.sub("\s+","",allwordtitle)] = "Title"

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

                # Load NameCache (people we've already searched for on Twitter to avoid hammering PeopleSearch)
                save = False
                try:
                    homedir = os.path.expanduser("~")
                    file = open(homedir + "/namecache.conf",'r')
                    save = True
                except IOError:
                    e = sys.exc_info()[1]
                    Print ("Failed to load name cache - will attempt to create a new file: " ,  e)

                if save:
                    raw_config = file.read()
                    file.close()
                    try:
                        config = cjson.decode(raw_config)
                    except cjson.DecodeError:
                        e = sys.exc_info()[1]
                        config = dict()
                else:
                    config = dict()

                s = g.subjects(predicate=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),object=rdflib.URIRef('http://purl.org/ontology/po/Role'))

                for x in s:
                    rid = g.value(predicate=rdflib.URIRef('http://purl.org/ontology/po/role'),object=rdflib.BNode(x))
                    pid = g.value(subject=rdflib.BNode(rid),predicate=rdflib.URIRef('http://purl.org/ontology/po/participant'))
                    firstname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/givenName')))
                    lastname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/familyName')))

                    if ((firstname + " " + lastname) in config):
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
                                # Only use this Twitter screen name if there's a good chance they're the person we're after
                                if ("verified" in user):
                                    if (user['verified'] == True or user['followers_count'] > 10000) and string.lower(user['name']) == string.lower(firstname + " " + lastname):
                                        screenname = user['screen_name']
                                        keywords[screenname] = "Twitter"
                                        break
                        except AttributeError:
                            pass
                        config[firstname + " " + lastname] = screenname
                    keywords[firstname + " " + lastname] = "Participant"

                s = g.subjects(predicate=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),object=rdflib.URIRef('http://purl.org/ontology/po/Character'))

                for x in s:
                    character = str(g.value(subject=rdflib.BNode(x),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/name')))
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
                    if ((firstname + " " + lastname) in config):
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
                                if ("verified" in user):
                                    if (user['verified'] == True or user['followers_count'] > 10000) and string.lower(user['name']) == string.lower(firstname + " " + lastname):
                                        screenname = user['screen_name']
                                        keywords[screenname] = "Twitter"
                                        break
                        except AttributeError:
                            pass
                        config[firstname + " " + lastname] = screenname
                    keywords[firstname + " " + lastname] = "Actor"

                # Radio appears to have been forgotten about a bit in RDF / scheduling at the mo
                # So, let's do some extra queries and see if the show title is a person's name on Twitter
                if "radio" in channel or "6music" in channel or "asiannetwork" in channel or "sportsextra" in channel or "worldservice" in channel:
                    # However, radio shows are often named using the DJ - The cases where this isn't true will cause problems however as they'll be saved in json - DOH! TODO
                    if (titlesave in config):
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
                                if ("verified" in user):
                                    if (user['verified'] == True or user['followers_count'] > 10000) and  string.lower(user['name']) == titlesave.lower():
                                        screenname = user['screen_name']
                                        keywords[screenname] = "Twitter"
                                        break
                        except AttributeError:
                            pass
                        config[titlesave] = screenname

                try:
                    file = open(homedir + "/namecache.conf",'w')
                    raw_config = cjson.encode(config)
                    file.write(raw_config)
                    file.close()
                except IOError:
                    Print ("Failed to save name cache - could cause rate limit problems")

                return [keywords,data]
            
        else:
            if pid == None:
                Print(channel , ": No change - Off Air")
            else:
                Print (channel , ": No change - " , title)

    def main(self):
        self.dbConnect()
        oldkeywords = None
        while not self.finished():
            Print ("### Checking current programmes ###")
            if self.channel != "all":
                oldpid = self.channels[self.channel]
                if oldpid == None:
                    self.db_update("""UPDATE programmes SET imported = 1 WHERE channel = %s""",(self.channel))
                data = self.doStuff(self.channel)
                if data != None:
                    keywords = data[0]
                    pid = data[1][0]
                    title = data[1][1]
                    offset = data[1][2]
                    duration = data[1][3]
                    timestamp = data[1][4]
                    utcoffset = data[1][5]
                    self.db_update("""UPDATE programmes SET imported = 1 WHERE pid != %s AND channel = %s""",(pid,self.channel))
                    self.db_select("""SELECT channel FROM programmes WHERE pid = %s AND timestamp = %s""",(pid,timestamp))
                    progentrytest = self.db_fetchone()
                    self.db_select("""SELECT duration FROM programmes_unique WHERE pid = %s""",(pid))
                    progtest2 = self.db_fetchone()
                    if progentrytest == None:
                        self.db_insert("""INSERT INTO programmes (pid,timediff,timestamp,utcoffset,channel) VALUES (%s,%s,%s)""", (pid,offset,timestamp,utcoffset,self.channel))
                        if progtest2 == None:
                            self.db_insert("""INSERT INTO programmes_unique (pid,title,duration) VALUES (%s,%s,%s)""", (pid,title,duration))
                            for word in keywords:
                                self.db_insert("""INSERT INTO keywords (pid,keyword,type) VALUES (%s,%s,%s)""", (pid,word,keywords[word]))
                    else:
                        # Fix for programmes where the duration is changed last minute
                        if progtest2[0] < duration:
                            #self.db_update("""UPDATE programmes SET duration = %s WHERE pid = %s AND timestamp = %s""",(duration,pid,timestamp))
                            self.db_update("""UPDATE programmes_unique SET duration = %s WHERE pid = %s""",(duration,pid))
                    keywords = list()
                else:
                    keywords = None

                self.db_select("""SELECT keyword FROM keywords WHERE pid = %s""",(pid))
                keywordquery = self.db_fetchall()
                for keyword in keywordquery:
                    # This ^ is a temporary fix until I work out a better DB structure
                    if "^" in keyword[0]:
                        keywords.append(string.replace(keyword[0],"^"," "))
                    else:
                        keywords.append(keyword[0])

                if (keywords != oldkeywords) & (keywords != None):
                    Print(keywords)
                    self.send([keywords,[pid]],"outbox")
                    pass
                
            else:
                # Still need to fix the 'changed to - off air' problem, but it isn't causing twitter keyword redos thankfully (purely a Printing error)
                # Possible issue will start to occur if programmes change too often - tweet stream will miss too much
                keywords = list()
                for channel in self.channels:
                    oldpid = self.channels[channel]
                    if oldpid == None:
                        self.db_update("""UPDATE programmes SET imported = 1 WHERE channel = %s""",(channel))
                    data = self.doStuff(channel)
                    if data != None:
                        keywordappender = data[0]
                        pid = data[1][0]
                        title = data[1][1]
                        offset = data[1][2]
                        duration = data[1][3]
                        timestamp = data[1][4]
                        utcoffset = data[1][5]
                        self.db_update("""UPDATE programmes SET imported = 1 WHERE pid != %s AND channel = %s""",(pid,channel))
                        self.db_select("""SELECT channel FROM programmes WHERE pid = %s AND timestamp = %s""",(pid,timestamp))
                        progentrytest = self.db_fetchone()
                        self.db_select("""SELECT duration FROM programmes_unique WHERE pid = %s""",(pid))
                        progtest2 = self.db_fetchone()
                        if progentrytest == None:
                            self.db_insert("""INSERT INTO programmes (pid,timediff,timestamp,utcoffset,channel) VALUES (%s,%s,%s,%s,%s)""", (pid,offset,timestamp,utcoffset,channel))
                            if progtest2 == None:
                                self.db_insert("""INSERT INTO programmes_unique (pid,title,duration) VALUES (%s,%s,%s)""", (pid,title,duration))
                                for word in keywordappender:
                                    self.db_insert("""INSERT INTO keywords (pid,keyword,type) VALUES (%s,%s,%s)""", (pid,word,keywordappender[word]))
                        else:
                            # Fix for programmes where the duration is changed last minute
                            if progtest2[0] < duration:
                                #self.db_update("""UPDATE programmes SET duration = %s WHERE pid = %s AND timestamp = %s""",(duration,pid,timestamp))
                                self.db_update("""UPDATE programmes_unique SET duration = %s WHERE pid = %s""",(duration,pid))

                currentpids = list()
                for channel in self.channels:
                    if self.channels[channel] != "" and self.channels[channel] != None:
                        currentpids.append(self.channels[channel])

                for pid in currentpids:
                    self.db_select("""SELECT keyword FROM keywords WHERE pid = %s""",(pid))
                    keywordquery = self.db_fetchall()
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
                    Print(keywords)
                    self.send([keywords,currentpids],"outbox") #epicfail: now need to send all pids, and search through them further down the line
                    pass


            oldkeywords = keywords
            # At this point, find the version tags to allow further info finding
            # Then, pass keywords to TwitterStream. DataCollector will pick up the data
            # Must deal with errors passed back from TwitterStream here
            self.firstrun = False
            time.sleep(30) # Wait for 30 secs - don't need as much given the wait time between /programmes requests
            # Could always get this to wait until the programme is due to change, but this *may* miss last minute schedule changes
            

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

from Axon.ThreadedComponent import threadedcomponent

class Requester(threadedcomponent):
    Inboxes = ["inbox", "control", "whatson", "proginfo", "search"]
    Outboxes = ["outbox", "signal", "whatson", "proginfo", "search"]

    def __init__(self, channel,dbuser,dbpass):
        super(Requester, self).__init__()
        self.channel = channel
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.channels = {"bbcone" : "",
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
                        "radio5" : "",
                        "worldservice" : "",
                        "6music" : "",
                        "radio7" : "",
                        "1xtra" : "",
                        "bbcparliament" : "",
                        "asiannetwork" : "",
                        "sportsextra" : ""}
        # Modify this to construct the dictionary based on the channel names passed in?
        self.firstrun = True

    def doStuff(self, channel):
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
        if pid != self.channels[channel]:
            #TODO: Will need to check, esp in radio case if presenter name is the same as show name to reduce duplicate keywords
            # Perhaps just do a duplicate scan before creating Twitter stream
            if pid == None:
                if self.firstrun:
                    print (channel + ": Off Air")
                else:
                    print (channel + ": Changed to - Off Air")
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
                g.parse("tempRDF.txt")

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

                # Remove punctuation
                for item in """!"#$%&()*+,-./:;<=>?@[\\]?_'`{|}?""":
                    title = title.replace(item,"")

                #print "Twitter Keywords for " + pid + ":"
                #print "#" + channel + " #" + re.sub("\s+","",title)
                # TODO: Should remove CONTENT of brackets, not just the brackets
                # TODO: Remove 'the' from the start of programme names like '#thedailypolitics' - trouble is, #theoneshow needs to keep its 'the'
                if string.find(title,"The",0,3) != -1:
                    newtitle = string.replace(re.sub("\s+","",title),"The","",1)
                    keywords = [channel,"#" + string.lower(re.sub("\s+","",title)),'#' + string.lower(re.sub("\s+","",newtitle))]
                else:
                    keywords = [channel,"#" + string.lower(re.sub("\s+","",title))]

                # Load NameCache
                save = False
                try:
                    homedir = os.path.expanduser("~")
                    file = open(homedir + "/namecache.conf",'r')
                    save = True
                except IOError, e:
                    print ("Failed to load name cache - postponing twitter searches: " + str(e))

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
                    #role = g.value(subject=rdflib.BNode(x),predicate=rdflib.URIRef('http://purl.org/dc/elements/1.1/title'))
                    rid = g.value(predicate=rdflib.URIRef('http://purl.org/ontology/po/role'),object=rdflib.BNode(x))
                    pid = g.value(subject=rdflib.BNode(rid),predicate=rdflib.URIRef('http://purl.org/ontology/po/participant'))
                    firstname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/givenName')))
                    lastname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/familyName')))
                    #print role + " is " + firstname + " " + lastname
                    #print firstname + " " + lastname

                    if config.has_key(firstname + " " + lastname):
                        # Found a cached value
                        if config[firstname + " " + lastname] != "":
                            keywords.append(config[firstname + " " + lastname])
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
                                        keywords.append(screenname)
                                        break
                        except AttributeError, e:
                            pass
                        config[firstname + " " + lastname] = screenname
                    keywords.append(firstname + " " + lastname)

                s = g.subjects(predicate=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),object=rdflib.URIRef('http://purl.org/ontology/po/Character'))

                for x in s:
                    character = str(g.value(subject=rdflib.BNode(x),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/name')))
                    # TODO: Character names would probably work best as just first names, but watch out for Dr. etc appearing first
                    rid = g.value(predicate=rdflib.URIRef('http://purl.org/ontology/po/role'),object=rdflib.BNode(x))
                    pid = g.value(subject=rdflib.BNode(rid),predicate=rdflib.URIRef('http://purl.org/ontology/po/participant'))
                    firstname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/givenName')))
                    lastname = str(g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/familyName')))
                    #print character + " is " + firstname + " " + lastname
                    #print firstname + " " + lastname
                    keywords.append(character + " " + channel)
                    keywords.append(character + " " + title)
                    if " " in character:
                        # Looks like we have a firstname + surname situation
                        charwords = string.split(character)
                        if charwords[0] != "Dr" and charwords[0] != "Miss" and charwords[0] != "Mr" and charwords[0] != "Mrs" and charwords[0] != "Ms":
                            # As long as the first word isn't a title, add it as a first name
                            keywords.append(charwords[0] + " " + channel)
                            keywords.append(charwords[0] + " " + title)
                        elif len(charwords) > 2:
                            # If the first word was a title, and the second word isn't a surname (checked by > 2) add the first name
                            keywords.append(charwords[1] + " " + channel)
                            keywords.append(charwords[1] + " " + title)
                    if config.has_key(firstname + " " + lastname):
                        # Found a cached value
                        if config[firstname + " " + lastname] != "":
                            keywords.append(config[firstname + " " + lastname])
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
                                        keywords.append(screenname)
                                        break
                        except AttributeError, e:
                            pass
                        config[firstname + " " + lastname] = screenname
                    keywords.append(firstname + " " + lastname)

                # Radio appears to have been forgotten about a bit in RDF / scheduling at the mo
                if "radio" in channel:
                    # However, radio shows are often named using the DJ - The cases where this isn't true will cause problems however as they'll be saved in json - DOH! TODO
                    if config.has_key(title):
                        # Found a cached value
                        if config[title] != "":
                            keywords.append(config[title])
                    else:
                        self.send(title, "search")
                        while not self.dataReady("search"):
                            pass
                        twitdata = self.recv("search")
                        screenname = ""
                        try:
                            for user in twitdata:
                                if user.has_key('verified'):
                                    if (user['verified'] == True or user['followers_count'] > 10000) and  string.lower(user['name']) == string.lower(title):
                                        screenname = user['screen_name']
                                        keywords.append(screenname)
                                        break
                        except AttributeError, e:
                            pass
                        config[title] = screenname

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
        oldpid = None # only relevant for single channel selection
        while 1:
            print ("### Checking current programmes ###")
            if self.channel != "all":
                data = self.doStuff(self.channel)
                if data != None:
                    keywords = data[0]
                    pid = data[1][0]
                    title = data[1][1]
                    offset = data[1][2]
                    if oldpid != None and oldpid != pid:
                        # Pid has changed - tie off the last prog ready for analysis
                        cursor.execute("""SELECT * FROM programmes WHERE pid = %s""",(oldpid))
                        if cursor.fetchone() == None:
                            cursor.execute("""UPDATE programmes SET imported = 1 WHERE pid = %s""",(oldpid))
                        oldpid = pid
                    cursor.execute("""SELECT * FROM programmes WHERE pid = %s""",(pid))
                    if cursor.fetchone() == None:
                        cursor.execute("""INSERT INTO programmes (pid,title,timediff) VALUES (%s,%s,%s)""", (pid,title,offset))
                        for word in keywords:
                            cursor.execute("""INSERT INTO keywords (pid,keyword) VALUES (%s,%s)""", (pid,word))
                else:
                    keywords = None
                
                if (keywords != oldkeywords) & (keywords != None):
                    print keywords
                    self.send([keywords,pid],"outbox")
                    pass
            else:
                # This bit just got complicated - won't work yet so concentrating on one channel - ABOVE
                # Now, adding some stuff above I've definitely broken this
                keywords = list()
                for channel in self.channels:
                    newwords = self.doStuff(channel)
                    if (newwords != None):
                        keywords.append(newwords)
                if (keywords != oldkeywords) & (keywords != None):
                    print keywords
                    pass
            if self.dataReady("inbox"):
                print self.recv("inbox")
            oldkeywords = keywords
            # At this point, find the version tags to allow further info finding
            # Then, pass keywords to TwitterStream. DataCollector will pick up the data
            # Must deal with errors passed back from TwitterStream here
            self.firstrun = False
            time.sleep(60) # Wait a minute!
            # Could always get this to wait until the programme is due to change, but this *may* miss last minute schedule changes
            
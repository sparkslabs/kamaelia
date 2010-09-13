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

#import rdfxml
import urllib2
import cjson
import os
#from rdflib.TripleStore import TripleStore
from rdflib.Graph import Graph
import rdflib

if __name__ == "__main__":
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


    if config['proxy']:
        proxy = config['proxy']

    # Configure proxy and opener
    if proxy:
        proxyhandler = urllib2.ProxyHandler({"http" : proxy})
        bbcopener = urllib2.build_opener(proxyhandler)
    else:
        bbcopener = urllib2.build_opener()

    # Get ready to grab BBC data
    urllib2.install_opener(bbcopener)


    #progurl = "http://www.bbc.co.uk/programmes/b00tmk13.rdf"
    progurl = "http://www.bbc.co.uk/programmes/b00jjmm3.rdf"
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
        filepath = "tempRDF.txt"
        file = open(filepath, 'w')
        file.write(content)
        file.close()
        #data = rdfxml.parseRDF(content).result
        #print(data)


        g = Graph()
        g.parse("tempRDF.txt")
 

        # Perhaps adapt this to store people in lists like:
        # ['Writer','Steven','Moffat']
        # or
        # ['Executive Producer','Steven','Moffat']
        # or
        # ['Character','James','Nesbitt','Clem']

        # Need to search all versions of a programme, but try to detect the right one! (b00b07kw.rdf)
        # To do this, ensure there is a broadcast element relating to the region of choice and the date and time expected (may be first or repeat - identify channel here too if not already done via schedule)

        #b = g.triples([None,None,None])
        #for x in b:
        #    print x

        s = g.subjects(predicate=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),object=rdflib.URIRef('http://purl.org/ontology/po/Role'))

        firstrun = True
        for x in s:
            if firstrun:
                print "#### General People ####"
            role = g.value(subject=rdflib.BNode(x),predicate=rdflib.URIRef('http://purl.org/dc/elements/1.1/title'))
            rid = g.value(predicate=rdflib.URIRef('http://purl.org/ontology/po/role'),object=rdflib.BNode(x))
            pid = g.value(subject=rdflib.BNode(rid),predicate=rdflib.URIRef('http://purl.org/ontology/po/participant'))
            firstname = g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/givenName'))
            lastname = g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/familyName'))
            print role + " is " + firstname + " " + lastname
            firstrun = False


        
        s = g.subjects(predicate=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),object=rdflib.URIRef('http://purl.org/ontology/po/Character'))

        firstrun = True
        for x in s:
            if firstrun:
                print "#### Characters ####"
            character = g.value(subject=rdflib.BNode(x),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/name'))
            rid = g.value(predicate=rdflib.URIRef('http://purl.org/ontology/po/role'),object=rdflib.BNode(x))
            pid = g.value(subject=rdflib.BNode(rid),predicate=rdflib.URIRef('http://purl.org/ontology/po/participant'))
            firstname = g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/givenName'))
            lastname = g.value(subject=rdflib.BNode(pid),predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/familyName'))
            print character + " is " + firstname + " " + lastname
            firstrun = False
            


        #(rdflib.BNode('WHdDoSan37'), rdflib.URIRef('http://xmlns.com/foaf/0.1/name'), rdflib.Literal(u'Lowe'))
        #(rdflib.BNode('WHdDoSan37'), rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://purl.org/ontology/po/Character'))

#! /usr/bin/python

# Bookmarks.py
# - Identifies current BBC programmes and generates keywords based on them.
# - Collects Twitter streaming API data based on generated keywords.
# Program run initially to join up all mailboxes etc

#### NOTE: THIS PROGRAMME CURRENTLY NEEDS A PROXY FREE CONNECTION IF OAUTH KEYS NEED REFRESHING

#### NOTE: Error handling is unfinished for HTTP based connections. Currently it purely prints to the screen.
#### Eventually Twitter and others would welcome an exponential backoff in places.

import cjson
import os

from Kamaelia.Chassis.Graphline import Graphline

from BBCProgrammes import WhatsOn, ProgrammeData
from Requester import Requester
from TwitterStream import TwitterStream
from TwitterSearch import PeopleSearch
from DataCollector import DataCollector

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
    dbuser = config['dbuser']
    dbpass = config['dbpass']

    # Set proxy server if available
    if config.has_key('proxy'):
        proxy = config['proxy']
    else:
        proxy = False

    # Set OAuth keypair if available
    if config.has_key('key') & config.has_key('secret'):
        keypair = [config['key'],config['secret']]
    else:
        keypair = False


    system = Graphline(CURRENTPROG = WhatsOn(proxy),
                    RDFSOURCE = ProgrammeData(proxy),
                    REQUESTER = Requester("all",dbuser,dbpass), # Can set this for specific channels to limit Twitter requests whilst doing dev
                    FIREHOSE = TwitterStream(username, password, proxy, True),
                    SEARCH = PeopleSearch(username, keypair, proxy),
                    COLLECTOR = DataCollector(dbuser,dbpass),
                    linkages = {("REQUESTER", "whatson") : ("CURRENTPROG", "inbox"), # Request what's currently broadcasting
                                ("CURRENTPROG", "outbox") : ("REQUESTER", "whatson"), # Pass back results of what's on
                                ("REQUESTER", "proginfo") : ("RDFSOURCE", "inbox"), # Request additional data about current programmes
                                ("RDFSOURCE", "outbox") : ("REQUESTER", "proginfo"), # Pass back additional data
                                ("REQUESTER", "outbox") : ("FIREHOSE", "inbox"), # Send generated keywords to Twitter streaming API
                                ("FIREHOSE", "outbox") : ("REQUESTER", "inbox"), # Process errors from streaming API TODO
                                ("FIREHOSE", "data") : ("COLLECTOR", "inbox"), # Collect data from streaming API
                                ("REQUESTER", "search") : ("SEARCH", "inbox"), # Perform Twitter people search based on keywords
                                ("SEARCH", "outbox") : ("REQUESTER", "search") # Return Twitter people search results
                                }
                            ).run()

    
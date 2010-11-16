#! /usr/bin/python

# Bookmarks.py
# - Identifies current BBC programmes and generates keywords based on them.
# - Collects Twitter streaming API data based on generated keywords.
# Program run initially to join up all mailboxes etc

### Danger area: Adding OAuth to both Twitter components will result in them both trying to renew the received key and secret
### To avoid this, there needs to be a way to pass received keys and secrets to components needing them before they try to make requests too.
### Also need to farm out access to config file from OAuth utilising components so they're more generic

import cjson
import os

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline

from BBCProgrammes import WhatsOn
from Requester import Requester
from TwitterStream import TwitterStream
from TwitterSearch import PeopleSearch
from DataCollector import DataCollector, RawDataCollector
from URLGetter import HTTPGetter
from LiveAnalysis import LiveAnalysis, LiveAnalysisNLTK
from TweetFixer import RetweetFixer, TweetCleaner, LinkResolver

from Kamaelia.Util.TwoWaySplitter import TwoWaySplitter

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
    bitlyusername = config['bitlyusername']
    bitlyapikey = config['bitlyapikey']

    # Set proxy server if available
    if config.has_key('proxy'):
        proxy = config['proxy']
    else:
        proxy = False

    # Set OAuth consumer keypair
    consumerkeypair = [config['consumerkey'],config['consumersecret']]

    # Set OAuth keypair if available
    if config.has_key('key') and config.has_key('secret'):
        keypair = [config['key'],config['secret']]
    else:
        keypair = False

    LINKER = Graphline(LINKRESOLVE = LinkResolver(bitlyusername,bitlyapikey),
                        LINKREQUESTER = HTTPGetter(proxy, "BBC R&D Grabber"),
                        linkages = {("self", "inbox") : ("LINKRESOLVE", "inbox"),
                                    ("LINKRESOLVE", "outbox") : ("self", "outbox"),
                                    ("LINKRESOLVE", "urlrequests") : ("LINKREQUESTER", "inbox"),
                                    ("LINKREQUESTER", "outbox") : ("LINKRESOLVE", "responses")}).activate()
    system = Graphline(CURRENTPROG = WhatsOn(proxy),
                    REQUESTER = Requester("all",dbuser,dbpass), # Can set this for specific channels to limit Twitter requests whilst doing dev
                    FIREHOSE = TwitterStream(username, password, proxy, True, 60), # Twitter API sends blank lines every 30 secs so timeout of 60 should be fine
                    SEARCH = PeopleSearch(consumerkeypair, keypair, proxy),
                    COLLECTOR = DataCollector(dbuser,dbpass),
                    RAWCOLLECTOR = RawDataCollector(dbuser,dbpass),
                    HTTPGETTER = HTTPGetter(proxy, "BBC R&D Grabber"),
                    HTTPGETTERRDF = HTTPGetter(proxy, "BBC R&D Grabber"),
                    TWOWAY = TwoWaySplitter(),
                    ANALYSIS = LiveAnalysis(dbuser,dbpass),
                    NLTKANALYSIS = LiveAnalysisNLTK(dbuser,dbpass),
                    TWEETCLEANER = Pipeline(LINKER,RetweetFixer(),TweetCleaner(['user_mentions','urls','hashtags'])),
                    linkages = {("REQUESTER", "whatson") : ("CURRENTPROG", "inbox"), # Request what's currently broadcasting
                                ("CURRENTPROG", "outbox") : ("REQUESTER", "whatson"), # Pass back results of what's on
                                ("REQUESTER", "outbox") : ("FIREHOSE", "inbox"), # Send generated keywords to Twitter streaming API
                                ("FIREHOSE", "outbox") : ("TWOWAY" , "inbox"),
                                ("TWOWAY", "outbox") : ("COLLECTOR" , "inbox"),
                                ("TWOWAY", "outbox2") : ("RAWCOLLECTOR" , "inbox"),
                                ("REQUESTER", "search") : ("SEARCH", "inbox"), # Perform Twitter people search based on keywords
                                ("SEARCH", "outbox") : ("REQUESTER", "search"), # Return Twitter people search results
                                ("REQUESTER", "dataout") : ("HTTPGETTERRDF", "inbox"),
                                ("CURRENTPROG", "dataout") : ("HTTPGETTER", "inbox"),
                                ("HTTPGETTER", "outbox") : ("CURRENTPROG", "datain"),
                                ("HTTPGETTERRDF", "outbox") : ("REQUESTER", "datain"),
                                ("ANALYSIS", "nltk") : ("NLTKANALYSIS", "inbox"),
                                ("NLTKANALYSIS", "outbox") : ("ANALYSIS", "nltk"),
                                ("NLTKANALYSIS", "tweetfixer") : ("TWEETCLEANER", "inbox"),
                                ("TWEETCLEANER", "outbox") : ("NLTKANALYSIS", "tweetfixer"),
                                }
                            ).run()

    
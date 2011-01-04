#! /usr/bin/python

'''
Bookmarks.py - Main Executable
- Identifies current BBC programmes and generates keywords based on them.
- Collects Twitter streaming API data based on generated keywords.
- Analyses the collected data to identify frequent words, hence allowing the web interface to generate bookmarks.
'''

### Danger area: Adding OAuth to both Twitter components will result in them both trying to renew the received key and secret
### To avoid this, there needs to be a way to pass received keys and secrets to components needing them before they try to make requests too.
### Also need to farm out access to config file from OAuth utilising components so they're more generic

# This program requires a config based on the included twitter-login.conf.dist saving to /home/<yourusername>/twitter-login.conf
# During the running of the program, it will create a file called tempRDF.txt in the running directory
# It will also create files called namecache.conf, linkcache.conf and oversizedtweets.conf in your home directory
# See the README for more information

import os
import sys

from Kamaelia.Apps.SocialBookmarks.BBCProgrammes import WhatsOn
from Kamaelia.Apps.SocialBookmarks.DataCollector import DataCollector, RawDataCollector
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.TwoWaySplitter import TwoWaySplitter
from Kamaelia.Apps.SocialBookmarks.LiveAnalysis import FinalAnalysisNLTK, LiveAnalysis, LiveAnalysisNLTK
from Kamaelia.Apps.SocialBookmarks.Requester import Requester
from Kamaelia.Apps.SocialBookmarks.TweetFixer import LinkResolver, RetweetCorrector, RetweetFixer, TweetCleaner
from Kamaelia.Apps.SocialBookmarks.TwitterSearch import PeopleSearch
from Kamaelia.Apps.SocialBookmarks.TwitterStream import TwitterStream
from Kamaelia.Apps.SocialBookmarks.URLGetter import HTTPGetter
import cjson


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

    # Set OAuth secret keypair if available - if not it will be sourced from Twitter
    if config.has_key('key') and config.has_key('secret'):
        keypair = [config['key'],config['secret']]
    else:
        keypair = False

    # Linker component for LiveAnalysis
    LINKER = Graphline(LINKRESOLVE = LinkResolver(bitlyusername,bitlyapikey),
                        LINKREQUESTER = HTTPGetter(proxy, "BBC R&D Grabber", 10),
                        linkages = {("self", "inbox") : ("LINKRESOLVE", "inbox"),
                                    ("LINKRESOLVE", "outbox") : ("self", "outbox"),
                                    ("LINKRESOLVE", "urlrequests") : ("LINKREQUESTER", "inbox"),
                                    ("LINKREQUESTER", "outbox") : ("LINKRESOLVE", "responses")}).activate()
    # Linker component for FinalAnalysis
    # This duplication could probably be avoided by doing some tagging/filtering TODO
    LINKERFINAL = Graphline(LINKRESOLVE = LinkResolver(bitlyusername,bitlyapikey),
                        LINKREQUESTER = HTTPGetter(proxy, "BBC R&D Grabber", 10),
                        linkages = {("self", "inbox") : ("LINKRESOLVE", "inbox"),
                                    ("LINKRESOLVE", "outbox") : ("self", "outbox"),
                                    ("LINKRESOLVE", "urlrequests") : ("LINKREQUESTER", "inbox"),
                                    ("LINKREQUESTER", "outbox") : ("LINKRESOLVE", "responses")}).activate()
    system = Graphline(CURRENTPROG = WhatsOn(proxy),
                    REQUESTER = Requester("all",dbuser,dbpass), # Can set this for specific channels to limit Twitter requests whilst doing dev
                    FIREHOSE = TwitterStream(username, password, proxy, True, 40), # Twitter API sends blank lines every 30 secs so timeout of 40 should be fine
                    SEARCH = PeopleSearch(consumerkeypair, keypair, proxy),
                    COLLECTOR = DataCollector(dbuser,dbpass),
                    RAWCOLLECTOR = RawDataCollector(dbuser,dbpass),
                    HTTPGETTER = HTTPGetter(proxy, "BBC R&D Grabber", 10),
                    HTTPGETTERRDF = HTTPGetter(proxy, "BBC R&D Grabber", 10),
                    TWOWAY = TwoWaySplitter(),
                    ANALYSIS = LiveAnalysis(dbuser,dbpass),
                    NLTKANALYSIS = LiveAnalysisNLTK(dbuser,dbpass),
                    TWEETCLEANER = Pipeline(LINKER,RetweetFixer(),RetweetCorrector(dbuser,dbpass),TweetCleaner(['user_mentions','urls','hashtags'])),
                    NLTKANALYSISFINAL = FinalAnalysisNLTK(dbuser,dbpass),
                    TWEETCLEANERFINAL = Pipeline(LINKERFINAL,RetweetFixer(),RetweetCorrector(dbuser,dbpass),TweetCleaner(['user_mentions','urls','hashtags'])),
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
                                ("ANALYSIS", "nltkfinal") : ("NLTKANALYSISFINAL", "inbox"),
                                ("NLTKANALYSISFINAL", "outbox") : ("ANALYSIS", "nltkfinal"),
                                ("NLTKANALYSISFINAL", "tweetfixer") : ("TWEETCLEANERFINAL", "inbox"),
                                ("TWEETCLEANERFINAL", "outbox") : ("NLTKANALYSISFINAL", "tweetfixer"),
                                }
                            ).run()

    

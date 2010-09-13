#! /usr/bin/python

# Program run initially to join up all mailboxes etc


#### NOTE: THIS PROGRAMME CURRENTLY NEEDS A PROXY FREE CONNECTION IF OAUTH KEYS NEED REFRESHING
#### NOTE: THIS PROGRAMME MUST ALSO BE ABLE TO ACCESS REITH IP ADDRESSES FOR THE DVB BRIDGE

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

    if config.has_key('proxy'):
        proxy = config['proxy']
    else:
        proxy = False

    if config.has_key('key') & config.has_key('secret'):
        keypair = [config['key'],config['secret']]
    else:
        keypair = False


    system = Graphline(CURRENTPROG = WhatsOn(proxy),
                    RDFSOURCE = ProgrammeData(proxy),
                    REQUESTER = Requester("bbctwo",dbuser,dbpass), # Can set this for specific channels to limit Twitter requests whilst doing dev
                    FIREHOSE = TwitterStream(username, password, proxy), # Not technically using firehose yet, but will be made to work the same way with that later (or gardenhose more likely)
                    SEARCH = PeopleSearch(username, keypair, proxy),
                    COLLECTOR = DataCollector(dbuser,dbpass),
                    linkages = {("REQUESTER", "whatson") : ("CURRENTPROG", "inbox"),
                                ("CURRENTPROG", "outbox") : ("REQUESTER", "whatson"),
                                ("REQUESTER", "proginfo") : ("RDFSOURCE", "inbox"),
                                ("RDFSOURCE", "outbox") : ("REQUESTER", "proginfo"),
                                ("REQUESTER", "outbox") : ("FIREHOSE", "inbox"),
                                ("FIREHOSE", "outbox") : ("REQUESTER", "inbox"),
                                ("FIREHOSE", "data") : ("COLLECTOR", "inbox"),
                                ("REQUESTER", "search") : ("SEARCH", "inbox"),
                                ("SEARCH", "outbox") : ("REQUESTER", "search")
                                }
                            ).run()

    
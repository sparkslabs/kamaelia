#!/usr/bin/python

import feedparser
import pprint
import Axon
import base64
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Util.PureTransformer import PureTransformer

def AuthenticatedRequestStream(user, passwd):
    auth = "Basic %s" % base64.encodestring("%s:%s" % (user,passwd))[:-1]
    def AuthRequest(line):
        request = {"url":line, 
                   "extraheaders": {"Authorization": auth},
                  }
        return request
    return AuthRequest

import sys
username = sys.argv[1]
password = sys.argv[2]

Pipeline(
    ConsoleReader(eol=""),
    PureTransformer(AuthenticatedRequestStream(username, password)),
    SimpleHTTPClient(),
    PureTransformer(feedparser.parse),
    PureTransformer(pprint.pformat),
    ConsoleEchoer(),
).run()

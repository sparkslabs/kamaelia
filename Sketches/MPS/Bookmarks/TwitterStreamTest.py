#!/usr/bin/python
# -*- coding: utf-8 -*-

from TwitterStream import TwitterStream
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Util.Console import ConsoleEchoer

import os
import sys


import urllib2
import cjson

def get_url(url):
    X = urllib2.urlopen(url)
    response = X.read()
    X.close()
    return response

try:
    username = os.environ["TWITTERUSERNAME"]
    password =  os.environ["TWITTERPASSWORD"]
except KeyError:
    print "For this script to work, you must set TWITTERUSERNAME to your twitter username"
    print "For this script to work, you must set TWITTERPASSWORD to your twitter password"
    print "eg"
    print "export TWITTERUSERNAME=example"
    print "export TWITTERPASSWORD=password"
    sys.exit(1)

try:
    proxy = os.environ["http_proxy"]
except KeyError:
    print "Not using a proxy. If you want to use a proxy, you need to do something like this"
    print "export http_proxy=http://www-cache.your.site.com:3128/"
    proxy = None

print username, password, proxy

pids = ["b00001", "b00002", "b00003"]
# keywords = [ "Sarah Jane", "CBBC"] #trending topics earlier

trends_url = "http://api.twitter.com/1/trends/current.json"
raw_trending = get_url(trends_url)
trending_cooked = cjson.decode(raw_trending)

print "Trending Topics", trending_cooked

trending_topics = [X["query"] for X in trending_cooked["trends"].values()[0]]

keywords = trending_topics

# request = [ pids, keywords ]
request = [ keywords, pids ] # docstring wrong, should be this way round

Pipeline(
    DataSource( [ request] ),
    TwitterStream(username=username, password = password, proxy = proxy),
    PureTransformer(lambda x: repr(x) + "\n"),
    ConsoleEchoer(),
).run()



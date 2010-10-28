#!/usr/bin/python

import base64
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor 
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline
from TwitterStream import HTTPClientResponseHandler, LineFilter
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Console import ConsoleEchoer
import cjson

class MyTransformer(PureTransformer):
    def processMessage(self, msg):
        try:
            return cjson.decode(msg)
        except cjson.DecodeError, e:
            print
            print "cjson.DecodeError", e
            print repr(msg)


if 0:
    # Takes base64 encoded stream and decodes it to a normal stream
    Pipeline(
        ReadFileAdaptor("tweets.b64.txt", readmode="line"),
        PureTransformer(base64.b64decode),
        SimpleFileWriter("b64decodedTweets.txt")
    ).run()

if 0:
    # Takes the normal stream and decodes it, successfully
    Pipeline(
        ReadFileAdaptor("b64decodedTweets.txt", readmode="line"),
        PureTransformer(lambda x: x.rstrip()),
        MyTransformer(),
    ).run()


if 0:
    # Given the non-fragmented stream, this successfully decodes the data.
    Pipeline(
        ReadFileAdaptor("b64decodedTweets.txt", readmode="line"),
        HTTPClientResponseHandler(suppress_header = True),
        PureTransformer(lambda x: x.rstrip()),
        MyTransformer(),
    ).run()

if 1:
    Pipeline(
        ReadFileAdaptor("ParsedCombinedBody.txt", readmode="line"),
        MyTransformer(),
#        HTTPClientResponseHandler(suppress_header = True),
#        SimpleFileWriter("ParsedCombinedBody.txt")
#        LineFilter(eol="\r\n"),
#        PureTransformer(lambda x: x.rstrip()),
#        MyTransformer(),
    ).run()

if 0:
    Pipeline(
        ReadFileAdaptor("tweets.b64.txt", readmode="line"),
        PureTransformer(base64.b64decode),
        HTTPClientResponseHandler(suppress_header = True),
        SimpleFileWriter("ParsedCombinedBody.txt")
#        LineFilter(eol="\r\n"),
#        PureTransformer(lambda x: x.rstrip()),
#        MyTransformer(),
    ).run()

if 0:
    Pipeline(
        ReadFileAdaptor("tweets.b64.txt", readmode="line"),
        PureTransformer(base64.b64decode),
        HTTPClientResponseHandler(suppress_header = True),
        PureTransformer(lambda x: x.rstrip()),
    #    PureTransformer(cjson.decode),
        MyTransformer(),
    #    SimpleFileWriter("tweets.b64raw.txt"),
    #    ConsoleEchoer(),
    ).run()

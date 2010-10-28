#!/usr/bin/python

import base64
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor 
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline
from TwitterStream import HTTPClientResponseHandler
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Console import ConsoleEchoer

Pipeline(
    ReadFileAdaptor("tweets.b64.txt", readmode="line"),
    PureTransformer(base64.b64decode),
    HTTPClientResponseHandler(suppress_header = True),
    SimpleFileWriter("tweets.b64raw.txt"),
).run()

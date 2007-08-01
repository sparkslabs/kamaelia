#!/usr/bin/python

import Axon
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer

class linesender(Axon.Component.component):
    def __init__(self, *lines):
        super(linesender, self).__init__()
        self.lines = lines[:]
    def main(self):
        for line in self.lines:
           self.send(line+"\r\n", "outbox")
           yield 1

pipeline(
    linesender("GET /cgi-bin/blog/feed.cgi HTTP/1.0",
               "Host: 127.0.0.1",
               ""),
    TCPClient("127.0.0.1", 80),
    ConsoleEchoer(),
).run()

#!/usr/bin/python

import Axon
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.SingleServer import SingleServer
 
class Cat(Axon.Component.component):
    def __init__(self, messages):
        super(Cat, self).__init__()
        for message in messages:
            self.send(message, "outbox")
    def main(self):
        while 1:
            self.pause()
            yield 1
import random

port = random.randint(1600,1699)
print "PORT", port
pipeline(
     Cat([
         "Hello World", "Hello World", "Hello World", "Hello World",
         "Hello World", "Hello World", "Hello World", "Hello World",
         "Hello World", "Hello World", "Hello World", "Hello World",
     ]),
     MessageRateLimit(2, 1),
     SingleServer(port=port),
#).run()
).activate()

pipeline(
    TCPClient("127.0.0.1", port),
    ConsoleEchoer(),
).run()

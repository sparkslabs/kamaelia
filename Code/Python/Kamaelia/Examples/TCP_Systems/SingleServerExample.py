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
        self.messages = messages
    def main(self):
        for message in self.messages:
            self.send(message, "outbox")
        while 1:
            self.pause()
            yield 1

port = 1602
pipeline(
     Cat([
         "Hello World", "Hello World", "Hello World", "Hello World",
         "Hello World", "Hello World", "Hello World", "Hello World",
         "Hello World", "Hello World", "Hello World", "Hello World",
     ]),
     MessageRateLimit(2, 1),
     SingleServer(port=port),
).activate()

pipeline(
    TCPClient("127.0.0.1", port),
    ConsoleEchoer(),
).run()
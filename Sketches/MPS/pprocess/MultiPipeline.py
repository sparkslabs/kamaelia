#!/usr/bin/python

import Axon.LikeFile
import pprocess
import time

class ProcessWrapComponent(object):
    def __init__(self, somecomponent):
        self.exchange = pprocess.Exchange()
        self.channel = None
        self.inbound = []
        self.thecomponent = somecomponent
        self.ce = None



    def run(self, channel):
        from Axon.LikeFile import likefile, background
        background().start()
        self.exchange.add(channel)
        self.channel = channel
        self.ce = likefile(self.thecomponent)
        for i in self.main():
            pass

    def activate(self):
        channel = pprocess.start(self.run)
        return channel

    def main(self):
        t = 0
        while 1:
            if time.time() - t > 0.2:
#                print "Wrapper!"
                t = time.time()

            if self.exchange.ready(0):
                chan = self.exchange.ready(0)[0]
                D = chan._receive()
#                print chan,D
                self.ce.put(*D)

            D = self.ce.anyReady()
            if D:
                for boxname in D:
                    D = self.ce.get(boxname)
#                    print "DATA FROM COMPONENT",boxname, D
                    self.channel._send((D, boxname))
#                print D
            yield 1

import Axon

class Flooble(Axon.Component.component):
    def __init__(self, tag):
        super(Flooble, self).__init__()
        self.tag = tag
    def main(self):
        t = 0
        while 1:
            if time.time() - t > 0.2:
#                print self.tag
                t = time.time()
            if self.dataReady("inbox"):
#                print "WOOOOOOOOOOOOOOOOOOOO", self.tag, self.recv("inbox")
                self.send("OK, let's reply..."+self.tag, "outbox")
            yield 1

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

# X = ProcessWrapComponent(Flooble("Flooble"))
# Y = ProcessWrapComponent(Flooble("Bazzle"))

from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox

X = ProcessWrapComponent(Textbox(position=(20, 340),
                                 text_height=36,
                                 screen_width=900,
                                 screen_height=400,
                                 background_color=(130,0,70),
                                 text_color=(255,255,255)))
#Y = ProcessWrapComponent(ConsoleEchoer())

Y = ProcessWrapComponent( TextDisplayer(position=(20, 90),
                                        text_height=36,
                                        screen_width=400,
                                        screen_height=540,
                                        background_color=(130,0,70),
                                        text_color=(255,255,255)) )


exchange = pprocess.Exchange()
chan1 = X.activate()
chan2 = Y.activate()

exchange.add(chan1)
exchange.add(chan2)

# print chan

while 1:
    for chan in exchange.ready(0):
        if chan == chan1:
            D = chan._receive()
            if D[1] == "outbox":
                chan2._send( (D[0], "inbox") )
    time.sleep(0.1)

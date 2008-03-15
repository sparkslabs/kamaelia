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
                print "Wrapper!"
                t = time.time()

            if self.exchange.ready(0):
                chan = self.exchange.ready(0)[0]
                D = chan._receive()
                print chan,D
                self.ce.put(*D)

            D = self.ce.anyReady()
            if D:
                for boxname in D:
                    D = self.ce.get(boxname)
                    print "DATA FROM COMPONENT",boxname, D
                    self.channel._send((D, boxname))
                print D
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
                print self.tag
                t = time.time()
            if self.dataReady("inbox"):
                print "WOOOOOOOOOOOOOOOOOOOO", self.tag, self.recv("inbox")
                self.send("OK, let's reply..."+self.tag, "outbox")
            yield 1

X = ProcessWrapComponent(Flooble("Flooble"))
Y = ProcessWrapComponent(Flooble("Bazzle"))

exchange = pprocess.Exchange()
chan = X.activate()
chan2 = Y.activate()

exchange.add(chan)
exchange.add(chan2)

print chan

while 1:
    chan._send(("hello","inbox"))
    for chan in exchange.ready(0):
        D = chan._receive()
        print "PASSED BACK OUT FROM COMPONENT IN OTHER PROCESS", D
    time.sleep(1)

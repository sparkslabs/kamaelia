#!/usr/bin/python

import Axon
from Axon.Scheduler import scheduler
import Axon.LikeFile
import pprocess
import time
import pprint

class ProcessWrapComponent(object):
    def __init__(self, somecomponent):
        print "somecomponent.name",somecomponent.name
        self.exchange = pprocess.Exchange()
        self.channel = None
        self.inbound = []
        self.thecomponent = somecomponent
        self.ce = None
        self.tick = time.time()

    def ticking(self):
        if time.time() - self.tick > 1:
            print "TICK", self.thecomponent.name
            self.tick = time.time()

    def run(self, channel):
        self.exchange.add(channel)
        self.channel = channel
        from Axon.LikeFile import likefile, background
        background(zap=True).start()
        time.sleep(0.1)

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
                t = time.time()

            if self.exchange.ready(0):
                chan = self.exchange.ready(0)[0]
                D = chan._receive()
                print "pwc:- SEND", D, "TO", self.thecomponent.name, ".",".", 
                self.ce.put(*D)
                print ".","SENT"

            D = self.ce.anyReady()
            if D:
                for boxname in D:
                    D = self.ce.get(boxname)
                    self.channel._send((D, boxname))
            yield 1
            if self.channel.closed:
                print self.channel.closed

def ProcessPipeline(*components):
    exchange = pprocess.Exchange()
    debug = False
    chans = []
    print "TESTING ME"
    for comp in components:
        A = ProcessWrapComponent( comp )
        chan = A.activate()
        chans.append( chan )
        exchange.add(chan )

    mappings = {}
    for i in xrange(len(components)-1):
         mappings[ (chans[i], "outbox") ] = (chans[i+1], "inbox")
         mappings[ (chans[i], "signal") ] = (chans[i+1], "control")

    while 1:
        for chan in exchange.ready(0):
            D = chan._receive()
            try:
                dest = mappings[ ( chan, D[1] ) ]
                dest[0]._send( (D[0], dest[1] ) )
                print "FORWARDED", D
            except KeyError:
                if debug:
                    print "WARNING: Data sent to outbox not linked to anywhere. Error?"
                    print "chan, D[1] D[0]", chan, D[1], repr(D[0])
                    pprint.pprint( mappings )

        time.sleep(0.1)

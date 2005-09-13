#!/usr/bin/python
#
#
# Simple class that limits the rate that messages pass through it to at 
# maximum the number of messages specified. Does not enforce a minimum
# frame rate.
#
# Originally from Sketches/dirac/DiracDecoder.py 
# Probably has some minor border issues.
#

from Axon.Component import component

class RateLimit(component):
    def __init__(self, messages_per_second):
        super(RateLimit, self).__init__()
        self.mps = messages_per_second
        self.interval = 1.0/(messages_per_second*1.1)
    def main(self):
        while self.dataReady("inbox") <60:
            self.pause()
            yield 1
        c = 0
        start = 0
        last = start
        interval = self.interval # approximate rate interval
        mps = self.mps
        while 1:
            try:
                while not( self.scheduler.time - last > interval):
                   yield 1
                c = c+1
                last = self.scheduler.time
                if last - start > 1:
                    rate = (last - start)/float(c)
                    start = last
                    c = 0
                data = self.recv("inbox")
                self.send(data, "outbox")
            except IndexError:
                pass
            yield 1

#!/usr/bin/env python
# RETIRED
print """
/Sketches/filereading/VariableRateControl.py

 This file has been retired.
 It is retired because it is now part of the main code base.
 If you want to use this, you should be using Kamaelia.Util.RateFilter.VariableByteRate_RequestControl

 This file now deliberately exits to encourage you to fix your code :-)
"""
import sys
sys.exit(0)

import Axon
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

import time


class VariableRateControl(component):
    """Controls rate from a data source.
       Requests data from a data source at the specified rate in the specified chunksize
    """
   
    Inboxes = { "inbox"   : "",
                "control" : ""
              }
    Outboxes = { "outbox" : "requests for 'n' items",
                 "signal" : ""
               }
   
    def __init__(self, rate=100000, chunksize=None, chunkrate=10, allowchunkaggregation = False):
        """Initialisation
            rate = qty data per second target rate
            
            EITHER: chunksize = qty per chunk of data requested
                                Eg. if rate = 10*chunksize, 10 chunks will be sent per second
            OR:     chunkrate = chunks per second
                                Eg. if chunkrate = 10, then chunksize=rate/10
    
            allowchunkaggregation = True/False - if true, chunks requested may be aggregated
                                    if 'catching up' is necessary, otherwise multiple chunks are sent
            
            Non-integer values are permitted. Requested chunk sizes will be integer, but
            rounding errors are averaged out over time. Rounding will occur if chunksize, either
            specified, or calculated from chunkrate, is non-integer.
    
        """
        super(VariableRateControl, self).__init__()
    
        self.rate = rate
    
        if not chunksize is None:
            self.chunksize = chunksize
            chunkrate = float(rate) / float(chunksize)
    
        elif not chunkrate is None:
            self.chunksize = float(rate) / float(chunkrate)
    
        else:
            raise ValueError("chunksize or chunkrate must be specified, but not both or neither")
    
        self.timestep = 1.0 / float(chunkrate)
    
        self.aggregate = allowchunkaggregation


    def main(self):

        self.resetTiming(time.time())

        while not self.shutdown():
            now = time.time()
            
            while self.dataReady("inbox"):
                newrate = self.recv("inbox")
                self.changeRate( newrate, now )
            
            for chunk in self.getChunksToSend( now ):
                self.send( chunk, "outbox" )

            yield 1
#        print "RC done"


    def shutdown(self):
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send( msg, "signal")
                return True
        return False


    def resetTiming(self, now):
        """Resets the timing variables
            used to determine when the next time to send a request is
        """

        # primed to start sending requests immediately
        # 'toSend' accumulates the chunksize to be sent
        self.nextTime = now
        self.toSend = 0.0               
        self.lastTime = self.nextTime - self.timestep
        

    def getChunksToSend(self, now):
        """Generator. Returns the size of chunks to be requested (if any) to 'catch up' since last
            time this method was called"""

        # see if we're due/overdue to send
        if now >= self.nextTime:
            timeSinceLast = now - self.lastTime
            progress = timeSinceLast / self.timestep
            self.toSend += progress * self.chunksize
            self.lastTime = now

        # move nextTime on to the next future time to send
        while now >= self.nextTime:
            self.nextTime += self.timestep

        # send 'requests' if required
        while self.toSend >= self.chunksize:
            chunk = self.toSend           # aggregating ... send everything in one go
            if not self.aggregate:        # otherwise limit max size to self.chunksize
                chunk = min(chunk, self.chunksize)

            chunk = int(chunk)
            yield chunk
            self.toSend -= chunk

            
    def changeRate(self, newRate, now):
        """Change the rate"""
        
        # if rate is unchanged, simply return - easiest solution
        if newRate == self.rate:
            return

        # first work out how much toSend should have accumulated by now
        timeSinceLast = now - self.lastTime
        progress = timeSinceLast / self.timestep
        
        self.toSend += progress * self.chunksize

        remaining = 1.0 - (self.toSend / self.chunksize)
        
        self.lastTime = now
        self.rate     = newRate
        self.timestep = self.chunksize / float(self.rate)
        self.nextTime = now + self.timestep * remaining

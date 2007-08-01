#!/usr/bin/env python
# RETIRED
print """
/Sketches/filereading/RateControl.py:

 This file has been retired.
 It is retired because it is now part of the main code base.
 If you want to use this, you should be using Kamaelia.Util.RateFilter.ByteRate_RequestControl

 This file now deliberately exits to encourage you to fix your code :-)
"""
import sys
sys.exit(0)


import Axon
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

import time


class RateControl(component):
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
        super(RateControl, self).__init__()
    
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

        self.resetTiming()

        while not self.shutdown():
            for chunk in self.getChunksToSend():
                self.send( chunk, "outbox" )

            yield 1

    def shutdown(self):
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send( msg, "signal")
                return True
        return False


    def resetTiming(self):
        """Resets the timing variable
           used to determine when the next time to send a request is
        """
        self.nextTime = time.time()     # primed to start sending requests immediately
        self.toSend = 0.0               # 'persistent' between calls to getChunksToSend to accumulate rounding errors


    def getChunksToSend(self):
        """Generator. Returns the size of chunks to be requested (if any) to 'catch up' since last
           time this method was called"""

        # check timers
        while time.time() >= self.nextTime:
            self.toSend += self.chunksize
            self.nextTime += self.timestep

        # send 'requests' if required
        while self.toSend >= 1:
            chunk = self.toSend                # aggregating ... send everything in one go
            if not self.aggregate:        # otherwise limit max size to self.chunksize
                chunk = min(chunk, self.chunksize)

            chunk = int(chunk)
            yield chunk
            self.toSend -= chunk


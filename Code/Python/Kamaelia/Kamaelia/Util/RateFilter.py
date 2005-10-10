#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
# Simple class that limits the rate that messages pass through it to at 
# maximum the number of messages specified. Does not enforce a minimum
# frame rate.
#
# Originally from Sketches/dirac/DiracDecoder.py 
# Probably has some minor border issues.
#

#import Axon
#import Axon
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import time

class MessageRateLimit(component):
    """Class to limit the message rate per second. Buffers a number of messages before forwarding. 
       This can be reduced to a buffer size of zero"""
    def __init__(self, messages_per_second, buffer=60):
        super(MessageRateLimit, self).__init__()
        self.mps = messages_per_second
        self.interval = 1.0/(messages_per_second*1.1)
        self.buffer = buffer
    def main(self):
        while self.dataReady("inbox") <self.buffer:
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


class ByteRate_RequestControl(component):
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
        super(ByteRate_RequestControl, self).__init__()
    
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
        self.nextTime = time.time()  # primed to start sending requests immediately
        self.toSend = 0.0                    # 'persistent' between calls to getChunksToSend to accumulate rounding errors


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




class VariableByteRate_RequestControl(component):
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
        super(VariableByteRate_RequestControl, self).__init__()
    
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

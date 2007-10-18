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
"""\
These components limit the rate of data flow, either by buffering or by taking
charge and requesting data at a given rate.

=====================
Message Rate limiting
=====================

This component buffers incoming messages and limits the rate at which they are
sent on.



Example Usage
-------------
Regulating video to a constant framerate, buffering 2 seconds of data before
starting to emit frames::

    Pipeline( RateControlledFileReader(...),
              DiracDecoder(),
              MessageRateLimit(messages_per_second=framerate, buffer=2*framerate),
              VideoOverlay(),
            ).activate()



How does it work?
-----------------

Data items sent to this component's "inbox" inbox are buffered. Once the buffer
is full, the component starts to emit items at the specified rate to its
"outbox" outbox.

If there is a shortage of data in the buffer, then the specified rate of output
will, obviously, not be sustained. Items will be output when they are available.

The specified rate serves as a ceiling limit - items will never be emitted
faster than that rate, though they may be emitted slower.

Make sure you choose a sufficient buffer size to handle any expected
jitter/temporary shortages of data.

If a producerFinished or shutdownMicroprocess message is received on the
components' "control" inbox, it is sent on out of the "signal" outbox. The
component will then immediately terminate.



============
Rate Control
============

These components control the rate of a system by requesting data at a given
rate. The 'variable' version allows this rate to the changed whilst running.



Example Usage
-------------
            
Reading from a file at a fixed rate::

    Graphline( ctrl   = ByteRate_RequestControl(rate=1000, chunksize=32),
               reader = PromptedFileReader(filename="myfile", readmode="bytes"),
               linkages = {
                    ("ctrl", "outbox") : ("reader","inbox"),
                    ("reader", "outbox") : ("self", "outbox"),
    
                    ("self", "control") : ("reader", "control"),
                    ("reader", "signal") : ("ctrl", "control"),
                    ("ctrl, "signal") : ("self", "signal"),
                  }

Note that the "signal"-"control" path goes in the opposite direction so that
when the file is finished reading, the ByteRate_RequestControl component
receives a shutdown message.


Reading from a file at a varying rate (send new rates to the "inbox" inbox)::

    Graphline( ctrl   = VariableByteRate_RequestControl(rate=1000, chunksize=32),
               reader = PromptedFileReader(filename="myfile", readmode="bytes"),
               linkages = {
                      ("self", "inbox") : ("ctrl", "inbox"),
                      ("ctrl", "outbox") : ("reader","inbox"),
                      ("reader", "outbox") : ("self", "outbox"),
    
                      ("self", "control") : ("reader", "control"),
                      ("reader", "signal") : ("ctrl", "control"),
                      ("ctrl, "signal") : ("self", "signal"),
                  }
             ).activate()

Note that the "signal"-"control" path goes in the opposite direction so that
when the file is finished reading, the VariableByteRate_RequestControl component
receives a shutdown message.



How does it work?
-----------------

These components emit from their "outbox" outboxes, requests for data at the
specified rate. Each request is an integer specifying the number of items.

Rates are in no particular units (eg. bitrate, framerate) - you can use it for
whatever purpose you wish. Just ensure your values fit the units you are working
in.

At initialisation, you specify not only the rate, but also the chunk size or
chunk rate. For example, a rate of 12 and chunksize of 4 will result in 3
requests per second, each for 4 items. Conversely, specifying a rate of 12 and
a chunkrate of 2 will result in 2 requests per second, each for 6 items.

The rate and chunk size or chunk rate you specify does not have to be integer or
divide into integers. For example, you can specify a rate of 10 and a chunksize
of 3. Requests will then be emitted every 0.3 seconds, each for 3 items.

When requests are emitted, they will always be for an integer number of items.
Rounding errors are averaged out over time, and should not accumulate. Rounding
will occur if chunksize, either specified, or calculated from chunkrate, is
non-integer.

At initialisation, you can also specify that chunk 'aggregation' is permitted.
If permitted, then the component can choose to exceed the specified chunksize.
For example if, for some reason, the component gets behind, it might aggregate
two requests together - the next request will be for twice as many items.

Another example would be if you, for example, specify a rate of 100 and
chunkrate of 3. The 3 requests emitted every second will then be for 33, 33 and
34 items.

The VariableByteRate_RequestControl component allows the rate to be changed
on-the-fly. Send a new rate to the component's "inbox" inbox and it will be
adopted immediately. You cannot change the chunkrate or chunksize.

The new rate is adopted at the instant it is received. There will be no glitches
in the apparent rate of requests due to your changing the rate.

If a producerFinished or shutdownMicroprocess message is received on the
components' "control" inbox, it is sent on out of the "signal" outbox. The
component will then immediately terminate.



========================
Flow limiting by request
========================

This component buffers incoming data and emits it one item at a time, whenever
a "NEXT" request is received.



Example Usage
-------------

An app that reads data items from a file, then does something with then one at a
time when the user clicks a visual button in pygame::

    Graphline( source   = RateControlledFileReader(..., readmode="lines"),
               limiter  = OnDemandLimit(),
               trigger  = Button(caption="Click for next",msg="NEXT"),
               dest     = consumer(...),
               linkages = {
                       ("source", "outbox") : ("limiter", "inbox"),
                       ("limiter", "outbox") : ("dest", "inbox"),
                       ("trigger", "outbox") : ("limiter", "slidecontrol")
                   }
             ).activate()



How does it work?
-----------------

Data items sent to the component's "inbox" inbox are buffered in a queue.
Whenever a "NEXT" message is received on the component's "slidecontrol" inbox,
an item is taken out of the queue and sent out of the "outbox" outbox.

Items come out in the same order they go in.

If a "NEXT" message is received but there are no items waiting in the queue, the
"NEXT" message is discarded and nothing is emitted.

If a producerFinished message is received on the components' "control" inbox, it
is sent on out of the "signal" outbox. The component will then immediately
terminate.
"""


from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import time

#
# Simple class that limits the rate that messages pass through it to at 
# maximum the number of messages specified. Does not enforce a minimum
# frame rate.
#
# Originally from Sketches/dirac/DiracDecoder.py 
# Probably has some minor border issues.
#

class MessageRateLimit(component):
    """\
    MessageRateLimit(messages_per_second[, buffer]) -> new MessageRateLimit component.

    Buffers messages and outputs them at a rate limited by the specified rate
    once the buffer is full.

    Keyword arguments:
    
    - messages_per_second  -- maximum output rate
    - buffer               -- size of buffer (0 or greater) (default=60)
    """

    Inboxes = { "inbox"   : "Incoming items/messages",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Items/messages limited to specified maximum output rate",
                 "signal" : "NOT USED",
               }
    hardlimit = 0
    def __init__(self, messages_per_second, buffer=60, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(MessageRateLimit, self).__init__(**argd)
        self.mps = messages_per_second
        self.interval = 1.0/(messages_per_second*1.1)
        self.buffer = buffer

        
    def main(self):
        """Main loop."""
        while self.dataReady("inbox") <self.buffer:
            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                    return
            self.pause()
            yield 1
        c = 0
        start = 0
        last = start
        interval = self.interval # approximate rate interval
        mps = self.mps
        if self.hardlimit:
            self.setInboxSize("inbox", self.hardlimit)
        while 1:
            try:
                while not( self.scheduler.time - last > interval):
                    while self.dataReady("control"):
                        msg = self.recv("control")
                        self.send(msg,"signal")
                        if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                            return
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
    """\
    ByteRate_RequestControl([rate][,chunksize][,chunkrate][,allowchunkaggregation]) -> new ByteRate_RequestControl component.

    Controls rate of a data source by, at a controlled rate, emitting
    integers saying how much data to emit.

    Keyword arguments:
    
    - rate                   -- qty of data items per second (default=100000)
    - chunksize              -- None or qty of items per 'chunk' (default=None)
    - chunkrate              -- None or number of chunks per second (default=10)
    - allowchunkaggregation  -- if True, chunksize will be enlarged if 'catching up' is necessary (default=False)

    Specify either chunksize or chunkrate, but not both.
    """
   
    Inboxes = { "inbox"   : "NOT USED",
                "control" : "Shutdown signalling"
              }
    Outboxes = { "outbox" : "requests for 'n' items",
                 "signal" : "Shutdown signalling"
               }
   
    def __init__(self, rate=100000, chunksize=None, chunkrate=None, allowchunkaggregation = False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ByteRate_RequestControl, self).__init__()
    
        self.rate = rate
        
        if chunksize is None and chunkrate is None:
            chunksize=max(1,rate/1000)               # a sensible-ish default
    
        if not chunksize is None:
            self.chunksize = chunksize
            chunkrate = float(rate) / float(chunksize)
    
        elif not chunkrate is None:
            self.chunksize = float(rate) / float(chunkrate)
    
        else:
            raise ValueError("chunksize or chunkrate must be specified, but not both or neither")
            
        if self.chunksize < 1.0:
            raise ValueError("chunksize cannot be less than 1, specify a sensible chunkrate or chunksize")
    
        self.timestep = 1.0 / float(chunkrate)
    
        self.aggregate = allowchunkaggregation


    def main(self):
        """Main loop."""

        self.resetTiming()

        while not self.shutdown():
            for chunk in self.getChunksToSend():
                self.send( chunk, "outbox" )

            yield 1

    def shutdown(self):
        """Returns True if shutdown message received."""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send( msg, "signal")
                return True
        return False


    def resetTiming(self):
        """\
        Resets the timing variable used to determine when the next time to send
        a request is.
        """
        self.nextTime = time.time()  # primed to start sending requests immediately
        self.toSend = 0.0                    # 'persistent' between calls to getChunksToSend to accumulate rounding errors


    def getChunksToSend(self):
        """\
        Generator. Returns the size of chunks to be requested (if any) to
        'catch up' since last time this method was called.
        """

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
    """\
    ByteRate_RequestControl([rate][,chunksize][,chunkrate][,allowchunkaggregation]) -> new ByteRate_RequestControl component.

    Controls rate of a data source by, at a controlled rate, emitting
    integers saying how much data to emit. Rate can be changed at runtime.

    Keyword arguments:
    - rate                   -- qty of data items per second (default=100000)
    - chunksize              -- None or qty of items per 'chunk' (default=None)
    - chunkrate              -- None or number of chunks per second (default=10)
    - allowchunkaggregation  -- if True, chunksize will be enlarged if 'catching up' is necessary (default=False)

    Specify either chunksize or chunkrate, but not both.
    """
   
    Inboxes = { "inbox"   : "New rate",
                "control" : "Shutdown signalling"
              }
    Outboxes = { "outbox" : "requests for 'n' items",
                 "signal" : "Shutdown signalling"
               }
   
    def __init__(self, rate=100000, chunksize=None, chunkrate=10, allowchunkaggregation = False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
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
        """Main loop."""
        self.resetTiming(time.time())

        while not self.shutdown():
            now = time.time()
            
            while self.dataReady("inbox"):
                newrate = self.recv("inbox")
                self.changeRate( newrate, now )
            
            for chunk in self.getChunksToSend( now ):
                self.send( chunk, "outbox" )

            yield 1


    def shutdown(self):
        """Returns True if shutdown message received."""
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send( msg, "signal")
                return True
        return False


    def resetTiming(self, now):
        """\
        Resets the timing variable used to determine when the next time to send
        a request is.
        """

        # primed to start sending requests immediately
        # 'toSend' accumulates the chunksize to be sent
        self.nextTime = now
        self.toSend = 0.0               
        self.lastTime = self.nextTime - self.timestep
        

    def getChunksToSend(self, now):
        """\
        Generator. Returns the size of chunks to be requested (if any) to
        'catch up' since last time this method was called.
        """

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
        """\
        Change the rate.

        Guaranteed to not cause a glitch in the rate of output.
        """
        
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


        
        
class OnDemandLimit(component):
    """\
    OnDemandLimit() -> new OnDemandLimit component.

    A component that receives data items, but only emits them on demand, one at
    a time, when "NEXT" messages are received on the "slidecontrol" inbox.
    """
            
    Inboxes = { "inbox"        : "Data items to be passed on, on demand.",
                "control"      : "Shutdown signalling",
                "slidecontrol" : "'NEXT' requests to emit a data item.",
              }

    Outboxes = { "outbox" : "Data items, when requested.",
                 "signal" : "Shutdown signalling",
               }
               
    def main(self):
        """Main loop."""
        send_queue = []
        send_data = []
        while 1:
            self.pause()
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                send_queue.append(data)
            if self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data, Axon.Ipc.producerFinished):
                    self.send(data, "signal") # pass on the shutdown
                    return
            while self.dataReady("slidecontrol"):
                data = self.recv("slidecontrol")
                if data == "NEXT":
                    send_data.append(True)
            if len(send_data)>0:
                try:
                    data = send_queue[0]
                    del send_queue[0]
                    self.send(data, "outbox")
                    del send_data[0]
                except IndexError:
                    pass
            yield 1

__kamaelia_components__  = ( MessageRateLimit, ByteRate_RequestControl, VariableByteRate_RequestControl, OnDemandLimit, )

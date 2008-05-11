#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
======================================
Filter items out that are not in range
======================================

RangeFilter passes through items received on its "inbox" inbox where item[0]
lies within one or more of a specfied set of ranges of value. Items that don't
match this are discarded.



Example Usage
-------------

Reading all video frames from a YUV4MPEG format video file, but only passing on
video frames 25-49 and 100-199 inclusive further along the pipeline::

    Pipeline( RateControlledFileReader("myvideo.yuv4mpeg",readmode="bytes"),
              YUV4MPEGToFrame(),
              TagWithSequenceNumber(),
              RangeFilter(ranges=[ (25,49), (100,199) ]),
              ...
            ).run()



Behaviour
---------

At initialisation, specify a list of value ranges that RangeFilter should allow.
The list should be of the form::
    
    [ (low,high), (low,high), (low, high), ... ]
    
The ranges specified are inclusive.

Send an item to the "inbox" inbox of the form (value, ....). If the value 
matches one or more of the ranges specified, then the whole item (including the
value) will immediately be sent on out of the "outbox" outbox.

RangeFilter can therefore be used to select slices through sequence numbered or
timestamped data.

If the size limited inbox is full, this component will pause until it is able
to send out the data,.

If a producerFinished message is received on the "control" inbox, this component
will complete parsing any data pending in its inbox, and finish sending any
resulting data to its outbox. It will then send the producerFinished message on
out of its "signal" outbox and terminate.

If a shutdownMicroprocess message is received on the "control" inbox, this
component will immediately send it on out of its "signal" outbox and immediately
terminate. It will not complete processing, or sending on any pending data.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class RangeFilter(component):
    """\
    RangeFilter(ranges) -> new RangeFilter component.
    
    Filters out items of the form (value, ...) not within at least one of a
    specified value set of range. Items within range are passed through.
    
    Keyword arguments::
        
    - ranges  -- list of (low,high) pairs representing ranges of value. Ranges are inclusive.
    """
    
    Outboxes = { "outbox" : "items in range",
                 "signal" : "Shutdown signalling"
               }

    def __init__(self, ranges):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(RangeFilter,self).__init__()
        self.ranges=ranges

    def inRange(self,index):
        """\
        Returns one of the ranges that the specified index falls within, 
        otherwise returns None.
        """
        for (start,end) in self.ranges:
            if index>=start and index<=end:
                return (start,end)
        return None

    def main(self):
        """Main loop"""
        self.shutdownMsg = None
        try:
            while 1:
                while self.dataReady("inbox"):
                    item = self.recv("inbox")
                    index = item[0]
                    if self.inRange(index):
                        for _ in self.waitSend(item,"outbox"): yield _
                    
                if self.canStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                    

        except "STOP":
            self.send(self.shutdownMsg,"signal")

    # shutdown handling

    def handleControl(self):
        """\
        Collects any new shutdown messages arriving at the "control" inbox, and
        ensures self.shutdownMsg contains the highest priority one encountered
        so far.
        """
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        """\
        Checks for any shutdown messages arriving at the "control" inbox, and
        returns true if the component should terminate when it has finished
        processing any pending data.
        """
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        """\
        Checks for any shutdown messages arriving at the "control" inbox, and
        returns true if the component should terminate immediately.
        """
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)

    # data sending

    def waitSend(self,data,boxname):
        """\
        Generator.
        
        Sends data out of the "outbox" outbox. If the destination is full
        (noSpaceInBox exception) then it waits until there is space. It keeps
        retrying until it succeeds.
        
        If the component is ordered to immediately terminate then "STOP" is
        raised as an exception.
        """
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                if self.mustStop():
                    raise "STOP"


__kamaelia_components__ = ( RangeFilter, )


if __name__=="__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    print "Only items in ranges 1-5 and 8-12 should be output...\n\n"
    
    data = [
        (0, "shouldn't pass through"),
        (1, "YES!"),
        (2, "YES!"),
        (5, "YES!"),
        (6, "shouldn't pass through"),
        
        (7, "shouldn't pass through"),
        (8, "YES!"),
        (11, "YES!"),
        (12, "YES!"),
        (13, "shouldn't pass through"),
        
        (29, "shouldn't pass through"),
        (3, "YES!"),
    ]
    
    Pipeline( DataSource( data ),
              RangeFilter( [ (1,5), (8,12) ] ),
              ConsoleEchoer(),
            ).run()

    print
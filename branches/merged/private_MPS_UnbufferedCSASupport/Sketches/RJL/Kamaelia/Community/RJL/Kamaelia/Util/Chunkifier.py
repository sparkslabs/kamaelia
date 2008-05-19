#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=========================
Chunkifier
=========================

A component that fixes the message size of an input stream to a given value,
outputting blocks of that size when sufficient input has accumulated. This
component's input is stream orientated - all messages received are
concatenated to the interal buffer without divisions.

Example Usage
-------------

Chunkifying a console reader::

pipeline(
    ConsoleReader(eol=""),
    Chunkifier(20),
    ConsoleEchoer()
).run()

How does it work?
-----------------

Messages received on the "inbox" are buffered until at least N bytes have
been collected. A message containing those first N bytes is sent out
"outbox". A CharacterFIFO object is used to do this in linear time.

The usual sending of a producerFinished/shutdown to the "control"
inbox will shut it down.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

import string

class CharacterFIFO(object):
    """An efficient character queue type"""
    def __init__(self):
        self.queuearray = []
        self.length = 0
        self.startboundary = 0
        
    def push(self, text):
        self.queuearray.append(text)
        self.length += len(text)
        
    def __len__(self):
        return self.length
        
    def poplength(self, length):
        if len(self) < length:
            raise IndexError
        else:
            thischunk = []
            sizeneeded = length
            while 1:
                chunk = self.queuearray[0]
                sizeneeded -= len(chunk) - self.startboundary
                
                if sizeneeded < 0: # new start boundary in the middle of this chunk
                    thischunk.append(chunk[self.startboundary:len(chunk) + sizeneeded])
                    self.startboundary = len(chunk) + sizeneeded
                else: # this chunk is completely within the requested string
                    if self.startboundary > 0:
                        thischunk.append(chunk[self.startboundary:])
                    else:
                        thischunk.append(chunk)
                    
                    self.queuearray.pop(0)
                    self.startboundary = 0
                    
                if sizeneeded <= 0:
                    break

            self.length -= length
            return string.join(thischunk, "")
    
class Chunkifier(component):
    """\
    Chunkifier([chunksize]) -> new Chunkifier component.
    
    Flow controller - collects incoming data and outputs it only as quanta of
    a given length in bytes (chunksize), unless the input stream ends (producerFinished). 
    
    Keyword arguments:
    - chunksize  -- Chunk size in bytes
    """
    
    Inboxes = { "inbox" : "Data stream to be split into chunks",
                "control": "UNUSED" }
    Outboxes = { "outbox" : "Each message is a chunk",
                "signal": "UNUSED" }

    def __init__(self, chunksize = 1048576, nodelay = False):
        super(Chunkifier, self).__init__()
        self.forwardqueue = CharacterFIFO()
        self.chunksize = chunksize
        self.nodelay = nodelay
    
    def sendPartialChunk(self):
        if len(self.forwardqueue) > 0:
            self.send(self.forwardqueue.poplength(len(self.forwardqueue)), "outbox")
    
    def sendChunk(self):
        self.send(self.forwardqueue.poplength(self.chunksize), "outbox")

    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                self.forwardqueue.push(msg)
            
            while len(self.forwardqueue) >= self.chunksize:
                self.sendChunk()
                
            if self.nodelay:
                self.sendPartialChunk()
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    self.sendPartialChunk()
                    self.send(msg, "signal")
                    return
                elif isinstance(msg, shutdown):
                    self.send(msg, "signal")
                    return
            self.pause()

__kamaelia_components__  = ( Chunkifier, )

if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader

    pipeline(
        ConsoleReader(eol=""),
        Chunkifier(20),
        ConsoleEchoer()
    ).run()

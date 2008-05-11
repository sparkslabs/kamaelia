#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=====================================================
Buffering of data items until requested one at a time
=====================================================

PromptedTurnstile buffers items received, then sends them out one at a time in
response to requests, first-in first-out style.



Example Usage
-------------

Displaying a script from a file, one line at a time, when a pygame button is
clicked::

    Graphline(
        SOURCE = RateControlledFileReader("script.txt",readmode="lines", ...),
        GATE   = PromptedTurnstile(),
        SINK   = ConsoleEchoer(),
        NEXT   = Button(label="Click for next line of script"),
        linkages = {
            ("SOURCE", "outbox") : ("GATE", "inbox"),
            ("GATE",   "outbox") : ("SINK", "inbox"),
            ("NEXT",   "outbox") : ("GATE", "next"),
            
            ("SOURCE", "signal") : ("GATE", "control"),
            ("GATE",   "signal") : ("SINK", "control"),
            ("SINK",   "signal") : ("NEXT", "control"),
            }
        )



Behaviour
---------

Send items to the "inbox" inbox and PromptedTurnstile will buffer them.

Send anything to the "next" inbox and the oldest buffered item will be sent out
of the "outbox" outbox.

If there is a backlog of "next" requests (because there is nothing left in the
buffer) those items will be sent out as soon as they arrive. There is no need
to send another "next" request.

Send a producerFinished message to the "control" inbox to tell PromptedTurnstile
that there will be no more data. When prompted turnstile then receives a "next"
request and has nothing left in its buffer, it will send a producerFinised()
message to its "signal" outbox and immediately terminate.

If a shutdownMicroprocess message is received on the "control" inbox. It is
immediately sent on out of the "signal" outbox and the component then
immediately terminates.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class PromptedTurnstile(component):
    """\
    PromptedTurnstile() -> new PromptedTurnstile component.
    
    Buffers all items sent to its "inbox" inbox, and only sends them out, one at
    a time when requested.
    """
                    
    Inboxes = { "inbox" : "Data items",
                "next"  : "Requests to send out items",
                "control" : "Shutdown signalling"
              }
              
    Outboxes = { "outbox" : "Data items",
                 "signal" : "Shutdown signalling",
               }
                    
    def main(self):
        """Main loop"""
        noMore = False
        queue = []
        backlog = 0
        
        # while there is stuff in the queue or we've not yet been asked to stop
        while queue or not noMore:
            if not self.anyReady():
                self.pause()
                yield 1
            
            while self.dataReady("next"):
                self.recv("next")
                backlog += 1
                
            while self.dataReady("inbox"):
                queue.append(self.recv("inbox"))
                
            while queue and backlog:
                self.send(queue.pop(0), "outbox")
                backlog -= 1
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    shutdownMsg = msg
                    noMore = True
                    break
                elif isinstance(msg, shutdownMicroproces):
                    self.send(msg, "signal")
                    return
                else:
                    self.send(msg, "signal")
        
        yield 1
        # ok, we've kinda finished, now, if it was a producerFinished, then we'll
        # wait for there to be demands for another item to be sent out (eg. there
        # is a backlog already, or we receive a new "next" request)
        #
        # but if we get a shutdownmicroprocess we'll terminate immediately anyway
        while backlog == 0:
            while not self.dataReady("next"):
                while self.dataReady("control"):
                    msg = self.recv("control")
                    if isinstance(msg, shutdownMicroprocess):
                        self.send(msg, "signal")
                        return
                self.pause()
                yield 1
            self.recv("next")
            backlog -= 1
                
        self.send(shutdownMsg, "signal")


__kamaelia_components__ = ( PromptedTurnstile, )

#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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

This is useful for controlling or limiting the rate of flow of data.



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

Send items to the "inbox" inbox where they will queue up. Then each time you
send anything to the "next" inbox; one item will be taken from the queue and
forwarded out of the "outbox" outbox.

Think of it like a turnstile gate with people queuing up for it. Each message
sent to the "next" inbox is a signal to let one person through the turnstile.

This component supports sending data out of its outbox to a size limited inbox.
If the size limited inbox is full, this component will pause until it is able
to send out the data. Data will not be consumed from the inbox if this component
is waiting to send to the outbox.

If there is a backlog of "next" requests (because there is nothing left in the
buffer) those items will be sent out as soon as they arrive. There is no need
to send another "next" request.

Send a producerFinished message to the "control" inbox to tell PromptedTurnstile
that there will be no more data. When prompted turnstile then receives a "next"
request and has nothing left queued, it will send a producerFinised()
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

    def checkShutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg
                self.mustStop=True
                self.canStop=True
            elif isinstance(msg, producerFinished):
                if not isinstance(msg, shutdownMicroprocess):
                    self.shutdownMsg = msg
                    self.canStop=True
        return self.canStop, self.mustStop
                
               
    def main(self):
        self.shutdownMsg = None
        self.canStop = False
        self.mustStop = False

        try:
            while 1:
    
                while self.dataReady("inbox"):
                    canStop, mustStop = self.checkShutdown()
                    if mustStop:
                        raise UserWarning("STOP")

                    # ok, so there is data waiting to be emitted, so now we must wait for the 'next' signal
                    while not self.dataReady("next"):
                        canStop, mustStop = self.checkShutdown()
                        if mustStop:
                            raise UserWarning("STOP")
                        self.pause()
                        yield 1
                    self.recv("next")
    
                    data = self.recv("inbox")
                    while 1:
                        try:
                            self.send(data,"outbox")
                            break
                        except noSpaceInBox:
                            canStop, mustStop = self.checkShutdown()
                            if mustStop:
                                raise UserWarning( "STOP")
                            self.pause()
                            yield 1
    
                canStop, mustStop = self.checkShutdown()
                if canStop:
                    raise UserWarning( "STOP")

                if not self.dataReady("inbox") and not self.dataReady("control"):
                    self.pause()
                    
                yield 1
            
        except UserWarning:
            if self.shutdownMsg:
                self.send(self.shutdownMsg,"signal")
            else:
                self.send(producerFinished(),"signal")
            return
                        
        self.send(producerFinished(),"signal")


__kamaelia_components__ = ( PromptedTurnstile, )

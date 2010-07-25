#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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



class PromptedBlockingTurnstile(component):
    
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
                if not isinstance(self.shutdownMsg, shutdownMicroprocess):
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
                        raise "STOP"

                    # ok, so there is data waiting to be emitted, so now we must wait for the 'next' signal
                    while not self.dataReady("next"):
                        canStop, mustStop = self.checkShutdown()
                        if mustStop:
                            raise "STOP"
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
                                raise "STOP"
                            self.pause()
                            yield 1
    
                canStop, mustStop = self.checkShutdown()
                if canStop or mustStop:
                    raise "STOP"

                if not self.dataReady("inbox") and not self.dataReady("control"):
                    self.pause()
                    
                yield 1
            
        except "STOP":
            if self.shutdownMsg:
                self.send(self.shutdownMsg,"signal")
            else:
                self.send(producerFinished(),"signal")
            return
                        
        self.send(producerFinished(),"signal")

        
__kamaelia_components__ = ( PromptedTurnstile, PromptedBlockingTurnstile, )

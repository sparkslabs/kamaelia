#!/usr/bin/env python5~
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
========================
Send stuff to two places
========================

Splits a data source sending it to two destinations. Forwards both things sent
to its "inbox" inbox and "control" inboxes, so shutdown messages propogate
through this splitter. Fully supports delivery to size limited inboxes.



Example Usage
-------------

Send from a data source to two destinations. Do this for both the inbox->outbox
path and the signal->control paths, so both destinations receive shutdown
messages when the data source finishes::

    Graphline( SOURCE = MyDataSource(),
               SPLIT  = TwoWaySplitter(),
               DEST1  = MyDataSink1(),
               DEST2  = MyDataSink2(),
               linkages = {
                   ("SOURCE", "outbox") : ("SPLIT", "inbox"),
                   ("SOURCE", "signal") : ("SPLIT", "control")
                       
                   ("SPLIT", "outbox") : ("DEST1", "inbox"),
                   ("SPLIT", "signal") : ("DEST1", "control"),

                   ("SPLIT", "outbox2") : ("DEST1", "inbox"),
                   ("SPLIT", "signal2") : ("DEST1", "control"),
               }
             ).run()



Behaviour
---------

Send a message to the "inbox" inbox of this component and it will be sent on out
of the "outbox" and "outbox2" outboxes.

This component supports sending to a size limited inbox. If the size limited
inbox is full, this component will pause until it is able to send out the data.

Send a message to the "control" inbox of this component and it will be sent on
out of the "signal" and "signal2" outboxes. If the message is a
shutdownMicroprocess message then this component will also terminate
immediately. If it is a producerFinished message then this component will finish
sending any messages still waiting at its "inbox" inbox, then immediately
terminate.

"""

import Axon
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess

class TwoWaySplitter(Axon.Component.component):
    """\
    TwoWaySplitter() -> new TwoWaySplitter component
    
    Anything sent to the "inbox" or "control" inboxes is sent on out of the
    "outbox" and "outbox2" or "signal" and "signal2" outboxes respectively.
    """
    Inboxes = { "inbox"   : "Message to be sent to the 'outbox' and 'outbox2' outboxes",
                "control" : "Shutdown signalling (also sent to the 'signal' and 'signal2' outboxes",
              }
    
    Outboxes = { "outbox"  : "Messages sent to the 'inbox' inbox",
                 "outbox2" : "Messages sent to the 'inbox' inbox",
                 "signal"  : "Messages sent to the 'control' inbox",
                 "signal2" : "Messages sent to the 'control' inbox",
               }

    def main(self):
        self.shutdownMsg = None

        try:
            while 1:
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    for _ in self.waitSendMultiple((data,"outbox"),
                                                   (data,"outbox2")):
                        yield _

                if self.canStop():
                    raise UserWarning("STOP")

                self.pause()
                yield 1

        except UserWarning:
            self.send(self.shutdownMsg,"signal")
            self.send(self.shutdownMsg,"signal2")

            
    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
    
    def waitSendMultiple(self,*things):
        things = list(things)
        while 1:
            # try to send everything, removing from the list each item we successfull send
            i=0
            while i<len(things):
                try:
                    data,boxname = things[0]
                    self.send(data,boxname)
                    del things[0]
                except noSpaceInBox:
                    i=i+2     # only increment if we couldn't send (and delete the item)

            # if nothing left to send, we're done
            if len(things)==0:
                return
            else:
                # otherwise we need to wait to be unpaused
                if self.mustStop():
                    raise UserWarning( "STOP")
    
                self.pause()
                yield 1


__kamaelia_components__ = ( TwoWaySplitter, )


if __name__ == "__main__":
    from Kamaelia.Experimental.Chassis import Graphline,Pipeline
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.RateFilter import MessageRateLimit
    from Kamaelia.Util.Console import ConsoleEchoer

    Graphline(
        SRC = DataSource([str(i)+"\n" for i in range(0,100)]),
        SPLIT = TwoWaySplitter(),
        DST1 = Pipeline(10, MessageRateLimit(10,5),
                           ConsoleEchoer(),
                       ),
        DST2 = Pipeline(10, MessageRateLimit(20,5),
                           ConsoleEchoer(),
                       ),
        linkages = {
            ("SRC","outbox") : ("SPLIT","inbox"),
            ("SPLIT","outbox") : ("DST1","inbox"),
            ("SPLIT","outbox2") : ("DST2","inbox"),

            ("SRC","signal") : ("SPLIT","control"),
            ("SPLIT","signal") : ("DST1","control"),
            ("SPLIT","signal2") : ("DST2","control"),
        },
        boxsizes = {
            ("SPLIT","inbox") : 999,
        }
        ).run()
        
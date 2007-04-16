#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import Axon
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess

class TwoWaySplitter(Axon.Component.component):
    Outboxes = { "outbox"  : "",
                 "outbox2" : "",
                 "signal"  : "",
                 "signal2" : "",
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
                    raise "STOP"

                self.pause()
                yield 1

        except "STOP":
            self.send(self.shutdownMsg,"signal")
            self.send(self.shutdownMsg,"signal2")
            print "done"

            
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
                    raise "STOP"
    
                self.pause()
                yield 1


__kamaelia_components__ = ( TwoWaySplitter, )


if __name__ == "__main__":
    from Chassis import Graphline,Pipeline
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
        
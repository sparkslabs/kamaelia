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

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel

class OneShot(component):
    def __init__(self, msg=None):
        super(OneShot, self).__init__()
        self.msg = msg
    def main(self):
        self.send(self.msg,"outbox")
        yield 1
        self.send(producerFinished(self),"signal")


class TagWithSequenceNumber(component):
    def main(self):
        index = 0
        while 1:
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                self.send( (index,msg), "outbox")
                index+=1
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    self.send(msg, "signal")
                    return
                
            self.pause()
            yield 1


def InboxControlledCarousel(factory):
    return Graphline( CAROUSEL = Carousel( factory ),
                      linkages = {
                          ("", "inbox")   : ("CAROUSEL", "next"),
                          ("", "data_inbox") : ("CAROUSEL", "inbox"),
                          ("", "control") : ("CAROUSEL", "control"),
                          ("CAROUSEL", "outbox") : ("", "outbox"),
                          ("CAROUSEL", "signal") : ("", "signal"),
                      }
                    )

class PromptedTurnstile(component):
                    
    Inboxes = { "inbox" : "Data items",
                "next"  : "Requests to fetch items",
                "control" : "shutdown signalling"
              }
                    
    def main(self):
        noMore = False
        queue = []
        backlog = 0
        
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
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    shutdownMsg = msg
                    noMore = True
                    break
                else:
                    self.send(msg, "signal")
        
        yield 1
        # ok, we've kinda finished, now, if it was a producerFinished, then we'll
        # wait for the next 'next' request before admitting termination!
        # but if we get a shutdownmicroprocess we'll terminate immediately anyway
        if isinstance(msg, producerFinished):
            while not self.dataReady("next"):
                while self.dataReady("control"):
                    msg = self.recv("control")
                    if isinstance(msg, shutdownMicroprocess):
                        self.send(msg, "signal")
                        return
                self.pause()
                yield 1
            self.recv("next")
                
        self.send(shutdownMsg, "signal")

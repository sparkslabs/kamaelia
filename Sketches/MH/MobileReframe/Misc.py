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
                print index
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

class IgnoreUntil(component):
    def __init__(self,pattern):
        super(IgnoreUntil,self).__init__()
        self.pattern=pattern
        
    def checkShutdown(self,noNeedToWait):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,shutdownMicroprocess):
                self.shutdownMsg=msg
                raise "STOP"
            elif isinstance(msg, producerFinished):
                if not isinstance(self.shutdownMsg, shutdownMicroprocess):
                    self.shutdownMsg=msg
            else:
                pass
        if self.shutdownMsg and noNeedToWait:
            raise "STOP"
        
        
    def main(self):
        found=False
        buffer=""
        pos=-1
        i=0
        self.shutdownMsg=None
        
        try:
            while i<len(self.pattern):
                if pos==len(buffer)-1:
                    while not self.dataReady("inbox"):
                        self.checkShutdown(noNeedToWait=True)
                        self.pause()
                        yield 1
                    buffer = self.recv("inbox")
                    pos=-1
                index = buffer.find(self.pattern[i],pos+1)
                if index<=-1:
                    buffer=""
                    i=0
                elif index==pos+1 or i==0:
                    i+=1
                    pos=index
                else:
                    i=0
                    
            self.send(self.pattern + buffer[pos+1:],"outbox")
            
            while 1:
                while self.dataReady("inbox"):
                    buffer = self.recv("inbox")
                    self.send(buffer,"outbox")
                self.checkShutdown(noNeedToWait=True)
                self.pause()
                yield 1
        
        except "STOP":
            pass
        
        self.send(self.shutdownMsg,"signal")


class FirstOnly(component):
    def main(self):
        while not self.dataReady("inbox"):
            if self.dataReady("control"):
                self.send(self.recv("control"),"signal")
                return
            self.pause()
            yield 1
            
        self.send(self.recv("inbox"),"outbox")
        
        while not self.dataReady("control"):
            while self.dataReady("inbox"):
                self.recv("inbox")          # absorb anything sent to me
            self.pause()
            yield 1
            
        self.send(self.recv("control"),"signal")
        
class Chunk(component):
    def __init__(self,datarate,quanta,chunkrate):
        super(Chunk,self).__init__()
        self.datarate  = datarate
        self.quanta    = quanta
        self.chunkrate = chunkrate
    def main(self):
        quantaPerChunk = float(self.datarate)/self.chunkrate/self.quanta
        
        nextChunk = quantaPerChunk
        
        buffer = ""
        while 1:
            while self.dataReady("inbox"):
                newdata=self.recv("inbox")
                buffer += newdata
                
                while len(buffer) >= (int(nextChunk)*self.quanta):
                    amount = (int(nextChunk)*self.quanta)
                    toSend = buffer[:amount]
                    buffer = buffer[amount:]
                    nextChunk = nextChunk - int(nextChunk) + quantaPerChunk
                    self.send(toSend,"outbox")
        
            while  self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                    return
                
            self.pause()
            yield 1

from Kamaelia.Internet.Selector import Selector
from Axon.Ipc import shutdown

class StopSelector(component):
    Outboxes = {"outbox":"","signal":"","selector_shutdown":""}
    def main(self):
        while not (self.dataReady("inbox") or self.dataReady("control")):
            self.pause()
            yield 1
        
        # stop the selector
        selectorService, selectorShutdownService, newSelectorService = Selector.getSelectorServices(self.tracker) # get a reference to a     
        link = self.link((self,"selector_shutdown"),selectorShutdownService)
        self.send(shutdown(),"selector_shutdown")
        self.unlink(thelinkage=link)
        
        while self.dataReady("control"):
            self.send(self.recv("control"), "signal")
            
        self.send(producerFinished(self), "signal")
        print "DONE"


class Sync(component):
    """Waits for 'n' items before sending one of them on"""
    def __init__(self, n=2):
        super(Sync,self).__init__()
        self.n=n
    def main(self):
        while 1:
            for i in range(self.n):
                while not self.dataReady("inbox"):
                    while self.dataReady("control"):
                        msg = self.recv("control")
                        self.send(msg,"signal")
                        if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                            return
                    self.pause()
                    yield 1
                data = self.recv("inbox")
            self.send(data,"outbox")

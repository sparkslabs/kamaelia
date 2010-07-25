#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# a little experiment to see if WaitComplete and reactivate behaviour can be
# implemented again in the current optimised axon and, preferably making the
# scheduler a little simpler in the process

from Axon.Ipc import WaitComplete,reactivate

class Microprocess(object):
    def __init__(self):
        super(Microprocess,self).__init__()

#     def next(self):
#         return self.__thread.next()

    def _microprocessGenerator(self,main,continuation=None):
        pc = main
        while 1:
            try:
                v = pc.next()
                if isinstance(v,WaitComplete):
                    newMain = v.args[0]
                    self.__thread = self._microprocessGenerator(newMain,self.__thread)
                    self.next = self.__thread.next
                yield v
            except StopIteration:
                if continuation:
                    self.__thread = continuation
                    self.next = self.__thread.next
                    yield 1
                    # replace this generator with the continuation
                    # this generator will not be executed
                else:
                    raise

    def main(self):
        """STUB"""
        yield 1
        return

    def activate(self, scheduler, mainmethod="main"):
        self.scheduler = scheduler
        main = self.__getattribute__(mainmethod)()
        self.__thread = self._microprocessGenerator(main)
        self.next = self.__thread.next
        self.scheduler.activateThread(self)
        return self

    def closeDownMicroprocess(self):
        return None
    
    def pause(self):
        self.scheduler.pauseThread(self)
        
    def unPause(self):
        self.scheduler.wakeThread(self)
        
    
    
class Scheduler(object):
    def __init__(self):
        super(Scheduler,self).__init__()
        self.runqueue = {}
        
    def activateThread(self, thread):
        self.runqueue[thread] = 1
        
    def pauseThread(self, thread):
        if thread in self.runqueue:
            self.runqueue[thread] = 0
        
    def wakeThread(self, thread):
        if thread in self.runqueue:
            self.runqueue[thread] = 1
        
    def main(self):
        while self.runqueue:
            
            for (thread,active) in self.runqueue.items():     # implicit copy of runqueue state
                if active:
                    try:
                        retval = thread.next()
                    except StopIteration:
                        del self.runqueue[thread]


class Component(Microprocess):
    def __init__(self):
        super(Component,self).__init__()
        self.inboxes = { "inbox":[], "control":[] }
        self.outboxes = { "outbox":None, "signal":None }
        
    def link(self, (src,srcbox), (dst,dstbox)):
        src.outboxes[srcbox] = (dst,dstbox)
        
    def dataReady(self,boxname):
        return len(self.inboxes[boxname])
    
    def recv(self,boxname):
        return self.inboxes[boxname].pop(0)
    
    def send(self, value, boxname):
        (dst,dstbox) = self.outboxes[boxname]
        dst.inboxes[dstbox].append(value)
        dst.unPause()
    
    
    
# --------------------------------------

import time,sys

class Source(Component):
    def waitALittle(self):
        t=time.time()
        while time.time() < t+0.5:
            yield 1
        
    def main(self):
        for i in range(10,-1,-1):
            yield WaitComplete(self.waitALittle())
                
            self.send(i,"outbox")


class Sink(Component):
    def waitForData(self):
        paused=False
        while not self.dataReady("inbox"):
            paused=True
            self.pause()
            yield 1
            assert(self.dataReady("inbox"))
        assert(paused)
            
    def main(self):
        done=False
        while not done:
            yield WaitComplete(self.waitForData())
            
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                sys.stdout.write(str(data)+"\n")
                sys.stdout.flush()
                done = data==0
                
            yield 1
            
            
scheduler = Scheduler()
            
src = Source().activate(scheduler)
dst = Sink().activate(scheduler)
src.link((src,"outbox"),(dst,"inbox"))


scheduler.main()

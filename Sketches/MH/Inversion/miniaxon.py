#!/usr/bin/env python

import Queue
import threading
import time

class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1
    def activate(self,scheduler):
        scheduler.activateMicroprocess(self)
        return self


class scheduler(microprocess):
    def __init__(self):
        super(scheduler, self).__init__()
        self.active = []
        self.newqueue = []
    def main(self): 
        while len(self.newqueue):
            self.active = self.newqueue
            self.newqueue = []
            for current in self.active:
                yield 1
                try:
                    result = current.next()
                    if result is not -1:
                        self.newqueue.append(current)
                except StopIteration:
                    pass
    def activateMicroprocess(self, someprocess, mainmethod="main"):
        microthread = someprocess.__getattribute__(mainmethod)()
        self.newqueue.append(microthread)


class component(microprocess):
    def __init__(self):
        super(component, self).__init__()
        self.boxes = { "inbox" : [], "outbox": [] }
    def send(self, value, outboxname):
        self.boxes[outboxname].append(value)
    def recv(self, inboxname):
        result = self.boxes[inboxname][0]
        del self.boxes[inboxname][0]
        return result
    def dataReady(self, inboxname):
        return len(self.boxes[inboxname])
    def link(self, src, dst):
        scomp,sbox = src
        dcomp,dbox = dst
        while len(scomp.boxes[sbox]):
            dcomp.boxes[dbox].append(scomp.boxes[sbox].pop(0))
        scomp.boxes[sbox] = dcomp.boxes[dbox]
        return (src, dst)
    def unlink( linkage ):
        ((scomp,sbox),(dcomp,dbox)) = linkage
        scomp.boxes[sbox] = []

class threadedcomponent(component):
    """Very basic threaded component, with poor thread safety"""
    def __init__(self):
        super(threadedcomponent,self).__init__()
        self.queues = {}
        self.isInbox = { "inbox":1, "outbox":0 }
        for box in self.boxes:
            self.queues[box] = Queue.Queue()
    def activate(self,scheduler):
        scheduler.activateMicroprocess(self, "_localmain")
        return self
    def send(self, value, outboxname):
        self.queues[outboxname].put(value)
    def recv(self, inboxname):
        return self.queues[inboxname].get()
    def dataReady(self, inboxname):
        return self.queues[inboxname].qsize()
    
    def _localmain(self):
        self._thread = threading.Thread(target=self.main)
        self._thread.setDaemon(True)
        self._thread.start()
        while self._thread.isAlive():
            yield 1
            for boxname in self.queues:
                if self.isInbox[boxname]:
                    while component.dataReady(self,boxname):
                        self.queues[boxname].put( component.recv(self,boxname) )
                else:
                    while not self.queues[boxname].empty():
                        component.send(self, self.queues[boxname].get(), boxname)

##  events!!!
# --------------------------------------------------

class Producer(threadedcomponent):
    def main(self):
        for i in range(10):
#            yield 1
            time.sleep(0.1)
            self.send(i,"outbox")
        self.send("DONE","outbox")

class Output(component):
    def main(self):
        done=False
        while not done:
            yield 1
            if self.dataReady("inbox"):
                msg=self.recv("inbox")
                print str(msg)
                done = msg=="DONE"

sched=scheduler()
p=Producer().activate(sched)
o=Output().activate(sched)

p.link( (p,"outbox"),(o,"inbox") )

for _ in sched.main():
    pass

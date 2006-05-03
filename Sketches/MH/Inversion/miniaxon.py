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
        self.event = threading.Event()
    def notify(self):
        self.event.set()
    def main(self): 
        while len(self.newqueue):
            self.active = self.newqueue
            self.newqueue = []
            activityCount = 0
            waitingCount = 0
            for current in self.active:
                yield 1
                try:
                    result = current.next()
                    if result is not -1:
                        activityCount +=1 
                        self.newqueue.append(current)
                        if result=="BLOCK" or "PAUSE":
                            waitingCount += 1
                except StopIteration:
                    pass
            if activityCount > 0 and waitingCount == activityCount:
                print "waiting"
                self.event.wait()
                self.event.clear()
    def activateMicroprocess(self, someprocess, mainmethod="main"):
        microthread = someprocess.__getattribute__(mainmethod)()
        self.newqueue.append(microthread)

class box(list):
    def __init__(self, notify):
        self.notify=notify
        super(box,self).__init__()
    def append(self, value):
        super(box,self).append(value)
        self.notify()

class component(microprocess):
    def __init__(self):
        super(component, self).__init__()
        self.boxes = { "inbox" : box(self.notify), "outbox": box(self.notify) }
        self.paused=False
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
        scomp.boxes[sbox] = box(self.notify)
    def notify(self):
        self.paused=False
    def pause(slf):
        self.paused=True

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
        self.scheduler = scheduler
        return self
    def send(self, value, outboxname):
        self.queues[outboxname].put(value)
        self.scheduler.notify()
    def recv(self, inboxname):
        return self.queues[inboxname].get()
    def dataReady(self, inboxname):
        return self.queues[inboxname].qsize()
    
    def _localmain(self):
        self._thread = threading.Thread(target=self.main)
        self._thread.setDaemon(True)
        self._thread.start()
        while self._thread.isAlive():
            yield "BLOCK"
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
            time.sleep(0.2)
            self.send(i,"outbox")
        self.send("DONE","outbox")

class Output(component):
    def main(self):
        done=False
        while not done:
            while self.dataReady("inbox"):
                msg=self.recv("inbox")
                print str(msg)
                done = msg=="DONE"
            yield "PAUSE"

sched=scheduler()
p=Producer().activate(sched)
o=Output().activate(sched)

p.link( (p,"outbox"),(o,"inbox") )

for _ in sched.main():
    pass

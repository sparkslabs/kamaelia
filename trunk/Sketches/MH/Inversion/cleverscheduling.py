#!/usr/bin/env python

import Queue
import threading
import time

class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1
    def activate(self, scheduler,mainmethod="main"):
        self._mprocess = self.__getattribute__(mainmethod)()
        self.scheduler = scheduler
        self.scheduler.addThread(self)
        return self
    def next(self):
        return self._mprocess.next()


class scheduler(microprocess):
    def __init__(self):
        super(scheduler, self).__init__()
        self.wakeups = Queue.Queue()
    
    def wakeThread(self,thread):
        self.wakeups.put(thread)
        
    def main(self):
        taskset = {}        # all microprocesses, whether paused or not
        newqueue = []       # currently running (non paused) microprocesses
        running = True
        while running:
            
            active = newqueue
            newqueue = []
            for current in active:
                yield 1
                try:
                    result = current.next()
                    if result =="PAUSE":
                        taskset[current] = 0
                    else:
                        newqueue.append(current)
                except StopIteration:
                    del taskset[current]
                    
            blocked = len(taskset) and not len(newqueue)
            
            # process 'wakeup' events coming from thread(s)
            while self.wakeups.qsize() or blocked:
                thread = self.wakeups.get()
                if taskset.get(thread, 0) == 0:
                    newqueue.insert(0,thread)
                taskset[thread] = 1
                blocked = False
            
            running = len(taskset)   # or len(newqueue)
                
    def addThread(self, thread):
        self.wakeThread(thread)
        
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
        self.boxes = { "inbox" : box(self.unpause), "outbox": box(self.unpause) }
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
        scomp.boxes[sbox] = box(self.unpause)
    def unpause(self):
        self.scheduler.wakeThread(self)

class threadedcomponent(component):
    """Very basic threaded component, with poor thread safety"""
    def __init__(self):
        super(threadedcomponent,self).__init__()
        self.queues = {}
        self.isInbox = { "inbox":1, "outbox":0 }
        for box in self.boxes:
            self.queues[box] = Queue.Queue()
    def activate(self,scheduler):
        return component.activate(self, scheduler, "_localmain")
    def send(self, value, outboxname):
        self.queues[outboxname].put(value)
        self.unpause()
    def recv(self, inboxname):
        return self.queues[inboxname].get()
    def dataReady(self, inboxname):
        return self.queues[inboxname].qsize()
    
    def _localmain(self):
        self._thread = threading.Thread(target=self._threadrun)
        self._thread.setDaemon(True)
        self._threadalive=True
        self._thread.start()
        running=True    
        while running:
            running = self._threadalive and self._thread.isAlive()
            for boxname in self.queues:
                if self.isInbox[boxname]:
                    while component.dataReady(self,boxname):
                        self.queues[boxname].put( component.recv(self,boxname) )
                else:
                    while not self.queues[boxname].empty():
                        component.send(self, self.queues[boxname].get(), boxname)
            if running:
                yield "PAUSE"

    def _threadrun(self):
        self.main()
        self._threadAlive=False
        self.unpause()
        
# --------------------------------------------------

class Producer(threadedcomponent):
    def main(self):
        for i in range(10):
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
                done = done or (msg == "DONE")
            if not done:
                yield "PAUSE"

sched=scheduler()
p=Producer().activate(sched)
o=Output().activate(sched)

p.link( (p,"outbox"),(o,"inbox") )

for _ in sched.main():
    pass

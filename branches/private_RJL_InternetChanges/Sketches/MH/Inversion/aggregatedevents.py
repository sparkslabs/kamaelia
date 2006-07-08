#!/usr/bin/env python

import Queue
import threading
import time

class NullScheduler(object):
    def __init__(self):
        super(NullScheduler,self).__init__()
    def sleepThread(self,thread):
        pass
    def wakeThread(self,thread):
        pass

nullscheduler = NullScheduler()

class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
        self.scheduler = nullscheduler
    def main(self):
        yield 1
    def activate(self, scheduler,mainmethod="main"):
        self._mprocess = self.__getattribute__(mainmethod)()
        self.scheduler = scheduler
        self.scheduler.addThread(self)
        return self
    def next(self):
        return self._mprocess.next()
    def pause(self):
        self.scheduler.sleepThread(self)
    def unpause(self):
        self.scheduler.wakeThread(self)
    def paused(self):
        return self.scheduler.isThreadPaused(self)

_ACTIVE = object()             # status value for active running threads
_SLEEPING = object()           # status value for sleeping threads
_GOINGTOSLEEP = object()       # status value for threads that should be put to sleep (but might still be in runqueue)

class scheduler(microprocess):
    def __init__(self):
        super(scheduler, self).__init__()
        self.taskset = {}        # all microprocesses, whether paused or not
        self.changesLock = threading.Condition()
        self.changes = {}
    
    def wakeThread(self,thread):
        self.changesLock.acquire()
        self.changes[thread] = _ACTIVE     # mark to be woken up
        self.changesLock.notify()
        self.changesLock.release()
        
    def sleepThread(self,thread):
        self.changesLock.acquire()
        self.changes[thread] = _GOINGTOSLEEP    # mark as 'put to sleep'
        self.changesLock.notify()
        self.changesLock.release()
        
    def main(self,canblock=False):
        nextrunqueue = []
        running = True
        while running:
            
            runqueue = nextrunqueue
            nextrunqueue = []
            for mprocess in runqueue:
                
                yield 1
                try:
                    if self.taskset[mprocess] == _ACTIVE:
                        result = mprocess.next()
                        nextrunqueue.append(mprocess)
                    else:
                        # mprocess might be 'going to sleep', needs to be marked as 'sleeping'
                        self.taskset[mprocess] = _SLEEPING
                except StopIteration:
                    del self.taskset[mprocess]
                    
            
            blocked = len(self.taskset)>0 and len(nextrunqueue)==0
            if blocked:
                print "----------- scheduler blocked, waiting for wakeup event -----------"
            
            # fetch latest batch of microprocess wakeup/sleep requests
            # if we're blocked and there are no requests yet, wait for some
            changes = self.fetchChanges(waitforchanges = canblock and blocked)
            
            # process the requests, updating self.taskset and nextrunqueue
            for (mprocess,newstate) in changes:
                if newstate == _ACTIVE and self.taskset.get(mprocess,_SLEEPING) == _SLEEPING:
                    print mprocess.name,"waking"
                    nextrunqueue.append(mprocess)
                self.taskset[mprocess] = newstate
                if newstate == _GOINGTOSLEEP:
                    print mprocess.name,"blocking"
            
            running = len(self.taskset)
        
    def fetchChanges(self,waitforchanges=False):
        self.changesLock.acquire()
        while waitforchanges and 0==len(self.changes):
            self.changesLock.wait()
        changes = self.changes.items()
        self.changes = {}
        self.changesLock.release()
        return changes
        
    def runThreads(self):
        for i in self.main(canblock=True):
            pass
        
    def addThread(self, thread):
        self.wakeThread(thread)
        
    def isThreadPaused(self,thread):
        return self.taskset[thread] != _ACTIVE
    
    def getCurrentMicroprocesses(self):
        return self.taskset.keys()
        
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
                self.pause()
            yield 1

    def _threadrun(self):
        self.main()
        self._threadAlive=False
        self.unpause()
        
# --------------------------------------------------

class Producer(threadedcomponent):
    def __init__(self, name,sleeptime=0.2):
        super(Producer,self).__init__()
        self.sleeptime=sleeptime
        self.name=name
    def main(self):
        for i in range(10):
            time.sleep(self.sleeptime)
            print self.name,"thread sends",i
            self.send(i,"outbox")
        self.send("DONE","outbox")

class Output(component):
    def __init__(self,name):
        super(Output,self).__init__()
        self.name=name
    def main(self):
        done=False
        while not done:
            while self.dataReady("inbox"):
                msg=self.recv("inbox")
                print self.name+" "+str(msg)
                done = done or (msg == "DONE")
            if not done:
                self.pause()
                yield 1
                print self.name+" reawoken..."

sched=scheduler()
p=Producer("P1").activate(sched)
o=Output("                   O1").activate(sched)

p.link( (p,"outbox"),(o,"inbox") )

# shouldn't affect first outputter
p2=Producer("                                    P2",0.4).activate(sched)
o2=Output("                                                         O2").activate(sched)

p.link( (p2,"outbox"),(o2,"inbox") )

sched.runThreads()

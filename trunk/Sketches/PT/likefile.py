#!/usr/bin/env python
"""
Note 1: Threadsafeness of activate().

when a component is activated, it calls the method inherited from microprocess, which calls _addThread(self)
on an appropriate scheduler. _addThread calls wakeThread, which places the request on a threadsafe queue.

"""

from Axon.Scheduler import scheduler
from Axon.AxonExceptions import noSpaceInBox
import Queue, threading, time, copy, Axon
queuelengths = 0

class dummyComponent(Axon.Component.component):
    """A dummy component. Functionality: None. Prevents the scheduler from dying immediately."""
    def main(self):
        while True:
            self.pause()
            yield 1

class schedulerThread(threading.Thread):
    """A python thread which runs a scheduler."""
    thread = None
    def __init__(self,slowmo=0):
        if schedulerThread.thread: raise "only one scheduler for now can be run!"
        schedulerThread.thread = self
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when the caller dies
    def run(self):
        dummyComponent().activate() # to keep the scheduler from exiting immediately.
        scheduler.run.runThreads(slowmo = self.slowmo)


class componentWrapper(Axon.Component.component):
    def __init__(self, childcomponent):
        super(componentWrapper, self).__init__()
        self.queuelengths = queuelengths
        self.child = childcomponent
        self.inqueues = dict() # queue for data traversing from, e.g, stdin to a component's inbox
        self.outqueues = dict()# queue for data traversing from, e.g, stdout to a component's outbox
        self.addChildren(self.child)

        # for now, these are hard-coded.
        # this means, e.g. our own outbox is linked to the child's inbox. childSink:parentSource
        self.childInboxMapping = { "inbox": "outbox", "control": "signal" }

        # this means, e.g. the child's outbox is linked to our own inbox. childSource:parentSink
        self.childOutboxMapping = { "outbox": "inbox", "signal": "control" }

        for childSink, parentSource in self.childInboxMapping.iteritems():
            self.inqueues[childSink] = Queue.Queue(self.queuelengths)
            self.link((self, parentSource),(self.child, childSink))

        for childSource, parentSink in self.childOutboxMapping.iteritems():
            self.outqueues[childSource] = Queue.Queue(self.queuelengths)
            self.link((self.child, childSource),(self, parentSink))

        # note to self: this can be slightly optimised by making self.outqueues/self.inqueues keyed by the parentSource/parentSink,
        # avoiding an extra lookup below in the box mapping iteritems()


    def main(self):
        self.child.activate()
        while True:
            for childSink, parentSource in self.childInboxMapping.iteritems():
                queue = self.inqueues[childSink]
                # to aid a lack of confusion, this is where information would traverse from stdin to a child component's inbox.
                while not queue.empty():
                    if not self.outboxes[parentSource].isFull():
                        msg = queue.get_nowait()
                        try:
                            self.send(msg, parentSource)
                        except noSpaceInBox, e:
                            raise "Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?"
                    else: # if the component's inboxes are full, do something here. Preferably not succeed.
                        break


            for childSource, parentSink in self.childOutboxMapping.iteritems():
                queue = self.outqueues[childSource]
                # to aid a lack of confusion, this is where information would traverse from a child component's outbox to stdout.
                while self.dataReady(parentSink):
                    if not queue.full():
                        msg = self.recv(parentSink)
                        queue.put_nowait(msg)
                    else: break # permit a horrible backlog to build up inside our boxes. What could go wrong?
            yield 1

class likeFile(object):
    def __init__(self, componenttowrap):
        component = componentWrapper(componenttowrap)
        self.inqueues = copy.copy(component.inqueues)
        self.outqueues = copy.copy(component.outqueues)
        # reaching into the component like this is threadsafe since it has not been activated yet, and __init__
        # runs in the current thread
        component.activate() # threadsafe, see note 1
        self.alive = True

    def get(self, boxname):
        if self.alive: 
            return self.outqueues[boxname].get()
        else: raise "shutdown was previously called!"

    def put(self, msg, boxname):
        if self.alive: self.inqueues[boxname].put_nowait(msg)
        else: raise "shutdown was previously called!"

    def shutdown(self):
        if self.alive: self.inqueues["control"].put_nowait(Axon.Ipc.shutdownMicroprocess())
        else: raise "shutdown was previously called!"
        self.alive = False

    def __del__(self):
        if self.alive: self.shutdown()


if __name__ == "__main__":
    background = schedulerThread(slowmo=0.01)
    background.start()
    from helloworld import Reverser

    p = likeFile( Reverser() ) # allegedly threadsafe
    while True:
        try: 
            p.put("hello, world", "inbox")
            time.sleep(0.5) # longer than axon's slowmo
            reversed = p.get("outbox")
            print "hello world, reversed, is:" , reversed
        except KeyboardInterrupt:
            p.shutdown()
            time.sleep(0.1)
            break
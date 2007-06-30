#!/usr/bin/env python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
=================================================
LikeFile - file-like interaction with components.
=================================================







Note 1: Threadsafeness of activate().

when a component is activated, it calls the method inherited from microprocess, which calls _addThread(self)
on an appropriate scheduler. _addThread calls wakeThread, which places the request on a threadsafe queue.

"""

from Axon.Scheduler import scheduler
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess
import Queue, threading, time, copy, Axon
queuelengths = 0


def addBox(self, names, boxMap, addBox):
        """Add an extra wrapped box"""
        if type(names) == str:
            names = (names,)
        for boxname in names:
            if boxname in boxMap:
                raise ValueError, "%s %s already exists!" % (direction, boxname)
            realboxname = addBox(boxname)
            boxMap[boxname] = realboxname

class SchedulerShutdown(Exception):
    """An exception used internally to provide a way of shutting down a thread."""
    pass

class dummyComponent(Axon.Component.component):
    """A dummy component. Functionality: None. Prevents the scheduler from dying immediately.
    Currently this object prevents the scheduler from cleanly exiting, but most components don't
    exit cleanly anyway, so that's not a problem."""
    def main(self):
        while True:
            self.pause()
            yield 1

class schedulerThread(threading.Thread):
    """A python thread which runs a scheduler."""
    lock = threading.Lock()
    def __init__(self,slowmo=0):
        if not schedulerThread.lock.acquire(False):
            raise "only one scheduler for now can be run!"
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when the caller dies
    def run(self):
        dummyComponent().activate() # to keep the scheduler from exiting immediately.
        try:
            scheduler.run.runThreads(slowmo = self.slowmo)
        except SchedulerShutdown:
            pass
        schedulerThread.lock.release()

class componentWrapperWaker(Axon.ThreadedComponent.threadedcomponent):
    """This is a companion to the component wrapper, which wakes up the component wrapper whenever
    information is pending on one of its queues, to avoid polling."""
    def __init__(self):
        super(componentWrapperWaker, self).__init__()
        self.wakeUp = threading.Event()
        # this is the Event on which we will wait.
    def main(self):
        while True:
            self.wakeUp.wait()
            # We were woken up, first thing to do is to reset the wakeUp event.
            self.wakeUp.clear()
            # Now, we send a message to the component wrapper indicating that we were woken up
            # by likefile, signalling that some data is waiting on a queue.
            # it doesn't matter what we send.
            self.send(object)


class componentWrapper(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """A component which takes a child component and connects its boxes to queues, which communicate
    with the LikeFile component."""
    def __init__(self, childcomponent, extraInboxes = None, extraOutboxes = None):
        super(componentWrapper, self).__init__()
        self.queuelengths = queuelengths
        self.child = childcomponent
        self.inQueues = dict()
        self.outQueues = dict()
        self.addChildren(self.child)
        self.commandQueue = Queue.Queue()
        
        # set up the service that will wake us up when our queues have data.
        self.wakeboxname = self.addInbox(str(id(self))) # unlikely to be a clash in names.
        self.waker = componentWrapperWaker()
        self.addChildren(self.waker)
        self.link((self.waker, "outbox"), (self, self.wakeboxname))

        # parentSource:childSink
        # used to deliver information to a wrapped component from non-kamaelionic environments.
        self.childInboxMapping = { "inbox": "outbox", "control": "signal" }
        if extraInboxes:
            addBox(extraInboxes, self.childInboxMapping, self.addOutbox)

        # childSource:parentSink
        # used to retrieve information from a kamaelia system to a non-kamaelionic environment.
        self.childOutboxMapping = { "outbox": "inbox", "signal": "control" }
        if extraOutboxes:
            addBox(extraOutoxes, self.childOutboxMapping, self.addInbox)

        # Now, we set up all the linkages between us and our child.

        # Now, add all the queues and link to the children. These are two
        # unrelated operations but they use the same dict iteration.
        for childSink, parentSource in self.childInboxMapping.iteritems():
            self.inQueues[childSink] = Queue.Queue(self.queuelengths)
            self.link((self, parentSource),(self.child, childSink))
        for childSource, parentSink in self.childOutboxMapping.iteritems():
            self.outQueues[childSource] = Queue.Queue(self.queuelengths)
            self.link((self.child, childSource),(self, parentSink))


    def main(self):
        self.child.activate()
        self.waker.activate()
        while True:
            self.pause()
            yield 1
            # print "likefile woken for some reason."
            if self.checkWakeupReason():
                self.pollQueues()
            # there might have been data arriving from the child and the waker in the same 
            # scheduler cycle, so always do the pending send.
            self.sendPending()

    def pollQueues(self):
        """This method checks all the queues from the outside world, and forwards any waiting data
        to the child component."""
        for childSink, parentSource in self.childInboxMapping.iteritems():
            queue = self.inQueues[childSink]
            while not queue.empty():
                if not self.outboxes[parentSource].isFull():
                    msg = queue.get_nowait() # won't fail, we're the only one reading from the queue.
                    try:
                        self.send(msg, parentSource)
                    except noSpaceInBox, e:
                        raise "Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?"
                    if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                        return
                        # relying on a child component to propogate a shutdown back to our own control inbox is potentially flawed.
                else:
                    # if the component's inboxes are full, do something here. Preferably not succeed.
                    break

    def sendPending(self):
        """This method will take any data sent to us from a child component and stick it on a queue 
        to the outside world."""
        for childSource, parentSink in self.childOutboxMapping.iteritems():
            queue = self.outQueues[childSource]
            while self.dataReady(parentSink):
                if not queue.full():
                    msg = self.recv(parentSink)
                    queue.put_nowait(msg)
                else:
                    break
                    # permit a horrible backlog to build up inside our boxes. What could go wrong?

    def checkWakeupReason(self):
        """Returns True if we were woken  up because of pending data on a Queue.
        also prevents the wakeup box from overflowing."""
        if self.dataReady(self.wakeboxname):
            while self.dataReady(self.wakeboxname):
                self.recv(self.wakeboxname)
            return True
        return False

class LikeFile(object):
    """An interface to the message queues from a wrapped component, which is activated on a backgrounded scheduler."""
    def __init__(self, componenttowrap, extrainboxes = None, extraoutboxes = None):
        self.alive = False
        if schedulerThread.lock.acquire(False): 
            schedulerThread.lock.release()
            raise "no running scheduler found!"
        try: component = componentWrapper(componenttowrap, extrainboxes, extraoutboxes)
        except KeyError, e:
            raise KeyError, 'component to wrap has no such box: %s' % e
        self.inQueues = copy.copy(component.inQueues)
        self.outQueues = copy.copy(component.outQueues)

        # reaching into the component and its child like this is threadsafe since it has not been activated yet.
        self.component = component
        self.componentWaker = component.waker.wakeUp

    def activate(self):
        """activates the component on the backgrounded scheduler and permits IO."""
        if self.alive:
            return
        self.component.activate() # threadsafe, see note 1
        self.alive = True

    def get(self, boxname = "outbox"):
        """Performs a blocking read on the queue corresponding to the named outbox on the wrapped component."""
        if self.alive:
            return self.outQueues[boxname].get()
        else: raise "shutdown was previously called!"

    def put(self, msg, boxname = "inbox"):
        """Places an object on a queue which will be directed to a named inbox on the wrapped component."""
        if self.alive:
            self.inQueues[boxname].put_nowait(msg)

            # and clear the Event so that the componentWrapper knows to check for data.
            self.componentWaker.set()
        else: raise "shutdown was previously called!"

    def shutdown(self):
        """Will send terminatory signals to the wrapped component, and shut down the componentWrapper.
        Due to the way axon handles component shutdown, this may never terminate the scheduler thread. It would be nice if it did."""
        if self.alive: 
            self.inQueues["control"].put_nowait(Axon.Ipc.shutdown()) # legacy support.
            self.inQueues["control"].put_nowait(Axon.Ipc.producerFinished())
            self.inQueues["control"].put_nowait(Axon.Ipc.shutdownMicroprocess()) # should be last, this is what we honour
        else:
            raise "shutdown was previously called, or we were never activated."
        self.alive = False

    def __del__(self):
        if self.alive:
            self.shutdown()


if __name__ == "__main__":
    background = schedulerThread(slowmo=0.01).start()
    time.sleep(0.1)
    from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    import time
    p = LikeFile(SimpleHTTPClient())
    p.activate()
    p.put("http://google.com")
    p.put("http://slashdot.org")
    p.put("http://whatismyip.org")
    google = p.get()
    slashdot = p.get()
    whatismyip = p.get()
    print "google is", len(google), "bytes long, and slashdot is", len(slashdot), "bytes long. Also, our IP address is:", whatismyip

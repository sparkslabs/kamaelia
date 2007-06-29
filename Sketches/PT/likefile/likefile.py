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
==============================================
LikeFile - Non-Kamaelionic component interface
==============================================




todo: documentation




todo: this is a programming note, the end-user doesn't care. move it into a comment.

Note 1: Threadsafeness of activate().

when a component is activated, it calls the method inherited from microprocess, which calls _addThread(self)
on an appropriate scheduler. _addThread calls wakeThread, which places the request on a threadsafe queue.

"""

from Axon.Scheduler import scheduler
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess
import Queue, threading, time, copy, Axon
queuelengths = 0


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


class componentWrapper(Axon.ThreadedComponent.threadedadaptivecommscomponent):
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
        # parentSource:childSink
        # used to deliver information to a wrapped component from non-kamaelionic environments.
        self.childInboxMapping = { "inbox": "outbox", "control": "signal" }
        if extraInboxes:
            self.__addBox("Inbox", extraInboxes)

        # childSource:parentSink
        # used to retrieve information from a kamaelia system to a non-kamaelionic environment.
        self.childOutboxMapping = { "outbox": "inbox", "signal": "control" }
        if extraOutboxes:
            self.__addBox("Outbox", extraOutboxes)

        for childSink, parentSource in self.childInboxMapping.iteritems():
            self.__addQueue("Inbox", parentSource, childSink)
        for childSource, parentSink in self.childOutboxMapping.iteritems():
            self.__addQueue("Outbox", childSource, parentSink)

       
    def __addBox(self, direction, names):
        """Function used internally to add a new wrapped box. Direction is either
        "Inbox" or "Outbox". This is the box's direction on the child."""
        if direction == "Inbox":
            boxMap, addBox = self.childInboxMapping, self.addOutbox
        elif direction == "Outbox":
            boxMap, addBox = self.childOutboxMapping, self.addInbox
        else:
            raise ValueError, "%s is not a valid direction." % direction
        if type(names) == str:
            names = (names,)
        for boxname in names:
            if boxname in boxMap:
                raise ValueError, "%s %s already exists!" % (direction, boxname)
            realboxname = addBox(boxname)
            boxMap[boxname] = realboxname


    def __addQueue(self, direction, source, sink):
        """Function used internally to add a new Queue, and create the link
        used to communicate between the Queue and the child component.
        No sanity checking!. Assumes all boxes exist, and are not previously linked."""
        if direction == "Inbox":
            self.inQueues[sink] = Queue.Queue(self.queuelengths)
            self.link((self, source),(self.child, sink))
        elif direction == "Outbox":
            self.outQueues[source] = Queue.Queue(self.queuelengths)
            self.link((self.child, source),(self, sink))
        else: raise ValueError, "%s is not a valid direction." % direction

    def main(self):
        
        self.child.activate()
        while True:
            for childSink, parentSource in self.childInboxMapping.iteritems():
                queue = self.inQueues[childSink]
                # to aid a lack of confusion, this is where information would traverse from stdin to a child component's inbox.
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
            self.pause() # go to sleep until our child has processed this.
            for childSource, parentSink in self.childOutboxMapping.iteritems():
                queue = self.outQueues[childSource]
                # to aid a lack of confusion, this is where information would traverse from a child component's outbox to stdout.
                while self.dataReady(parentSink):
                    if not queue.full():
                        msg = self.recv(parentSink)
                        queue.put_nowait(msg)
                    else:
                        break
                        # permit a horrible backlog to build up inside our boxes. What could go wrong?


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
        # reaching into the component like this is threadsafe since it has not been activated yet.
        self.component = component
        self.threadWakeUp = component.threadWakeUp

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
            self.threadWakeUp.set() # wake the thread up to process the data we've just sent.
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

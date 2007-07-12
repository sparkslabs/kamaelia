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



THE OUTSIDE WORLD
     +----------------------------------+
     |             LikeFile             |
     +----------------------------------+
          |                      / \
          |                       |
      InQueues                 OutQueues
          |                       |
+---------+-----------------------+---------+
|        \ /                      |         |
|    +---------+               +--------+   |
|    |  Input  |   Shutdown    | Output |   |
|    | Wrapper |-------------->|        |   |
|    | (thread)|   Message     |Wrapper |   |
|    +---------+               +--------+   |
|         |                      / \        |
|         |                       |         |
|     Inboxes                 Outboxes      |
|         |                       |         |
|        \ /                      |         |
|    +----------------------------------+   |
|    |      the wrapped component       |   |
|    +----------------------------------+   |
|                                           |
|                                           |
|  AXON SCHEDULED COMPONENTS                |
+-------------------------------------------+



Note 1: Threadsafeness of activate().

when a component is activated, it calls the method inherited from microprocess, which calls _addThread(self)
on an appropriate scheduler. _addThread calls wakeThread, which places the request on a threadsafe queue.

"""

from Axon.Scheduler import scheduler
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess
import Queue, threading, time, copy, Axon, warnings


queuelengths = 0
DEFIN = ("inbox", "control")
DEFOUT = ("outbox", "signal")

def addBox(names, boxMap, addBox):
        """Add an extra wrapped box called name, using the addBox function provided
        (either self.addInbox or self.addOutbox), and adding it to the box mapping
        which is used to coordinate message routing within component wrappers."""
        if type(names) != tuple:
            names = (names,)
        for boxname in names:
            if boxname in boxMap:
                raise ValueError, "%s %s already exists!" % (direction, boxname)
            realboxname = addBox(boxname)
            boxMap[boxname] = realboxname


def validateBoxes(extraboxes, whitelist):
    """Helper function, will determine whether or not extra boxes are members of the whitelist."""
    for box in extraboxes:
        if box not in whitelist:
            raise KeyError, "box %s not a valid box" % box



class ComponentWrapperInput(Axon.ThreadedComponent.threadedadaptivecommscomponent):
    """A wrapper that takes a child component and waits on an event from the foreground, to signal that there is 
    queued data to be placed on the child's inboxes."""
    def __init__(self):
        super(ComponentWrapperInput, self).__init__()

        # this maps from the child component object to a dict of box mappings of the form:
        # ParentSource: ChildSink
        self.children = dict()

        # This queue is used by the foreground to send us data
        # where data is to be delivered to boxname.
        self.inQueue = Queue.Queue()


    def handleControlCommand(self, args):
        """We were sent some form of information from a foreground thread.

        for now, the only control command is one to add an extra component to watch,
        we are sent the unactivated component object and a tuple of pre-validated inboxes
        to wrap as well as the defaults."""
        child, extraInboxes = args
        self.addNewChild(child, extraInboxes + DEFIN)


    def addNewChild(self, child, inboxes):
        """Commences wrapping a new child. It seems that the actual linkage step is very slow."""
        inboxMapping = dict()
        childId = str(id(child))
        for childSink in inboxes:
            parentSource = self.addOutbox(childSink + childId) # TODO - benchmark the best way to wrap this.
            inboxMapping[childSink] = parentSource
            self.link((self, parentSource), (child, childSink))
        self.children[child] = inboxMapping
        


    def deleteChild(self, child):
        """Finishes monitoring a child component. Triggered by the relaying of ."""
        self.unlink(thecomponent = child)
        for parentSource in self.children[child].itervalues():
            self.deleteOutbox(parentSource)
        del self.children[child]

    def main(self):
        while True:
            self.pollQueue()


    def pollQueue(self):
        """This method checks the queue from the outside world, and forwards any waiting data
        to the appropriate child component."""

        delivered = self.inQueue.get() # blocks
        try:
            # delivered can either be a 3-value tuple, or more rarely some control information.
            msg, childSink, child = delivered
        except ValueError:
            self.handleControlCommand(delivered)
            return
        parentSource = self.children[child][childSink]
        if not self.outboxes[parentSource].isFull():
            try:
                self.send(msg, parentSource)
            except noSpaceInBox, e:
                raise "Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?"
            if childSink == "control" and isinstance(msg, (shutdownMicroprocess, producerFinished)):
                self.deleteChild(child)
        else:
            raise NotImplementedError # TODO - congestion handling.



class schedulerThread(threading.Thread):
    """A python thread which runs a scheduler."""
    lock = threading.Lock()
    inputWrapper = None
    def __init__(self,slowmo=0):
        if not schedulerThread.lock.acquire(False):
            raise "only one scheduler for now can be run!"
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when the caller dies
        schedulerThread.inputWrapper = ComponentWrapperInput()
    def run(self):
        schedulerThread.inputWrapper.activate()
        scheduler.run.runThreads(slowmo = self.slowmo)
        schedulerThread.lock.release()



class ComponentWrapperOutput(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """A component which takes a child component and connects its outboxes to queues, which communicate
    with the LikeFile component."""
    def __init__(self, child, extraInboxes = (), extraOutboxes = ()):
        super(ComponentWrapperOutput, self).__init__()
        self.queuelengths = queuelengths
        self.child = child
        self.addChildren(self.child)

        # This queue maps from the name of the outbox on the child which is to be wrapped,
        # to the Queue which conveys that data to the foreground thread.
        self.outQueues = dict()

        # set up notification from the input handler to kill us when appropriate.
        # we cannot rely on shutdown messages being propogated through the child.
        self.isDead = threading.Event()

        # This sets up the linkages between us and our child, avoiding extra
        # box creation by connecting the "basic two" in the same way as, e.g. a pipeline.
        self.childOutboxMapping = dict()
        self.wrapChildOutbox(DEFOUT + extraOutboxes)
        # Tell the input wrapper to start delivering messages to the child.
        schedulerThread.inputWrapper.inQueue.put_nowait((child, extraInboxes))


    def wrapChildOutbox(self, outboxes):
        """This method takes a tuple of names of an outbox on the child and adds
        all the appropriate queues and linkages and so on, so that the outbox
        is handled properly on the next iteration."""
        for boxname in outboxes:
            realboxname = self.addInbox(boxname)
            self.childOutboxMapping[boxname] = realboxname
            self.outQueues[boxname] = Queue.Queue(self.queuelengths)
            self.link((self.child, boxname), (self, realboxname))

    def handleShutdown(self):
        """we got a shutdown signal propogated from the child - we should inform the parent that we're about to exit."""
        self.isDead.set()

    def main(self):
        self.child.activate()
        while True:
            self.pause()
            yield 1
            if not self.sendPendingOutput():
                return

    def sendPendingOutput(self):
        """This method will take any outgoing data sent to us from a child component and stick it on a queue 
        to the outside world."""
        for childSource, parentSink in self.childOutboxMapping.iteritems():
            queue = self.outQueues[childSource]
            while self.dataReady(parentSink):
                if not queue.full():
                    msg = self.recv(parentSink)
                    if childSource == "signal" and isinstance(msg, (shutdownMicroprocess, producerFinished)):
                        self.handleShutdown()
                        return False
                    queue.put_nowait(msg)
                else:
                    break
                    # permit a horrible backlog to build up inside our boxes. What could go wrong?
        return True



class LikeFile(object):
    alive = False
    """An interface to the message queues from a wrapped component, which is activated on a backgrounded scheduler."""
    def __init__(self, componenttowrap, extraInboxes = (), extraOutboxes = ()):

        # the rest of the code is considerably terser if we always know these are tuples.
        # Duck typing leads to a catastrophe here; if we have a string arg where a tuple
        # is assumed, the code will not fail but instead add many boxes of one letter names.
        if type(extraInboxes) != tuple:
            extraInboxes = (extraInboxes, )
        if type(extraOutboxes) != tuple:
            extraOutboxes = (extraOutboxes, )

        self.child = componenttowrap
        if schedulerThread.lock.acquire(False): 
            schedulerThread.lock.release()
            raise AttributeError, "no running scheduler found."

        # ensure that the additional boxes specified are valid boxes on the child;
        # doing it manually allows us to move more code into another thread.
        validateBoxes(extraInboxes,  type(self.child).Inboxes.keys()  )
        validateBoxes(extraOutboxes, type(self.child).Outboxes.keys() )
        self.validInboxes = extraInboxes + DEFIN
        self.validOutboxes = extraOutboxes + DEFOUT

        outputComponent = ComponentWrapperOutput(componenttowrap, extraInboxes, extraOutboxes)

        self.inQueue = schedulerThread.inputWrapper.inQueue
        self.outQueues = copy.copy(outputComponent.outQueues)
        # reaching into the component and its child like this is threadsafe since it has not been activated yet.
        self.outputComponent = outputComponent


    def activate(self):
        """Activates the component on the backgrounded scheduler and permits IO."""
        if self.alive:
            return
        self.outputComponent.activate()
        self.alive = True

    def recv(self, boxname = "outbox"):
        """Performs a blocking read on the queue corresponding to the named outbox on the wrapped component.
        raises AttributeError if the LikeFile is not alive."""
        if self.alive:
            return self.outQueues[boxname].get()
        else: raise AttributeError, "shutdown was previously called, or we were never activated."
    get = recv # alias for backwards compatibility.

    def send(self, msg, boxname = "inbox"):
        """Places an object on a queue which will be directed to a named inbox on the wrapped component."""
        if boxname not in self.validInboxes:
            # we need to do explicit checking here since otherwise we'd need to block on error return from the other thread.
            raise KeyError, "%s is not a valid inbox" % boxname
        if self.alive:
            self.inQueue.put_nowait((msg, boxname, self.child))
        else: raise AttributeError, "shutdown was previously called, or we were never activated."
    put = send # alias for backwards compatibility

    def shutdown(self):
        """Sends terminatory signals to the wrapped component, and shut down the componentWrapper.
        will warn if the shutdown took too long to confirm in action."""
        if self.alive: 
            self.send(Axon.Ipc.shutdown(),               "control") # legacy support.
            self.send(Axon.Ipc.shutdownMicroprocess(),   "control") # should be last, this is what we honour
        else:
            raise AttributeError, "shutdown was previously called, or we were never activated."
        self.outputComponent.isDead.wait(1)
        if not self.outputComponent.isDead.isSet(): # we timed out instead of someone else setting the flag
            warnings.warn("Timed out waiting on shutdown confirmation, may not be dead.")
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
    p.send("http://google.com")
    p.send("http://slashdot.org")
    p.send("http://whatismyip.org")
    google = p.recv()
    slashdot = p.recv()
    whatismyip = p.recv()
    print "google is", len(google), "bytes long, and slashdot is", len(slashdot), "bytes long. Also, our IP address is:", whatismyip
    p.shutdown()
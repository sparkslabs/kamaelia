#!/usr/bin/env python

# parts of this may look strangely familiar to anyone who wrote ThreadedComponent :)
#
#
# In order for a seperate thread to communicate information into a kamaelia system,
# we must have Queue objects that carry all communications, meaning something like 
# a threadedcomponent turned inside out.
#
#
#
#
#            +------------------------------------------+
#            |            the outside world             |
#            |                                          |
#            |              +-----------+               |
#            |              | scheduled |               |
#  (STDIN) INBOX -------> inbox       outbox -------> OUTBOX (STDOUT)
#            |  inqueue     | component |  outqueue     |
#            |              +-----------+               |
#            +------------------------------------------+
#
#
#
#



from Axon.Component import component
from Axon.Scheduler import scheduler
from Axon.AxonExceptions import noSpaceInBox
import Queue, copy, threading
queuelengths = 1000



class schedulerThread(threading.Thread):
    def __init__(self,slowmo=0):
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when the interactive shell dies
    def run(self):
       scheduler.run.runThreads(slowmo = self.slowmo)


class Componentwrapper(component):
    def __init__(self, childcomponent):
        self.queuelengths = queuelengths
        self.child = childcomponent
        self.inqueues = dict()
        self.outqueues = dict()
        self.addChildren(childcomponent)

        # create a queue for every inbox or outbox on the target component we need to wrap around.
        # It would be nice if we could just read/write to the target component's boxes directly.
        # in this case, we need 2 sets of queues. In one, the source is our inqueues and the sink 
        # is the inboxes of the target component.
        # In othe other, the source is the outboxes of the target component and the sink is our outqueues.


        for box in self.component.inboxes.iterkeys():
            self.inqueues[box] = Queue.Queue(self.queuelengths)
        for box in self.component.outboxes.iterkeys():
            self.outqueues[box] = Queue.Queue(self.queuelengths)

        # insert code here to hook them up correctly.

        super(Componentwrapper, self).__init__()



    def main(self):
        while True:
            stuffWaiting = False
            for box, queue in self.inqueues.iteritems():
                # to aid a lack of confusion, this is where information would traverse from stdin to a component's inbox.
                while not queue.empty():
                    if not self.child.inboxes[box].isFull():
                        msg = queue.get()
                        try:
                            self.child.send(msg, box) # WRONG
                        except noSpaceInBox, e:
                            raise "Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?"
                    else:
                        stuffWaiting = True
                        break

            for box, queue in self.outqueues.iteritems():
                # to aid a lack of confusion, this is where information would traverse from a component's outbox to stdout.
                while self.component.dataReady(box):
                    if not queue.full():
                        msg = self.child.recv(box) # WRONG
                        self.inqueues[box].put(msg)
                    else:
                        stuffWaiting = True
                        break
            if not stuffWaiting: self.pause() # go to sleep unless we know we have un-processed data.
            yield 1

class Likefile(object):
    def __init__(self, componenttowrap):
        self.component = Componentwrapper(componenttowrap)
        self.component.activate()
    def get(self, boxname):
        return self.component.outqueues[boxname].get()
    def put(self, msg, boxname):
        self.component.inqueues[boxname].put(msg)

background = schedulerThread(slowmo=0.01)

background.start()

from helloworld import Reverser
import time

p = Likefile(Reverser())

while True:
    p.put("hello, world", "inbox")
    time.sleep(1)
    print p.get("outbox")
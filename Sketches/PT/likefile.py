#!/usr/bin/env python

# parts of this may look strangely familiar to anyone who wrote ThreadedComponent :)
#
#
# In order for a seperate thread to communicate information into a kamaelia system,
# we must have Queue objects that carry all communications, meaning something like 
# a threadedcomponent or a UnixProcess turned inside out.
#


from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent, component
from Axon.Scheduler import scheduler
from Axon.AxonExceptions import noSpaceInBox
import Axon
import Queue, threading, time
queuelengths = 1000



class schedulerThread(threading.Thread):
    def __init__(self,slowmo=0):
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when the caller dies
    def run(self):
       scheduler.run.runThreads(slowmo = self.slowmo)


class Componentwrapper(AdaptiveCommsComponent):
    def __init__(self, childcomponent):
        super(Componentwrapper, self).__init__()
        self.queuelengths = queuelengths
        self.child = childcomponent
        self.inqueues = dict() # queue for data traversing from, e.g, stdin to a component's inbox
        self.outqueues = dict()# queue for data traversing from, e.g, stdout to a component's outbox
        self.addChildren(self.child)

        # any shutdown signals sent to the child ought to propogate back to us and stop us as well.
        self.link((self.child, "signal"), (self, "control"))

        # Inspect our child, and whatever inboxes it has, give ourselves an outbox of the same name.
        # This is an ugly hack. It would better to have a custom mapping so that the componentwrapper's "outbox" 
        # sends to the child's "inbox" like every other kamaelia component.

        for box in self.child.inboxes.iterkeys():
            self.inqueues[box] = Queue.Queue(self.queuelengths)
            if box != self.addOutbox(box):
                raise "box name taken when encapsulating! This really ought not to happen!"
            self.link((self, box), (self.child, box))
            # this leads to the confusing situation where we have an outbox called "inbox"
            # having all the box names the same between parent and child makes this programmatically easier.

        for box in self.child.outboxes.iterkeys():
            self.outqueues[box] = Queue.Queue(self.queuelengths)
            if box != self.addInbox(box):
                raise "box name taken when encapsulating! This really ought not to happen!"
            self.link((self.child, box), (self, box))

        self.child.activate() # allegedly threadsafe?

    def main(self):
        while True:
            for box, queue in self.inqueues.iteritems():
                # to aid a lack of confusion, this is where information would traverse from stdin to a component's inbox.
                while not queue.empty():
                    if not self.outboxes[box].isFull():
                        msg = queue.get_nowait()
                        try:
                            self.send(msg, box)
                        except noSpaceInBox, e:
                            raise "Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?"
                    else: break


            for box, queue in self.outqueues.iteritems():
                # to aid a lack of confusion, this is where information would traverse from a component's outbox to stdout.
                while self.dataReady(box):
                    if not queue.full():
                        msg = self.recv(box)
                        queue.put_nowait(msg)
                    else: break # permit a horrible backlog to build up inside our boxes. What could go wrong?
            yield 1

class likeFile(object):
    def __init__(self, componenttowrap):
        self.component = Componentwrapper(componenttowrap) # this instantiation might be threadsafe?
        self.component.activate() # allegedly threadsafe
        self.alive = True

    def get(self, boxname, blocking = False):
        # this dictionary lookup of a queue is technically not threadsafe, but the only time the dict
        # is modified is during instantiation, which is in the current thread.
        if self.alive: 
            if blocking: return self.component.outqueues[boxname].get()
            else:
                try: return self.component.outqueues[boxname].get_nowait()
                except Queue.Empty: return
        else: raise "shutdown was previously called!"

    def put(self, msg, boxname):
        if self.alive: self.component.inqueues[boxname].put_nowait(msg)
        else: raise "shutdown was previously called!"

    def shutdown(self):
        if self.alive: self.component.inqueues["control"].put_nowait(Axon.Ipc.shutdownMicroprocess())
        else: raise "shutdown was previously called!"


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
#!/usr/bin/python
"""
Another optimisation test. This does the following:
   * Only instantiates boxes when a linkage is made
   * Does "direct linking" - shared out/inbox.
   * 

Controlled by a flag 'nonOptimised' which allows limited
cross testing on systems/components for this optimised
version vs the standard non-optimised version.

This shows that this approach is about 10-15 times faster
than the naive (standard axon) approach.
"""
import time

nonOptimised = True

if nonOptimised:
    from Axon.Component import component
    from Axon.Scheduler import scheduler
    from Kamaelia.Util.PipelineComponent import pipeline
else:

    class nullScheduler(object):
        def pause(self, _):
            pass
    class nullbox(object):
        def append(self, data):
            pass
        def __len__(self):
            return 0

    class realbox(list):
        pass

    class microprocess(object):
        def __init__(self):
            self.scheduler = nullScheduler()
            self.mthread = None
        def main(self):
            yield -1
        def run(self):
            p = self.main()
            for _ in p:
                pass
        def activate(self, scheduler):
            self.scheduler = scheduler
            self.mthread = self.main()
            self.unpause()

        def pause(self):
            self.scheduler.pause(self.mthread)

        def unpause(self):
            self.scheduler.append(self.mthread)
        

    class scheduler(microprocess):
        def __init__(self):
            self.runqueue = {}
        def main(self):
            while 1:
                remove = []
                for x in self.runqueue:
                    if self.runqueue[x]:
                        x.next()
                    else:
                        remove.append(x)
                for r in remove:
                    del self.runqueue[r]
                if len(self.runqueue) == 0:
                   time.sleep(0.1)
        def append(self, mprocess):
            self.runqueue[mprocess] = 1

        def pause(self, mprocess):
            self.runqueue[mprocess] = 0

    class component(microprocess):
        Inboxes = {}
        Outboxes = {}
        def __init__(self):
            super(component, self).__init__()
            self.outboxes = {}
            for boxname in self.Outboxes:
                self.outboxes[boxname] = nullbox()
            self.inboxes = {}
            for boxname in self.Inboxes:
                self.inboxes[boxname] = nullbox()
        def main(self):
            yield 1
        def send(self, data, outbox):
            self.outboxes[outbox].append(data)
        def recv(self, inbox):
            return self.inboxes[inbox].pop(0)
        def dataReady(self, inbox):
            return len(self.inboxes[inbox])
        def instantiate(self, inbox):
            if self.inboxes[inbox].__class__ == nullbox:
                self.inboxes[inbox] = realbox()
            return self.inboxes[inbox]
        def mergeOutbox(self, outbox, box):
            if self.outboxes[outbox].__class__ == nullbox:
                self.outboxes[outbox] = box
            else:
                # This was linked somewhere else. Since the data has already been
                # delivered (at point of send), the logic is identical here.
                # But being explicit about it!
                self.outboxes[outbox] = box

    links = {}
    def linkage((sourcecomponent, sourcebox), (sinkcomponent, sinkbox)):
        box = sinkcomponent.instantiate(sinkbox)
        sourcecomponent.mergeOutbox(sourcebox, box)

    class pipeline(object):
        def __init__(self, source, sink):
            self.source = source
            self.sink = sink
            linkage((source, "outbox"), (sink, "inbox"))
        def run(self):
            p = self.source.main()
            q = self.sink.main()
            while 1:
                p.next()
                q.next()

class producer(component):
    Outboxes = {
        "outbox" : "Data gets sent here!",
        "signal" : "",
    }
    def main(self):
        c, last = 0,0
        while 1:
            t = time.time()
            if t-last > 4:
                print "PRODUCED:", c
                last,c = t,0
            # Switch the comments on the next 2 lines to kill the non-Optimised Axon
            # almost instantaneously due to memory storage requirement growth explosion.
            # By comparison, this does not kill this optimised Axon
            self.send("hello", "outbox")
#            self.send("h"*c, "outbox")
            c +=1
            yield 1

class consumer(component):
    Inboxes = {
        "inbox" : "Data is recieved here!",
        "control": "",
    }
    def main(self):
        c, last,ds = 0,0,0
        while 1:
            if self.dataReady("inbox"):
                c = c+1
                d = self.recv("inbox")
                ds += len(d)
                t = time.time()
                if t-last > 4:
                    print "CONSUMED:", c, ds
                    last,c = t,0
            else:
               self.pause()
            yield 1


test = 3
if test == 1:
    # This test passes - the producer runs and produces, and does not cause a memory explosion
    # since the output isn't linked anywhere
    producer().run()

if test == 2:
    # This test passes, the consumer runs.
    # Issues with this test: CPU is caned.
    consumer().run()

if test == 2.5:
    if nonOptimised:
        print "This test is a low level test and won't function 'as is' with standard Axon"
    # This test passes, the consumer runs.
    # This modified version also does NOT cane the CPU :-)
    #
    # In practice, it's worth observing that this is how "2" is implemented effectively
    # in normal axon, so there's no reason this can't stay this way.
    S = scheduler()
    C = consumer()
    C.activate(S)
    S.run()

if test == 3:
    # Simple pipeline equivalent? Contains a scheduler.
    pipeline(
        producer(),
        consumer()
    ).run()

if test == 4:
    if nonOptimised:
        print "This test is a low level test and won't function 'as is' with standard Axon"
    S = scheduler()
    S.run()

if test == 5:
    if nonOptimised:
        print "This test is a low level test and won't function 'as is' with standard Axon"
    S = scheduler()
    C = consumer()
    P = producer()
    linkage((P, "outbox"), (C, "inbox"))
    C.activate(S)
    P.activate(S)
    S.run()

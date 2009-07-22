#!/usr/bin/python

import os
import re
import Axon

class Find(Axon.Component.component):
    path = "."
    walktype = "a"
    act_like_find = True
    def find(self, path = ".", walktype="a"):
        if walktype == "a":
            addfiles = True
            adddirs = True
        elif walktype == "f":
            addfiles = True
            adddirs = False
        elif walktype == "d":
            adddirs = True
            addfiles = False

        deque = []
        deque.insert(0,  (os.path.join(path,x) for x in os.listdir(path)) )
        while len(deque)>0:
            try:
                fullentry = deque[0].next()
                if os.path.isdir(fullentry):
                    if adddirs:
                        yield fullentry
                    try:
                        X= [ os.path.join(fullentry,x) for x in os.listdir(fullentry) ]
                        deque.insert(0, iter(X))
                    except OSError:
                        if not self.act_like_find:
                            raise
                elif os.path.isfile(fullentry):
                    if addfiles:
                        yield fullentry
            except StopIteration:

                deque.pop(0)

    def main(self):
        gotShutdown = False
        for e in self.find(path = self.path, walktype=self.walktype):
            self.send(e, "outbox")
            yield 1
            if self.dataReady("control"):
                gotShutdown = True
                break

        if not gotShutdown:
            self.send(Axon.Ipc.producerFinished(), "signal")
        else:
            self.send(self.recv("control"), "signal")

class Sort(Axon.Component.component):
    def main(self):
        dataset = []
        while 1:
            for i in self.Inbox("inbox"):
                dataset.append(i)
            if self.dataReady("control"):
                break
            self.pause()
            yield 1
        dataset.sort()
        for i in dataset:
            self.send(i, "outbox")
            yield 1
        self.send(self.recv("control"), "signal")

class Grep(Axon.Component.component):
    pattern = "."
    invert = False
    def main(self):
        match = re.compile(self.pattern)
        while 1:
            for i in self.Inbox("inbox"):
                if match.search(i):
                    if not self.invert:
                        self.send(i, "outbox")
                else:
                    if self.invert:
                        self.send(i, "outbox")
            if self.dataReady("control"):
                break
            self.pause()
            yield 1
        self.send(self.recv("control"), "signal")

class TwoWayBalancer(Axon.Component.component):
    Outboxes=["outbox1", "outbox2", "signal1","signal2"]
    def main(self):
        c = 0
        while 1:
            yield 1
            for job in self.Inbox("inbox"):
                if c == 0:
                    dest = "outbox1"
                else:
                    dest = "outbox2"
                c = (c + 1) % 2

                self.send(job, dest)
                job = None
            if not self.anyReady():
                self.pause()
            if self.dataReady("control"):
                break
        R=self.recv("control")
        self.send(R, "signal1")
        self.send(R, "signal2")

if __name__ == "__main__":

    from Kamaelia.Chassis.Graphline import Graphline 
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Util.Console import ConsoleEchoer

    Graphline(
        FILES = Pipeline(
                    Find(path=".",walktype="f"),
                    Sort(),
                    Grep(pattern="py$", invert = False),
                ),
        SPLIT = TwoWayBalancer(), # Would probably be nicer as a chassis, or a customised PAR chassis
        CONSUME1 = Pipeline( 
                      PureTransformer(lambda x: "1: "+ str(x)+"\n"),
                      ConsoleEchoer(),
                   ),
        CONSUME2 = Pipeline( 
                      PureTransformer(lambda x: "2: "+ str(x)+"\n"),
                      ConsoleEchoer(),
                   ),
        linkages = {
            ("FILES","outbox"):("SPLIT","inbox"),
            ("SPLIT","outbox1"):("CONSUME1","inbox"),
            ("SPLIT","outbox2"):("CONSUME2","inbox"),

            ("FILES","signal"):("SPLIT","control"),
            ("SPLIT","signal1"):("CONSUME1","control"),
            ("SPLIT","signal2"):("CONSUME2","control"),
        }
    ).run()

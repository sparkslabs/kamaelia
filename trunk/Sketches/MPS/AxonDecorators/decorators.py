#!/usr/bin/python

import Axon

class BlockingProducer(Axon.ThreadedComponent.threadedcomponent):
    g = None
    def main(self):
        def source():
            for i in range(10):
                yield str(i)+"\n"
            yield
            print "Source done"
        if self.g:
            source = self.g

        while not self.dataReady("control"):
            for data in source():
                self.send(data, "outbox")
            break

        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

def blockingProducer(GF):
    def replacement(*argv, **argd):
        return BlockingProducer(g= lambda : GF(*argv,**argd))
    return replacement

def TransformerGenComponent(GF):
    class SourceIt(Axon.Component.component):
        def __init__(self, *argv, **argd):
            self.argv = argv
            self.argd = argd
            self.F = GF
            super(SourceIt, self).__init__()
        def main(self):
            F = self.F
            argv = self.argv
            if argv[0] == None:
                argv = (self.Inbox,) + argv[1:]

            argd = self.argd

            gen = F( *argv, **argd )
            while not self.dataReady("control"):
                for line in gen:
                    if line:
                        self.send(line, "outbox")
                    else:
                        break
                yield

            if self.dataReady("control"):
                self.send(self.recv("control"), "signal")
            else:
                self.send(Axon.Ipc.producerFinished(), "signal")
    return SourceIt

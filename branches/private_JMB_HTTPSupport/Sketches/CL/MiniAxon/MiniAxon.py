#!/usr/bin/env python2.5
# -------------------------------------------------------------------------
"""\
=================
MiniAxon
=================

A simple framework for component-based concurrency system development

As its name suggests, it is a mini version of Kamaelia Axon.

"""

# A Generator with Context
class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1

# A mechanism to run generators repeatedly        
class scheduler(microprocess):
    def __init__(self):
        super(scheduler, self).__init__()
        self.active = []
        self.newqueue = []
    def main(self): 
        for element in xrange(100):
            for current in self.active:
                yield 1
                try:
                    nextData = current.next()
                except StopIteration:
                    pass
                else:
                    if nextData is not -1:
                        self.newqueue.append(current)                    
            self.active = self.newqueue
            self.newqueue = []
    def activateMicroprocess(self, someprocess):
        generator = someprocess.main()
        self.newqueue.append(generator)

# A prototype of components
class component(microprocess):
    boxes_model = {"inbox" : "", "outbox" : ""}
    def __init__(self):
        super(component, self).__init__()
        self.boxes = {}
        for boxName in self.boxes_model:
            self.boxes[boxName] = list()
    def dataReady(self, someoutbox):
        return len(self.boxes[someoutbox])
    """ / --IMIO, dataOut/ dataIn may be more straitforward. :-)
--recv or collect (from outbox of source)/ send or deliver (to inbox of sink)
are postman's job, not components'.
--Here, these two methods only serve as delegates, get data out (dataOut)
or get data in (dataIn).
"""
    def dataOut(self, someoutbox):
        data = self.boxes[someoutbox][0]
        del self.boxes[someoutbox][0]
        return data
    def dataIn(self, data, someinbox):
        self.boxes[someinbox].append(data)
        """ / --not work
        for element in data: # in case more than one data
            self.boxes[someinbox].append(element)
            """

# A connection module which links components
class postman(microprocess):
    def __init__(self, source, sourceoutbox, sink, sinkinbox):
        self.source = source
        self.sourceoutbox = sourceoutbox
        self.sink = sink
        self.sinkinbox = sinkinbox
    def main(self):
        while 1:
            yield 1
            if self.source.dataReady(self.sourceoutbox):
                d = self.source.dataOut(self.sourceoutbox)
                self.sink.dataIn(d, self.sinkinbox)

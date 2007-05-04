#!/usr/bin/env python
#
# mini-axon tutorial end-result.

class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1

class scheduler(microprocess):
    def __init__(self):
        super(scheduler, self).__init__()
        self.active = []
        self.newqueue = []

    def main(self):
        for i in xrange(100):
            for current in self.active:
                yield 1
                try: 
                    if current.next() != -1:
                        self.newqueue.append(current)
                except StopIteration: continue
            self.active = self.newqueue
            self.newqueue = []

    def activateMicroprocess(self, someprocess):
        self.newqueue.append(someprocess.main())

class printer(microprocess):
    def __init__(self, tag):
        super(printer, self).__init__()
        self.tag = tag
    def main(self):
        while 1:
            yield 1
            print self.tag

class component(microprocess):
    def __init__(self):
        super(component, self).__init__()
        self.boxes = {"inbox": [], "outbox": []}
    def send(self, value, boxname):
        self.boxes[boxname].append(value)
    def recv(self, boxname):
        return self.boxes[boxname].pop(0)
    def dataReady(self, boxname):
        return len(self.boxes[boxname])

class postman(microprocess):
    def __init__(self, source, sourcebox, sink, sinkbox):
        super(postman, self.__init__())
        self.source = source
        self.sourcebox = sourcebox
        self.sink = sink
        self.sinkbox = sinkbox
    def main(self):
        while 1:
            yield 1
            if self.source.dataReady:
                thedata = self.source.recv(self.sourcebox)
                self.sink.send(thedata, sinkbox)

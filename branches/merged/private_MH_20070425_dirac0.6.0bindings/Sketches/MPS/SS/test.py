#!/usr/bin/python

class microprocess:
    def __init__(self,name="hello"):
        self.name = name


#
#------------------
def scheduler_main(zelf): 
    result = 1 # force type of result to int
    for i in xrange(100):
        for current in zelf.active:
            yield 1
            try:
                result = current.next()
                if result is not -1:
                    zelf.newqueue.append(current)
            except StopIteration:
                pass

        # This shenanigans is needed to allow the type checker to understand
        # The various types in this function...
        for a in xrange(len(zelf.active)): zelf.active.pop()
        for b in zelf.newqueue: zelf.active.append(b)
        for c in xrange(len(zelf.newqueue)): zelf.newqueue.pop()

class scheduler(microprocess):
    def __init__(self):
        # super(.... not supported)
        microprocess.__init__(self)
        self.active = []
        self.newqueue = []

    def activateMicroprocess(self, some_gen, some_obj):
        microthread = some_gen(some_obj)
        self.newqueue.append(microthread)
#------------------
#

#
#------------------
class component(microprocess):
    def __init__(self):
        microprocess.__init__(self)
        self.boxes = { "inbox" : [], "outbox": [] }
    def send(self, value, outboxname):
        self.boxes[outboxname].append(value)
    def recv(self, inboxname):
        result = self.boxes[inboxname][0]
        del self.boxes[inboxname][0]
        return result
    def dataReady(self, inboxname):
        return len(self.boxes[inboxname])
#------------------
#

#
#------------------
def postman_main(zelf):
    while 1:
        yield 1
        if zelf.source.dataReady(zelf.sourcebox):
            d = zelf.source.recv(zelf.sourcebox)
            zelf.sink.send(d, zelf.sinkbox)

class postman(microprocess):
    def __init__(self, source, sourcebox, sink, sinkbox):
        microprocess.__init__(self)
        self.source = source
        self.sourcebox = sourcebox
        self.sink = sink
        self.sinkbox = sinkbox
#------------------
#

#
#------------------
def Producer_main(zelf):
    while 1:
        yield 1
        zelf.send(zelf.message, "outbox")

class Producer(component):
    def __init__(self, message):
        component.__init__(self)
        self.message = message
#-------------------
#

#
#------------------
def Consumer_main(zelf):
    count = 0
    while 1:
        yield 1
        count += 1 # This is to show our data is changing :-)
        if zelf.dataReady("inbox"):
            data = zelf.recv("inbox")
            print data, count

class Consumer(component):
    def __init__(self):
        component.__init__(self)
#-------------------
#

p = Producer("Hello World")
c = Consumer()
postie = postman(p, "outbox", c, "inbox")

myscheduler = scheduler()
myscheduler.activateMicroprocess(Consumer_main,c)
myscheduler.activateMicroprocess(Producer_main,p)
myscheduler.activateMicroprocess(postman_main,postie)


MT = scheduler_main(myscheduler)
for i in MT:
    pass

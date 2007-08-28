#/--------------------------------------------------------------------------------------------------
#
# Pretty standard fibonacci function
#
#
def fibonacci():
   a,b = 1,1
   while 1:
      print a
      a,b = b, a+b

fibonacci()
#
#
#
#
#
#
#
#
#
#
#
#
#\--------------------------------------------------------------------------------------------------
#/--------------------------------------------------------------------------------------------------
#
# Generator form
#
#
def fibonacci():
   a,b = 1,1
   while 1:
      yield a # was print a
      a,b = b, a+b

g =fibonacci()
print g
print g.next()
print g.next()
print g.next()
#
#
#
#
#
#
#
#
#\--------------------------------------------------------------------------------------------------
#/--------------------------------------------------------------------------------------------------
#
# Put the generator into a class
#
class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self): #<--- Look its here!!!
        yield 1
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#\--------------------------------------------------------------------------------------------------
#/--------------------------------------------------------------------------------------------------
#
# Create something to call the generator and manage run queues
#
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
                    result = current.next()
                    if result is not -1:
                        self.newqueue.append(current)
                except StopIteration:
                    pass
            self.active = self.newqueue
            self.newqueue = []
    def activateMicroprocess(self, someprocess):
        microthread = someprocess.main()
        self.newqueue.append(microthread)
#\--------------------------------------------------------------------------------------------------
#/--------------------------------------------------------------------------------------------------
#
# Example microprocess, usage and running
#
class printer(microprocess):
    def __init__(self, tag):
        super(printer, self).__init__()
        self.tag = tag
    def main(self):
        while 1:
            yield 1 # Must be a generator
            print self.tag

X = printer("Hello World")
Y = printer("Game Over") # Another well known 2 word phrase :-)

myscheduler = scheduler()

myscheduler.activateMicroprocess(X)
myscheduler.activateMicroprocess(Y)

for _ in myscheduler.main():
    pass
#
#\--------------------------------------------------------------------------------------------------
#/--------------------------------------------------------------------------------------------------
#
# Basic Component
#
class component(microprocess):
    Boxes = {
        "inbox" : "This is where we expect to receive messages",
        "outbox" : "This is where we send results/messages"
    }
    def __init__(self):
        super(component, self).__init__()
        self.boxes = {}
        for box in self.Boxes:
            self.boxes[box] = list()
    def send(self, value, outboxname):
        self.boxes[outboxname].append(value)
    def recv(self, inboxname):
        result = self.boxes[inboxname][0]
        del self.boxes[inboxname][0]
        return result
    def dataReady(self, inboxname):
        return len(self.boxes[inboxname])
#
#
#\--------------------------------------------------------------------------------------------------
#/--------------------------------------------------------------------------------------------------
#
# Someone to ensurce deliveries
#
class postman(microprocess):
    def __init__(self, source, sourcebox, sink, sinkbox):
        self.source = source
        self.sourcebox = sourcebox
        self.sink = sink
        self.sinkbox = sinkbox
    def main(self):
        while 1:
            yield 1
            if self.source.dataReady(self.sourcebox):
                d = self.source.recv(self.sourcebox)
                self.sink.send(d, self.sinkbox)
#
#
#
#
#
#
#
#
#\--------------------------------------------------------------------------------------------------
#/--------------------------------------------------------------------------------------------------
#
# Simple Producer/Consumer components & example usage
#
class Producer(component):
    def __init__(self, message):
        super(Producer, self).__init__()
        self.message = message
    def main(self):
        while 1:
            yield 1
            self.send(self.message, "outbox")

class Consumer(component):
    def main(self):
        count = 0
        while 1:
            yield 1
            count += 1 # This is to show our data is changing :-)
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                print data, count

p = Producer("Hello World")
c = Consumer()
postie = postman(p, "outbox", c, "inbox")

myscheduler = scheduler()
myscheduler.activateMicroprocess(p)
myscheduler.activateMicroprocess(c)
myscheduler.activateMicroprocess(postie)

for _ in myscheduler.main():
    pass
#
#
#\--------------------------------------------------------------------------------------------------

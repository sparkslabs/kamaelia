import time
from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component

class Producer(threadedcomponent):
    # Lazy timed source
    def main(self):
        for i in xrange(1000):
            self.send(range(i), "outbox")
            time.sleep(1)

class Transformer(component):
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                d = self.recv("inbox")
                self.send(len(d), "outbox")
            yield 1

class Triangular(component):
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                d = self.recv("inbox")
                self.send((d*(d+1))/2, "outbox")
            yield 1

class Square(component):
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                d = self.recv("inbox")
                self.send(d*d, "outbox")
            yield 1

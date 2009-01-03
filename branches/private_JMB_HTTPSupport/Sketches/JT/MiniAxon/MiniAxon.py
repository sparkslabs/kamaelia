#!/usr/bin/env python
class MicroProcess(object):
    """A basic miniaxon microprocess - a generator and nothing more"""
    def __init__(self):
        super(MicroProcess, self).__init__()

    def main(self):
        yield 1


class Component(MicroProcess):
    """
    A basic miniaxon component - a microprocess with an inbox and an outbox
    for communication between components.
    """

    def __init__(self):
        super(Component, self).__init__()
        self.boxes = {"inbox":[], "outbox":[]}

    def send(self, value, boxname):
        self.boxes[boxname].append(value)

    def recv(self, boxname):
        return self.boxes[boxname].pop(0)

    def dataReady(self, boxname):
        return len(self.boxes[boxname])

class Postman(MicroProcess):
    """Sends data from one component's outbox to another component's inbox"""
    def __init__(self, source, sourcebox, sink, sinkbox):
        super(Postman, self).__init__()
        self.source = source
        self.sourcebox = sourcebox
        self.sink = sink
        self.sinkbox = sinkbox

    def main(self):
        while 1:
            if self.source.dataReady(self.sourcebox):
                self.sink.send(self.source.recv(self.sourcebox), self.sinkbox)
            yield 1


class Scheduler(MicroProcess):
    """Runs any activated microprocesses 100 times, then stops."""
    def __init__(self):
        super(Scheduler, self).__init__()
        self.active = []
        self.newqueue = []

    def main(self):
        for i in range(100):
            if i == 0:
                # On the first run through we can activate any new jobs
                # straight away
                self.active = self.newqueue
                self.newqueue = []
            for microprocess in self.active:
                yield 1
                # Print the class of the generator function in an interesting
                # (and more than a little hacky) way
                #print microprocess.gi_frame.f_locals["self"].__class__
                try:
                    result = microprocess.next()
                    if result != -1:
                        self.newqueue.append(microprocess)
                except StopIteration:
                    pass
            self.active = self.newqueue
            self.newqueue = []

    def activate_microprocess(self, microprocess):
        microthread = microprocess.main()
        self.newqueue.append(microthread)


class Producer(Component):
    """Sends an object (tag) to it's outbox"""
    def __init__(self, tag):
        super(Producer, self).__init__()
        self.tag = tag

    def main(self):
        while 1:
            self.send(self.tag, "outbox")
            yield 1


class Consumer(Component):
    """
    Receives an object on it's inbox and prints it to the terminal, along
    with a count of how many objects it's received
    """
    def __init__(self):
        super(Consumer, self).__init__()

    def main(self):
        count = 0
        while 1:
            count += 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                print data, count
            yield 1

if __name__ == "__main__":
    producer = Producer("Hello World")
    consumer = Consumer()
    postman = Postman(producer, "outbox", consumer, "inbox")
    scheduler = Scheduler()

    # Need to be activated in the order they are to be called so the
    # counting goes to 100
    scheduler.activate_microprocess(producer)
    scheduler.activate_microprocess(postman)
    scheduler.activate_microprocess(consumer)

    # Mainloop
    for _ in scheduler.main():
        pass

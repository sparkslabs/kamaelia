#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1

class printer(microprocess):
    def __init__(self, tag):
        super(printer, self).__init__()
        self.tag = tag
    def main(self):
        while 1:
            yield 1
            print self.tag

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

class component(microprocess):
    Boxes = {
        "inbox" : "This is where we expect to receive messages for work",
        "outbox" : "This is where we expect to send results/messages to after doing work"
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
            count += 1
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






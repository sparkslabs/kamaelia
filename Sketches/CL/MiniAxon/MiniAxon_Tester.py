#!/usr/bin/env python2.5
# -------------------------------------------------------------------------
"""\
=================
MiniAxon_Tester
=================

A script that tests the MiniAxon framework

Small changes from the MiniAxon tutorial

"""

import MiniAxon

# A component that produces messages
class Producer(MiniAxon.component):
    def __init__(self, message):
        super(Producer, self).__init__()
        self.message = message
    def main(self):
        while 1:
            yield 1
            self.dataIn(self.message, "outbox")

# A component that receives messages
class Consumer(MiniAxon.component):
    def main(self):
        count = 0
        while 1:
            yield 1
            count += 1 # This is to show our data is changing :-)
            if self.dataReady("inbox"):
                data = self.dataOut("inbox")
                print data, count

#p = Producer(["Hello World", "Game Over"])
p = Producer("Hello World")
c = Consumer()
postie = postman(p, "outbox", c, "inbox")

myscheduler = scheduler()
myscheduler.activateMicroprocess(p)
# change the order of postie and c, so that the count starts from 1
myscheduler.activateMicroprocess(postie)
myscheduler.activateMicroprocess(c)

for _ in myscheduler.main():
    pass



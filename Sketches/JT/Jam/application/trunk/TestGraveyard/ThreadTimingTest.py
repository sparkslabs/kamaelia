#! /usr/bin/env python
import time

from Axon.ThreadedComponent import threadedcomponent
from Axon.Scheduler import scheduler

class ThreadedTest(threadedcomponent):
    def __init__(self):
        super(ThreadedTest, self).__init__()
        self.last = time.time()

    def main(self):
        while 1:
            t = time.time()
            print t - self.last
            self.last = t
            time.sleep(0.0005)


if __name__ == "__main__":
    ThreadedTest().run()



#! /usr/bin/env python
#
# This code is really testing (sorta) python's resolution of time.sleep
# It's not perfect though because there isn't:
#    * Anything going on in the background on the machine doing the test
#    * Anything else happening in this kamaelia thread
#
# The SpinWait()er helps with showing that this can cause problems...
#
# Added based on discussions regarding time.sleep. Derived from
# http://orphans.pastebin.com/d1dc6ea3b
#

import time

from Axon.ThreadedComponent import threadedcomponent
from Axon.Scheduler import scheduler

class SpinWait(threadedcomponent):
   def main(self):
      t = time.time()
      L = 0
      while time.time() - t<8:
          L = L+1

class ThreadedTest(threadedcomponent):
    target = 0.0005
    runs = 1000
    def __init__(self, **argd):
        super(ThreadedTest, self).__init__(**argd)
        self.last = time.time()

    def main(self):
        L = []
        last = self.last
        target = self.target
        runs = self.runs
        while len(L)<runs:
            time.sleep(target)
            t = time.time() # This may also not be accurate enough
            L.append(t - last)
            last = t
        L.sort()
        X = 0
        for l in L:
           X = X+l
        mean = X/len(L)
        print "   Mean", mean, "(diff:", int((target - mean)*10000)/10.0,"ms)"
        print "   5th percentile", L[int(len(L)*0.05)], "(diff:", int(( target - L[int(len(L)*0.05)] )*10000)/10.0,"ms)"
        print "   lower quartile", L[int(len(L)*0.25)], "(diff:", int(( target - L[int(len(L)*0.25)] )*10000)/10.0,"ms)"
        print "   median", L[int(len(L)*0.5)], "(diff:", int(( target - L[int(len(L)*0.5)] )*10000)/10.0,"ms)"
        print "   upper quartile", L[int(len(L)*0.75)], "(diff:", int(( target - L[int(len(L)*0.75)] )*10000)/10.0,"ms)"
        print "   95th percentile", L[int(len(L)*0.95)], "(diff:", int(( target - L[int(len(L)*0.95)] )*10000)/10.0,"ms)"


if __name__ == "__main__":
    print "time.sleep testing"

    timePerRun = 5.0
    for i in [0.005, 0.010, 0.020, 0.050, 0.100, 0.500]:
        
        runs = int(timePerRun/i)
        for spinwaiters in [0,1,2,3,4]:
          print
          print "Target", i, "runs", runs
          print "spinners", spinwaiters
          for _ in range(spinwaiters):
              SpinWait().activate()
          ThreadedTest(target = i, runs=runs).run()
          print "--------------"
#    ThreadedTest().run()

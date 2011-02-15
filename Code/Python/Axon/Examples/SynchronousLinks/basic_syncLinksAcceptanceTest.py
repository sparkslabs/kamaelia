#!/usr/bin/python

import Axon
import time
import sys

class SlowConsumer(Axon.Component.component):    
    delay = 0.2
    def main(self):
        print ("     Consumer starting")
        yield 1
        t = time.time()
        i = 0
        while i < 10: # Only accepting 10 items at most
            if time.time() - t > self.delay:
                if self.dataReady("inbox"):
                    print ("     C: got:", self.recv("inbox"), i)
                    t = time.time()
                    i = i + 1
            yield 1
        print ("     Consumer has finished consumption !")

class Producer(Axon.Component.component):
   def main(self):
      for i in range(10):
         success = False
         message = "hello" + str(i)
         while not success: # Since we know this may fail, we need to loop until it succeeds. You would wrap this normally
             yield 1
             try:
                self.send(message, "outbox")
                print ("     P: sent:", message)
                success = True
#             except Axon.AxonExceptions.noSpaceInBox, e:  # python2.6 and earlier
#             except Axon.AxonExceptions.noSpaceInBox as e: # python2.6, later and python 3
             except Axon.AxonExceptions.noSpaceInBox: # cross versions of python
                e = sys.exc_info()[1]                 # cross versions of python
                print ("                                ","P: fail:", message, "PAUSING UNTIL READY TO SEND")
                self.pause()
      print ("     Producer has finished production !!!")

print ("=======================================")
print ("Synchronous Link")

class testComponent(Axon.Component.component):
    def main(self):
        producer = Producer().activate()
        consumer = SlowConsumer().activate()
        self.link((producer,"outbox"),(consumer, "inbox"),synchronous=True)
        self.addChildren(producer, consumer)
        while 1:
            yield 1
            if producer._isStopped() and consumer._isStopped():
                break
            else:
                self.pause() # Awoken when children exit

testComponent().run()
print ("---------------------------------------")
print ()
print ("=======================================")
print ("link - Explicit Pipewidth = 1")

class testComponent(Axon.Component.component):
    def main(self):
        producer = Producer().activate()
        consumer = SlowConsumer().activate()
        self.link((producer,"outbox"),(consumer, "inbox"),pipewidth=1)
        self.addChildren(producer, consumer)
        while 1:
            yield 1
            if producer._isStopped() and consumer._isStopped():
                break
            else:
                self.pause() # Awoken when children exit

testComponent().run()

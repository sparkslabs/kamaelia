#!/usr/bin/python

import threading
import Queue
import time

simpleQueue = Queue.Queue(maxsize=10)

class newMainThread(threading.Thread):
    def run(self):
        ts = t = time.time()
        while time.time()-ts < 1:
            if time.time()-t >0.1:
                data = True
                while data:
                    try:
                        next = simpleQueue.get(timeout=0.1)
                        print "got", next
                    except Queue.Empty:
                        print "NOTGOT"
                        data = False
                t = time.time()

class newWorker(threading.Thread):
    def run(self):
        print "newWorker Running"
        ts = t = time.time()
        while time.time() - ts < 1:
            pass

if __name__ == "__main__":
    n = newMainThread()
    nw = newWorker()
    n.start()
    nw.start()
    xs = x = time.time()
    while time.time() -xs <1:
        if time.time()-x >0.2:
            try:
                simpleQueue.put_nowait("something")
                t = time.time()
            except Queue.Full:
                pass

"""
if 0:
#            if time.time()-t >0.5:
#                try:
#                    simpleQueue.put_nowait("newWorker")
#                    t = time.time()
#                except Queue.Full:
#                    pass



#    s = mainThread()
#    f1 = aFeederThread()
#    f2 = anotherFeederThread()
#    f1.start()
#    f2.start()
#    s.start()
    pass

class mainThread(threading.Thread):
     def run(self):
         useless = threading.Event()
         for i in xrange(10):
             while doneSomething.isSet():
                 print time.time(),"Something happened! We clear the set here"
                 useless.wait(2)
                 doneSomething.clear()
                 print time.time(),"End of processing something happening"
             doneSomething.wait(1)
         print time.time(),"EXITING OTHER THREAD"

doneSomething = threading.Event()

class aFeederThread(threading.Thread):
    def run(self):
        useless = threading.Event()
        for i in xrange(10):
            print time.time(),i
            if i%2: doneSomething.set()
            useless.wait(0.5)

class anotherFeederThread(threading.Thread):
    def run(self):
        useless = threading.Event()
        for i in xrange(10):
            print time.time(),i
            if i%2: doneSomething.set()
            useless.wait(0.5)
"""
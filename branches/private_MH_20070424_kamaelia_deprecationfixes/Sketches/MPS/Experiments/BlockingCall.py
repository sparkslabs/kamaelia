#!/usr/bin/python

import time
import Axon
import Axon.ThreadedComponent

class Test(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while 1:
            time.sleep(0.1)
            while self.dataReady("inbox"):
                tag, func, args = self.recv("inbox")
                result = func(*args)
                self.send((tag, result), "outbox")

class NotReady(Exception):
    pass

class usesAsyncService(object):
    def __init__(self,outbox="outbox", inbox="inbox"):

        super(usesAsyncService, self).__init__()
        self.resultBox = inbox
        self.requestBox = outbox
        self.async = Test()
        self.asyncService()
        self.callswaiting = {}
        self.results = {}
    def asyncService(self, outbox="outbox", inbox="inbox"):
        self.link((self, outbox), (self.async, "inbox"))
        self.link((self.async, "outbox"), (self, inbox))
        self.async.activate()

    def callAsync(self, tag, func, *args):
        self.send((tag, func, args), self.requestBox)
        self.callswaiting[tag] = self.callswaiting.get(tag, 0) + 1

    def asyncReady(self, tagRequested):
        while self.dataReady(self.resultBox):
            tag, result = self.recv("inbox")
            if tag in [ x for x in self.callswaiting if self.callswaiting[x]>0 ]:
                self.results[tag] = self.results.get(tag, []) + [ result ]
        
        if tagRequested in [ x for x in self.results if len(self.results[x]) > 0 ]:
            return True
    
    def asyncResult(self, tagRequested):
        if tagRequested in [ x for x in self.results if len(self.results[x]) > 0 ]:
            return self.results[tagRequested].pop(0)
        raise NotReady

class Timer(usesAsyncService, Axon.Component.component):
    def printer(self, what,delay=1):
        for i in what:
            print i,
            time.sleep(delay)
            print i
        return "DONE"

    def main(self):
        self.queueAsyncCall("printer", self.printer, ["hello", "world"], 2)
        self.queueAsyncCall("pronter", self.printer, ["game", "over"], 1)
        yield 1
        t = time.time()
        while 1:
            if self.asyncReady("printer"):
                result = self.asyncResult("printer")
                print "Printer done!", result
            
            if self.asyncReady("pronter"):
                result = self.asyncResult("pronter")
                print "Second Printer done!", result
            
            if time.time() - t > 0.2:
                print "."
                t = time.time()
            yield 1
            
Timer().run()


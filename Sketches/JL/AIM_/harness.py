#! /usr/bin/env python

from OSCARClient import *
from gen import *
from negotiation import *
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.Component import component

class AIMHarness(component):
    Inboxes = {"inbox" : "NOT USED",
               "control" : "NOT USED",
               "internal inbox" : "links to various child components",
               "internal control" : "links to signal outbox of various child components",
               }
    Outboxes = {"outbox" : "NOT USED",
                "signal" : "NOT USED",
                "internal outbox" : "outbox to various child components",
                "internal signal" : "sends shutdown handling signals to various child components",
                }
    
    def __init__(self):
        super(AIMHarness, self).__init__()
        oscar = OSCARClient('login.oscar.aol.com', 5190)
        auth = AuthCookieGetter()
        self.link((auth, "outbox") , (oscar, "inbox"))
        self.link((oscar, "outbox") , (auth, "inbox"))
        self.link((auth, "_cookie") , (self, "internal inbox"))
        oscar.activate()
        auth.activate()
        self.oscar, self.auth = oscar, auth
        self.addChildren(self.oscar, self.auth)
        self.debugger.addDebugSection("AIMHarness.main", 5)

    def main(self):
        while not self.dataReady("internal inbox"):
            yield 1
        BOS_server, port, cookie = self.recv("internal inbox")
        self.removeChildren(*self.children)
        neg = ProtocolNegotiator(cookie)
        oscar = OSCARClient(BOS_server, port)
        self.link((neg, "outbox") , (oscar, "inbox"))
        self.link((oscar, "outbox") , (neg, "inbox"))
        self.link((neg, "signal"), (self, "internal control"))
        
        oscar.activate()
        neg.activate()
        self.oscar, self.neg = oscar, neg
        self.addChildren(self.oscar, self.neg)
        while not self.dataReady("internal control"):
            yield 1
        self.removeChildren(neg)
        assert self.debugger.note("AIMHarness.main", 5, "Harness finished")

    def removeChildren(self, *children):
        for child in children:
            self.removeChild(child)


if __name__ == '__main__':
    AIMHarness().run()

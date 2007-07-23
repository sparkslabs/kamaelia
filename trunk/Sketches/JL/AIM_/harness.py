from OSCARClient import *
from gen import *
from negotiation import *
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.Component import component

class AIMHarness(component):
    Inboxes = {"inbox" : "NOT USED",
               "control" : "NOT USED",
               "internal" : "links to various child components",
               "internal control" : "links to signal outbox of various child components",
               }
    
    def __init__(self):
        super(AIMHarness, self).__init__()
        oscar = OSCARClient('login.oscar.aol.com')
        auth = AuthCookieGetter()
        self.link((auth, "outbox") , (oscar, "inbox"))
        self.link((oscar, "outbox") , (auth, "inbox"))
        self.link((auth, "_cookie") , (self, "internal"))
        oscar.activate()
        auth.activate()
        self.oscar, self.auth = oscar, auth
        self.addChildren(self.oscar, self.auth)

    def main(self):
        while not self.dataReady("internal"):
            yield 1
        BOS_server, port, cookie = self.recv("internal")
        self.stopChildren(*self.children)
        self.removeChildren(*self.children)
        neg = ProtocolNegotiator()
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
        self.stopChildren(neg)


    def stopChildren(self, *children):
        for child in children:
            self.unlink(child)
        self.removeChildren(*children)

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
        self.loginer = LoginHandler().activate()
        self.link((self.loginer, "signal"), (self, "internal inbox"))
        self.addChildren(self.loginer)
        self.debugger.addDebugSection("AIMHarness.main", 5)

    def main(self):
        while not self.dataReady("internal inbox"):
            yield 1
        self.oscar = self.recv("internal inbox")
        link_loginer_to_one_outbox()
        chat_manager_to_another()


if __name__ == '__main__':
    AIMHarness().run()

#! /usr/bin/env python

from OSCARClient import *
import login
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.Component import component
import chat

class AIMHarness(component):
    Inboxes = {"inbox" : "NOT USED",
               "control" : "NOT USED",
               "internal inbox" : "links to various child components",
               "internal control" : "links to signal outbox of various child components",
               }
    Outboxes = {"outbox" : "",
                "signal" : "NOT USED",
                "internal outbox" : "outbox to various child components",
                "internal signal" : "sends shutdown handling signals to various child components",
                }
    
    def __init__(self):
        super(AIMHarness, self).__init__()
        self.loginer = login.LoginHandler('kamaelia1', 'abc123').activate()
        self.link((self.loginer, "signal"), (self, "internal inbox")) #quite a hack, sending other data out through "signal"
        self.addChildren(self.loginer)
        self.debugger.addDebugSection("AIMHarness.main", 5)

    def main(self):
        while not self.dataReady("internal inbox"):
            yield 1
        self.oscar = self.recv("internal inbox")
        queued = self.recv("internal inbox")
        self.unlink(self.oscar)
        assert self.debugger.note("AIMHarness.main", 5, "%i queued messages" % len(queued))
        self.chatter = chat.ChatManager().activate()
        self.link((self, "internal outbox"), (self.chatter, "inbox"))
        self.link((self.chatter, "heard"), (self, "outbox"), passthrough=2)
        while len(queued):
            self.send(queued[0], "internal outbox")
            del(queued[0])
        for _ in range(20):
            yield 1
        self.link((self, "internal outbox"), (self.chatter, "talk"))
        self.link((self.oscar, "outbox"), (self.chatter, "inbox"))
        while True:
            yield 1
        
            


if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    Pipeline(AIMHarness(), ConsoleEchoer()).run()

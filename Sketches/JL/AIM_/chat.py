#! /usr/bin/env python

from OSCARClient import *
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.Component import component

class ChatManager(SNACExchanger):
    Inboxes = {"inbox" : "incoming FLAPs on channel 2",
               "errors" : "error messages",
               "control" : "NOT USED",
               "talk" : "outgoing messages",
               }

    Outboxes = {"outbox" : "outgoing FLAPs",
                "signal" : "NOT USED",
                "heard" : "echoes peer messages to this box."
                }

    def __init__(self):
        super(ChatManager, self).__init__()
        self.debugger.addDebugSection("ChatManager.main", 7)

    def main(self):
        while True:
            yield 1
            if self.dataReady():
                header, body = self.recvSnac()
                kind = (header[0], header[1])
                if kind == (0x03, 0x0b):
                    l, = struct.unpack('!B', body[0])
                    buddy = body[1:1+l]
                    assert self.debugger.note("ChatManager.main", 7, buddy + " came online")
                    buddyinfo = {"name" : buddy}
                    self.send(("buddy online", buddyinfo), "heard")
                elif kind == (0x04, 0x07):
                    msgid, msgchan, l = struct.unpack('!QHB', body[:11])
                    sender = body[11:11+l]
                    assert self.debugger.note("ChatManager.main", 7, "message from " + sender)
                    self.send(("message", sender, "we're working on the parsing algorithm!"), "heard")
                else:
                    print "unknown message", header
                    

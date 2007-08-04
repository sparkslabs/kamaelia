#! /usr/bin/env python

from OSCARClient import *
from oscarutil import *
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
        debugSections = {"ChatManager.main" : 7,
                        "ChatManager.receiveMessage" : 5}
        self.debugger.addDebug(**debugSections)

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
                    self.receiveMessage(body)
                else:
                    print "unknown message", header

    def receiveMessage(self, body):
        msgid, msgchan, l = struct.unpack('!QHB', body[:11])
        sender = body[11:11+l]
        assert self.debugger.note("ChatManager.receiveMessage", 7, "message from %s on channel %i" % (sender, msgchan))
        TLVchain = body[11 + l + 4:]
        parsed = readTLVs(TLVchain)
        if msgchan == 1:
            fragments = readTLVs(parsed[0x02])
            msgText = fragments[0x0101]
            charSetID, charSubset = struct.unpack("!HH", msgText[:4]) #ignoring these for now, but they might come in handy
            message = msgText[4:]
        elif msgchan == 2:
            message = "%s requesting unsupported function" % sender
        elif msgchan == 3:
            message = parsed[0x05][8:]
            
        self.send(("message", sender, message), "heard")

if __name__ == '__main__':
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
    import sys
    sys.path.append('..')
    from likefile import *
    
    flap = open('/home/jlei/aim/snacs/0407').read()
    class Chargen(component):
        def main(self):
            self.send((2, flap[6:]))
            yield 1
            
    p = Graphline(chargen = Chargen(),
                  cm = ChatManager(),
                  ce = ConsoleEchoer(),
                  linkages = {("chargen", "outbox") : ("cm", "inbox"),
                              ("cm", "heard") : ("ce", "inbox"),
                              }
                  )
    p.run()

#! /usr/bin/env python
##
## (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
##     All Rights Reserved.
##
## You may only modify and redistribute this under the terms of any of the
## following licenses(2): Mozilla Public License, V1.1, GNU General
## Public License, V2.0, GNU Lesser General Public License, V2.1
##
## (1) Kamaelia Contributors are listed in the AUTHORS file and at
##     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
##     not this notice.
## (2) Reproduced in the COPYING file, and at:
##     http://kamaelia.sourceforge.net/COPYING
## Under section 3.5 of the MPL, we are using this text since we deem the MPL
## notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
## notice is prohibited.
##
## Please contact us via: kamaelia-list-owner@lists.sourceforge.net
## to discuss alternative licensing.
## -------------------------------------------------------------------------
"""\
================
AIM Client
================

Deals with post-login messages from the AIM server, mostly by parsing them and
sending them out to its "heard" outbox in a slightly more useable form. Also
sends messages to the server based on commands coming through its "talk" inbox.



How it works:
-------------
ChatManager expects to receive FLAPs containing SNACs through its "inbox". It
recognizes certain types of SNACs. For these SNACS, ChatManager parses them, and
sends the relevant data out to its "heard" outbox in tuple format. The following
lists the SNACs ChatManager understands and the tuples that it consequently
sends out:

=========   ================    ====================================
SNAC        DESCRIPTION         TUPLE SENT TO "heard"
=========   ================    ====================================
(03, 0b)    Buddy is online     ("buddy online", {name: buddy name})
(04, 07)    Incoming message    ("message", sender, message text)
=========   ================    ====================================

The "buddy online" message contains a dictionary instead of just a text field
for the buddy name because this will make it easier to add more buddy data
to a "buddy online" message, such as online time or alias. The server sends this
data, but right now ChatManager just discards it. 

ChatManager also understands tuple-based commands sent to its "talk" inbox. The
following lists the commands it understands, and the corresponding actions it
takes.

=================================================   ======================
COMMAND                                             ACTION
=================================================   ======================
("message", recipient's screenname, message text)   Sends instant message to
                                                    server (SNAC (04, 07))
=================================================   ======================



Example Usage
-------------
Simple client with a truly horrible interface::

    class AIMHarness(component):
        def main(self):
            self.loginer = LoginHandler('sitar63112', 'sitar63112').activate()
            self.link((self.loginer, "signal"), (self, "internal inbox"))
            self.addChildren(self.loginer)
            while not self.dataReady("internal inbox"): yield 1
            self.oscar = self.recv("internal inbox")
            queued = self.recv("internal inbox")
            self.unlink(self.oscar)
            
            self.chatter = ChatManager().activate()
            self.link((self.chatter, "heard"), (self, "outbox"), passthrough=2)
            self.link((self, "inbox"), (self.chatter, "talk"), passthrough=1)
            self.link((self.chatter, "outbox"), (self.oscar, "inbox"))
            self.link((self.oscar, "outbox"), (self.chatter, "inbox"))
            self.link((self, "internal outbox"), (self.chatter, "inbox"))
            while len(queued):
                self.send(queued[0], "internal outbox")
                del(queued[0])
            while True:
                yield 1
                
    def tuplefy(data):
        data = data.split()
        if len(data) > 1: 
            data = ("message", data[0], " ".join(data[1:]))
            return data
           
    Pipeline(ConsoleReader(),
             PureTransformer(tuplefy),
             AIMHarness(),
             ConsoleEchoer()
            ).run()

"""

from OSCARClient import *
from OscarUtil import *
from OscarUtil2 import *
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.Component import component
import re

__kamaelia_components__ = (OSCARClient, TCPClient)

class ChatManager(SNACExchanger):
    """
    ChatManager() -> new ChatManager component.
    """
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
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ChatManager, self).__init__()
        debugSections = {"ChatManager.main" : 5,
                        "ChatManager.receiveMessage" : 5,
                         "ChatManager.sendMessage" : 4,}
        self.debugger.addDebug(**debugSections)

    def main(self):
        "Main loop."
        while True:
            yield 1
            while self.dataReady():
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
##                else:
##                    self.send(("unknown message", header[0], header[1]), "heard")
            while self.dataReady("talk"):
                data = self.recv("talk")
                assert self.debugger.note("ChatManager.main", 7, "received " + str(data))
                if data[0] == "message" :
                    self.sendMessage(data[1], data[2])
                    
    def receiveMessage(self, body):
        """
        Extracts the sender and message text from SNAC body, and sends the tuple
        ("message", sender, message) to "heard".
        """
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
            message = self.cleanMessage(message)
        elif msgchan == 2:
            message = "%s requesting unsupported function" % sender
        elif msgchan == 3:
            message = parsed[0x05][8:]
            
        self.send(("message", sender, message), "heard")

    def sendMessage(self, buddyname, text):
        """
        constructs SNAC (04, 06), the "send message" SNAC and sends it to "outbox"
        """
        frag = TLV(0x0501, struct.pack("!i", 0))
        frag2 = TLV(0x0101, struct.pack("!HH", 0, 0) + text)
        msgCookie = '\x32\x36\x37\x31\x34\x36\x36\x00'
        msgChan = 1
        buddyinfo = Single(len(buddyname)) + buddyname
        body = msgCookie + Double(msgChan) + buddyinfo + TLV(0x02, frag + frag2)
        self.sendSnac(0x04, 0x06, body)

    def cleanMessage(self, message):
        """strips HTML tags off messages"""
        p = re.compile("<[^<^>]*>")
        message = p.sub("", message)
        return message

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

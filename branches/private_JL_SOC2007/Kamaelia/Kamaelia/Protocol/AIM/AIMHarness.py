#! /usr/bin/env python
##
## (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
========================
AIM Harness
========================

Provides a high-level Kamaelia interface to AIM.

For a Kamaelia interface at the FLAP and SNAC levels, see OSCARClient.py



Example Usage
-------------
A simple command-line client with a truly horrible interface::

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



How it works
-------------
AIMHarness ties LoginHandler and ChatManager together. First it initializes a
LoginHandler, waits for it to send out a logged-in OSCARClient, then wires up a
ChatManager to the OSCARClient. It wires up its "inbox" to ChatManager's "talk",
and ChatManager's "heard" to "outbox".

To send an instant message to another user, send the command
("message", recipient, text of the message) to its "inbox". 

AIMHarness will send out the following notifications through its "outbox":

======================================  ===================================
NOTIFICATION                            EVENT
======================================  ===================================
("buddy online", {buddy information})   A buddy comes online
("message", sender, message text)       An instant message arrives for you
======================================  ===================================



Known issues
-------------
This component does not terminate. 

"""

from Kamaelia.Protocol.AIM.OSCARClient import *
import Kamaelia.Protocol.AIM.LoginHandler
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.Component import component
import Kamaelia.Protocol.AIM.ChatManager

__kamaelia_components__ = (Kamaelia.Protocol.AIM.LoginHandler.LoginHandler,
                           Kamaelia.Protocol.AIM.ChatManager.ChatManager,
                           TCPClient,
                           )
__kamaelia_prefabs__ = (OSCARClient,)

class AIMHarness(component):
    """
    AIMHarness() -> new AIMHarness component

    Send ("message", recipient, message) commands to its "inbox" to send
    instant messages. It will output ("buddy online", {name: buddyname}) and
    ("message", sender, message) tuples whenever a buddy comes online or a new
    message arrives for you.
    """
    Inboxes = {"inbox" : "tuple-based commands for ChatManager",
               "control" : "NOT USED",
               "internal inbox" : "links to various child components",
               "internal control" : "links to signal outbox of various child components",
               }
    Outboxes = {"outbox" : "tuple-based notifications from ChatManager",
                "signal" : "NOT USED",
                "internal outbox" : "outbox to various child components",
                "internal signal" : "sends shutdown handling signals to various child components",
                }
    
    def __init__(self, screenname, password):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(AIMHarness, self).__init__()
        self.loginer = Kamaelia.Protocol.AIM.LoginHandler.LoginHandler(screenname, password).activate()
        self.link((self.loginer, "signal"), (self, "internal inbox")) #quite a hack, sending other data out through "signal"
        self.addChildren(self.loginer)
        self.debugger.addDebugSection("AIMHarness.main", 5)

    def main(self):
        """Waits for logged-in OSCARClient and links it up to ChatManager"""
        while not self.dataReady("internal inbox"):
            yield 1
        result = self.recv("internal inbox")
        if type(result) == type((1,2)):
            self.send(result)
        else:
            self.oscar = result
            queued = self.recv("internal inbox")
            self.unlink(self.oscar)
            
            assert self.debugger.note("AIMHarness.main", 9, "%i queued messages" % len(queued))
            self.chatter = Kamaelia.Protocol.AIM.ChatManager.ChatManager().activate()
            self.link((self.chatter, "heard"), (self, "outbox"), passthrough=2)
            self.link((self, "inbox"), (self.chatter, "talk"), passthrough=1)
            self.link((self.chatter, "outbox"), (self.oscar, "inbox"))
            self.link((self.oscar, "outbox"), (self.chatter, "inbox"))
            self.link((self, "internal outbox"), (self.chatter, "inbox"))
            while len(queued):
                self.send(queued[0], "internal outbox")
                del(queued[0])
            assert self.debugger.note("AIMHarness.main", 5, "Everything linked up and initialized, starting normal operation")
            while True:
                yield 1
        
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
    from Kamaelia.Util.PureTransformer import PureTransformer

    def tuplefy(data):
        data = data.split()
        if len(data) > 1: 
            data = ("message", data[0], " ".join(data[1:]))
            return data
           
    Pipeline(ConsoleReader(),
             PureTransformer(tuplefy),
             AIMHarness("kamaelia1", "abc123"),
             ConsoleEchoer()
             ).run()

#!/usr/bin/env python
#
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

import cgi
import time
import Axon
from Kamaelia.Protocol.AIM.AIMHarness import AIMHarness
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.UnixProcess import UnixProcess

class AIMUserTalkAdapter(Axon.ThreadedComponent.threadedcomponent):
    Inboxes = {
        "from_user" : "We receive plain text from the user here. Initially we just pass on messages almost as is",
        "from_aim" : "We recieive 'raw' AIM messages here",
        "control" : "We expect shutdown messages here",
    }
    Outboxes = {
        "to_user" : "We send plain text to the user here.",
        "to_aim" : "We send formatted messages here, which are for aim, targetted to a particular user",
        "signal" : "We pass on shutdown messages here",
    }
    user = "zathmadscientist"
    ratelimit = 0.5
    def __init__(self, **argd):
        super(AIMUserTalkAdapter, self).__init__(**argd)
        print "CREATED AIMUserTalkAdapter", repr(argd)

    def main(self):
        print "STARTED AIMUserTalkAdapter"
        while not self.dataReady("control"):
            for message in self.Inbox("from_user"):
                 message = cgi.escape(message,1)
                 lines = message.split("\n")
                 c = 0
                 for line in lines:
                     if c > 0:
                         time.sleep(self.ratelimit)
                     c += 1
                     message = ("message", self.user, line )
                     self.send(message, "to_aim")

            for message in self.Inbox("from_aim"):
                 if len(message) == 3:
                     if message[0] == "message":
                         text = message[2]+"\n"
                         self.send(text, "to_user")

            if not self.anyReady():
                self.pause()

        print "EXITED AIMUserTalkAdapter"
        if self.dataReady("control"):
            print "GOT CONTROL MESSAGE"
            self.send(self.recv("control"), "signal")
        else: 
            print "SOME OTHER REASON"
            self.send(Axon.Ipc.ProducerFinished(), "signal")


class MessageDemuxer(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    ignore_first = True
    protocol=None
    
    def demuxFilter(self, message):
        if len(message) == 3:
            if message[0] == "message":
                return True
        return False

    def getOutbox(self, message):
        skip = False
        print "MESSAGE",
        fromuser = message[1]
        text = message[2]
        print "FROM USER", fromuser, "TEXT", text
         
        bundle = self.bundles.get(fromuser, None)
                                 
        if bundle == None:
            print "NOT SEEN THIS USER BEFORE"
            protocol = self.protocol
            bundle = {
                "outbox" : self.addOutbox("outbox_tohandler"),
                "signal" : self.addOutbox("signal_tohandler"),
                "handler" : protocol(message=message),
            }

            # Brings up all sorts of issues, thinking about it...
            l1 = self.link( (self,bundle["outbox"]), (bundle["handler"], "inbox") )
            l2 = self.link( (self,bundle["signal"]), (bundle["handler"], "control") )

            l3 = self.link( (bundle["handler"], "outbox"), (self, "outbox"), passthrough=2 )
            l4 = self.link( (bundle["handler"], "signal"), (self, "signal"), passthrough=2 ) # probably wrong...
            print "ACTIVATING", bundle["handler"]
            bundle["handler"].activate()
            bundle["links"] = [l1, l2, l3, l4]
            self.bundles[fromuser] = bundle

            print "USERBUNDLE", bundle

            if self.ignore_first:
                skip = True
        outbox = bundle["outbox"]

        return outbox,skip

    def initLocalState(self):
        self.bundles = {}

    def main(self):
        self.initLocalState()
        bundles = {}
        print "INITIALISING DEMUXER"
        print self.ignore_first
        while not self.dataReady("control"):
            yield 1
            for message in self.Inbox():
                print "PROCESSING MESSAGE", message
                if self.demuxFilter(message):
                    outbox,skip = self.getOutbox(message)
                    if skip:
                        continue
                        
                    self.send(message, outbox)
                        

        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
           self.send(Axon.Ipc.ProducerFinished(), "signal")

def AIMBotServerCore(screenname, password, protocol):
    print "ULTRABOT STARTING UP"
    print "For the moment, ultrabot may not say anything when it's told anything"

    return Graphline(
               AIM = AIMHarness(screenname, password),
               ADAPTER = MessageDemuxer(ignore_first=True,
                                        protocol=protocol),
               linkages = {               
                   ("AIM", "outbox"): ("ADAPTER","inbox"),
                   ("ADAPTER","outbox"):  ("AIM", "inbox"),
               }
           )

def UserHandler(command="cat /etc/motd"):
    C = command
    def mkHandler(**argd): # We receive the message that caused the demuxer to start us up...
        user = argd.get("message",["message","userid","..."])[1]
        command = C
        return Graphline(
                   ADAPTER = AIMUserTalkAdapter(user=user),
                   CONSOLEAPP = UnixProcess(command), # Actually, ought to abstract this tbh
                   linkages = {
                       ("self", "inbox"): ("ADAPTER","from_aim"),
                       ("ADAPTER","to_aim"):  ("self", "outbox"),

                       ("CONSOLEAPP","outbox"): ("ADAPTER","from_user"),
                       ("ADAPTER","to_user"): ("CONSOLEAPP","inbox"),
                   }
               )
    return mkHandler

if __name__ == '__main__':
    import sys
    if len(sys.argv)<3:
        print "Usage:"
        print "     ",
        print sys.argv[0], "username", "password"
        sys.exit(0)
        
    username,password = sys.argv[1],sys.argv[2]

    AIMBotServerCore(
          username, password,                                            # Listen on this username/password
          protocol=UserHandler(command="/home/zathras/tmp/rules_test.py") # This is our protocol...
    ).run()

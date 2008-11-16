#!/usr/bin/env python
##
## (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import cgi
import time
import Axon
from Kamaelia.Protocol.AIM.AIMHarness import AIMHarness
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.UnixProcess import UnixProcess


def outformat(data, buddyname):
    buddyname = buddyname.lower()
    if data[0] == "buddy online" and data[1]["name"].lower() ==  buddyname:
        return "%s is online" % data[1]["name"]
    elif data[0] == "message" and data[1].lower() == buddyname:
        return "%s: %s" % (data[1], data[2])
    elif data[0] == "error":
        return ": ".join(data)


# def ConsoleUser():
#     return UnixProcess("/home/zathras/tmp/rules_test.py")

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
    command = "cat /etc/motd"
    def main(self):
        bundles = {}
        print "INITIALISING DEMUXER"
        print self.ignore_first, self.command
        while not self.dataReady("control"):
            yield 1
            for message in self.Inbox():
                print "PROCESSING MESSAGE", message
                if len(message) == 3:
                    if message[0] == "message":
                        print "MESSAGE",
                        fromuser = message[1]
                        text = message[2]
                        print "FROM USER", fromuser, "TEXT", text
                         
                        bundle = bundles.get(fromuser, None)
                                                 
                        if bundle == None:
                            print "NOT SEEN THIS USER BEFORE"
                            bundle = {
                                "outbox" : self.addOutbox("outbox_tohandler"),
                                "signal" : self.addOutbox("signal_tohandler"),
                                "handler" : UserHandler(user=fromuser, command=self.command),
                            }

                            # Brings up all sorts of issues, thinking about it...
                            l1 = self.link( (self,bundle["outbox"]), (bundle["handler"], "inbox") )
                            l2 = self.link( (self,bundle["signal"]), (bundle["handler"], "control") )

                            l3 = self.link( (bundle["handler"], "outbox"), (self, "outbox"), passthrough=2 )
                            l4 = self.link( (bundle["handler"], "signal"), (self, "signal"), passthrough=2 ) # probably wrong...
                            print "ACTIVATING", bundle["handler"]
                            bundle["handler"].activate()
                            bundle["links"] = [l1, l2, l3, l4]
                            bundles[fromuser] = bundle

                            print "USERBUNDLE", bundle

                            if self.ignore_first:
                                continue
                        
                        self.send(message, bundle["outbox"])
                        

        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
           self.send(Axon.Ipc.ProducerFinished(), "signal")

def UserHandler(user="zathmadscientist", command="cat /etc/motd"):
    """
       AIM HANDLER (external)
   inbox|   ^outbox
        |   |
        V   |
       ADAPTER
        |   ^
        |   |
        V   |
       CONSOLE APP
    """
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

def UltraBot(screenname, password):
    print "ULTRABOT STARTING UP"
    print "For the moment, ultrabot may not say anything when it's told anything"

    return Graphline(
               AIM = AIMHarness(screenname, password),

               ADAPTER = MessageDemuxer(ignore_first=True,
                                        handler=UserHandler,
                                        command="/home/zathras/tmp/rules_test.py"),

               linkages = {               
                   ("AIM", "outbox"): ("ADAPTER","inbox"),
                   ("ADAPTER","outbox"):  ("AIM", "inbox"),
               }
           )

if __name__ == '__main__':


    UltraBot(bot_id, bot_password).run()

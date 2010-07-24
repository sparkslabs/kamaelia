#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
## -------------------------------------------------------------------------

import cgi
import time
import Axon
from Kamaelia.Protocol.AIM.AIMHarness import AIMHarness
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.UnixProcess import UnixProcess

def sendTo(recipient, text):
    return ("message", recipient, text)

def outformat(data, buddyname):
    buddyname = buddyname.lower()
    if data[0] == "buddy online" and data[1]["name"].lower() ==  buddyname:
        return "%s is online" % data[1]["name"]
    elif data[0] == "message" and data[1].lower() == buddyname:
        return "%s: %s" % (data[1], data[2])
    elif data[0] == "error":
        return ": ".join(data)

def ConsoleUser():
    return UnixProcess("/home/zathras/tmp/rules_test.py")


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
    def main(self):

        while not self.dataReady("control"):
            for message in self.Inbox("from_user"):
                 message = cgi.escape(message,1)
                 lines = message.split("\n")
                 for line in lines:
                     time.sleep(self.ratelimit)
                     message = sendTo(self.user, line ) # FIXME: Crap name
                     self.send(message, "to_aim")

            for message in self.Inbox("from_aim"):
                 if len(message) == 3:
                     if message[0] == "message":
                         text = message[2]+"\n"
                         self.send(text, "to_user")

            if not self.anyReady():
                self.pause()
        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
           self.send(Axon.Ipc.ProducerFinished(), "signal")

def UltraBot(screenname, password):
    print "ULTRABOT STARTING UP"
    print "For the moment, ultrabot may not say anything when it's told anything"

    return Graphline(
               AIM = AIMHarness(screenname, password),

               ADAPTER = AIMUserTalkAdapter(),
               USER = ConsoleUser(),
               linkages = {               
                   ("AIM", "outbox"): ("ADAPTER","from_aim"),
                   ("USER","outbox"):       ("ADAPTER","from_user"),

                   ("ADAPTER","to_aim"):  ("AIM", "inbox"),
                   ("ADAPTER","to_user"): ("USER","inbox"),
               }
           )

if __name__ == '__main__':

    import sys
    if len(sys.argv)<3:
        print "Usage:"
        print "     ",
        print sys.argv[0], "username", "password"
        sys.exit(0)

    username,password = sys.argv[1],sys.argv[2]

    UltraBot(username, password).run()
    

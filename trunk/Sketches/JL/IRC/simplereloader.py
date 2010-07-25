#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Component import component
import IRCClient
import formatters
from IRCClient import SimpleIRCClientPrefab
import time, os

class SimpleReloader(component):
    Outboxes = {"irc" : "to IRC, for user responses and login",
                "outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",
                }
    
    def __init__(self, channel='#kamtest', name="reloadbot"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SimpleReloader, self).__init__()
        self.channel = channel
        self.name = name
        self.debugger.addDebugSection("SimpleReloader.main", 0)

    def login(self):
        """registers with the IRC server"""
        self.send(("NICK", self.name), "irc")
        self.send(("USER", self.name, self.name, self.name, self.name), "irc")
        self.send(("PRIVMSG", 'nickserv', "identify abc123"), "irc")
        self.send(("JOIN", self.channel), "irc")

    def main(self):
        """Main loop"""
        self.login()
        yield 1        
        while True:
            yield 1 
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if (data[2] == self.channel or data[0] == 'NICK'):
                    self.doStuff(data)

    def doStuff(self, msg):
        if msg[0] == 'PRIVMSG' and msg[3].split(':')[0] == self.name:
            words = msg[3].split()[1:]
            if words[0] == 'reload' and len(words) > 1:
                try:
                    exec("reload(%s)" % words[1])
                except (NameError, TypeError):
                    self.send("'%s' not a module\n" % words[1], "irc")            
        formatted = formatters.outformat(msg, defaultChannel=self.channel)
        self.send(formatted)

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
Graphline(irc = SimpleIRCClientPrefab('irc.freenode.net', 6667),
          reloader = SimpleReloader(),
          cons = ConsoleEchoer(),
         linkages = {("reloader", "irc") : ("irc", "inbox"),
                     ("irc", "outbox") : ("reloader", "inbox"),
                     ("reloader", "outbox") : ("cons", "inbox"),
                    }
         ).run()

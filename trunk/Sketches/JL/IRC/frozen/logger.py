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

from IRCClient import SimpleIRCClientPrefab
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.PureTransformer import PureTransformer
from Axon.Component import component
import time

class IRCFormatter(component):
    
    Outboxes = {"outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",
                }
        
    def __init__(self, nick, channel):
        super(IRCFormatter, self).__init__()
        self.nick = nick  #the nick argument is actually pretty useless
        self.channel = channel
        
    def main(self):
        while True:
            yield 1
            
            if not self.anyReady():
                self.pause()

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                data2 = self.format(data)
                if data[2] == channel:
                    self.send(data2, "outbox")
                else:
                    self.send(data2, "system")
            
    def format(self, data):
        nick = self.nick
        channel = self.channel
        
        msgtype, sender, recipient, body = data
        end = '\n'
        if msgtype == 'PRIVMSG':
            if body[0:5] == '[off]': #we don't want to log lines prefixed by "[off]"
                return
            text = '<%s> %s' % (sender, body)
        elif msgtype == 'JOIN' :
            text = '*** %s has joined %s' % (sender, recipient)
        elif msgtype == 'PART' :
            text = '*** %s has parted %s' % (sender, recipient)
        elif msgtype == 'NICK':
            text = '*** %s is now known as %s' % (sender, recipient)
        elif msgtype == 'ACTION':
            text = '*** %s %s' % (sender, body)
        elif msgtype == 'TOPIC':
            text = '*** %s changed the topic to %s' % (sender, body)
        elif msgtype == 'QUIT': #test this, channel to outbox, not system
            text = '*** %s has quit IRC' % (sender)
        elif msgtype == 'MODE' and recipient == self.channel:
            text = '*** %s has set channel mode: %s' % (sender, body) 
        elif msgtype > '000' and msgtype < '400':
            text = 'Reply %s from %s to %s: %s' % data
        elif msgtype >= '400' and msgtype < '600':
            text = 'Error! %s %s %s %s' % data
        elif msgtype >= '600' and msgtype < '1000':
            text = 'Unknown numeric reply: %s %s %s %s' % data
        else:
            text = '%s from %s: %s' % (msgtype, sender, body)
        return text + end

channel = '#kamtest'

def Logger():
    return Graphline(irc = SimpleIRCClientPrefab(host="irc.freenode.net", nick="jinnaslogbot", \
                                               defaultChannel=channel),
                   formatter = IRCFormatter("jinnaslogbot", channel),
                   log = SimpleFileWriter("%s%i.log" % (channel[1:], time.time())),
                   info = SimpleFileWriter("%s%i.info" % (channel[1:], time.time())),
                   linkages = {("irc" , "outbox") : ("formatter", "inbox"),
                               ("irc", "signal") : ("formatter", "control"),
                               ("formatter", "outbox") : ("log", "inbox"),
                               ("formatter", "system") : ("info", "inbox"),
                               ("formatter", "signal") : ("log", "control"),
                               ("log", "signal") : ("info", "control"),
                               }
                     )
    
if __name__ == '__main__':
    Logger().run()

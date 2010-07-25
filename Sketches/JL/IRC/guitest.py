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

import string
from Axon.Component import component

defaultChannel = '#kamtest'
def informat(text):
    if text[0] != '/' or text.split()[0] == '/': #in case we were passed "/ word words", or simply "/"
        return ('PRIVMSG', defaultChannel, text)
    words = text.split()
    tag = words[0]
    tag = tag.lstrip('/').upper()
    if tag == 'MSG':
        tag = 'PRIVMSG'
    try:
        if tag == 'QUIT' and len(words) >= 2:
            return (tag, string.join(words[1:]))
        elif tag in ('PRIVMSG', 'MSG', 'NOTICE', 'KILL', 'TOPIC', 'SQUERY') and len(words) >= 3:
            return (tag, words[1], string.join(words[2:]))
        elif tag == 'KICK' and len(words) >= 4:
            return (tag, words[1], words[2], string.join(words[3:]))
        elif tag == 'USER':
            return (tag, words[1], words[2], words[3], string.join(words[4:]))
        elif tag == 'ME' and len(words) >= 2:
            return (tag, defaultChannel, string.join(words[1:]))
        else: 
            words[0] = tag
            if tag: #only false if we were passed "/" as text
                return words
    except IndexError:
        words[0] = tag
        return words

def outformat(data):
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
    elif msgtype == 'MODE' and recipient == defaultChannel:
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

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Axon.Ipc import producerFinished
    from IRCClient import IRC_Client
    from Textbox import Textbox
    from TextDisplayer import TextDisplayer
    
    #to connect to IRC, you need to type "/nick yournickname" followed by "/user arg1 arg2 arg3 arg4"
    #very fast, before the connection times out. 

    testfile = '/home/jlei/files/InputFormatter_test.txt'
    class LineFileReader(component):
        def main(self):
            fle = open(testfile, "r")
            data = "dummy"
            while data:
                yield 1
                data = fle.readline()
                if data and data != '\n':
                    self.send(data.rstrip('\n'))
            self.send(producerFinished(), "signal")

    g = Graphline(irc = IRC_Client(),
                  tcp = TCPClient('irc.freenode.net', 6667),
                  linkages = {("self", "inbox") : ("irc" , "talk"),
                              ("irc", "outbox") : ("tcp" , "inbox"),
                              ("tcp", "outbox") : ("irc", "inbox"),
                              ("irc", "heard") : ("self", "outbox"),
                              }
                  )

    Pipeline(Textbox(position=(0,340)), PureTransformer(informat), g, PureTransformer(outformat),
             TextDisplayer()
             ).run()

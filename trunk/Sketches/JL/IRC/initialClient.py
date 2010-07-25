#! /usr/bin/env python
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

#initial client
import time
import socket

def commandify(head, *body):
    for token in body:
        head += ' ' + token
    return head + ' \r\n'

def attachColon(*aTuple):
    result = list()
    for entry in aTuple:
        if ' ' in entry:
            result.append(':'+entry)
        else:
            result.append(entry)
    return tuple(result)

class ircClient:
    
    def __init__(self, nick,
                 uname = 'anonymous',
                 host='none',
                 server='none',
                 realname='Python IRC Client',
                 ircNetwork='irc.freenode.net',
                 bufsize = 8000,
                 port=6667):
        self.nick = nick
        self.uname = uname
        self.host = host
        self.server = server
        self.realname = realname
        self.ircNetwork = ircNetwork
        self.bufsize = bufsize
        self.port = port
        self.sock = self.connect()
        self.connectToNetwork()
        
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((self.ircNetwork, self.port))
        return sock

    def connectToNetwork(self):
        sock = self.sock
        sock.send(commandify('NICK', self.nick))
        uname_, host_, server_, realname_ = attachColon(self.uname, self.host, self.server, self.realname)
        sock.send(commandify('USER', uname_, host_, server_, realname_))
        
##    def mainLoop(self):
##        print
##        eval(read()))
##        self.mainLoop()
        
    def say(self, chan, text):
        self.sock.send(commandify('PRIVMSG', chan, ':' + text))

    def flushOutput(self): #new
        print self.sock.recv(self.bufsize)

    def join(self, chan):
        self.sock.send(commandify('JOIN', chan))

if __name__ == '__main__':
    nick = 'jollyolst'
    cli = ircClient(nick, uname='test_user1', bufsize = 4000)
    channel = '#kamtest'
    time.sleep(0.5)
    cli.flushOutput()
    cli.join(channel)
    time.sleep(0.9)
    cli.say(channel, 'hello, I am a python client')
    cli.say(channel, 'What?')
    cli.sock.close()

if 0:
    nick = 'guesswho'
    cli = ircClient(nick, uname='test_user2', bufsize = 4000)
    channel = '#kamtest'
    time.sleep(0.5)
    cli.join(channel)
    time.sleep(0.5)
    cli.say(channel, 'No -- I am your father.')
    cli.flushOutput()
    cli.sock.close()
    

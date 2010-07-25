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

import socket
import select
import threading
           
class inputThread(threading.Thread):
    def say(self, chan, words):
        send = 'PRIVMSG %s :%s\r\n' % (chan, words)
        sock.send(send)
            
    def run(self):
        global done
        while not done:
            msg = raw_input('IRC > ')
            if msg == 'QUIT':
                sock.send('QUIT')
                done = True
            self.say(channel, msg)


class outputThread(threading.Thread):
      
    def checkForMessages(self):
        read_list, write_list, error_list = \
                   select.select([sock], [], [sock], 0)
        if sock in read_list:
            raw = sock.recv(8000)
            self.printOutput(raw)

    def run(self):
        while not done:
            self.checkForMessages()

    def printOutput(self, text):
        if '\r' in text:
            text = text.replace('\r', '\n')
        lines = text.split('\n')
        for one_line in lines:
            if len(one_line) > 0:
                print self.formatLine(one_line)

    def formatLine(self, line):
        words = line.split()
        sender = ""
        if line[0] == ':' and len(words) >= 2:
            sender = line[1:line.find('!')]
            words = words[1:]
        tag = words[0].upper()
        if tag == 'PRIVMSG':
            return '%s: %s' % (sender, words[2])
        else:
            return line
    
network = 'irc.freenode.net'
port = 6667
nick = 'lolasuketo'
uname = 'jinna'
host = 'jlei-laptop'
server = 'comcast'
realname = 'python irc bot'
channel = '#kamtest'

sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
sock.connect ( ( network, port ) )
sock.send ('NICK %s \r\n' % nick )
sock.send ( 'USER %s %s %s :%s r\n' % (uname, host, server, realname))
sock.send ( 'JOIN #kamtest\r\n' )

done = False
input1 = inputThread()
output1 = outputThread()
input1.start()
output1.start()

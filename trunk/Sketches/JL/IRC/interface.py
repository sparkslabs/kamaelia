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

from IRCIPC import *
from Axon.Component import component

class Interface(component):
    #standard inboxes and outboxes
    def __init__(self):
        super(Interface, self).__init__()
        self.defaultChannel = '#kamtest'

    def main(self):
        while 1:
            yield 1
            if self.dataReady('inbox'):
                data = self.recv('inbox')
                tokens = data.split()
                head = tokens[0].lower()
                
                if head == '/nick':
                    toSend = IRCIPCChangeNick(nick = tokens[1])
                elif head == '/quit':
                    toSend = IRCIPCDisconnect()
                #IRCIPCConnect
                #IRCIPCLogin
                elif head == '/join':
                    toSend = IRCIPCJoinChannel(channel = tokens[1])
                elif head == '/part':
                    toSend = IRCIPCLeaveChannel(channel = tokens[1])
                elif head == '/topic':
                    toSend = IRCIPCSetChannelTopic(channel = tokens[1], topic = tokens[2])
                else:
                    toSend = IRCIPCSendMessage(recipient = self.defaultChannel, msg = data)
                self.send(toSend)


if __name__ == '__main__':
    print "running"
    from ryans_irc_client import *
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    host = 'irc.freenode.net'
    port = 6667
    nick = 'ryans_irc_client'
    pwd = ''
    user = 'jinna'

    Graphline(irc = IRCClient(host, port, nick, pwd, user),
              tcp = TCPClient(host, port),
              interface = Interface(),
              inputter = ConsoleReader(),
              out = ConsoleEchoer(),
              linkages = {
                  ("inputter", "outbox") : ("interface", "inbox"),
                  ("inputter", "signal") : ("interface", "control"),
                  ("interface", "outbox") : ("irc", "ipcObjects"),
                  ("interface", "signal") : ("irc", "control"),
                  ("irc", "outbox") : ("tcp", "inbox"),
                  ("irc", "signal") : ("tcp", "control"),
                  ("tcp", "outbox") : ("irc", "inbox"),
                  ("tcp", "signal") : ("irc", "control"),
                  ("irc", "heard") : ("out", "inbox")
                  }
              ).run()

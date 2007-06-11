#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#	 All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#	 http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#	 not this notice.
# (2) Reproduced in the COPYING file, and at:
#	 http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
"""\
=======================
IRC Logging Bot
=======================

This component interacts with an IRC server via its inbox and outbox.

This component does not terminate.
"""

import sys
import datetime
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.debug import debug
import string

from IRCIPC import *
from Kamaelia.Internet.TCPClient import TCPClient

class IRCClient(component):
    """\
    IRCClient() -> IRCClient 
    """
    Inboxes = {
        "inbox"       : "messages received from the server",
        "control"     : "receives shutdown signals",
        "user"  : "messages from the user"
    }
    
    Outboxes = {
        "outbox"      : "messages to send over TCP",
        "signal"      : "sends shutdown signals",
        "heard"       : "things from the server.",
    }

    ERR_NOSUCHNICK           = 401
    ERR_NOSUCHSERVER         = 402	
    ERR_NOSUCHCHANNEL        = 403
    ERR_CANNOTSENDTOCHAN     = 404
    ERR_TOOMANYCHANNELS      = 405
    ERR_WASNOSUCHNICK        = 406
    ERR_TOOMANYTARGETS       = 407
    #more to come

    MapIPCToFunction = {
        IRCIPCChangeNick      : (lambda x, self : self.changeNick(x.nick)),
        IRCIPCDisconnect      : (lambda x, self : self.disconnect()),
        IRCIPCConnect         : (lambda x, self : self.connect()),
        IRCIPCLogin           : (lambda x, self : self.login(x.nick, x.password, x.channel)),
        IRCIPCJoinChannel     : (lambda x, self : self.joinChannel(x.channel)),
        IRCIPCSendMessage     : (lambda x, self : self.say(x.recipient, x.msg)),
        IRCIPCLeaveChannel    : (lambda x, self : self.leaveChannel(x.channel)),
        IRCIPCSetChannelTopic : (lambda x, self : self.changeTopic(x.channel, x.topic)),
    }
        
    def __init__(self, host, port, nick, password, username):
        super(IRCClient, self).__init__()
        self.host = host
        self.port = port

        self.username = username        
        self.nick = nick
        self.password = password
        self.channels = {}

        self.debugger = debug()
        self.debugger.useConfig()
        sections = {"IRCClient.login" : 1,
                    "IRCClient.connect" : 1,
                    "IRCClient.disconnect" : 1,
                    "IRCClient.joinChannel" : 1,
                    "IRCClient.main" : 1}
        self.debugger.addDebug(**sections)
        
    def changeNick(self, newnick):
        self.nick = newnick
        self.send("NICK %s\r\n" % newnick, "outbox")

    def joinChannel(self, channel):
        self.channels[channel] = True
        self.send("JOIN %s\r\n" % channel, "outbox")

    def say(self, recipient, message):
        self.send("PRIVMSG %s :%s\r\n" % (recipient, message), "outbox")

    def leaveChannel(self, channel):
        self.send("PART %s\r\n" % channel, "outbox")

    def changeTopic(self, channel, topic):
        self.send("TOPIC %s :%s\r\n" % (channel, topic), "outbox")

    def login(self, nick, password, username):
        self.send("NICK %s\r\n" % nick, "outbox")
        if password:
            self.send("PASS %s\r\n" % password)
        if not username:
            username = nick
        self.send ("USER %s %s %s :%s\r\n" % (username, username, username, "Kamaelia IRC Bot"), "outbox")
        self.logging = True
        self.debugger.debug("IRCClient.login", 1, "sent NICK, PASS, and USER to outbox")

    def main(self):
        """Main loop"""
        
        self.login(self.nick, self.password, self.username)
        self.joinChannel("#kamtest")
        readbuffer = ""

        while 1:
            yield 1
            
            if self.dataReady("ipcObjects"):
                command = self.recv("ipcObjects")
		#so can be shut down 
                self.MapIPCToFunction[command.__class__](command, self) # get the appropriate function for that type of message and pass the message to it
                
            elif self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(IRCIPCDisconnected(), "outbox")
                
            elif self.dataReady("inbox"):
                readbuffer += self.recv("inbox")
                self.debugger.debug("IRCClient.main", 10, readbuffer)
                lines = string.split(readbuffer, "\n")
                readbuffer = lines.pop() #the remainder after final \n

                for line in lines:
                    print line
                    line = string.rstrip(line)
                    splitline = string.split(line)
                    linesender = ""
                    if splitline[0][0] == ":":
                        linesender = string.split(splitline[0][1:],"!")[0]
                        splitline.pop(0)

                    if splitline[0] == "NOTICE": #ignorable
                        msg = string.join(splitline[2:], ' ')
                        msg = ('NOTICE', splitline[1], msg)
                        self.send(msg, 'heard')
                        
                    elif splitline[0] == "PING":
                        # should alter this to consider if no second part given
                        msgsend = "PONG %s\r\n" % splitline[1]
                        self.send(msgsend, "outbox")

                    elif splitline[0] == "PRIVMSG":
                        msg = string.join(splitline[2:], " ")[1:]
                        self.send(IRCIPCMessageReceived(sender=linesender, recipient=splitline[1], msg=msg), "heard") 

                    elif splitline[0] == "PART":
                        msg = ( "PART", linesender, splitline[1] )
                        self.send(  msg, "heard")

                    elif splitline[0] == "JOIN":
                        msg = ( "JOIN", linesender, splitline[1] )
                        self.send(msg, "heard")
                        
                    elif splitline[0] == "QUIT":
                        msg = string.join(splitline[1:], " ")[1:]
                        msg = ( "PART", linesender, splitline[1], msg )
                        self.send(msg, "heard")

                    elif splitline[0] == "TOPIC":
                        msg = string.join(splitline[2:], " ")[1:]
                        msg = ( "TOPIC", linesender, splitline[1], msg )
                        self.send(msg, "heard")
                        
                    elif splitline[0] == "NICK":
                        msg = string.join(splitline[1:], " ")[1:]
                        msg = ( "NICK", linesender, splitline[1], msg )
                        self.send(msg, "heard")

                    elif splitline[0] > '000' and splitline[0] < '300 
            else:
                self.pause()

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
host = 'irc.freenode.net'
port = 6667
nick = 'ryans_irc_client'
pwd = ''
user = 'jinna'

if __name__ == '__main__':
    Graphline(irc = IRCClient(host, port, nick, pwd, user),
              tcp = TCPClient(host, port),
              out = ConsoleEchoer(),
              linkages = {
                  ("irc", "outbox") : ("tcp", "inbox"),
                  ("irc", "signal") : ("tcp", "control"),
                  ("tcp", "outbox") : ("irc", "inbox"),
                  ("tcp", "signal") : ("irc", "control"),
                  ("irc", "heard") : ("out", "inbox")
                  }
              ).run()

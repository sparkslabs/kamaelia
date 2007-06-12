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
"""
=======================
IRC Logging Bot
=======================

This component interacts with an IRC server via its inbox and outbox.

This component does not terminate.
"""

import sys
import datetime
import timeIRCIPCChangeNick
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
import string

from IRCIPC import *

class IRCClient(component):
    """\
    IRCClient() -> IRCClient 
    """
    Inboxes = {
        "inbox"       : "simple instructions for the bot",
        "control"     : "UNUSED",
        
        "_tcpinbox"   : "messages received over TCP",     
        "_tcpcontrol" : "for receiving connection shutdown signals from TCPClient"
    }
    
    Outboxes = {
        "outbox"      : "events e.g. private messages received",
        "signal"      : "UNUSED",
        
        "_tcpoutbox"  : "messages to send over TCP",
        "_tcpsignal"  : "shutdown signals for TCPClient"
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
        IRCIPCChangeNick      : (lambda x : self.changeNick(x.nick)),
        IRCIPCDisconnect      : (lambda x : self.disconnect()),
        IRCIPCConnect         : (lambda x : self.connect()),
        IRCIPCLogin           : (lambda x : self.login(x.nick, x.password, x.channel)
        IRCIPCJoinChannel     : (lambda x : self.joinChannel(x.channel)),
        IRCIPCSendMessage     : (lambda x : self.say(x.recipient, x.msg)),
        IRCIPCLeaveChannel    : (lambda x : self.leaveChannel(x.channel)),
        IRCIPCSetChannelTopic : (lambda x : self.changeTopic(x.channel, x.topic)),
    }
    
    def connect(self):
        self.tcpclient = TCPClient(self.host, self.port)
        self.link((self, "_tcpoutbox"), (self.tcpclient, "inbox"))
        self.link((self, "_tcpsignal"), (self.tcpclient, "control"))
        self.link((self.tcpclient, "outbox"), (self, "_tcpinbox"))
        self.link((self.tcpclient, "signal"), (self, "_tcpcontrol"))
                
        self.addChildren(self.tcpclient)

    def disconnect(self):
        self.unlink((self, "_tcpoutbox"), (self.tcpclient, "inbox"))
        self.unlink((self, "_tcpsignal"), (self.tcpclient, "control"))
        self.unlink((self.tcpclient, "outbox"), (self, "_tcpinbox"))
        self.unlink((self.tcpclient, "signal"), (self, "_tcpcontrol"))
        self.tcpclient = None
        
    def __init__(self, host, port, nick, password, username):
        super(IRCClient, self).__init__()
        self.host = host
        self.port = port

        self.username = username        
        self.nick = nick
        self.password = password
        self.channels = {}
        
    def changeNick(self, newnick):
        self.nick = newnick
        self.send("NICK %s\r\n" % newnick, "_tcpoutbox")

    def joinChannel(self, channel):
        self.channels[channel] = True
        self.send("JOIN %s\r\n" % channel, "_tcpoutbox")

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
        self.send ("USER %s %s %s :%s\r\n" % (username, nick, nick, "Kamaelia IRC Bot"), "outbox")
        self.logging = True

    def main(self):
        """Main loop"""
        
        self.connect()
        self.login()
        self.joinChannel()
        readbuffer = ""

        while 1:
            yield 1
            
            if self.dataReady("inbox"):
                command = self.recv("inbox")
                self.MapIPCToFunction(command.__class__)(command) # get the appropriate function for that type of message and pass the message to it
                self.send(command, "outbox")
                
            elif self.dataReady("_tcpcontrol"):
                msg = self.recv("_tcpcontrol")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(IRCIPCDisconnected(), "outbox")
                    self.disconnect()
                
            elif self.dataReady("_tcpinbox"):
                readbuffer += self.recv("_tcpinbox")
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
                        pass
                    elif splitline[0] == "PING":
                        # should alter this to consider if no second part given
                        msgsend = "PONG %s\r\n" % splitline[1]
                        self.send(msgsend, "outbox")

                    elif splitline[0] == "PRIVMSG":
                        msg = string.join(splitline[2:], " ")[1:]
                        self.send(IRCIPCMessageReceived(sender=linesender, recpient=splitline[1], msg=msg), "outbox") 

                    elif splitline[0] == "PART":
                        msg = ( "PART", linesender, splitline[1] )
                        self.send(msg, "heard")

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
            else:
                self.pause()

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

This component interacts with an IRC server via its inbox and outbox. It should be connected to a TCP client component

This component does not terminate.
"""

import sys
import datetime
import time
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
import string

class IRCBot(component):
    """\
    IRCBot() -> new IRCBot 
    """
    Inboxes = { "inbox"   : "messages received over TCP",
                "command" : "simple instructions for the bot",
                "control" : "UNUSED"
              }
    Outboxes = { "outbox" : "messages to send over TCP",
                 "signal" : "UNUSED",
                 "heard"   : "events e.g. private messages received",
               }

    ERR_NOSUCHNICK           = 401
    ERR_NOSUCHSERVER         = 402	
    ERR_NOSUCHCHANNEL        = 403
    ERR_CANNOTSENDTOCHAN     = 404
    ERR_TOOMANYCHANNELS      = 405
    ERR_WASNOSUCHNICK        = 406
    ERR_TOOMANYTARGETS       = 407
    #more to come

    def writeHeard(self, src):
        t = datetime.datetime.now()
        epochsecs = time.mktime(t.timetuple())
        msg = ("%d" % epochsecs) + " " + string.join(src, " ") + "\n"
        self.send(msg, "heard")

    def __init__(self, nick, password, channel, username):
        super(IRCBot, self).__init__()
        self.nick = nick
        self.password = password
        self.channel = channel
        self.username = username

    def changeNick(self, newnick):
        self.nick = newnick
        self.send("NICK %s\r\n" % newnick, "outbox")

    def joinChannel(self):
        self.send( 'JOIN %s\r\n' % self.channel, "outbox")
    def say(self, recipient, message):
        self.send("PRIVMSG %s :%s\r\n" % (recipient, message), "outbox")
    def leaveChannel(self, channel):
        self.send("PART %s\r\n" % channel, "outbox")
    def changeTopic(self, channel, topic):
        self.send("TOPIC %s :%s\r\n" % (channel, topic), "outbox")

    def login(self):
        self.send("NICK %s\r\n" % self.nick, "outbox")
        if self.password:
            self.send("PASS %s\r\n" % self.password)
        if not self.username:
            self.username = self.nick
        self.send ("USER %s %s %s :%s\r\n" % (self.username,self.nick,self.nick, "Kamaelia IRC Bot"), "outbox")
        self.logging = True

    def main(self):
        """Main loop"""
        self.login()
        self.joinChannel()
        readbuffer = ""

        while 1:
            yield 1
            
            if self.dataReady("command"):
                command = self.recv("command")
                self.send(command, "outbox")
            elif self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send("SIGNALCLOSE", "heard")
                    self.send(msg, "signal")
                    return
            elif self.dataReady("inbox"):
                readbuffer += self.recv("inbox")
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
                        msg = ( "PRIVMSG", linesender, splitline[1], msg )
                        self.send(msg, "heard")

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

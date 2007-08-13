#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#

"""\
===================
IRC Channel Logger
===================
Logger writes all traffic it receives to text files, changing files once per
day. It is built using IRC_Client as its core.  



Example Usage
-------------
To log the channel #sillyputty on server my.server.org::

    Logger('#sillyputty', host="my.server.org").run()

It will now log all messages to #kamtest except those prefixed by "[off]".



More Detail
-----------
BasicLogger is a higher-level IRC client that is meant to link to the base
client found in IRCClient.py. It sends command tuples to its "irc" outbox, and
receives them via its "inbox", allowing it to implement login, and ping
response. It uses IRC_Client's tuple-based output format to achieve some
demultiplexing of IRC output as well, though not of the multiple-channel sort.

BasicLogger depends heavily on the LoggerFunctions module. See LoggerFunctions
for a list of queries it responds to, how it formats the date and time, and how
it determines file names. 

Logger ultimately links BasicLogger's "irc" outbox to IRC_Client's "talk" inbox.
It also utilizes two Carousels and SimpleFileWriters. 



How it works
-------------
Logger writes everything it hears to two files in the specified directory. The
filenames are in the format "givenchannelnameDD-MM-YYYY.log" and
"givenchannelnameDD-MM-YYYY.info".

BasicLogger writes all channel output to its "outbox" and all other messages to
its "system" box. Once per loop, it checks the current date against its stored
date. If the date has changed, then it changes the name of its logfiles to
reflect the new date and sends the new names to "log_next" and "info_next".
Logger uses this in conjunction with a Carousel to create a new logfile and
close the old one.

By default BasicLogger uses ::outformat::, defined in IRCClient, to format
messages from IRCClient.SimpleIRCClientPrefab before writing to the log. To
format messages differently, pass in a different function to its "formatter"
keyword. 

Logger simply links BasicLogger with a IRCClient.SimpleIRCClientPrefab and two
Carousel-encapsulated SimpleFileWriters. It also slaps timestamps on messages.
It takes any keyword that BasicLogger or IRCClient.SimpleIRCClientPrefab will
take.



Command Line Usage
------------------
One can run Logger from the command line by entering::

    ./Logger.py \#somechannel desirednickname
"""
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Component import component
import IRCClient
import LoggerFunctions
import time, os

__kamaelia_components__ = (SimpleFileWriter, Graphline, Carousel, IRCClient)

class BasicLogger(component):
    """\
    BasicLogger(channel, **kwargs) -> new BasicLogger component

    Keyword arguments:

    - formatter -- function that takes an output tuple of IRC_Client's and
                   outputs a string. Default outformat from IRCClient.py
    - name      -- nickname of the logger bot. Default "jinnaslogbot"
    - logdir    -- directory logs are to be put into. Default is the directory
                   this module is in.
    """
    Outboxes = {"irc" : "to IRC, for user responses and login",
                "outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",

                "log_next" : "for the Log Carousel",
                "info_next" : "for the Info Carousel"
                }

    def __init__(self,
                 channel,
                 formatter=IRCClient.outformat,
                 name="jinnaslogbot",
                 logdir="",
                 password=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(BasicLogger, self).__init__()
        self.channel = channel
        self.format = formatter 
        self.name = name
        self.logdir = logdir.rstrip('/') or os.getcwd()
        self.logdir = self.logdir + '/'
        self.logname = ""
        self.infoname = ""
        self.password = password
        self.debugger.addDebugSection("Logger.main", 0)

        Graphline(log = Carousel(SimpleFileWriter),
                  info = Carousel(SimpleFileWriter),
                  logger = self,
                  linkages = {("logger", "log_next") : ("log", "next"),
                              ("logger", "info_next") : ("info", "next"),
                              ("logger", "outbox") : ("log", "inbox"),
                              ("logger", "system") : ("info", "inbox"),
                              }).activate()

    def login(self):
        """registers with the IRC server"""
        self.send(("NICK", self.name), "irc")
        self.send(("USER", self.name, self.name, self.name, self.name), "irc")
        if self.password:
            self.send(("PRIVMSG", 'nickserv', "identify " + self.password), "irc")
        self.send(("JOIN", self.channel), "irc")
        
    def main(self):
        """Main loop"""
        self.login()
        self.changeDate()
        yield 1
        
        while True:
            if self.currentDateString() != self.lastdatestring:
                self.changeDate()
                
            yield 1 
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                formatted_data = self.format(data)
                if (data[2] == self.channel or data[0] == 'NICK') and formatted_data: #format might return None
                    self.send(formatted_data, "outbox")
                    self.respondToQueries(data) 
                elif formatted_data:
                    self.send(formatted_data, "system")
                    self.respondToPings(data) 

    def respondToPings(self, msg):
        if msg[0] == 'PING':
            self.send(('PONG', msg[1]), 'irc')
            self.send("Sent PONG to %s \n" % msg[1], "system")

    def respondToQueries(self, msg):
        if msg[0] == 'PRIVMSG' and msg[3].split(':')[0] == self.name:
            words = msg[3].split()[1:]
            if len(words) > 1 and words[0] == "reload":
                try:
                    exec("reload(%s)" % words[1])
                    reply = "'%s' reloaded\n" % words[1]
                except:
                    reply = "'%s' isn't a module, or at least not one I can reload.\n" % words[1]
                self.send(('PRIVMSG', self.channel, reply), "irc")
                self.send(self.format(reply), "outbox")
        LoggerFunctions.respondToQueries(self, msg)

    def currentDateString(self):
        """returns the current date"""
        return LoggerFunctions.currentDateString()

    def currentTimeString(self):
        """returns current time"""
        return LoggerFunctions.currentTimeString()

    def getFilenames(self):
        """returns tuple (logname, infoname) according to the parameters given"""
        return LoggerFunctions.getFilenames(self.logdir, self.channel)
    
    def changeDate(self):
        """updates the date and requests new log files to reflect the date"""
        self.lastdatestring = self.currentDateString()
        self.logname, self.infoname = self.getFilenames()
        self.send(self.logname, "log_next")
        self.send(self.infoname, "info_next")

    
def Logger(channel,
           name=None,
           formatter=LoggerFunctions.TimedOutformat,
           logdir="",
           password=None,
           filewriter = LoggerFunctions.AppendingFileWriter,
           **irc_args):
    """\
    Logger(channel, **kwargs) ->
        Prefab that links the IRC components to BasicLogger
        and two Carousel-encapsulated AppendingFileWriters

    Keyword arguments:

    - formatter -- formatter to run incoming messages from IRC_Client through
      before writing to the log. Default TimedOutformat.
    - name      -- nickname of the loggerbot. Default is the default name defined in
                   BasicLogger.
    - logdir    -- directory logs are to be put into. Default is the directory
                   this module is in.
    - **irc_args  -- pointer to a dictionary containing arguments for IRCClient.SimpleIRCClientPrefab
    """
    return Graphline(irc = IRCClient.SimpleIRCClientPrefab(**irc_args),
                     logger = BasicLogger(channel, name=name, formatter=formatter, logdir=logdir, password=password),
                     log = Carousel(filewriter),
                     info = Carousel(filewriter),
                     linkages = {("logger", "irc") : ("irc", "inbox"),
                                 ("irc", "outbox") : ("logger", "inbox"),
                                 ("logger", "log_next") : ("log", "next"),
                                 ("logger", "outbox") : ("log", "inbox"),
                                 ("logger", "info_next") : ("info", "next"),
                                 ("logger", "system") : ("info", "inbox"),
                                }
                     ) 
    
if __name__ == '__main__':
    import sys
    channel = "#kamtest"
    Name = "jinnaslogbot"
    pwd = None
    if len(sys.argv) > 1: channel = sys.argv[1]
    if len(sys.argv) > 2: Name = sys.argv[2]
    if len(sys.argv) > 3: pwd = sys.argv[3]

    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Util.Introspector import Introspector
    from Kamaelia.Chassis.Pipeline import Pipeline
    Pipeline( Introspector(), TCPClient("127.0.0.1",1501) ).activate()
    print "Logging %s as %s" % (channel, Name)
    Logger(channel,
           name=Name,
           password=pwd,
           formatter=(lambda data: LoggerFunctions.HTMLOutformat(data)),
           filewriter = LoggerFunctions.LoggerWriter,
           ).run()

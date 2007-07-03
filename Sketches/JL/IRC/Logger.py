#!/usr/bin/env python

from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Component import component
from IRCClient import outformat
from IRCClient import SimpleIRCClientPrefab
import time, os

"""\
=============
IRC Channel Logger
=============
Logger writes everything it hears to two files in the specified directory. The
filenames are in the format "givenchannelnameDD-MM-YYYY.log" and
"givenchannelnameDD-MM-YYYY.info".

BasicLogger writes all channel output to its "outbox" and all other messages to
its "system" box. 

Example Usage
-------------
To log the channel #sillyputty on server my.server.org::
Logger('#kamtest', host="my.server.org").run()

How it works
-------------
BasicLogger sends messages to IRC via its "irc" outbox, allowing it to log in
and send responses. Once per loop, it checks the current date against its stored
date. If the date has changed, then it changes the name of its logfiles to
reflect the new date and sends the new names to "log_next" and "info_next".
This can be used in conjunction with a Carousel to create a new logfile and
close the old one.

BasicLogger separates channel traffic from all other traffic, sending channel
messages to its "outbox" and everything else to its "system" box.

BasicLogger responds to several private messages. So far, these include
"logfile," "infofile", "help", "date," and "dance." It will not record messages
prefixed by "[off]". 

By default BasicLogger uses ::outformat::, defined in IRCClient, to format
messages from SimpleIRCClientPrefab before writing to the log. To format
messages differently, pass in a different function to its "formatter" keyword. 

Logger simply links BasicLogger with a SimpleIRCClientPrefab and two
Carousel-encapsulated SimpleFileWriters. It also slaps timestamps on messages.
It takes any keyword that BasicLogger or SimpleIRCClientPrefab will take.

One can run Logger from the command line by entering::
./Logger.py \#somechannel
"""

class BasicLogger(component):
    
    Outboxes = {"irc" : "to IRC, for user responses and login",
                "outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",

                "log_next" : "for the Log Carousel",
                "info_next" : "for the Info Carousel"
                }

    def __init__(self, channel, formatter=outformat, name="jinnaslogbot", logdir=""):
        super(BasicLogger, self).__init__()
        self.channel = channel
        self.format = formatter or outformat #in case we get passed in None
        self.name = name or "jinnaslogbot" #"
        self.logdir = logdir.rstrip('/') or os.getcwd()
        self.logdir = self.logdir + '/'
        self.logname = ""
        self.infoname = ""

        Graphline(log = Carousel(SimpleFileWriter),
                  info = Carousel(SimpleFileWriter),
                  logger = self,
                  linkages = {("logger", "log_next") : ("log", "next"),
                              ("logger", "info_next") : ("info", "next"),
                              ("logger", "outbox") : ("log", "inbox"),
                              ("logger", "system") : ("info", "inbox"),
                              }).activate()

    def login(self):
        self.send(("NICK", self.name), "irc")
        self.send(("USER", self.name, self.name, self.name, self.name), "irc")
        self.send(("PRIVMSG", 'nickserv', "identify abc123"), "irc")
        self.send(("JOIN", self.channel), "irc")
        
    def main(self):
        self.login()
        self.changeDate()
        yield 1
        
        while True:
            if self.currentDateString() != self.lastdatestring:
                self.lastdatestring = self.currentDateString()
                self.changeDate()
                
            yield 1 
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                formatted_data = self.format(data)
                if data[2] == self.channel and formatted_data: #format might return None
                    self.send(formatted_data, "outbox")
                elif formatted_data:
                    self.send(formatted_data, "system")
                    self.respond(data) 

    def respond(self, msg):
        if msg[0] == 'PING':
            self.send(('PONG', msg[1]), 'irc')
            self.send("Sent PONG to %s \n" % msg[1], "system")
        if msg[0] == 'PRIVMSG' and msg[2] == self.name:
            words = msg[3].split()
            replyLines = ""
            if words[0] == 'logfile':
                replyLines = [self.logname]
            elif words[0] == 'infofile':
                replyLines = [self.infoname]
            elif words[0] == 'help':
                replyLines = ["Lines prefixed by [off] won't get recorded",
                              "Name: %s   Channel: %s" % (self.name, self.channel)
                              ]
            elif words[0] == 'date':
                replyLines = [self.currentDateString()]
            elif words[0] == 'dance':
                replyLines = ['\x01ACTION does the macarena\x01']

            if replyLines:
                for reply in replyLines:
                    self.send(('PRIVMSG', msg[1], reply), "irc")
                    self.send("Reply: %s \n" % reply, "system")
                
    def currentDateString(self):
       curtime = time.gmtime()
       return time.strftime("%d-%m-%Y", curtime)

    def changeDate(self):
        self.lastdatestring = self.currentDateString()
        self.logname = self.logdir+self.channel.lstrip('#')+self.lastdatestring+'.log'
        self.infoname = self.logdir+self.channel.lstrip('#')+self.lastdatestring+'.info'
        self.send(self.logname, "log_next")
        self.send(self.infoname, "info_next")


def AppendingFileWriter(filename):
    return SimpleFileWriter(filename, mode='ab')

def TimedOutformat(data):
    formatted = outformat(data)
    curtime = time.gmtime()
    timestamp = time.strftime("[%H:%M] ", curtime)
    return timestamp+formatted
    
def Logger(channel, formatter=TimedOutformat, name=None, logdir="", **irc_args):
    return Graphline(irc = SimpleIRCClientPrefab(**irc_args),
                     logger = BasicLogger(channel, formatter=formatter, name=name, logdir=logdir),
                     log = Carousel(AppendingFileWriter),
                     info = Carousel(AppendingFileWriter),
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
    if len(sys.argv) > 1:
        channel = sys.argv[1]
    else: channel = '#kamtest'
    print "Logging " + channel
    Logger(channel, name="aKamaeliaBot").run()

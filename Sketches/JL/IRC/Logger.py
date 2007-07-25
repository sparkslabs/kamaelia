#!/usr/bin/env python

from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Component import component
from IRCClient import outformat
from IRCClient import SimpleIRCClientPrefab
import time, os

"""\
===================
IRC Channel Logger
===================
Logger is built using IRC_Client as its core.  

Example Usage
-------------
To log the channel #sillyputty on server my.server.org::

    Logger('#sillyputty', host="my.server.org").run()

It will now log all messages to #kamtest except those prefixed by "[off]".

Logger responds to these private messages:
    logfile
    infofile
    date
    help
    dance

More Detail
-----------
BasicLogger is a higher-level IRC client that is meant to link to the base client found in
IRCClient.py. It sends command tuples to its "irc" outbox, and receives them via its "inbox", 
allowing it to implement login, and ping response. It uses IRC_Client's tuple-based output format to
achieve some demultiplexing of IRC output as well, though not of the multiple-channel sort.

Logger ultimately links BasicLogger's "irc" outbox to IRC_Client's "talk" inbox. It also utilizes
two Carousels and SimpleFileWriters. 


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
messages from SimpleIRCClientPrefab before writing to the log. To format
messages differently, pass in a different function to its "formatter" keyword. 

Logger simply links BasicLogger with a SimpleIRCClientPrefab and two
Carousel-encapsulated SimpleFileWriters. It also slaps timestamps on messages.
It takes any keyword that BasicLogger or SimpleIRCClientPrefab will take.

One can run Logger from the command line by entering::
    ./Logger.py \#somechannel desirednickname
"""

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

    def __init__(self, channel, formatter=outformat, name="jinnaslogbot", logdir=""):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(BasicLogger, self).__init__()
        self.channel = channel
        self.format = formatter or outformat #in case we get passed in None
        self.name = name or "jinnaslogbot" #"
        self.logdir = logdir.rstrip('/') or os.getcwd()
        self.logdir = self.logdir + '/'
        self.logname = ""
        self.infoname = ""
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
        self.send(("PRIVMSG", 'nickserv', "identify abc123"), "irc")
        self.send(("JOIN", self.channel), "irc")
        
    def main(self):
        """Main loop"""
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
                if (data[2] == self.channel or data[0] == 'NICK') and formatted_data: #format might return None
                    self.send(formatted_data, "outbox")
                    self.respond(data) 
                elif formatted_data:
                    self.send(formatted_data, "system")
                    assert self.debugger.note("Logger.main", 5, str(data))

    def respond(self, msg):
        """respond to queries from other clients and pings from the server"""
        if msg[0] == 'PING':
            self.send(('PONG', msg[1]), 'irc')
            self.send("Sent PONG to %s \n" % msg[1], "system")
        if msg[0] == 'PRIVMSG' and msg[3].split(':')[0] == self.name:
            words = msg[3].split()
            del(words[0])
            replyLines = ""
            tag = 'PRIVMSG'
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
                tag = 'ME'
                replyLines = ['does the macarena']
            elif words[0] == 'poke':
                replyLines = ['Hehe! That tickles!']
            elif words[0] == 'slap':
                replyLines = ['Ouch!']

            if replyLines:
                for reply in replyLines:
                    self.send((tag, self.channel, reply), "irc")
                    self.send("Reply: %s \n" % reply, "log")
                
    def currentDateString(self):
        """returns the current date in DD-MM-YYYY format"""
        curtime = time.gmtime()
        return time.strftime("%d-%m-%Y", curtime)

    def changeDate(self):
        """updates the date and requests new log files to reflect the date"""
        self.lastdatestring = self.currentDateString()
        self.logname = self.logdir+self.channel.lstrip('#')+self.lastdatestring+'.log'
        self.infoname = self.logdir+self.channel.lstrip('#')+self.lastdatestring+'.info'
        self.send(self.logname, "log_next")
        self.send(self.infoname, "info_next")


def AppendingFileWriter(filename):
    """appends to instead of overwrites logs"""
    return SimpleFileWriter(filename, mode='ab')

def TimedOutformat(data):
    """\
    prepends a timestamp onto formatted data and ignores all privmsgs prefixed
    by "[off]"
    """
    if data[0] == 'PRIVMSG' and data[3][0:5] == '[off]':
        return
    formatted = outformat(data)
    curtime = time.gmtime()
    timestamp = time.strftime("[%H:%M] ", curtime)
    if formatted: return timestamp+formatted
    
def Logger(channel, formatter=TimedOutformat, name=None, logdir="", **irc_args):
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
    - **irc_args  -- pointer to a dictionary containing arguments for SimpleIRCClientPrefab
    """
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
    channel = "#kamtest"
    Name = "jinnaslogbot"
    print sys.argv
    if len(sys.argv) > 1: channel = sys.argv[1]
    if len(sys.argv) > 2: Name = sys.argv[2]

    print "Logging %s as %s" % (channel, Name)
    Logger(channel, name=Name).run()

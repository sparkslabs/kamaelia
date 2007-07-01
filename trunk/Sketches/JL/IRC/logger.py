#!/usr/bin/env python

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Fanout import Fanout
from Axon.Component import component
from Axon.Ipc import WaitComplete
import time
from guitest import outformat
from IRCClient import SimpleIRCClientPrefab


class Logger(component):
    
    Outboxes = {"irc" : "to IRC, for user responses and login",
                "outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",
                "date" : "For sending out the date" #useful if your logfiles are going to be encapsulated in Carousels
                }
        
    def __init__(self, channel, formatter=outformat, name="jinnaslogbot"):
        super(Logger, self).__init__()
        self.channel = channel
        self.format = formatter
        self.name = name
        self.lastdatestring = self.currentDateString()

    def login(self):
        self.send(("NICK", self.name), "irc")
        self.send(("USER", self.name, self.name, self.name, self.name), "irc")
        self.send(("PRIVMSG", 'nickserv', "identify abc123"), "irc")
        self.send(("JOIN", self.channel), "irc")
        
    def main(self):
        self.login()
        self.send(self.lastdatestring, "date")
        yield 1
        
        while True:
            if self.currentDateString() != self.lastdatestring:
                self.lastdatestring = self.currentDateString()
                self.send(self.lastdatestring, "date")
                
            yield 1
            
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                formatted_data = self.format(data)
                if data[2] == self.channel and formatted_data: #format might return None
                    self.send(formatted_data, "outbox")
                elif formatted_data:
                    self.respond(data) 
                    self.send(formatted_data, "system")

    def respond(self, msg):
        if msg[0] == 'PRIVMSG' and msg[2] == self.name:
            words = msg[3].split()
            replyLines = ""
            if words[0] == 'logfile':
                replyLines = ["feature in progress!"]
            elif words[0] == 'help':
                replyLines = ["Lines prefixed by [off] won't get recorded",
                              "Name: %s   Channel: %s" % (self.name, self.channel)
                              ]
            elif words[0] == 'date':
                replyLines = [self.currentDateString()]

            if replyLines:
                for reply in replyLines:
                    self.send(('PRIVMSG', msg[1], reply), "irc")
                    self.send("Reply: %s \n" % reply, "system")
                
    def currentDateString(self):
       curtime = time.gmtime()
       return time.strftime("%d-%m-%Y-%M", curtime)


#unused code, but I wanted to have it in the repository anyway
class DateChecker(component):
    """Sends the new filename to its outbox every time there is a date change"""
    def __init__(self):
        super(DateChecker, self).__init__()
        self.lastdatestring = self.currentDateString()

    def main(self):
        self.send(self.lastdatestring)
        while True: 
            yield 1
            if self.currentDateString() != self.lastdatestring:
                self.lastdatestring = self.currentDateString()
                self.send(self.lastdatestring)

    def currentDateString(self):
        curtime = time.gmtime()
        return time.strftime("%d-%m-%Y", curtime)
#/unused code


def LogFile(channel, prefix="", suffix=""):
    def getfile(changybit):
        return SimpleFileWriter(prefix+channel.lstrip('#')+changybit+suffix)
    return getfile


def LoggerPrefab(channel):
    return Graphline(irc = SimpleIRCClientPrefab(),
                     logger = Logger(channel),
                     split = Fanout(("toLog", "toInfo")),
                     log = Carousel(LogFile(channel, suffix=".log")),
                     info = Carousel(LogFile(channel, suffix=".info")),
                     linkages = {("logger", "irc") : ("irc", "inbox"),
                                 ("irc", "outbox") : ("logger", "inbox"),
                                 ("logger", "outbox"): ("log", "inbox"),
                                 ("logger", "system"): ("info", "inbox"),

                                 ("logger", "date") : ("split", "inbox"),
                                 ("split", "toLog") : ("log", "next"),
                                 ("split", "toInfo") : ("info", "next"),
                                }
                     ) 
    
if __name__ == '__main__':
    LoggerPrefab('#kamtest').run()

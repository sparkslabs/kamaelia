#!/usr/bin/env python

from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Component import component
from guitest import outformat
from IRCClient import SimpleIRCClientPrefab
import time

class Logger(component):
    
    Outboxes = {"irc" : "to IRC, for user responses and login",
                "outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",

                "log_next" : "for the Log Carousel",
                "info_next" : "for the Info Carousel"
                }

    def __init__(self, channel, formatter=outformat, name="jinnaslogbot", logdir=""):
        super(Logger, self).__init__()
        self.channel = channel
        self.format = formatter
        self.name = name
        self.logdir = logdir
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
                    self.respond(data) 
                    self.send(formatted_data, "system")

    def respond(self, msg):
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



def LoggerPrefab(channel):
    return Graphline(irc = SimpleIRCClientPrefab(),
                     logger = Logger(channel),
                     linkages = {("logger", "irc") : ("irc", "inbox"),
                                 ("irc", "outbox") : ("logger", "inbox"),
                                }
                     ) 
    
if __name__ == '__main__':
    LoggerPrefab('#kamtest').run()

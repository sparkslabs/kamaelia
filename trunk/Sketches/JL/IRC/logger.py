#!/usr/bin/env python

from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Component import component
from guitest import outformat
from IRCClient import SimpleIRCClientPrefab
import time

class BasicLogger(component):
    
    Outboxes = {"irc" : "to IRC, for user responses and login",
                "outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",
                }


    def __init__(self, channel, formatter=outformat, name="jinnaslogbot"):
        super(BasicLogger, self).__init__()
        self.channel = channel
        self.format = formatter
        self.name = name
        self.Responses = {"help" : ["Lines prefixed by [off] won't get recorded",
                                  "Name: %s   Channel: %s" % (self.name, self.channel)
                                  ],
                          "dance" : ['\x01ACTION does the macarena\x01'],
                         }
        

    def login(self):
        self.send(("NICK", self.name), "irc")
        self.send(("USER", self.name, self.name, self.name, self.name), "irc")
        self.send(("PRIVMSG", 'nickserv', "identify abc123"), "irc")
        self.send(("JOIN", self.channel), "irc")
        
    def main(self):
        self.login()
        yield 1
        
        while True:
            yield 1
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                formatted_data = self.format(data)
                if data[2] == self.channel and formatted_data: #format might return None
                    self.send(formatted_data, "outbox")
                elif formatted_data:
                    self.send(formatted_data, "system")
                    self.respond(data) #changed order of these two lines. Wait and See. 

    def respond(self, msg):
        if msg[0] == 'PRIVMSG' and msg[2] == self.name:
            replyLines = self.Responses.get(msg[3])
            if replyLines:
                for reply in replyLines:
                    self.send(('PRIVMSG', msg[1], reply), "irc")
                    self.send("Reply: %s \n" % reply, "system")


class DateNamedLogger(BasicLogger):
    Outboxes = {"irc" : "to IRC, for user responses and login",
                "outbox" : "What we're interested in, the traffic over the channel",
                "system" : "Messages directed toward the client, numeric replies, etc.",
                "signal" : "Shutdown handling in the future",
                "log_next" : "For requesting the next log file",
                "info_next" : "For requesting the next system log file",
            }

    def __init__(self, channel, logdir="", **argd): 
        super(DateNamedLogger, self).__init__(channel, **argd)
        self.logdir = logdir
        self.channel = channel
        self.Responses['What else floats in water?'] = ['Churches!']
        
        subsystem = Graphline(log = Carousel(SimpleFileWriter),
                              info = Carousel(SimpleFileWriter),
                              irc = SimpleIRCClientPrefab(),
                              dnl = self,
                              linkages = {("irc", "outbox") : ("dnl", "inbox"),
                                          ("dnl", "irc") : ("irc", "inbox"),
                                          ("dnl", "outbox") : ("log", "inbox"),
                                          ("dnl", "system") : ("info", "inbox"),
                                          ("dnl", "log_next") : ("log", "next"),
                                          ("dnl", "info_next") : ("info", "next"),
                                          })
        self.addChildren(subsystem)
        subsystem.activate()

    def main(self):
        self.login()
        self.changeDate()
        yield 1
        
        while True:
            if self.lastdatestring != self.currentDateString():
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
            
                
    def changeDate(self):
        self.lastdatestring = self.currentDateString()
        self.logname = self.logdir+self.channel.lstrip('#')+self.lastdatestring+'.log'
        self.infoname = self.logdir+self.channel.lstrip('#')+self.lastdatestring+'.info'
        self.send(self.logname, "log_next")
        self.send(self.infoname, "info_next")
        self.Responses['logfile'] = [self.logname]
        self.Responses['infofile']= [self.infoname]
        self.Responses['date'] = [self.lastdatestring]
        

    def currentDateString(self):
       curtime = time.gmtime()
       return time.strftime("%d-%m-%Y", curtime)

    
if __name__ == '__main__':
    DateNamedLogger('#kamtest').run()

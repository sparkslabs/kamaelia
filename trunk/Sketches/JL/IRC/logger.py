#!/usr/bin/env python

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.PureTransformer import PureTransformer
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
                }
        
    def __init__(self, channel, formatter=outformat, name="jinnaslogbot"):
        super(Logger, self).__init__()
        self.channel = channel
        self.format = formatter
        self.name = name

    def login(self):
        self.send(("NICK", self.name), "irc")
        self.send(("USER", self.name, self.name, self.name, self.name), "irc")
        self.send(("JOIN", self.channel), "irc")
        
    def main(self):
        self.login()
        while True:
            yield 1
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                formatted_data = self.format(data)
                if data[2] == self.channel:
                    self.send(formatted_data, "outbox")
                else:
                    self.send(formatted_data, "system")

            
def LoggerPrefab(channel):
    return Graphline(irc = SimpleIRCClientPrefab(),
                     logger = Logger(channel),
                     log = SimpleFileWriter("%s%i.log" % (channel[1:], time.time())),
                     info = SimpleFileWriter("%s%i.info" % (channel[1:], time.time())),
                     linkages = {("logger", "irc") : ("irc", "inbox"),
                                 ("irc", "outbox") : ("logger", "inbox"),
                                 ("logger", "outbox"): ("log", "inbox"),
                                 ("logger", "system"): ("info", "inbox"),
                               }
                     )
    
if __name__ == '__main__':
    LoggerPrefab('#kamtest').run()

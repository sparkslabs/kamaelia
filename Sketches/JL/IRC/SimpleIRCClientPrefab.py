#! /usr/bin/env python

import Axon as _Axon
from IRCClient import *
from Kamaelia.Internet.TCPClient import TCPClient

def SimpleIRCClientPrefab(host="127.0.0.1",
                          port=6667,
                          nick="kamaeliabot",
                          nickinfo="Kamaelia",
                          defaultChannel="#kamaeliatest",
                          IRC_Handler=IRC_Client):
    return Graphline(
        CLIENT = TCPClient(host, port),
        PROTO = IRC_Handler(nick, nickinfo, defaultChannel),
        linkages = {
              ("CLIENT" , "outbox") : ("PROTO" , "inbox"),
              ("PROTO"  , "outbox") : ("CLIENT", "inbox"),
              ("PROTO"  , "heard")  : ("SELF", "outbox"), #SELF refers to the Graphline. Passthrough linkage
              ("SELF"  , "inbox") : ("PROTO" , "talk"), #passthrough
              ("SELF"  , "topic") : ("PROTO" , "topic"), #passthrough
              ("SELF"  , "control") : ("PROTO" , "control"), #passthrough
              ("PROTO"  , "signal") : ("CLIENT", "control"),
              ("CLIENT" , "signal") : ("SELF" , "signal"), #passthrough
              }
        )

if __name__ == '__main__':
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.Console import ConsoleReader
   from Kamaelia.UI.Pygame.Ticker import Ticker
   from Kamaelia.Chassis.Pipeline import Pipeline

   Pipeline(
       ConsoleReader(),
       SimpleIRCClientPrefab(host="irc.freenode.net", nick="kamaeliabot", defaultChannel="#kamtest"),
       Ticker(render_right = 800,render_bottom = 600),
   ).run()


#! /usr/bin/env python

import Axon as _Axon
from IRCClient import *
from Kamaelia.Internet.TCPClient import TCPClient

def SimpleIRCClientPrefab(host="irc.freenode.net",
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

#from SimpleIRCClientPrefab import *
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer
    bot = SimpleIRCClientPrefab(nick="SimpleIRCClient", nickinfo="testing SimpleIRCClientPrefab")
    display_helper = PureTransformer(lambda x: str(x) + "\n")
    Pipeline(ConsoleReader(), bot, display_helper, ConsoleEchoer()).run()
    
    
    

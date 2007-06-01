#! /usr/bin/env python
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Fanout import Fanout
from IRCClient import *

def ComplexIRCClientPrefab(host="127.0.0.1",
                          port=6667,
                          nick="kamaeliabot",
                          nickinfo="Kamaelia",
                          defaultChannel="#kamaeliatest",
                          IRC_Handler=IRC_Client):
    return Graphline(
        CLIENT = TCPClient(host, port),
        PROTO = IRC_Handler(nick, nickinfo, defaultChannel, sendAsString=True),
        SPLIT = Fanout(["toGraphline", "toTCP"]),
        linkages = {
              ("CLIENT" , "outbox") : ("PROTO" , "inbox"),
              ("PROTO"  , "outbox") : ("SPLIT", "inbox"),
              ("PROTO"  , "privmsg")  : ("SELF", "outbox"), #SELF refers to the Graphline. Passthrough linkage
              ("SELF"  , "inbox") : ("PROTO" , "talk"), #passthrough
              ("SELF"  , "topic") : ("PROTO" , "topic"), #passthrough
              ("SELF"  , "control") : ("PROTO" , "control"), #passthrough
              ("PROTO"  , "signal") : ("CLIENT", "control"),
              ("CLIENT" , "signal") : ("SELF" , "signal"), #passthrough
              ("PROTO", "nonPrivmsg") : ("SELF", "nonPrivmsg"), #passthrough
              ("SPLIT", "toGraphline") : ("SELF", "sentCopy"), #passthrough
              ("SPLIT", "toTCP") : ("CLIENT", "inbox")
              }
        )

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.UI.Pygame.Ticker import Ticker
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.PureTransformer import PureTransformer
    Graphline(
        reader = ConsoleReader(),
        irc = ComplexIRCClientPrefab(host="irc.freenode.net", nick="kamaeliabot", defaultChannel="#kamtest"),
        display1 = Ticker(render_right = 400,render_bottom = 300),
        display2 = Ticker(render_right = 400,render_bottom = 300, position = (440, 0)),
        display3 = Ticker(render_right = 400,render_bottom = 300, position = (0, 340)),
        linkages = {
            ("reader", "outbox") : ("irc", "inbox"),
            ("irc", "outbox") : ("display1", "inbox"),
            ("irc", "nonPrivmsg") : ("display2", "inbox"),
            ("irc", "sentCopy") : ("display3", "inbox")
            }
            
    ).run()

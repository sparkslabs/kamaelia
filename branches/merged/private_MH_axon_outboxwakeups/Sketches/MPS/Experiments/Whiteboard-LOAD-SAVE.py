#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import Axon
import pygame

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import Backplane, publishTo, subscribeTo
from Kamaelia.Util.Pipeline import Pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists

#
# The following application specific components will probably be rolled
# back into the repository.
#

from Whiteboard.TagFiltering import TagAndFilterWrapper, FilterAndTagWrapper
from Whiteboard.Tokenisation import tokenlists_to_lines, lines_to_tokenlists

from Whiteboard.Canvas import Canvas
from Whiteboard.Painter import Painter
from Whiteboard.TwoWaySplitter import TwoWaySplitter
from Whiteboard.SingleShot import OneShot

colours = { "black" :  (0,0,0), 
            "red" :    (192,0,0),
            "orange" : (192,96,0),
            "yellow" : (160,160,0),
            "green" :  (0,192,0),
            "turquoise" : (0,160,160),
            "blue": (0,0,255),
            "purple" : (192,0,192),
            "darkgrey" : (96,96,96),
            "lightgrey" :(192,192,192),
          }

colours_order = [ "black", "red", "orange", "yellow", "green", "turquoise", "blue", "purple", "darkgrey", "lightgrey" ]

def buildPalette(cols, order, topleft=(0,0), size=32):
    buttons = {}
    links = {}
    pos = topleft
    i=0
    # Interesting/neat trick MPS
    for col in order:
        buttons[col] = Button(caption="", position=pos, size=(size,size), bgcolour=cols[col], msg=cols[col])
        links[ (col,"outbox") ] = ("self","outbox")
        pos = (pos[0] + size, pos[1])
        i=i+1
    return Graphline( linkages = links,  **buttons )

def parseOptions():
    rhost, rport = None, None
    serveport = None

    shortargs = ""
    longargs  = [ "serveport=", "connectto=" ]
    optlist, remargs = getopt.getopt(sys.argv[1:], shortargs, longargs)

    for o,a in optlist:
        if o in ("-s","--serveport"):
            serveport = int(a)

        elif o in ("-c","--connectto"):
            rhost,rport = re.match(r"^([^:]+):([0-9]+)$", a).groups()
            rport = int(rport)

    return rhost, rport, serveport

def LocalEventServer(backplane="WHITEBOARD", port=1500):
        from Kamaelia.Chassis.ConnectedServer import SimpleServer
        from Kamaelia.Util.Console import ConsoleEchoer

        def clientconnector():
            return Pipeline(
                chunks_to_lines(),
                lines_to_tokenlists(),
                FilterAndTagWrapper(
                    Pipeline( publishTo(backplane),
                                # well, should be to separate pipelines, this is lazier!
                              subscribeTo(backplane),
                            )
                    ),
                tokenlists_to_lines(),
                )

        return SimpleServer(protocol=clientconnector, port=serveport)

def EventServerClients(rhost, rport, backplane="WHITEBOARD"):
        # plug a TCPClient into the backplae
        from Kamaelia.Internet.TCPClient import TCPClient

        loadingmsg = "Fetching sketch from server..."

        return Pipeline( subscribeTo(backplane),
                         TagAndFilterWrapper(
                         Graphline( GETIMG = OneShot(msg=[["GETIMG"]]),
                                    PIPE = Pipeline(
                                            tokenlists_to_lines(),
                                            TCPClient(host=rhost,port=rport),
                                            chunks_to_lines(),
                                            lines_to_tokenlists(),
                                        ),
                                    BLACKOUT = OneShot(msg=[["CLEAR",0,0,0],["WRITE",100,100,24,255,255,255,loadingmsg]]),
                                    linkages = { ("self","inbox") : ("PIPE","inbox"),
                                                 ("self","control") : ("PIPE","control"),
                                                 ("PIPE","outbox") : ("self","outbox"),
                                                 ("PIPE","signal") : ("self","signal"),
                                                 ("GETIMG","outbox") : ("PIPE","inbox"),
                                                 ("BLACKOUT","outbox") : ("self","outbox"),
                                               },
                                  )
                         ),
                         publishTo(backplane),
                       ) #.activate()

def parseCommands():
    from Kamaelia.Util.Marshalling import Marshaller

    class CommandParser:
        def marshall(data):
            output = [data]
            if data[0].upper() == "LOAD":
                output.append(["GETIMG"])    # to propogate loaded image to other connected canvases
            return output
        marshall = staticmethod(marshall)

    return Marshaller(CommandParser)

def makeBasicSketcher(left=0,top=0,width=1024,height=768):
    return Graphline( CANVAS  = Canvas( position=(left,top+32),size=(width,height-32) ),
                      PAINTER = Painter(),
                      PALETTE = buildPalette( cols=colours, order=colours_order, topleft=(left+64,top), size=32 ),
                      ERASER  = Button(caption="Eraser", size=(64,32), position=(left,top)),

                      LOAD  = Button(caption="LOAD",
                                     size=(63,32), 
                                     position=(left+64+32*len(colours), top),
                                     msg=[["LOAD", "default.png"]]),
                      SAVE  = Button(caption="SAVE",
                                     size=(63,32),
                                     position=(left+(64*2)+32*len(colours), top),
                                     msg=[["SAVE", "default.png"]]),

                      SPLIT   = TwoWaySplitter(),

                      linkages = {
                          ("CANVAS",  "eventsOut") : ("PAINTER", "inbox"),
                          ("PALETTE", "outbox")    : ("PAINTER", "colour"),
                          ("ERASER", "outbox")     : ("PAINTER", "erase"),

                          ("LOAD","outbox")        : ("CANVAS", "inbox"),
                          ("SAVE","outbox")        : ("CANVAS", "inbox"),

                          ("PAINTER", "outbox")    : ("SPLIT", "inbox"),
                          ("SPLIT", "outbox")      : ("CANVAS", "inbox"),

                          ("self", "inbox")        : ("CANVAS", "inbox"),
                          ("SPLIT", "outbox2")     : ("self", "outbox"),
                          ("CANVAS", "outbox")     : ("self", "outbox"),
                          },
                    )

mainsketcher = \
    Graphline( SKETCHER = makeBasicSketcher(width=1024,height=768),
               CONSOLE = Pipeline(ConsoleReader(),text_to_tokenlists(),parseCommands()),

               linkages = { ('self','inbox'):('SKETCHER','inbox'),
                            ('SKETCHER','outbox'):('self','outbox'),
                            ('CONSOLE','outbox'):('SKETCHER','inbox'),
                          }
                 )

# primary whiteboard
Pipeline( subscribeTo("WHITEBOARD"),
          TagAndFilterWrapper(mainsketcher),
          publishTo("WHITEBOARD")
        ).activate()

if __name__=="__main__":
    import sys, getopt, re

    rhost, rport, serveport = parseOptions()

    # setup a server, if requested
    if serveport:
        LocalEventServer("WHITEBOARD", port=serveport).activate()

    # connect to remote host & port, if requested
    if rhost and rport:
        EventServerClients(rhost, rport, "WHITEBOARD").activate()

    Backplane("WHITEBOARD").run()

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
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.UI.PygameDisplay import PygameDisplay
import pygame

class Canvas(Axon.Component.component):
    """\
    Canvas component - pygame surface that accepts drawing instructions
    """

    Inboxes =  { "inbox"   : "Receives drawing instructions",
                 "control" : "",
                 "fromDisplay"  : "For receiving replies from PygameDisplay service",
                 "eventsIn" : "For receiving PygameDisplay events",
               }
    Outboxes = { "outbox" : "Issues drawing instructions",
                 "signal" : "",
                 "toDisplay" : "For sending requests to PygameDisplay service",
                 "eventsOut" : "Events forwarded out of here",
               }

    def __init__(self, position=(0,0), size=(1024,768), ):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Canvas,self).__init__()
        self.position = position
        self.size = size

    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def requestDisplay(self, **argd):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"toDisplay"), displayservice)
        self.send(argd, "toDisplay")
        for _ in self.waitBox("fromDisplay"):
            yield 1
        self.surface = self.recv("fromDisplay")

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False


    def main(self):
        """Main loop"""

        yield WaitComplete(
              self.requestDisplay( DISPLAYREQUEST=True,
                                   callback = (self,"fromDisplay"),
                                   events = (self, "eventsIn"),
                                   size = self.size,
                                   position = self.position,
                                 )
              )

        self.surface.fill( (255,255,255) )
        self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")


        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEMOTION, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP, "surface" : self.surface},
                   "toDisplay" )

        while not self.finished():

            while self.dataReady("inbox"):
                msgs = self.recv("inbox")
                self.redrawNeeded = False
                for msg in msgs:
                    cmd = msg[0]
                    args = msg[1:]
                    # parse commands here
                    self.handleCommand(cmd, *args)
                if self.redrawNeeded:
                    self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")


            # pass on events received from pygame display
            while self.dataReady("eventsIn"):
                self.send( self.recv("eventsIn"), "eventsOut" )

            self.pause()
            yield 1

    def handleCommand(self, cmd, *args):
        #
        # Could really take a dispatch pattern
        # Would then be pluggable.
        #
        cmd = cmd.upper()
        if cmd=="CLEAR":
            if len(args) == 3:
                self.surface.fill( [int(a) for a in args[0:3]] )
            else:
                self.surface.fill( (255,255,255) )
            self.redrawNeeded = True

        elif cmd=="LINE":
            (r,g,b,sx,sy,ex,ey) = [int(v) for v in args[0:7]]
            pygame.draw.line(self.surface, (r,g,b), (sx,sy), (ex,ey))
            self.redrawNeeded = True

        elif cmd=="CIRCLE":
            (r,g,b,x,y,radius) = [int(v) for v in args[0:6]]
            pygame.draw.circle(self.surface, (r,g,b), (x,y), radius, 0)
            self.redrawNeeded = True

        elif cmd=="LOAD":
            filename = args[0]
            try:
                loadedimage = pygame.image.load(filename)
            except:
                pass
            else:
                self.surface.blit(loadedimage, (0,0))
            self.redrawNeeded = True

        elif cmd=="SAVE":
            filename = args[0]
            pygame.image.save(self.surface, filename)

        elif cmd=="GETIMG":
            imagestring = pygame.image.tostring(self.surface,"RGB")
            imagestring = zlib.compress(imagestring)
            w,h = self.surface.get_size()
            self.send( [["SETIMG",imagestring,str(w),str(h),"RGB"]], "outbox" )

        elif cmd=="SETIMG":
            w,h = int(args[1]), int(args[2])
            imagestring = zlib.decompress(args[0])
            recvsurface = pygame.image.fromstring(imagestring, (w,h), args[3])
            self.surface.blit(recvsurface, (0,0))
            self.redrawNeeded = True

        elif cmd=="WRITE":
            x,y,size,r,g,b = [int(a) for a in args[0:6]]
            text = args[6]
            font = pygame.font.Font(None,size)
            textimg = font.render(text, False, (r,g,b))
            self.surface.blit(textimg, (x,y))
            self.redrawNeeded = True

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
import zlib
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.UI.PygameDisplay import PygameDisplay
import pygame

try:
    import Image
except ImportError:
    print "WARNING: Python Imaging Library Not available, defaulting to bmp only mode"

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
                 "surfacechanged" : "If the surface gets changed from last load/save a 'dirty' message is emitted here",
               }

    def __init__(self, position=(0,0),
                       size=(1024,768),
                       displayExtra = None,
                ):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Canvas,self).__init__()
        self.position = position
        self.size = size
        self.antialias = False
        if self.antialias == True:
            self.pygame_draw_line = pygame.draw.aaline
        else:
            self.pygame_draw_line = pygame.draw.line
        self.dirty_sent = False
        self.displayExtra = displayExtra
        self.width = 3

    def waitBox(self,boxname):
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def requestDisplay(self, **argd):
        displayRequest = dict(argd)
        if self.displayExtra:
            displayRequest.update(self.displayExtra)
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"toDisplay"), displayservice)
#        self.send(argd, "toDisplay")
        self.send(displayRequest, "toDisplay")
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
#                \
#print repr(msgs)
                self.redrawNeeded = False
                for msg in msgs:
                    cmd = msg[0]
                    args = msg[1:]
                    # parse commands here
                    self.handleCommand(cmd, *args)
                if self.redrawNeeded:
                    self.send({"REDRAW":True, "surface":self.surface}, "toDisplay")
                    if not self.clean:
                        if not self.dirty_sent:
                            self.send("dirty", "surfacechanged")
                            self.dirty_sent = True

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
        if   cmd=="CLEAR":
            self.clear(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="LINE":
             self.line(args)
        elif cmd=="CIRCLE":
            self.circle(args)
            self.clean = False
        elif cmd=="LOAD":
            self.load(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="SAVE":
            self.save(args)
            self.clean = True
            self.dirty_sent = False
        elif cmd=="GETIMG":
            self.getimg(args)
            self.clean = False
        elif cmd=="SETIMG":
            self.setimg(args)
            self.clean = False
        elif cmd=="WRITE":
            self.write(args)
            self.clean = False

    def line(self, args):
        (r,g,b,sx,sy,ex,ey) = [int(v) for v in args[0:7]]
        self.pygame_draw_line(self.surface, (r,g,b), (sx,sy), (ex,ey),self.width)
#        pygame.draw.aaline(self.surface, (r,g,b), (sx,sy), (ex,ey))
        self.redrawNeeded = True
        if not((sy <0) or (ey <0)):
            self.clean = False

    def clear(self, args):
        if len(args) == 3:
            self.surface.fill( [int(a) for a in args[0:3]] )
        else:
            self.surface.fill( (255,255,255) )
        self.redrawNeeded = True
        self.dirty_sent = True
        self.clean = True

    def circle(self, args):
        (r,g,b,x,y,radius) = [int(v) for v in args[0:6]]
        pygame.draw.circle(self.surface, (r,g,b), (x,y), radius, 0)
        self.redrawNeeded = True

    def load(self, args):
            filename = args[0]
            print "ARGS", args
            try:
                loadedimage = pygame.image.load(filename)
            except:
                pass
            else:
                self.surface.blit(loadedimage, (0,0))
            self.redrawNeeded = True
            if not ( (len(args) >1) and args[1] == "nopropogate" ):
                self.getimg(())
            self.clean = True

    def save(self, args):
        filename = args[0]
        try:
            imagestring = pygame.image.tostring(self.surface,"RGB")
            pilImage = Image.fromstring("RGB", self.surface.get_size(), imagestring)
            pilImage.save(filename)
        except NameError:
            pygame.image.save(self.surface, filename)
        self.clean = True

    def getimg(self, args):
            imagestring = pygame.image.tostring(self.surface,"RGB")
            imagestring = zlib.compress(imagestring)
            w,h = self.surface.get_size()
            self.send( [["SETIMG",imagestring,str(w),str(h),"RGB"]], "outbox" )
            print "GETIMG"

    def setimg(self, args):
            w,h = int(args[1]), int(args[2])
            imagestring = zlib.decompress(args[0])
            recvsurface = pygame.image.frombuffer(imagestring, (w,h), args[3])
            self.surface.blit(recvsurface, (0,0))
            self.redrawNeeded = True

    def write(self, args):
            x,y,size,r,g,b = [int(a) for a in args[0:6]]
            text = args[6]
            font = pygame.font.Font(None,size)
            textimg = font.render(text, self.antialias, (r,g,b))
            self.surface.blit(textimg, (x,y))
            self.redrawNeeded = True


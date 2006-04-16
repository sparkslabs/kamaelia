#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import pygame
from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.Util.Graphline import Graphline



class Canvas(component):
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
        
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEMOTION, "surface" : self.surface},
                   "toDisplay" )
        self.send( {"ADDLISTENEVENT" : pygame.MOUSEBUTTONUP, "surface" : self.surface},
                   "toDisplay" )
        
        while not self.finished():
            
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                cmd = msg[0]
                args = msg[1:]
                # parse commands here
                self.handleCommand(cmd, *args)
                
            # pass on events received from pygame display
            while self.dataReady("eventsIn"):
                self.send( self.recv("eventsIn"), "eventsOut" )
                
            self.pause()
            yield 1
            
            
    def handleCommand(self, cmd, *args):
        if cmd=="CLEAR":
            self.surface.fill( (255,255,255) )
        elif cmd=="LINE":
            (r,g,b,sx,sy,ex,ey) = [int(v) for v in args[0:7]]
            pygame.draw.line(self.surface, (r,g,b), (sx,sy), (ex,ey))

class Painter(component):
    """\
    Painter() -> new Painter component.
    """
    
    Inboxes =  { "inbox"   : "For receiving PygameDisplay events",
                 "control" : "",
               }
    Outboxes = { "outbox" : "outputs drawing instructions",
                 "signal" : "",
               }
    
    def __init__(self):
        super(Painter,self).__init__()
     
    
    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
    
    
    def main(self):
        """Main loop"""
        
        yield 1
        r,g,b = 0,0,0
        dragging = False
        mode="LINE"
        
        
        while not self.finished():
        
            while self.dataReady("inbox"):
                message = self.recv("inbox")
                for data in message:
                    if data.type == pygame.MOUSEBUTTONDOWN:
                        oldpos = data.pos
                        dragging = True
                    elif data.type == pygame.MOUSEMOTION and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                    elif data.type == pygame.MOUSEBUTTONUP and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                        dragging = False
        
            self.pause()
            yield 1

    def cmd(self, mode, oldpos, newpos, r, g, b):
        if mode=="LINE":
            self.send( ["LINE", str(r),str(g),str(b), str(oldpos[0]), str(oldpos[1]), str(newpos[0]), str(newpos[1])], "outbox")


Graphline( CANVAS  = Canvas( position=(0,0),size=(1024,768) ),
           PAINTER = Painter(),
           
           linkages = {
               ("CANVAS",  "eventsOut") : ("PAINTER", "inbox"),
               ("PAINTER", "outbox")    : ("CANVAS", "inbox"),
           },
         ).run()



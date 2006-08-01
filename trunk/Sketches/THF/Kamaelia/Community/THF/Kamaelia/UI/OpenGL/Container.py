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
"""\
=====================
Container component
=====================
TODO
"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Util3D import *
from OpenGLComponent import *

class Container(OpenGLComponent):

    def __init__(self, **argd):
        super(Container, self).__init__(**argd)
        
        self.contents = argd.get("contents")
        
        self.oldTransform = None
        self.components = []
        self.rel_pos = {}
        self.poscomms = {}
        self.rotcomms = {}
        self.scacomms = {}
        
        for (comp, pos) in self.contents.items():
            self.components.append(comp)
            self.rel_pos[comp] = Vector(*pos)
            
            self.poscomms[comp] = self.addOutbox("pos")
            self.link( (self, self.poscomms[comp]), (comp, "position") )
            self.rotcomms[comp] = self.addOutbox("rot")
            self.link( (self, self.rotcomms[comp]), (comp, "rotation") )
            self.scacomms[comp] = self.addOutbox("sca")
            self.link( (self, self.scacomms[comp]), (comp, "scaling") )
            
            abspos = self.position+self.transform.transformVector(self.rel_pos[comp])
            self.send(abspos.toTuple(), self.poscomms[comp])
            self.send(self.rotation.toTuple(), self.rotcomms[comp])
            self.send(self.scaling.toTuple(), self.scacomms[comp])
        
           
    def frame(self):
        if self.oldTransform != self.transform:
            for comp in self.components:
                trans = self.transform.transformVector(self.rel_pos[comp])
                self.send((trans+self.position).toTuple(), self.poscomms[comp])
                self.send(self.rotation.toTuple(), self.rotcomms[comp])
                self.send(self.scaling.toTuple(), self.scacomms[comp])
            self.oldTransform = self.transform
        

if __name__=='__main__':
    from SimpleButton import *

    class Rotator(Axon.Component.component):
        def main(self):
            while 1:
                yield 1
                self.send( (0.1, 0.1, 0.1), "outbox")
    
    class Buzzer(Axon.Component.component):
        def main(self):
            r = 1.00
            f = 0.03
            while 1:
                yield 1
                if  r>1.0: f -= 0.0001
                else: f += 0.0001
                r += f
            
                self.send( (r, r, r), "outbox")
    
    b1 = SimpleButton(size=(1,1,1)).activate()
    b2 = SimpleButton(size=(1,1,1)).activate()
    r = Rotator().activate()
    b = Buzzer().activate()
    c = Container(contents = {b1:(-2,0,0), b2:(2,0,0)}, position=(0,0,-7) ).activate()
    
    r.link( (r, "outbox"), (c, "rel_rotation") )
    b.link( (b, "outbox"), (c, "scaling") )
    
    Axon.Scheduler.scheduler.run.runThreads()  

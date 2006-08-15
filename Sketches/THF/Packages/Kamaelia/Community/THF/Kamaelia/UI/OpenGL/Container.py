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

A container to control several OpenGLComponents.

"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Vector import Vector
from Transform import Transform


class Container(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):

    Inboxes = {
        "inbox": "",
        "control": "",
        "position" : "receive position triple (x,y,z)",
        "rotation": "receive rotation triple (x,y,z)",
        "scaling": "receive scaling triple (x,y,z)",
        "rel_position" : "receive position triple (x,y,z)",
        "rel_rotation": "receive rotation triple (x,y,z)",
        "rel_scaling": "receive scaling triple (x,y,z)",
    }
    
    Outboxes = {
        "outbox": "",
        "signal": ""
    }

    def __init__(self, **argd):
        super(Container, self).__init__()
        
        # get transformation data and convert to vectors
        self.size = Vector( *argd.get("size", (0,0,0)) )
        self.position = Vector( *argd.get("position", (0,0,0)) )
        self.rotation = Vector( *argd.get("rotation", (0.0,0.0,0.0)) )
        self.scaling = Vector( *argd.get("scaling", (1,1,1) ) )
        
        # for detection of changes
        self.oldrot = Vector()
        self.oldpos = Vector()
        self.oldscaling = Vector()

        # inital apply trasformations
        self.transform = Transform()

        self.components = []

        self.rel_positions = {}
        self.rel_rotations = {}
        self.rel_scalings = {}

        self.poscomms = {}
        self.rotcomms = {}
        self.scacomms = {}
        
        
        contents = argd.get("contents", None)
        if contents is not None:
            for (comp, params) in contents.items():
                self.addElement(comp, **params)


    def main(self):
        while 1:
            self.handleMovement()
            self.applyTransforms()
            yield 1

           
    def handleMovement(self):
        """ Handle movement commands received by corresponding inboxes. """
        while self.dataReady("position"):
            pos = self.recv("position")
            self.position = Vector(*pos)
        
        while self.dataReady("rotation"):
            rot = self.recv("rotation")
            self.rotation = Vector(*rot)
            
        while self.dataReady("scaling"):
            scaling = self.recv("scaling")
            self.scaling = Vector(*scaling)
            
        while self.dataReady("rel_position"):
            self.position += Vector(*self.recv("rel_position"))
            
        while self.dataReady("rel_rotation"):
            self.rotation += Vector(*self.recv("rel_rotation"))
            
        while self.dataReady("rel_scaling"):
            self.scaling = Vector(*self.recv("rel_scaling"))


    def applyTransforms(self):
        """ Use the objects translation/rotation/scaling values to generate a new transformation Matrix if changes have happened. """
        # generate new transformation matrix if needed
        if self.oldscaling != self.scaling or self.oldrot != self.rotation or self.oldpos != self.position:
            self.transform = Transform()
            self.transform.applyScaling(self.scaling)
            self.transform.applyRotation(self.rotation)
            self.transform.applyTranslation(self.position)
            
            self.rearangeElements()


    def rearangeElements(self):
        for comp in self.components:
            trans = self.transform.transformVector(self.rel_positions[comp])
            self.send(trans.toTuple(), self.poscomms[comp])
#                self.send(self.rotation.toTuple(), self.rotcomms[comp])
#                self.send(self.scaling.toTuple(), self.scacomms[comp])

            
    def addElement(self, comp, position=(0,0,0), rotation=(0,0,0), scaling=(1,1,1) ):
        self.components.append(comp)
        self.rel_positions[comp] = Vector( *position )
        self.rel_rotations[comp] = Vector( *rotation )
        self.rel_scalings[comp] = Vector( *scaling )
        
        self.poscomms[comp] = self.addOutbox("pos")
        self.link( (self, self.poscomms[comp]), (comp, "position") )
#        self.rotcomms[comp] = self.addOutbox("rot")
#        self.link( (self, self.rotcomms[comp]), (comp, "rotation") )
#        self.scacomms[comp] = self.addOutbox("sca")
#        self.link( (self, self.scacomms[comp]), (comp, "scaling") )

        self.rearangeElements()
        
        
    def removeElement(self, comp):
        self.components.remove(comp)
        self.rel_positions.pop(comp)
        self.rel_rotations.pop(comp)
        self.rel_scalings.pop(comp)
        
        # todo: unlink
        
        self.poscomms.pop(comp)
        self.rotcomms.pop(comp)
        self.scacomms.pop(comp)

        self.rearangeElements()
        

if __name__=='__main__':
    from SimpleButton import SimpleButton
    from SimpleCube import SimpleCube
    from ArrowButton import ArrowButton

    class Rotator(Axon.Component.component):
        def main(self):
            while 1:
                yield 1
                self.send( (0.1, 0.1, 0.0), "outbox")
    
    
    from Kamaelia.Chassis.Graphline import Graphline

    o1 = SimpleButton(size=(1,1,1)).activate()
    o2 = SimpleCube(size=(1,1,1)).activate()
    o3 = ArrowButton(size=(1,1,1)).activate()

    containercontents = {
        o1: {"position":(0,1,0)},
        o2: {"position":(1,-1,0)},
        o3: {"position":(-1,-1,0)},
    }

    Graphline(
        OBJ1=o1,
        OBJ2=o2,
        OBJ3=o3,
        CONTAINER=Container(contents=containercontents, position=(0,0,-10)),
        ROTATOR= Rotator(),
        linkages = {
            ("ROTATOR", "outbox") : ("CONTAINER","rel_rotation")
        }
    ).run()

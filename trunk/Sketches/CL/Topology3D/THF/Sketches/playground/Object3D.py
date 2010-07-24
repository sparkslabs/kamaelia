#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
=====================
General 3D Object
=====================
Methods to be overridden:
    draw()
    handleEvents()
    setup()
    frame()
"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Axon
from Util3D import *
from Display3D import Display3D

import time

class Object3D(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):#(Axon.ThreadedComponent.threadedadaptivecommscomponent):
    Inboxes = {
       "inbox": "Input events",
       "control": "ignored",
       "callback": "for the response after a displayrequest",
        "position" : "receive position triple (x,y,z)",
        "rotation": "receive rotation triple (x,y,z)",
        "scaling": "receive scaling triple (x,y,z)",
        "rel_position" : "receive position triple (x,y,z)",
        "rel_rotation": "receive rotation triple (x,y,z)",
        "rel_scaling": "receive scaling triple (x,y,z)",
    }
    
    Outboxes = {
        "outbox": "not used",
        "display_signal" : "Outbox used for communicating to the display surface",
        "position" : "send position status when updated",
        "rotation": "send rotation status when updated",
        "scaling": "send scaling status when updated",
    }
    
    def __init__(self, **argd):
        super(Object3D, self).__init__()

        # transformation data
        self.size = argd.get("size", None)
        self.pos = argd.get("pos",Vector(0,0,-15))
        self.rot = Vector(0.0,0.0,0.0)
        self.scaling = argd.get("scaling",Vector(1,1,1))
        
        # for detection of changes
        self.oldrot = Vector()
        self.oldpos = Vector()
        self.oldscaling = Vector()

        # name        
        self.name = argd.get("name", "nameless")

        # get display service
        displayservice = Display3D.getDisplayService()
        # link display_signal to displayservice
        self.link((self,"display_signal"), displayservice)
        
        self.transform = Transform()

                                          
    def applyTransforms(self):
        # generate new transformation matrix if needed
        if self.oldscaling != self.scaling or self.oldrot != self.rot or self.oldpos != self.pos:
            self.transform = Transform()
            self.transform.applyScaling(self.scaling)
            self.transform.applyRotation(self.rot)
            self.transform.applyTranslation(self.pos)

            if self.oldscaling != self.scaling:
                self.send(self.scaling, "scaling")
                self.oldscaling = self.scaling.copy()

            if self.oldrot != self.rot:
                self.send(self.rot, "rotation")
                self.oldrot = self.rot.copy()

            if self.oldpos != self.pos:
                self.send(self.pos, "position")
                self.oldpos = self.pos.copy()
                
            # send new transform to display service
            transform_update = { "TRANSFORM_UPDATE": True,
                                                 "objectid": id(self),
                                                 "transform": self.transform }
            self.send(transform_update, "display_signal")

    def handleMovement(self):
        while self.dataReady("position"):
            pos = self.recv("position")
            self.pos = Vector(*pos)
        
        while self.dataReady("rotation"):
            rot = self.recv("rotation")
            self.rot = Vector(*rot)
            
        while self.dataReady("scaling"):
            scaling = self.recv("scaling")
            self.scaling = Vector(*scaling)
            
        while self.dataReady("rel_position"):
            self.pos += Vector(*self.recv("rel_position"))
            
        while self.dataReady("rel_rotation"):
            self.rot += Vector(*self.recv("rel_rotation"))
            
        while self.dataReady("rel_scaling"):
            self.scaling = Vector(*self.recv("rel_scaling"))
            
            
    def main(self):
        # create display request
        self.disprequest = { "OGL_DISPLAYREQUEST" : True,
                                          "objectid" : id(self),
                                          "callback" : (self,"callback"),
                                          "events" : (self, "inbox"),
                                          "size": self.size,
                                          }
        # send display request
        self.send(self.disprequest, "display_signal")
        # setup function from derived objects
        self.setup()        
        # inital apply trasformations
        self.applyTransforms()
        # initial draw to display list
        self.redraw()

        # wait for response on displayrequest
        while not self.dataReady("callback"):  yield 1
        self.ogl_name = self.recv("callback")
        
        while 1:
            yield 1
            self.applyTransforms()
            self.handleMovement()
            self.handleEvents()
            # frame function from derived objects
            self.frame()

    ##
    # Methods to be used by derived objects
    ##

    def addListenEvents(self, events):
        for event in events:
            self.send({"ADDLISTENEVENT":event, "objectid":id(self)}, "display_signal")

    
    def removeListenEvents(self, events):
        for event in events:
            self.send({"REMOVELISTENEVENT":event, "objectid":id(self)}, "display_signal")


    def redraw(self):
       # display list id
        displaylist = glGenLists(1);
        # draw object to its displaylist
        glNewList(displaylist, GL_COMPILE)
        self.draw()
        glEndList()

        
        dl_update = { "DISPLAYLIST_UPDATE": True,
                                                "objectid": id(self),
                                                "displaylist": displaylist }
        self.send(dl_update, "display_signal")
        


    ##
    # Method stubs to be overridden by derived objects
    ##

    def handleEvents(self):
        """ Method stub """
        pass        


    def draw(self):
        """ Method stub """
        pass

    
    def setup(self):
        """ Method stub """
        pass

    def frame(self):
        """ Method stub """
        pass



if __name__=='__main__':
    o1 = Object3D(pos=Vector(2, 0,-12), name="center").activate()
    o2 = Object3D(pos=Vector(3, 1,-12), name="right").activate()
    o3 = Object3D(pos=Vector(-4, 0,-12), name="left").activate()
    Axon.Scheduler.scheduler.run.runThreads()  

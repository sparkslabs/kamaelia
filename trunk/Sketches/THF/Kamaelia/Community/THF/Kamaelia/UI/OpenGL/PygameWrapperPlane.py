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
Wrapper for pygame components
=====================

A wrapper for two dimensional pygame components that allows to display them on a Plane in 3D using OpenGL.

This component is a subclass of OpenGLComponent and therefore uses the OpenGL display service.

Example Usage
-------------

The following example shows a wrapped Ticker and MagnaDoodle component:

    # override pygame display service
    ogl_display = OpenGL.Display.getDisplayService()
    Pygame.Display.setDisplayService(ogl_display[0])

    TICKER = Ticker(size = (150, 150)).activate()
    TICKER_WRAPPER = PygameWrapperPlane(wrap=TICKER, position=(4, 1,-15)).activate()
    MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
    MAGNADOODLEWRAPPER = PygameWrapperPlane(wrap=MAGNADOODLE, position=(-2, -2,-15)).activate()
    READER = ConsoleReader().activate()
    
    READER.link( (READER,"outbox"), (TICKER, "inbox") )
    
    Axon.Scheduler.scheduler.run.runThreads()  
    
How does it work?
-----------------

This component is a subclass of OpenGLComponent. It overrides __init__(), setup(), draw(), handleEvents() and frame().

In setup() the needed additional mailboxes are created. These are the "eventrequest" and "wrapcallback" inboxes and the "wrapped_events" outbox:
- "eventrequest" is used for the reception of ADDLISTENEVENT and REMOVELISTENEVENT requests of the wrapped component.
- "wrapcallback" is used to receive the response from the display service.
- "wrapped_events" is where the input events get sent to.

In frame(), first a WRAPPERREQUEST is sent to the OpenGL display service. This request has to include the surface of the wrapped component. The surface is dermined by simply accessing the object variable directly.  In return it gets the OpenGL texture name of the component that is to be wrapped. 


"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Util3D import *
from OpenGLComponent import *
from Intersect3D import *

import copy

class PygameWrapperPlane(OpenGLComponent):
    
    def __init__(self, **argd):
        super(PygameWrapperPlane, self).__init__(**argd)

        self.pixelscaling = argd.get("pixelscaling", 100.0)
        self.wrapped_comp = argd.get("wrap")
        self.name = argd.get("name")

        self.texname = 0
        self.texsize = (0,0)
        self.wrappedsize = (0,0)
        self.eventswanted = {}
        self.vertices = []

        self.sent = False
        self.received = False


    def setup(self):
        # used to receive event requests from the wrapped components
        self.addInbox("eventrequests")
        # for response to wrapperrequest
        self.addInbox("wrapcallback")
        self.addOutbox("wrapped_events")
        

    def draw(self):
        # set texure
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texname)

#        w = self.wrappedsize[0]/self.pixelscaling
#        h = self.wrappedsize[1]/self.pixelscaling
        w = self.size.x
        h = self.size.y
        # draw faces 
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBegin(GL_QUADS)
        glColor3f(0,1,0)
        glTexCoord2f(0.0, 1.0-self.texsize[1]);
        glVertex3f(-w, -h,  0.0)
        glTexCoord2f(self.texsize[0], 1.0-self.texsize[1]);
        glVertex3f( w, -h,  0.0)
        glTexCoord2f(self.texsize[0], 1.0);
        glVertex3f( w,  h,  0.0)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-w,  h,  0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)


    def handleEvents(self):
        while self.dataReady("events"):
            event = copy.copy(self.recv("events"))
            try:
                if self.eventswanted[event.type]:
                    if self.identifier in event.hitobjects:
                        # transform vertices for intersection test
                        self.transformedVertices = [self.transform.transformVector(v) for v in self.vertices]    
                        # calculate distance of intersection
                        t = Intersect3D.ray_Polygon(Vector(0,0,0), event.direction, self.transformedVertices);
                        # point of intersection
                        p = event.direction*t
                        Ap = p-self.transformedVertices[0]
                        # vectors of edges
                        AB = self.transformedVertices[1]-self.transformedVertices[0]
                        AD = self.transformedVertices[3]-self.transformedVertices[0]
                        # calc position on plane
                        x = Ap.dot(AB)/(AB.length()**2)
                        y = Ap.dot(AD)/(AD.length()**2)
                        event.pos = (x*self.wrappedsize[0],y*self.wrappedsize[1])

                        self.send([event], "wrapped_events")
            except KeyError: pass # event not wanted


    def frame(self):
        if not self.sent:
            try:
                wraprequest = { "WRAPPERREQUEST" : True,
                                        "wrapcallback" : (self, "wrapcallback"),
                                        "eventrequests" : (self, "eventrequests"),
                                        "surface": self.wrapped_comp.display }
                self.send( wraprequest, "display_signal")
                self.sent = True
            except AttributeError: pass
        elif not self.received:
            if self.dataReady("wrapcallback"):
                response = self.recv("wrapcallback")
                self.texname = response["texname"]
                self.texsize = response["texsize"]
                self.wrappedsize = response["size"]
                if response["eventswanted"] is not None:
                    self.eventswanted = response["eventswanted"]
                    #todo: request events
                if response["eventservice"] is not None:
                    self.link((self, "wrapped_events"), response["eventservice"])
                #prepare vertices for intersection test
                x = self.wrappedsize[0]/self.pixelscaling
                y = self.wrappedsize[1]/self.pixelscaling
                self.vertices = [ Vector(-x, y, 0.0), Vector(x, y, 0.0), Vector(x, -y, 0.0), Vector(-x, -y, 0.0) ]
                self.redraw()
                self.received = True
        else:
            self.handleEventRequests()            
            self.handleEvents()
    

    def handleEventRequests(self):
        while self.dataReady("eventrequests"):
            message = self.recv("eventrequests")

            if message.get("ADDLISTENEVENT", None) is not None:
                    #todo: request events
                self.eventswanted[message["ADDLISTENEVENT"]] = True

            elif message.get("REMOVELISTENEVENT", None) is not None:
                    #todo: request events
                self.eventswanted[message["REMOVELISTENEVENT"]] = False


if __name__=='__main__':

    # override pygame display service
    ogl_display = OpenGL.Display.getDisplayService()
    Pygame.Display.setDisplayService(ogl_display[0])

    TICKER = Ticker(size = (150, 150)).activate()
    TICKER_WRAPPER = PygameWrapperPlane(wrap=TICKER, position=(4, 1,-15)).activate()
    MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
    MAGNADOODLEWRAPPER = PygameWrapperPlane(wrap=MAGNADOODLE, position=(-2, -2,-15)).activate()
    READER = ConsoleReader().activate()
    
    READER.link( (READER,"outbox"), (TICKER, "inbox") )
    
    Axon.Scheduler.scheduler.run.runThreads()  

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
=============================
Wrapper for pygame components
=============================

A wrapper for two dimensional pygame components that allows to display
them on a Plane in 3D using OpenGL.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

Example Usage
-------------
The following example shows a wrapped Ticker and MagnaDoodle component::

    # override pygame display service
    ogl_display = OpenGLDisplay.getDisplayService()
    PygameDisplay.setDisplayService(ogl_display[0])

    TICKER = Ticker(size = (150, 150)).activate()
    TICKER_WRAPPER = PygameWrapper(wrap=TICKER, position=(4, 1,-10), rotation=(-20,15,3)).activate()
    MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
    MAGNADOODLEWRAPPER = PygameWrapper(wrap=MAGNADOODLE, position=(-2, -2,-10), rotation=(20,10,0)).activate()
    READER = ConsoleReader().activate()
    
    READER.link( (READER,"outbox"), (TICKER, "inbox") )
    
    Axon.Scheduler.scheduler.run.runThreads()  
    
How does it work?
-----------------
This component is a subclass of OpenGLComponent. It overrides
__init__(), setup(), draw(), handleEvents() and frame().

In setup() first the needed additional mailboxes are created. These are
the "eventrequest" and "wrapcallback" inboxes and the "wrapped_events"
outbox:

- "eventrequest" is used for the reception of ADDLISTENEVENT and REMOVELISTENEVENT requests of the wrapped component.
- "wrapcallback" is used to receive the response from the display service.
- "wrapped_events" is where the input events get sent to.

Additionally, a WRAPPERREQUEST is sent to the OpenGL display service. It
contains the objectid of the wrapped component as well as the comms for
callback and eventrequests.

In frame(), it is waited for the response on the WRAPPERREQUEST. The
response should contain the OpenGL texture name, the texture size and
the size of the wrapped component. The wanted events are stored and the
"wrapped_events" outbox is linked to the wrapped components "events"
inbox. If the size of the wrapper is not set, it is calculated using the
wrapped component pixel size multiplied by the pixelscaling factor.

To handle event requests by the wrapped component, the method
handleEventRequests() gets called.

In handleEvents() received mouse events get translated into the 2d space
of the wrapped component and sent to it if requested. This is done by
using ray/polygon intersection to determine the point of intersection in
3d. The 2d coordinates are then calculated by using the dot product
between the point of intersection relative to the top left corner and
the edge vectors.

In draw() a cuboid gets drawn with the texture of the pygame component
on its front plane. If the z component of the size is set to zero, only
the front plane is drawn.

"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Vector import Vector
from Transform import Transform
from OpenGLComponent import *
from Intersect import *

import copy

class PygameWrapper(OpenGLComponent):
    """\
    PygameWrapper(...) -> A new PygameWrapper component.
    
    A wrapper for two dimensional pygame components that allows to display
    them on a Plane in 3D using OpenGL.
    
    Keyword arguments:
    
    - wrap          -- Pygame component to wrap
    - pixelscaling  -- Factor to convert pixels to units in 3d, ignored if size is specified (default=100)
    - sidecolour    -- Colour of side and back planes (default=(200,200,244))
    - thickness     -- Thickness of wrapper, ignored if size is specified (default=0.3)
    """
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PygameWrapper, self).__init__(**argd)

        self.pixelscaling = argd.get("pixelscaling", 100.0)
        self.sideColour = argd.get("sidecolour", (200,200,244))
        self.wrapped_comp = argd.get("wrap")
        self.thickness = argd.get("thickness", 0.3)

        self.texname = 0
        self.texsize = (0,0)
        self.wrappedsize = (0,0)
        self.eventswanted = {}
        self.vertices = []



    def setup(self):
        # used to receive event requests from the wrapped components
        self.addInbox("eventrequests")
        # for response to wrapperrequest
        self.addInbox("wrapcallback")
        self.addOutbox("wrapped_events")
        
        # send wrapper request
        wraprequest = { "WRAPPERREQUEST" : True,
                                "wrapcallback" : (self, "wrapcallback"),
                                "eventrequests" : (self, "eventrequests"),
                                "wrap_objectid": id(self.wrapped_comp) }
        self.send( wraprequest, "display_signal")
        

    def draw(self):
        """ Draw cuboid."""
        hs = self.size/2.0
        
        if hs.z != 0:
            # draw faces
            glBegin(GL_QUADS)
            glColor4f(self.sideColour[0]/256.0, self.sideColour[1]/256.0, self.sideColour[2]/256.0, 0.5)

            glVertex3f(hs.x,hs.y,hs.z)
            glVertex3f(hs.x,-hs.y,hs.z)
            glVertex3f(hs.x,-hs.y,-hs.z)
            glVertex3f(hs.x,hs.y,-hs.z)

            glVertex3f(-hs.x,hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,-hs.z)
            glVertex3f(-hs.x,hs.y,-hs.z)

            glVertex3f(hs.x,hs.y,hs.z)
            glVertex3f(-hs.x,hs.y,hs.z)
            glVertex3f(-hs.x,hs.y,-hs.z)
            glVertex3f(hs.x,hs.y,-hs.z)

            glVertex3f(hs.x,-hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,-hs.z)
            glVertex3f(hs.x,-hs.y,-hs.z)

            glVertex3f(hs.x,hs.y,-hs.z)
            glVertex3f(-hs.x,hs.y,-hs.z)
            glVertex3f(-hs.x,-hs.y,-hs.z)
            glVertex3f(hs.x,-hs.y,-hs.z)
            glEnd()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texname)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

        glBegin(GL_QUADS)
        # front plane
        glTexCoord2f(0.0, 1.0-self.texsize[1])
        glVertex3f(-hs.x,-hs.y,hs.z)
        glTexCoord2f(self.texsize[0], 1.0-self.texsize[1])
        glVertex3f(hs.x,-hs.y,hs.z)
        glTexCoord2f(self.texsize[0], 1.0)
        glVertex3f(hs.x,hs.y,hs.z)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x,hs.y,hs.z)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)


    def handleEvents(self):
        while self.dataReady("events"):
            event = copy.copy(self.recv("events"))
            try:
                if self.eventswanted[event.type] and self.identifier in event.hitobjects:
                    # transform vertices for intersection test
                    self.transformedVertices = [self.transform.transformVector(v) for v in self.vertices]    
                    # calculate distance of intersection
                    t = Intersect.ray_Polygon(Vector(0,0,0), event.direction, self.transformedVertices);
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
        if self.dataReady("wrapcallback"):
            response = self.recv("wrapcallback")
            self.texname = response["texname"]
            self.texsize = response["texsize"]
            self.wrappedsize = response["size"]

            if response["eventswanted"] is not None:
                self.eventswanted = response["eventswanted"]
                wantedevents = []
                for (event, wanted) in self.eventswanted.items():
                    if wanted: wantedevents.append(event)
                self.addListenEvents( wantedevents )

            if response["eventservice"] is not None:
                self.link((self, "wrapped_events"), response["eventservice"])
            
            # calc size if not set
            if self.size == Vector(0,0,0):
                w = self.wrappedsize[0]/self.pixelscaling
                h = self.wrappedsize[1]/self.pixelscaling
                self.size = Vector(w, h, self.thickness)

            #prepare vertices for intersection test
            hs = self.size/2.0
            self.vertices = [ Vector(-hs.x, hs.y, hs.z),
                              Vector(hs.x, hs.y, hs.z),
                              Vector(hs.x, -hs.y, hs.z),
                              Vector(-hs.x, -hs.y, hs.z)
                            ]

            self.redraw()

        self.handleEventRequests()            
    

    def handleEventRequests(self):
        while self.dataReady("eventrequests"):
            message = self.recv("eventrequests")

            if message.get("ADDLISTENEVENT", None) is not None:
                self.eventswanted[message["ADDLISTENEVENT"]] = True
                self.addListenEvents([message["ADDLISTENEVENT"]])

            elif message.get("REMOVELISTENEVENT", None) is not None:
                self.eventswanted[message["REMOVELISTENEVENT"]] = False
                self.removeListenEvents([message["REMOVELISTENEVENT"]])


__kamaelia_components__ = (PygameWrapper,)

if __name__=='__main__':
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.UI.PygameDisplay import PygameDisplay
    from Kamaelia.UI.Pygame.Ticker import Ticker
    import sys;
    sys.path.append("../Pygame/")
    from MagnaDoodle import *
    
    # override pygame display service
    ogl_display = OpenGLDisplay.getDisplayService()
    PygameDisplay.setDisplayService(ogl_display[0])

    TICKER = Ticker(size = (150, 150)).activate()
    TICKER_WRAPPER = PygameWrapper(wrap=TICKER, position=(4, 1,-10), rotation=(-20,15,3)).activate()
    MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
    MAGNADOODLEWRAPPER = PygameWrapper(wrap=MAGNADOODLE, position=(-2, -2,-10), rotation=(20,10,0)).activate()
    READER = ConsoleReader().activate()
    
    READER.link( (READER,"outbox"), (TICKER, "inbox") )
    
    Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF

#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
General 3D Object
=====================
TODO
"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Display3D import Display3D
from Util3D import *
from Object3D import *

from Intersect3D import *

import copy

class PygameWrapperPlane(Object3D):
    
    def __init__(self, **argd):
        super(PygameWrapperPlane, self).__init__(**argd)

        self.pixelscaling = argd.get("pixelscaling", 100.0)
        self.wrapped_comp = argd.get("wrap")
        self.name = argd.get("name")

        self.addInbox("eventrequests")
        self.addInbox("wrapcallback")
        self.addOutbox("wrapped_eventsfeedback")
        self.texname = 0
        self.texsize = (0,0)
        self.wrappedsize = (0,0)
        self.eventswanted = {}
        self.vertices = []


    def setup(self):
        self.addListenEvents( [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
        self.sent = False
        self.received = False


    def draw(self):
        # set texure
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texname)

        w = self.wrappedsize[0]/self.pixelscaling
        h = self.wrappedsize[1]/self.pixelscaling
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
        while self.dataReady("inbox"):
            event = copy.copy(self.recv("inbox"))
            try:
                if self.eventswanted[event.type]:
                    if self.ogl_name in event.hitobjects:
                        # transform vertices for intersection test
                        self.transformedVertices = [self.transform.transformVector(v) for v in self.vertices]    
                        # calculate distance of intersection
                        t = Intersect3D.ray_Polygon(Vector(0,0,0), event.dir, self.transformedVertices);
                        # point of intersection
                        p = event.dir*t
                        Ap = p-self.transformedVertices[0]
                        # vectors of edges
                        AB = self.transformedVertices[1]-self.transformedVertices[0]
                        AD = self.transformedVertices[3]-self.transformedVertices[0]
                        # calc position on plane
                        x = Ap.dot(AB)/(AB.length()**2)
                        y = Ap.dot(AD)/(AD.length()**2)
                        event.pos = (x*self.wrappedsize[0],y*self.wrappedsize[1])

                        self.send([event], "wrapped_eventsfeedback")
            except KeyError: pass # events not wanted


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
                if response["eventservice"] is not None:
                    self.link((self, "wrapped_eventsfeedback"), response["eventservice"])
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
                self.eventswanted[message["ADDLISTENEVENT"]] = True

            elif message.get("REMOVELISTENEVENT", None) is not None:
                self.eventswanted[message["REMOVELISTENEVENT"]] = False


if __name__=='__main__':
    class Bunch: pass
        
    text = """\
The size of these 2 Ticker components is (150,150).
The wrapped button is now fully functional (assigned to SPACE).
Bottom left there is a Magna Doodle (tm) component. You can draw 
green lines on it by using your left mouse button. Use the right mouse
button to erase your artwork.
"""
    class datasource(Axon.Component.component):
        def main(self):
            for x in text.split():
                self.send(x,"outbox")
                yield 1
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from Kamaelia.Util.Graphline import Graphline
    from Kamaelia.UI.Pygame.Ticker import Ticker
    from Kamaelia.UI.Pygame.Button import Button
    from SimpleCube import *
    import sys;
    sys.path.append("../../pygame/")
    from MagnaDoodle import *

    display3d = Display3D.getDisplayService()
    PygameDisplay.setDisplayService(display3d[0])
   
    TEXT = datasource().activate()
    TICKER1 = Ticker(size = (150, 150), render_left = 0, render_right=350, render_top=0, render_bottom=250).activate()
    TICKER1WRAPPER = PygameWrapperPlane(wrap=TICKER1, pos=Vector(-4, 1,-15), name="1st Wrapper Plane").activate()
    TICKER2 = Ticker(size = (150, 150), render_left = 0, render_right=350, render_top=0, render_bottom=250).activate()
    TICKER2WRAPPER = PygameWrapperPlane(wrap=TICKER2, pos=Vector(4, 1,-15),  name="2nd Wrapper Plane").activate()
    BUTTON = Button(caption="This button...",msg="...can be moved AND activated!", key=pygame.K_SPACE).activate()
    BUTTONWRAPPER = PygameWrapperPlane(wrap=BUTTON, pos=Vector(0, 0,-10),  name="Button Wrapper Plane").activate()
    BUTTON1 = Button(caption="This button...",msg="...also!", key=pygame.K_LCTRL).activate()
    BUTTONWRAPPER1 = PygameWrapperPlane(wrap=BUTTON1, pos=Vector(0, 0.4,-10),  name="Button1 Wrapper Plane").activate()
    MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
    MAGNADOODLEWRAPPER = PygameWrapperPlane(wrap=MAGNADOODLE, pos=Vector(-2, -2,-15),  name="Magna Doodle Wrapper Plane").activate() 
    ECHO = consoleEchoer().activate()
    CUBE = SimpleCube(pos = Vector(2,-2,-10)).activate()
    TICKER1WRAPPER.link((TICKER1WRAPPER, "outbox"), (TICKER2, "inbox"))
    TICKER2WRAPPER.link((TICKER2WRAPPER, "outbox"), (TICKER2, "inbox"))
    BUTTON.link((BUTTON, "outbox"), (TICKER2, "inbox"))
    BUTTON1.link((BUTTON1, "outbox"), (TICKER2, "inbox"))
    TEXT.link((TEXT, "outbox"), (TICKER1, "inbox"))
        
    Axon.Scheduler.scheduler.run.runThreads()  

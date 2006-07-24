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


import pygame
import Axon
from Axon.ThreadedComponent import threadedcomponent
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

from Kamaelia.UI.PygameDisplay import PygameDisplay
from Util3D import *
import time

_cat = Axon.CoordinatingAssistantTracker

class Bunch: pass

class Display3D(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes =  { "inbox"    : "Default inbox, not currently used",
                     "control" : "NOT USED",
                     "notify"  : "Receive requests for surfaces, overlays and events",
                     "events" : "Receive pygame events",
                  }
    Outboxes = { "outbox" : "NOT USED",
                     "signal" : "NOT USED",
                  }
                
                 
    def setDisplayService(pygamedisplay, tracker = None):
        """\
        Sets the given pygamedisplay as the service for the selected tracker or
        the default one.

        (static method)
        """
        if not tracker:
            tracker = _cat.coordinatingassistanttracker.getcat()
        tracker.registerService("3ddisplay", pygamedisplay, "notify")
    setDisplayService = staticmethod(setDisplayService)

    def getDisplayService(tracker=None): # STATIC METHOD
        """\
        Returns any live pygamedisplay registered with the specified (or default)
        tracker, or creates one for the system to use.

        (static method)
        """
        if tracker is None:
            tracker = _cat.coordinatingassistanttracker.getcat()
        try:
            service = tracker.retrieveService("3ddisplay")
            return service
        except KeyError:
            display = Display3D()
            display.activate()
            Display3D.setDisplayService(display, tracker)
            service=(display,"notify")
            return service
    getDisplayService = staticmethod(getDisplayService)
    
        
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Display3D,self).__init__()
        self.caption = argd.get("title", "http://kamaelia.sourceforge.net")
        self.width = argd.get("width",800)
        self.height = argd.get("height",600)
        self.background_colour = argd.get("background_colour", (255,255,255))
        self.fullscreen = pygame.FULLSCREEN * argd.get("fullscreen", 0)
        self.showFPS = argd.get("showFPS", True)
        
        # data for FPS measurement
        self.lastTime = 0
        self.fps = 0
        self.fpscounter = 0

        # 3D component handling
        self.objects = []
        self.sizes = {}
        self.displaylists = {}
        self.transforms = {}
        self.eventcomms = {}
        self.nextName = 1
        
        # determine projection parameters
        self.nearPlaneDist = argd.get("near", 1.0)
        self.farPlaneDist = argd.get("far", 100.0)
        self.perspectiveAngle = argd.get("perspective", 45.0)
        self.aspectRatio = float(self.width)/float(self.height)
        global pi
        self.farPlaneHeight = self.farPlaneDist*2.0/tan(pi/2.0-self.perspectiveAngle*pi/360.0)
        self.farPlaneWidth = self.farPlaneHeight*self.aspectRatio
        self.farPlaneScaling = self.farPlaneWidth/self.width
        
        # initialize the display      
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height), self.fullscreen| pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(self.caption)
        pygame.mixer.quit()
        
        glClearColor(1.0,1.0,1.0,0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        
        # enable translucency
#        glEnable (GL_BLEND);
#        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        # projection matrix
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()                                
        gluPerspective(self.perspectiveAngle, self.aspectRatio, self.nearPlaneDist, self.farPlaneDist)
    
        
    def handleDisplayRequest(self):
            while self.dataReady("notify"):
                message = self.recv("notify")
                if isinstance(message, Axon.Ipc.producerFinished): ### VOMIT : mixed data types
                    surface = message.message
                    message.message = None
                    message = None
                    self.surfaces = [ x for x in self.surfaces if x[0] is not surface ]
                    try:
                         eventcomms = self.surface_to_eventcomms[str(id(surface))]
                    except KeyError:
                         pass
                    else:
                         self.visibility = None
                         try:
                              self.removeOutbox(eventcomms)
                         except:
                              "This sucks"
                              pass
                elif message.get("3DDISPLAYREQUEST", False):
                    # generate a identifier for the requesting object
                    ident = self.nextName
                    self.nextName += 1
                    # store object
                    self.objects.append(ident)
                    self.sizes[ident] = message.get("size")
                    self.displaylists[ident] = message.get("displaylist")
                    self.transforms[ident] = message.get("transform")
                    # connect to eventcallback
                    eventservice = message.get("events", None)
                    if eventservice is not None:
                        eventcomms = self.addOutbox("eventsfeedback")
                        self.eventcomms[ident] = eventcomms
                        self.link((self,eventcomms), eventservice)
                        
#                    callbackcomms = self.addOutbox("displayerfeedback")
#                    self.link((self, callbackcomms), callbackservice)
#                    self.send(surface, callbackcomms)
                        

    def handleEvents(self):
        # pre-fetch all waiting events in one go
        events = [ event for event in pygame.event.get() ]

        # Determine direction vectors
        directions = {}
        for event in events:
            if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                # determine intersection ray
                xclick = float(event.pos[0]-self.width/2)*self.farPlaneWidth/float(self.width)
                yclick = float(-event.pos[1]+self.height/2)*self.farPlaneHeight/float(self.height)
                directions[id(event)] = Vector(xclick, yclick, -self.farPlaneDist).norm()

        # Handle events
        for event in events:
            if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                # compose event data
                e = Bunch()
                e.type = event.type
                e.pos = event.pos
                e.dir = directions[id(event)]
                if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
                    e.button = event.button
                if event.type == pygame.MOUSEMOTION:
                    e.rel = event.rel
                    e.buttons = event.buttons
                # object picking
                glSelectBuffer(512)
                glRenderMode(GL_SELECT)
                # prepare matrices
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glLoadIdentity()
                gluPickMatrix(event.pos[0], self.height-event.pos[1], 1, 1)
                gluPerspective(self.perspectiveAngle, self.aspectRatio, self.nearPlaneDist, self.farPlaneDist)
                # "draw" objects in select mode
                glInitNames()
                glPushName(0)
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                for obj in self.objects:
                    glLoadMatrixf(self.transforms[obj].getMatrix())
                    glLoadName(obj)
                    glCallList(self.displaylists[obj])
                glPopMatrix()

                # restore matrices
                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                # force completion
                glFlush()
                
                # process hits                
                hits = glRenderMode(GL_RENDER)
                for hit in hits:
                    self.send(e, self.eventcomms[hit[2][0]])
                    
        
    def drawBackground(self):
        glBegin(GL_QUADS)
        glColor4f(0.85, 0.85, 1.0, 1.0)
        glVertex3f(-self.farPlaneWidth/2.0, self.farPlaneHeight/2.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, self.farPlaneHeight/2.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glVertex3f(-self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glColor4f(0.75, 1.0, 0.75, 1.0)
        glVertex3f(-self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, 0.0, -self.farPlaneDist)
        glVertex3f(self.farPlaneWidth/2.0, -self.farPlaneHeight/2.0, -self.farPlaneDist)
        glVertex3f(-self.farPlaneWidth/2.0, -self.farPlaneHeight/2.0, -self.farPlaneDist)
        glEnd()
        

        
    def updateDisplay(self):
        # draw all 3D objects
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        for obj in self.objects:
            glLoadMatrixf(self.transforms[obj].getMatrix())
            glCallList(self.displaylists[obj])
        glPopMatrix()
        
        # show frame
        glFlush()
        pygame.display.flip()
        
        # clear drawing buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # draw background
        self.drawBackground()

        

    def main(self):
        """Main loop."""

        while 1:
            #show fps
            if self.showFPS:
                self.fpscounter += 1
                if self.fpscounter > 100:
                    # determine fps
                    currentTime = time.time()
                    self.fps = 100/(currentTime-self.lastTime)
                    self.lastTime = currentTime
                    pygame.display.set_caption("%s FPS:%d" % (self.caption, self.fps) )
                    self.fpscounter = 0

            self.handleDisplayRequest()
            self.handleEvents()
            self.updateDisplay()
            yield 1




if __name__=='__main__':
        
    Axon.Scheduler.scheduler.run.runThreads()  

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
General 3D Object
=====================
TODO
"""

import pygame
import Axon
from OpenGL.GL import *
from OpenGL.GLU import *
from math import tan, pi
from Util3D import *
from Axon.ThreadedComponent import threadedcomponent
import time

_cat = Axon.CoordinatingAssistantTracker

#"events" : (self, "events"),#

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
        self.objects = []
        self.events_wanted = {}
        self.surface_to_eventcomms = {}

        self.nearPlaneDist = argd.get("near", 1.0)
        self.farPlaneDist = argd.get("far", 100.0)
        self.perspectiveAngle = argd.get("perspective", 45.0)
        self.aspectRatio = float(self.width)/float(self.height)
        global pi
        self.farPlaneHeight = self.farPlaneDist*2.0/tan(pi/2.0-self.perspectiveAngle*pi/360.0)
        self.farPlaneWidth = self.farPlaneHeight*self.aspectRatio
        
        pygame.init()
        
    def handleDisplayRequest(self):
            """\
            Check "notify" inbox for requests for surfaces, events and overlays and
            process them.
            """
            if self.dataReady("notify"):
                message = self.recv("notify")
                if isinstance(message, Axon.Ipc.producerFinished): ### VOMIT : mixed data types
#                    print "SURFACE", message
                    surface = message.message
#                    print "SURFACE", surface
                    message.message = None
                    message = None
#                    print "BEFORE", [id(x[0]) for x in self.surfaces]
                    self.surfaces = [ x for x in self.surfaces if x[0] is not surface ]
#                    print "AFTER", self.surfaces
#                    print "Hmm...", self.surface_to_eventcomms.keys()
                    try:
                         eventcomms = self.surface_to_eventcomms[str(id(surface))]
                    except KeyError:
                         # This simply means the component wasn't listening for events!
                         pass
                    else:
#                         print "EVENT OUTBOX:", eventcomms
                         self.visibility = None
                         try:
                              self.removeOutbox(eventcomms)
                         except:
                              "This sucks"
                              pass
#                         print "REMOVED OUTBOX"
                elif message.get("3DDISPLAYREQUEST", False):
                    eventservice = message.get("events", None)
                    eventcomms = None
                    if eventservice is not None:
                        eventcomms = self.addOutbox("eventsfeedback")
                        self.link((self,eventcomms), eventservice)
                    
                    self.objects.append( (message.get("object"), eventcomms) )
                    
                elif message.get("ADDLISTENEVENT", None) is not None:
                    eventcomms = self.surface_to_eventcomms[str(id(message["object3d"]))]
                    self.events_wanted[eventcomms][message["ADDLISTENEVENT"]] = True

                elif message.get("REMOVELISTENEVENT", None) is not None:
                    eventcomms = self.surface_to_eventcomms[str(id(message["object3d"]))]
                    self.events_wanted[eventcomms][message["REMOVELISTENEVENT"]] = False
                        

    def handleEvents(self):
        # pre-fetch all waiting events in one go
        events = [ event for event in pygame.event.get() ]

        directions = {}
        for event in events:
            if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                # determine intersection ray
                xclick = float(event.pos[0]-self.width/2)*self.farPlaneWidth/float(self.width)
                yclick = float(-event.pos[1]+self.height/2)*self.farPlaneHeight/float(self.height)
                directions[event] = Vector(xclick, yclick, -self.farPlaneDist).norm()

        for obj, eventcomms in self.objects:
            # see if this component is interested in events
            if eventcomms is not None:
                # go through events, for each, check if the listener is interested in that time of event         
                bundle = []
                for event in events:
                    if event.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN ]:
                        e = Bunch()
                        e.type = event.type
                        e.dir = directions[event]
                        if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
                            e.button = event.button
                        if event.type == pygame.MOUSEMOTION:
                            e.rel = event.rel
                            e.buttons = event.buttons
    
                        bundle.append(e)
    
                # only send events to listener if we've actually got some
                if bundle != []:
                    self.send(bundle, eventcomms)
        
    def updateDisplay(self):
        # Display
        glFlush()
        pygame.display.flip()

        # clear drawing buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def main(self):
        """Main loop."""
        # initialize the display      
        display = pygame.display.set_mode((self.width, self.height), self.fullscreen| pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(self.caption)
        pygame.mixer.quit()

        # set clear color
        glClearColor(0,0,0,1.0)
        # enable depth tests
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)

        # projection matrix
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()                                
        gluPerspective(self.perspectiveAngle, self.aspectRatio, self.nearPlaneDist, self.farPlaneDist)
        # model matrix

        while 1:
            self.handleDisplayRequest()
            self.handleEvents()
            self.updateDisplay()
            yield 1

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

_cat = Axon.CoordinatingAssistantTracker

#"events" : (self, "events"),#


class Display3D(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes =  { "inbox"    : "Default inbox, not currently used",
                     "control" : "NOT USED",
                     "notify"  : "Receive requests for surfaces, overlays and events",
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
                    pass
                elif message.get("ADDLISTENEVENT", None) is not None:
                    eventcomms = self.surface_to_eventcomms[str(id(message["object3d"]))]
                    self.events_wanted[eventcomms][message["ADDLISTENEVENT"]] = True

                elif message.get("REMOVELISTENEVENT", None) is not None:
                    eventcomms = self.surface_to_eventcomms[str(id(message["object3d"]))]
                    self.events_wanted[eventcomms][message["REMOVELISTENEVENT"]] = False
                        

    def updateDisplay(self,display):
        """\
            Clear the screen, handle input and draw all registered objects
        """
        # pre-fetch all waiting events in one go
        events = [ event for event in pygame.event.get() ]

        # handle input
        # TODO
        
        # Draw objects
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()                                
        #TODO

        # Display
        glFlush()
        pygame.display.flip()

        # clear drawing buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def main(self):
        """Main loop."""
        # initialize the display      
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height), self.fullscreen| pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(self.caption)
        pygame.mixer.quit()

        # clear color
        glClearColor(0,0,0,1.0)
        # enable depth tests
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)

        # projection matrix
        glMatrixMode(GL_PROJECTION)                 
        glLoadIdentity()                                
        gluPerspective(45.0, self.width/self.height, 0.1, 100.0)
        # model matrix

        while 1:
            self.handleDisplayRequest()
            self.updateDisplay(display)
            yield 1

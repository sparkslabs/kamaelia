#!/usr/bin/env python
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
from pygame.locals import *
import Axon as _Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay

class PyGameApp(_Axon.Component.component):
    """Simple Axon component for a PyGame application.
    
    Provides a simple main loop and PyGame event dispatch mechanism.

    Implement your runtime loop in mainLoop().
    
    Use addHandler() and removeHandler() register handlers for pygame events.
        
    """
    Inboxes = ["inbox", "events", "displaycontrol", "control"]
    Outboxes = [ "signal", "outbox", "displaysignal" ]

    def __init__(self, screensize, caption="PyGame Application", fullscreen=False, depth=0):
        super(PyGameApp, self).__init__()
        pygame.init()
        
        flags = DOUBLEBUF
        if fullscreen:
            flags = flags | -abs(FULLSCREEN)
        self.flags = flags
        self.depth = depth
        self.screensize = screensize
        self.caption = caption

        self.eventHandlers = {}
        
        self.flip = False
    
    def waitBox(self,boxname):
        waiting = True
        while waiting:
           if self.dataReady(boxname): return
           else: yield 1

    def main(self):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"displaysignal"), displayservice)
        self.send({ "DISPLAYREQUEST" : True,
                    "events" : (self, "events"),
                    "callback" : (self, "displaycontrol"),
                    "size" : self.screensize,
                  }, "displaysignal")
        for _ in self.waitBox("displaycontrol"): 
#             print "Waiting for display"
            yield 1
        display = self.recv("displaycontrol")

        self.screen = display
        pygame.display.set_caption(self.caption)
        self.screensize = self.screen.get_width(), self.screen.get_height()
        self.addHandler(QUIT, lambda event : self.quit(event))
        self.flip = True

        self.initialiseComponent()
        self.quitting = False
        # Event loop
        while not self.quitting:
            self._dispatch()
            if not self.quitting:
                self.mainLoop()
            if not self.quitting and self.flip:
                pygame.display.flip()
                yield 1
            else:
                yield 0
        print "QUIT"

    def initialiseComponent(self):
        pass
        
    def go(self):
        """Call this to run the pygame app, without using an Axon scheduler.
        
           Returns when the app 'quits'
        """
        for i in self.main():
           pass

    def mainLoop(self):
        """Implement your runtime loop in this method here."""
        return 1


    def events(self):
       while self.dataReady("events"):
          event_bundle = self.recv("events")
          for event in event_bundle:
             yield event

    def _dispatch(self):
        """Internal pygame event dispatcher.
        
           For all events received, it calls all event handlers in sequence
           until one returns True
        """
#        for event in pygame.event.get():
        for event in self.events():
            if self.eventHandlers.has_key(event.type):
                for handler in self.eventHandlers[event.type]:
                    if handler(event):
                        break

    def addHandler(self, eventtype, handler):
        """Add an event handler, for a given PyGame event type.
        
        Handler is passed the pygame event object when called.
        
        Multiple handlers can be registered for a given PyGame event.
        They are called in the order in which they are registered.
        
        The even is passed to all registered handlers, in the order in
        which they were registered. If, however, one of the handlers returns
        something that evaluates to True, then the event is deemed to have
        been 'claimed' and it will not be passed on any further.
        """
        if not self.eventHandlers.has_key(eventtype):
            self.eventHandlers[eventtype] = []
            self.send({ "ADDLISTENEVENT" : eventtype,
                        "surface" : self.screen,
                      }, "displaysignal")
        self.eventHandlers[eventtype] += [handler]
        return handler
            
    def removeHandler(self, eventtype, handler):
        """Remove the specified pygame event handler"""
        if self.eventHandlers.has_key(eventtype): 
            self.eventHandlers[eventtype].remove(handler) # Latent bug, handler not in list
#            if len(self.eventHandlers[eventtype]) == 0:
#               self.send({ "REMOVELISTENEVENT" : eventtype,
#                           "surface" : self.screen,
#                         }, "displaysignal")


    def quit(self, event = None):
        """Call this method/event handler to finish"""
        self.quitting = True

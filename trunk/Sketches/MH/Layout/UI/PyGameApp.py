#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import pygame
from pygame.locals import *
import Axon as _Axon

class PyGameApp(_Axon.Component.component):
    """Simple Axon component for a PyGame application.
    
    Provides a simple main loop and PyGame event dispatch mechanism.

    Implement your runtime loop in mainLoop().
    
    Use addHandler() and removeHandler() register handlers for pygame events.
        
    """

    def __init__(self, screensize, caption="PyGame Application", fullscreen=False, depth=0):
        super(PyGameApp, self).__init__()
        pygame.init()
        
        flags = DOUBLEBUF
        if fullscreen:
            flags = flags | -abs(FULLSCREEN)
        self.screen = pygame.display.set_mode( screensize, flags, depth )
        pygame.display.set_caption(caption)

        self.eventHandlers = {}
        self.screensize = self.screen.get_width(), self.screen.get_height()
        self.addHandler(QUIT, lambda event : self.quit(event))
        
        self.flip = True
    
    def initialiseComponent(self):
        pass
        
    def go(self):
        """Call this to run the pygame app, without using an Axon scheduler.
        
           Returns when the app 'quits'
        """
        for i in self.main():
           pass

    def main(self):
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

    def mainLoop(self):
        """Implement your runtime loop in this method here."""
        return 1


    def _dispatch(self):
        """Internal pygame event dispatcher.
        
           For all events received, it calls all event handlers in sequence
           until one returns True
        """
        for event in pygame.event.get():
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
        self.eventHandlers[eventtype] += [handler]
        return handler
            
    def removeHandler(self, eventtype, handler):
        """Remove the specified pygame event handler"""
        if self.eventHandlers.has_key(eventtype):
            self.eventHandlers[eventtype].remove(handler)

    def quit(self, event = None):
        """Call this method/event handler to finish"""
        self.quitting = True

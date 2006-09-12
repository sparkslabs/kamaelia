#!/usr/bin/env python
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===================================
Simple Pygame application framework
===================================

A component that sets up a pygame display surface and provides a main loop and
simple event dispatch framework.

The rendering surface is requested from the Pygame Display service component, so
this component can coexist with other components using pygame.



Example Usage
-------------
::
    class SimpleApp1(PyGameApp):
    
        def initialiseComponent(self):
            self.addHandler(MOUSEBUTTONDOWN, lambda event : self.mousedown(event))
            
        def mainLoop(self):
            ... draw and do other stuff here...
            return 1

        def mousedown(self, event):
            print "Mouse down!"
    
    app = SimpleApp1( (800,600) ).run()



How does it work?
-----------------

Subclass this component to implement your own pygame 'app'. Replace the
mainLoop() stub with your own code to redraw the display surface etc. This
method will be called every cycle - do not incorporate your own loop!

The self.screen attribute is the pygame surface you should render to.

The component provides a simple event dispatch framework. Call addHandler and
removeHandler to register and deregister handlers from events.

More than one handler can be registered for a given event. They are called in
the order in which they were registered. If a handler returns True then the
event is 'claimed' and no further handlers will be called.

The component will terminate if the user clicks the close button on the pygame
display window, however your mainLoop() method will not be notified, and there
is no specific 'quit' event handler.
"""


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX TODO
#
# - 'mainloop' ought to be modded to be a true loop - something that yields.
#   but users of this class will need to be modded too.
# - redundant args in initialiser need removing too (same applies)
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import pygame
from pygame.locals import *
import Axon as _Axon
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class PyGameApp(_Axon.Component.component):
    """\
    PyGameApp(screensize[,caption][,transparency][,position]) -> new PyGameApp component.

    Creates a PyGameApp component that obtains a pygame display surface and provides
    an internal pygame event dispatch mechanism.

    Subclass to implement your own pygame "app".
    
    Keyword arguments:
    
    - screensize    -- (width,height) of the display area (default = (800,600))
    - caption       -- Caption for the pygame window (default = "Topology Viewer")
    - fullscreen    -- True to start up in fullscreen mode (default = False)
    - transparency  -- None, or (r,g,b) colour to make transparent
    - position      -- None, or (left,top) position for surface within pygame window
    """
    
    Inboxes  = { "inbox"          : "NOT USED",
                 "control"        : "NOT USED",
                 "events"         : "Event notifications from Pygame Display service",
                 "displaycontrol" : "Replies from Pygame Display service",
               }
    Outboxes = { "signal"        : "NOT USED",
                 "outbox"        : "NOT USED",
                 "displaysignal" : "Requests to Pygame Display service",
               }

    def __init__(self, screensize, 
                 caption="PyGame Application", 
                 fullscreen=False, 
                 depth=0, 
                 transparency = None,
                 position = None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PyGameApp, self).__init__()
        pygame.init() # FIXME: This should NEVER be called inside a component unless it is the
                      #        PygameDisplay or GraphicDisplay or similar.
        
#        flags = DOUBLEBUF
#        if fullscreen:
#            flags = flags | -abs(FULLSCREEN)
#        self.flags = flags
#        self.depth = depth
        self.screensize = screensize
        self.caption = caption
        self.transparency = transparency
        self.eventHandlers = {}
        self.position = position
        
        self.flip = False
    
    def waitBox(self,boxname):
        """Generator. Yields until data ready on the named inbox."""
        waiting = True
        while waiting:
           if self.dataReady(boxname): return
           else: yield 1

    def main(self):
        """Main loop. Do not override"""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"displaysignal"), displayservice)
        displayrequest = { "DISPLAYREQUEST" : True,
                    "events" : (self, "events"),
                    "callback" : (self, "displaycontrol"),
                    "transparency": self.transparency,
                    "size" : self.screensize,
                  }
        if self.position is not None:
           displayrequest["position"] = self.position
        self.send(displayrequest, "displaysignal")
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
            self.send({"REDRAW":True, "surface":self.screen}, "displaysignal")
            if not self.quitting and self.flip:
                # FIXME: This does not play nicely at all with the standard pygame display
                #        handling, despite requesting it's display from the standard
                #        location.
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
        """Implement your runtime loop in this method here.
           FIXME: This is less than ideal.
        """
        return 1


    def events(self):
       """Generator. Receive events on "events" inbox and yield then one at a time."""
       while self.dataReady("events"):
          event_bundle = self.recv("events")
          for event in event_bundle:
             yield event

    def _dispatch(self):
        """\
        Internal pygame event dispatcher.
        
        For all events received, it calls all event handlers in sequence
        until one returns True.
        """
        for event in self.events():
            if self.eventHandlers.has_key(event.type):
                for handler in self.eventHandlers[event.type]:
                    if handler(event):
                        break

    def addHandler(self, eventtype, handler):
        """\
        Add an event handler, for a given PyGame event type.
        
        The handler is passed the pygame event object as its argument when called.
        """
        if not self.eventHandlers.has_key(eventtype):
            self.eventHandlers[eventtype] = []
            self.send({ "ADDLISTENEVENT" : eventtype,
                        "surface" : self.screen,
                      }, "displaysignal")
        self.eventHandlers[eventtype] += [handler]
        return handler
            
    def removeHandler(self, eventtype, handler):
        """Remove the specified pygame event handler from the specified event."""
        if self.eventHandlers.has_key(eventtype): 
            self.eventHandlers[eventtype].remove(handler) # Latent bug, handler not in list


    def quit(self, event = None):
        """Call this method/event handler to finish"""
        self.quitting = True

__kamaelia_components__  = ( PyGameApp, )

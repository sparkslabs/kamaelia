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
component = _Axon.Component.component

import time

class PyGameApp(component):
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
            flags = flags | FULLSCREEN
        self.screen = pygame.display.set_mode( screensize, flags, depth )
        pygame.display.set_caption(caption)

        self.eventHandlers = {}
        self.screensize = self.screen.get_width(), self.screen.get_height()
        self.addHandler(QUIT, lambda event : self.quit(event))
    
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
            if not self.quitting:
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
    


class DragHandler(object):
    """Dragging Handler framework.
    
    Implement detect() drag() and release() to create a dragging handler.
    Register this handler like this:
       pygameapp.addHandler(MOUSEMOTION, lambda event : MyDragHandler(event, pygameapp, *args, **argsd))
       
    If you add your own constructor, remember to initialise any variables you may need before calling the super
    class constructor.
    """
    
    def __init__(self, event, app):
        self.app     = app
        centre = self.detect(event.pos, event.button)
        if centre:
            self.startx =  centre[0]
            self.starty =  centre[1]
            self.offsetx = centre[0] - event.pos[0]
            self.offsety = centre[1] - event.pos[1]
            
            self.mm_handler = self.app.addHandler(MOUSEMOTION,   lambda event : self._drag(event.pos) )
            self.mu_handler = self.app.addHandler(MOUSEBUTTONUP, lambda event : self._release(event.pos) )
    
    def detect(self, pos, button):
        """Override this method. If you wish to accept the drag event and commence a drag,
        return the starting coordinates of the drag (x,y), otherwise return False
        to abort the drag"""
        return False
        
    def _drag(self, pos):
        self.drag( pos[0] + self.offsetx, pos[1] + self.offsety )
        
    def _release(self, pos):
        self.app.removeHandler(MOUSEMOTION,   self.mm_handler)
        self.app.removeHandler(MOUSEBUTTONUP, self.mu_handler)
        self.release( pos[0] + self.offsetx, pos[1] + self.offsety )

    def drag(self,newx,newy):
        """Override this method to handle whenever the drag moves to a new position"""
        pass
                
    def release(self,newx, newy):
        """Override this method to handle whenever the drag finishes at the final position"""
        pass


        
        
if __name__=="__main__":
    """Test the drag handler and PyGameApp class
    """

    class CircleDragHandler(DragHandler):
        """Handler for dragging of the circle"""
        
        def __init__(self, event, app, circle):
            self.circle = circle
            super(CircleDragHandler, self).__init__(event, app)
        
        def detect(self, pos, button):
            if (pos[0] - self.circle.x)**2 + (pos[1] - self.circle.y)*2 < (self.circle.radius**2):
                self.tvx = self.circle.vx
                self.tvy = self.circle.vy
                self.circle.vx = 0
                self.circle.vy = 0
                return (self.circle.x, self.circle.y)
            else:
                return False
                
        def drag(self,newx,newy):
            self.circle.x = newx
            self.circle.y = newy
            
        def release(self,newx, newy):
            self.drag(newx, newy)
            self.circle.vx = self.tvx
            self.circle.vy = self.tvy
            


    class CircleObject(object):
        """Simple draggable, moving, circle object"""
    
        def __init__( self, app, position, velocity, radius):
            """Initialise, registering dragging event handler and setting initial position and velocity"""
            self.app = app
            self.app.addHandler(MOUSEBUTTONDOWN, lambda event : CircleDragHandler(event, self.app, self))

            (self.x,  self.y)  = position
            (self.vx, self.vy) = velocity
            self.radius        = radius
            
        def move(self, cycles=1):
            """Move the circle"""
            while cycles > 0:
                cycles -= 1

                self.x += self.vx
                if self.x > self.app.screen.get_width()-self.radius or self.x < self.radius:
                    self.vx = - self.vx
                    
                self.y += self.vy
                if self.y > self.app.screen.get_height()-self.radius or self.y < self.radius:
                    self.vy = - self.vy
                    
        def draw(self):
            """Render the circle at its current location"""
            pygame.draw.circle(self.app.screen, (255,128,128), (self.x, self.y), self.radius)
                                

    class SimpleApp1(PyGameApp):
        """Simple test application - makes a small window containing a blob that bounces around.
           You can drag the blob with the mouse
        """
    
        def __init__(self, screensize):
            super(SimpleApp1, self).__init__(screensize)

        def initialiseComponent(self):
            self.circle = CircleObject( self, (100,100), (1,1), 32 )

            
        def mainLoop(self):
            self.screen.fill( (255,255,255) )
            self.circle.draw()            
            self.circle.move()
            return 1


    app = SimpleApp1( (1280, 600) )
    app.go()

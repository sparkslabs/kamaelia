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
"""\
===========================
Pygame 'drag' event Handler
===========================

A class, to implement "click and hold" dragging operations in pygame. Hooks into
the event dispatch mechanism provided by the PyGameApp component.

Subclass this class to implement your required dragging functionality.



Example Usage
-------------

A set of circles that can be dragged around the pygame window::
    
    class Circle(object):
        def __init__(self, x, y, radius):
            self.x, self.y, self.radius = x, y, radius
    
        def draw(self, surface):
            pygame.draw.circle(surface, (255,128,128), (self.x, self.y), self.radius)
    
    
    class CircleDragHandler(DragHandler):
        def __init__(self, event, app, theCircle):
            self.circle = theCircle
            super(CircleDragHandler,self).__init__(event, app)
    
        def detect(self, pos, button):
            if (pos[0] - self.circle.x)**2 + (pos[1] - self.circle.y)**2 < (self.circle.radius**2):
                return (self.circle.x, self.circle.y)
            return False
    
        def drag(self,newx,newy):
            self.circle.x = newx
            self.circle.y = newy
    
        def release(self,newx, newy):
            self.drag(newx, newy)
    
    
    class DraggableCirclesApp(PyGameApp):
    
        def initialiseComponent(self):
            self.circles = []
            for i in range(100,200,20):
                circle = Circle(i, 2*i, 20)
                self.circles.append(circle)
                handler = lambda event, circle=circle : CircleDragHandler.handle(event, self, circle)
                self.addHandler(MOUSEBUTTONDOWN, handler)
    
    
        def mainLoop(self):
            self.screen.fill( (255,255,255) )
            for circle in self.circles:
                circle.draw(self.screen)
            return 1
    
    DraggableCirclesApp((800,600)).run()



How does it work?
-----------------

Subclass DragHandler to use it, and (re)implement the __init__(...),
detect(...), drag(...) and release(...) methods.

Bind the handler(...) static method to the event (usually MOUSEBUTTONDOWN),
providing the arguments for the initializer.

The DragHandler will instantiate upon the event and the detect(...) method will
be called to determine whether a drag operation should begin.

The 'event' and 'app' attributes are set to the event that triggered this and
the PyGameApp component concerned respectively.

Implement detect(...) so that it returns False to abort the drag operation, or
(x,y) coordinates for the start of the drag operation. These co-ordinates don't
have to be the same as the ones supplied - they are your opportunity to specify
the origin for the drag.

During the drag, the DragHandler object will bind to the MOUSEMOTION and
MOUSEBUTTONUP pygame events.

Whilst dragging, your drag(...) method will be called whenever the mouse moves
and release(...) will be called when the mouse button(s) are finally released.

drag(...) and release(...) are passed updated x,y coordinates. These are the
origin coordinates (returned by detect(...) method) plus motion since the drag
began.
"""

import pygame
from pygame.locals import *


class DragHandler(object):
    """\
    DragHandler(event,app) -> new DragHandler object

    Subclass this to implement mouse dragging operations in pygame. Bind the
    handle(...) class method to the MOUSEBUTTONDOWN pygame event to use it (via
    a lambda function or equivalent)

    Keyword Arguments:
    - event  -- pygame event object cuasing this
    - app    -- PyGameApp component this is happening in
    """
    
    def handle(cls, *arg, **argD):
        """\
        handle(cls, <args for __init__>) -> False or new DragHandler object

        Instantiates the drag handler object and returns it if it wishes to
        commence the drag - determined by calling the detect(...) method.
        Otherwise returns False.
        
        Class method.
        """
        newHandler = cls(*arg, **argD)
        centre = newHandler.detect(newHandler.event.pos, newHandler.event.button)
        if centre:
            newHandler._start(centre)
            return newHandler
        else:
            return False
    handle=classmethod(handle)

    
    def __init__(self, event, app):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.app     = app
        self.event   = event

    def _start(self, centre):
        """\
        Begin the drag operation. Binds MOUSEMOTION and MOUSEBUTTONUP events and
        sets up internal state.
        """
        self.startx =  centre[0]
        self.starty =  centre[1]
        self.offsetx = centre[0] - self.event.pos[0]
        self.offsety = centre[1] - self.event.pos[1]

        self.mm_handler = self.app.addHandler(MOUSEMOTION,   lambda event : self._drag(event.pos, event.buttons) )
        self.mu_handler = self.app.addHandler(MOUSEBUTTONUP, lambda event : self._release(event.pos) )
        self.isDragging=True
    
    def detect(self, pos, button):
        """\
        detect(pos, button) -> (startx,starty) or False
        
        Stub method, always returns False. Replace with your own.

        Determine whether the drag operation should start. Returns start (x,y)
        to begin the drag, otherwise returns False.
        """
        return False
        
    def _drag(self, pos, buttons):
        """\
        MOUSEMOTION event handler.

        Calls drag(...) or _release(...) depending on whether mouse buttons are
        still depressed.
        """
        if [ True for button in buttons if button ]:
            self.drag( pos[0] + self.offsetx, pos[1] + self.offsety )
        else:
            self._release(pos)
        
    def _release(self, pos):
        """\
        MOUSEBUTTONUP event handler.

        Terminates drag by calling release(...) and unbinding event handlers.
        """
        self.app.removeHandler(MOUSEMOTION,   self.mm_handler)
        self.app.removeHandler(MOUSEBUTTONUP, self.mu_handler)
        self.release( pos[0] + self.offsetx, pos[1] + self.offsety )

    def drag(self,newx,newy):
        """\
        Stub method. Called whenever mouse moves during drag.

        (newx,newy) are (startx,starty) + movement since dragging began.

        (startx,starty) are the values returned by detect(...)
        """
        pass
                
    def release(self,newx, newy):
        """\
        Stub method. Called when the drag has finished.

        (newx,newy) are (startx,starty) + movement since dragging began.

        (startx,starty) are the values returned by detect(...)
        """
        pass


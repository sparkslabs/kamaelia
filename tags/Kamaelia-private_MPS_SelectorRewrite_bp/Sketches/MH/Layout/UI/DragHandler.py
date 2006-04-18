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

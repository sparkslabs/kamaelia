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

import time

class PyGameApp:
    def __init__(self, screensize, caption="PyGame Application", border=100):
        pygame.init()
        self.screen = pygame.display.set_mode( screensize, DOUBLEBUF, 32 )
        pygame.display.set_caption(caption)

        self.eventHandlers = {}
        self.addHandler(QUIT, lambda event : self.handler_quit(event))
        self.screensize = screensize
        self.border = border
    
    def main(self):
        self.initialiseComponent()
        self.quitting = False

        # Event loop
        while not self.quitting:
            self.dispatch()
            if not self.quitting:
                self.mainLoop()
            if not self.quitting:
                pygame.display.flip()
                time.sleep(0.01)
            yield 1

    def mainloop(self):
        for i in self.main():
           pass

    def dispatch(self):
        for event in pygame.event.get():
            if self.eventHandlers.has_key(event.type):
                for handler in self.eventHandlers[event.type]:
                    if handler(event):
                        break

    def addHandler(self, eventtype, handler):
        if not self.eventHandlers.has_key(eventtype):
            self.eventHandlers[eventtype] = []
        self.eventHandlers[eventtype] += [handler]
        return handler
            
    def removeHandler(self, eventtype, handler):
        if self.eventHandlers.has_key(eventtype):
            self.eventHandlers[eventtype].remove(handler)

    def handler_quit(self, event):
        self.quitting = True
    
    def initialiseComponent(self):
        pass
        
    def mainLoop(self):
        return 1



class DragHandler:
    def __init__(self, event, app):
        self.app = app
        centre = self.detect(event.pos)
        if centre:
            self.startx = centre[0]
            self.starty = centre[1]
            self.offsetx = centre[0] - event.pos[0]
            self.offsety = centre[1] - event.pos[1]
            
            self.mm_handler = app.addHandler(MOUSEMOTION, lambda event : self._drag(event.pos) )
            self.mu_handler = app.addHandler(MOUSEBUTTONUP, lambda event : self._release(event.pos) )
    
    def detect(self, pos):
        return False
        
    def _drag(self, pos):
        self.drag( pos[0] + self.offsetx, pos[1] + self.offsety )
        
    def _release(self, pos):
        self.app.removeHandler(MOUSEMOTION, self.mm_handler)
        self.app.removeHandler(MOUSEBUTTONUP, self.mu_handler)
        self.release( pos[0] + self.offsetx, pos[1] + self.offsety )



if __name__=="__main__":

    class SimpleApp1(PyGameApp):
        class CircleDragHandler(DragHandler):
            def detect(self, pos):
                if (pos[0] - self.app.circlex)**2 + (pos[1] - self.app.circley)*2 < (self.app.circlerad**2):
                    self.tvx = self.app.circlevx
                    self.tvy = self.app.circlevy
                    self.app.circlevx = 0
                    self.app.circlevy = 0
                    return self.app.circlex, self.app.circley
                else:
                    return False
                    
            def drag(self,newx,newy):
                self.app.circlex = newx
                self.app.circley = newy
                
            def release(self,newx, newy):
                self.drag(newx, newy)
                self.app.circlevx = self.tvx
                self.app.circlevy = self.tvy
                
                
                
        def __init__(self, screensize):
            PyGameApp.__init__(self, screensize)

        def initialiseComponent(self):
            self.addHandler(MOUSEBUTTONDOWN, lambda event : self.CircleDragHandler(event,self))

            self.circlex = 100
            self.circley = 100
            self.circlevx = 1
            self.circlevy = 1
            self.circlerad = 32
            pass

        def mainLoop(self):
            self.screen.fill( (255,255,255) )
            pygame.draw.circle(self.screen, (255,128,128), (self.circlex, self.circley), self.circlerad)
            self.circlex += self.circlevx
            if self.circlex > self.screen.get_width()-self.circlerad or self.circlex < self.circlerad:
              self.circlevx = - self.circlevx
            self.circley += self.circlevy
            if self.circley > self.screen.get_height()-self.circlerad or self.circley < self.circlerad:
              self.circlevy = - self.circlevy
            return 1


    app = SimpleApp1( (320, 240) )
    app.mainloop()

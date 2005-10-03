#!/usr/bin/python
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
#

import pygame as _pygame

class EventHandler(object):
   def __init__(self, trace=1):
      self.trace = trace
   def dispatch(self, event, where):
      if event.type == _pygame.QUIT: self.quit(where)
      if event.type == _pygame.ACTIVEEVENT: self.active(event.gain, event.state, where)
      if event.type == _pygame.KEYDOWN: self.keydown(event.unicode, event.key, event.mod, where)
      if event.type == _pygame.KEYUP: self.keyup(event.key, event.mod, where)
      if event.type == _pygame.MOUSEMOTION: self.mousemotion(event.pos, event.rel, event.buttons, where)
      if event.type == _pygame.MOUSEBUTTONUP: self.mousebuttonup(event.pos, event.button, where)
      if event.type == _pygame.MOUSEBUTTONDOWN: self.mousebuttondown(event.pos, event.button, where)
      if event.type == _pygame.JOYAXISMOTION: self.joyaxismotion(event.joy, event.axis, event.value, where)
      if event.type == _pygame.JOYBALLMOTION: self.joyballmotion(event.joy, event.ball, event.rel, where)
      if event.type == _pygame.JOYHATMOTION: self.joyhatmotion(event.joy, event.hat, event.value, where)
      if event.type == _pygame.JOYBUTTONUP: self.joybuttonup(event.joy, event.button, where)
      if event.type == _pygame.JOYBUTTONDOWN: self.joybuttondown(event.joy, event.button, where)
      if event.type == _pygame.VIDEORESIZE: self.videoresize(event.size, where)
      if event.type == _pygame.VIDEOEXPOSE: self.videoexpose(where)
      if event.type == _pygame.USEREVENT: self.userevent(event.code,where)

   def quit(self, where): 
      if self.trace:
         print "QUIT: (", ")"

   def active(self, gain, state ,where): 
      if self.trace:
         print "ACTIVE: (", gain, state, ")"

   def keydown(self, unicode, key, mod, where):
      if self.trace:
         print "KEYDOWN: (", repr(unicode), key, mod, ")"

   def keyup(self, key, mod, where):
      if self.trace:
         print "KEYUP: (", key, mod, ")"

   def mousemotion(self, pos, rel, buttons, where):
      if self.trace:
         print "MOUSEMOTION: (", pos, rel, buttons, ")"

   def mousebuttonup(self, pos, button, where):
      if self.trace:
         print "MOUSEBUTTONUP: (", pos, button, ")"

   def mousebuttondown(self, pos, button, where):
      if self.trace:
         print "MOUSEBUTTONDOWN: (", pos, button, ")"

   def joyaxismotion(self, joy, axis, value, where):
      if self.trace:
         print "JOYAXISMOTION: (", joy, axis, value, ")"

   def joyballmotion(self, joy, ball, rel, where):
      if self.trace:
         print "JOYBALLMOTION: (", joy, ball, rel, ")"

   def joyhatmotion(self, joy, hat, value, where):
      if self.trace:
         print "JOYHATMOTION: (", joy, hat, value, ")"

   def joybuttonup(self, joy, button, where):
      if self.trace:
         print "JOYBUTTONUP: (", joy, button, ")"

   def joybuttondown(self, joy, button, where):
      if self.trace:
         print "JOYBUTTONDOWN: (", joy, button, ")"

   def videoresize(self, size, where):
      if self.trace:
         print "VIDEORESIZE: (", size, ")"

   def videoexpose(self, where):
      if self.trace:
         print "VIDEOEXPOSE: (", ")"

   def userevent(self, code, where): 
      if self.trace:
         print "USEREVENT: (", code, ")"

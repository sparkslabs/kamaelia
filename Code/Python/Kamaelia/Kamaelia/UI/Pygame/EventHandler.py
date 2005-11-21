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
Pygame event handling
=====================

A simple framework for handling pygame events. Reimplement the appropriate stub
method to handle a given event.



Example Usage
-------------

Detecting key presses and mouse button depressions and releases::
    class MyEventHandler(EventHandler):
        def __init__(self, target):
            super(MyEventHandler,self).__init__()
            self.target = target

        def keydown(self, key, mod, where):
            print "Keypress '"+key+"' detected by "+where

        def mousebuttondown(self, pos, button, where):
            print "Mouse button depressed"

        def mousebuttonup(self, pos, button, where):
            print "Mouse button released"



How does it work?
-----------------

Implement your event handler by subclassing EventHandler and reimplementing the
stub methods for the particular events you wish to handle.

The code that reads the events from pygame should pass them one at a time to
EventHandler by calling the dispatch(...) method.

The optional 'trace' argument to the initialiser, when non-zero, causes the
existing stub handlers to print messages to standard out, notifying you that
the given event has taken place.
"""

import pygame as _pygame

class EventHandler(object):
   """\
   EventHandler([trace]) -> new EventHandler object.

   Pygame event dispatcher. Subclass and reimplement the stub methods to handle
   events. Pass in events to be handled by calling the dispatch(...) method.

   Keyword arguments:
   - trace  -- Cause existing stub handlers to print messages to standard output.
   """
            
   def __init__(self, trace=1):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      self.trace = trace
      
   def dispatch(self, event, where):
      """\
      dispatch(event, where).
      
      Dispatch the specified pygame event to relevant handler. You should also
      specify where the event is coming from.
      """
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
      """Pygame QUIT event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "QUIT: (", ")"

   def active(self, gain, state ,where): 
      """Pygame ACTIVEEVENT event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "ACTIVE: (", gain, state, ")"

   def keydown(self, unicode, key, mod, where):
      """Pygame KEYDOWN event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "KEYDOWN: (", repr(unicode), key, mod, ")"

   def keyup(self, key, mod, where):
      """Pygame KEYUP event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "KEYUP: (", key, mod, ")"

   def mousemotion(self, pos, rel, buttons, where):
      """Pygame MOUSEMOTION event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "MOUSEMOTION: (", pos, rel, buttons, ")"

   def mousebuttonup(self, pos, button, where):
      """Pygame MOUSEBUTTONUP event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "MOUSEBUTTONUP: (", pos, button, ")"

   def mousebuttondown(self, pos, button, where):
      """Pygame MOUSEBUTTONDOWN event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "MOUSEBUTTONDOWN: (", pos, button, ")"

   def joyaxismotion(self, joy, axis, value, where):
      """Pygame JOYAXISMOTION event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "JOYAXISMOTION: (", joy, axis, value, ")"

   def joyballmotion(self, joy, ball, rel, where):
      """Pygame JOYBALLMOTION event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "JOYBALLMOTION: (", joy, ball, rel, ")"

   def joyhatmotion(self, joy, hat, value, where):
      """Pygame JOYHATMOTION event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "JOYHATMOTION: (", joy, hat, value, ")"

   def joybuttonup(self, joy, button, where):
      """Pygame JOYBUTTONUP event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "JOYBUTTONUP: (", joy, button, ")"

   def joybuttondown(self, joy, button, where):
      """Pygame JOYBUTTONDOWN event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "JOYBUTTONDOWN: (", joy, button, ")"

   def videoresize(self, size, where):
      """Pygame VIDEORESIZE event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "VIDEORESIZE: (", size, ")"

   def videoexpose(self, where):
      """Pygame VIDEOEXPOSE event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "VIDEOEXPOSE: (", ")"

   def userevent(self, code, where): 
      """Pygame USEREVENT event handler stub method. Reimplement to handle this event."""
      if self.trace:
         print "USEREVENT: (", code, ")"

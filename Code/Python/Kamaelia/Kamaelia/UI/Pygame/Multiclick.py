#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
================================
Pygame Multi-click Button Widget
================================

A button widget for pygame display surfaces. Sends a message when clicked. The
message can be different for each mouse button.

Uses the Pygame Display service.



Example Usage
-------------
Three buttons that output messages to the console::

    msgs = [ "button 1", "button 2", "button 3", "button 4", "button 5" ]
    button1 = Button(caption="Click different mouse buttons!",msgs=msgs).activate()
    
    ce = ConsoleEchoer().activate()
    button1.link( (button1,"outbox"), (ce,"inbox") )
    


How does it work?
-----------------

The component requests a display surface from the Pygame Display service
component. This is used as the surface of the button. It also binds event
listeners to the service, as appropriate.

Arguments to the constructor configure the appearance and behaviour of the
button component:

- If "msgs" is specified, then a different message can be specified for each
  mouse button. If it is not specified, then "msg" is used instead, for all
  buttons.
  
- If an output "msg" is not specified, the default is a tuple ("CLICK", id)
  where id is the self.id attribute of the component.

- you can set the text label, colour, margin size, size and position of the
  button

- if you do not specify the size yourself, the size will default to fit the
  caption of the button.

- the button can have a transparent background

If a producerFinished or shutdownMicroprocess message is received on its
"control" inbox. It is passed on out of its "signal" outbox and the component
terminates.

Upon termination, this component does *not* unbind itself from the Pygame Display
service. It does not deregister event handlers and does not relinquish the
display surface it requested.
"""


import pygame
import Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class Multiclick(Axon.Component.component):
   """\
   Multiclick(...) -> new Multiclick component.

   Create a button widget in pygame, using the Pygame Display service. Sends a
   message out of its outbox when clicked.

   Keyword arguments (all optional):
   
   - caption      -- text (default="Button <component id>")
   - position     -- (x,y) position of top left corner in pixels
   - margin       -- pixels margin between caption and button edge (default=8)
   - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
   - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
   - msg          -- sent when clicked (default=("CLICK",self.id)) of msgs is not specified
   - msgs         -- list of messages. msgs[x] is sent when button X is clicked (default=None)
   - transparent  -- draw background transparent if True (default=False)
   - size         -- (width,height) pixels size of the button (default=scaled to fit caption)
   """
   
   Inboxes = { "inbox"    : "Receive events from Pygame Display",
               "control"  : "Shutdown messages: shutdownMicroprocess or producerFinished",
               "callback" : "Receive callbacks from Pygame Display"
             }
   Outboxes = { "outbox" : "button click events emitted here",
                "signal" : "Shutdown signalling: shutdownMicroprocess or producerFinished",
                "pygamesignal" : "For sending messages to pygame", # BUGFIX: Axon.AxonExceptions.BoxAlreadyLinkedToDestination:
              }
   
   def __init__(self, caption=None, position=None, margin=8, bgcolour = (224,224,224), fgcolour = (0,0,0), 
                msg=None,
                msgs = None,
                transparent = True,
                size = None):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Multiclick,self).__init__()
      
      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.margin = margin
      self.size = size
      self.msgs = msgs

      if caption is None:
         caption = "Button "+str(self.id)
      
      pygame.font.init()      
      self.buildCaption(caption)

      if msg is None:
         msg = ("CLICK", self.id)
      self.eventMsg = msg      
      if transparent:
         transparency = bgcolour
      else:
         transparency = None
      self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "inbox"),
                           "size": self.size,
                           "transparency" : transparency }
      
      if not position is None:
        self.disprequest["position"] = position         

   def buildCaption(self, text):
      """Pre-render the text to go on the button label."""
      # Text is rendered to self.image
      font = pygame.font.Font(None, 14)
      self.image = font.render(text,True, self.foregroundColour, )
      
      (w,h) = self.image.get_size()
      if self.size is None:
          self.size = (w + 2*self.margin, h + 2*self.margin)
      self.imagePosition = (self.margin, self.margin)
      
       
   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1

   
   def main(self):
      """Main loop."""
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"pygamesignal"), displayservice)

      self.send( self.disprequest,
                  "pygamesignal")
             
      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      self.blitToSurface()
      
      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                  "surface" : self.display},
                  "pygamesignal")
                  

      done = False
      while not done:
      
         if self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               done = True
         
         while self.dataReady("inbox"):
            for event in self.recv("inbox"):
                if event.type == pygame.MOUSEBUTTONDOWN:
                   bounds = self.display.get_rect()
                   if bounds.collidepoint(*event.pos):
                      try:
                         message = self.msgs[event.button]
                      except KeyError: # No message for this key
                         continue
                      except IndexError: # No message for this key
                         continue
                      except TypeError: # No lookup table
                         message = self.eventMsg
                      self.send( message, "outbox" )
         yield 1
            
      
   def blitToSurface(self):
       """Clears the background and renders the text label onto the button surface."""
       try:
           self.send({"REDRAW":True, "surface":self.display}, "pygamesignal")
           self.display.fill( self.backgroundColour )
           self.display.blit( self.image, self.imagePosition )
       except:
           pass

__kamaelia_components__  = ( Multiclick, )

                  
if __name__ == "__main__":
   pass

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
====================
Pygame Button Widget
====================

A button widget for pygame display surfaces. Sends a message when clicked.

Uses the Pygame Display service.



Example Usage
-------------
Three buttons that output messages to the console::
    
    button1 = Button(caption="Press SPACE or click",key=K_SPACE).activate()
    button2 = Button(caption="Reverse colours",fgcolour=(255,255,255),bgcolour=(0,0,0)).activate()
    button3 = Button(caption="Mary...",msg="Mary had a little lamb", position=(200,100)).activate()
    
    ce = consoleEchoer().activate()
    button1.link( (button1,"outbox"), (ce,"inbox") )
    button2.link( (button2,"outbox"), (ce,"inbox") )
    button3.link( (button3,"outbox"), (ce,"inbox") )
    


How does it work?
-----------------

The component requests a display surface from the Pygame Display service
component. This is used as the surface of the button. It also binds event
listeners to the service, as appropriate.

Arguments to the constructor configure the appearance and behaviour of the
button component:

- If an output "msg" is not specified, the default is a tuple ("CLICK", id) where
id is the self.id attribute of the component.

- A pygame keycode can be specified that will also trigger the button as if it
had been clicked

- you can set the text label, colour, margin size and position of the button

- the button can have a transparent background

- you can specify a size as width,height. If specified, the margin size is
  ignored and the text label will be centred within the button

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
from Kamaelia.UI.Pygame.Display import Display

class Button(Axon.Component.component):
   """\
   Button(...) -> new Button component.

   Create a button widget in pygame, using the Pygame Display service. Sends a
   message out of its outbox when clicked.

   Keyword arguments (all optional):
   - caption      -- text (default="Button <component id>")
   - position     -- (x,y) position of top left corner in pixels
   - margin       -- pixels margin between caption and button edge (default=8)
   - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
   - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
   - msg          -- sent when clicked (default=("CLICK",self.id))
   - key          -- if not None, pygame keycode to trigger click (default=None)
   - transparent  -- draw background transparent if True (default=False)
   - size         -- None or (w,h) in pixels (default=None)
   """
   
   Inboxes = { "inbox"    : "Receive events from Pygame Display",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from Pygame Display"
             }
   Outboxes = { "outbox" : "button click events emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
   
   def __init__(self, caption=None, position=None, margin=8, bgcolour = (224,224,224), fgcolour = (0,0,0), msg=None,
                key = None,
                transparent = False, size=None):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Button,self).__init__()
      
      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.margin = margin
      self.key = key
###      print "KEY",key
      
      if caption is None:
         caption = "Button "+str(self.id)
      
      self.size = size
      
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
      if not self.size:
          self.size = (w + 2*self.margin, h + 2*self.margin)
          self.imagePosition = (self.margin, self.margin)
      else:
          self.imagePosition = ( (self.size[0]-w)/2, (self.size[1]-h)/2 )
      
       
   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1

   
   def main(self):
      """Main loop."""
      displayservice = Display.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,
                  "display_signal")
             
      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      self.blitToSurface()
      
      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                  "surface" : self.display},
                  "display_signal")
      if self.key is not None:
###         print "ADDING LISTEN", self.key, pygame.KEYDOWN, self.display
         message = { "ADDLISTENEVENT" : pygame.KEYDOWN,
                     "surface" : self.display,
                     "TRACE" : "ME"}
###         print "----------------", message
         self.send(message, "display_signal")
#      while self.outboxes["display_signal"]  != []:
#         print dir(self)
#         print "Waiting clean out", self.outboxes["display_signal"], self
#         yield 1
      done = False
      while not done:
         while self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               self.send(cmsg, "signal")
               done = True
         
         while self.dataReady("inbox"):
            for event in self.recv("inbox"):
###                print event
                if event.type == pygame.MOUSEBUTTONDOWN:
#                   print "BUTTON", event.button
                   bounds = self.display.get_rect()
                   if bounds.collidepoint(*event.pos):
                      self.send( self.eventMsg, "outbox" )
                if event.type == pygame.KEYDOWN:
###                   print "EVENT", event.type, event.key
                   if event.key == self.key:
                      self.send( self.eventMsg, "outbox" )
         self.pause()
         yield 1
            
      
   def blitToSurface(self):
       """Clears the background and renders the text label onto the button surface."""
       try:
           self.display.fill( self.backgroundColour )
           self.display.blit( self.image, self.imagePosition )
       except:
           pass
       self.send({"REDRAW":True, "surface":self.display}, "display_signal")

__kamaelia_components__  = ( Button, )

                  
if __name__ == "__main__":
   from Kamaelia.Util.Console import ConsoleEchoer
   from pygame.locals import *
   
   button1 = Button(caption="Press SPACE or click",key=K_SPACE).activate()
   button2 = Button(caption="Reverse colours",fgcolour=(255,255,255),bgcolour=(0,0,0)).activate()
   button3 = Button(caption="Mary...",msg="Mary had a little lamb", position=(200,100)).activate()
   
   ce = ConsoleEchoer().activate()
   button1.link( (button1,"outbox"), (ce,"inbox") )
   button2.link( (button2,"outbox"), (ce,"inbox") )
   button3.link( (button3,"outbox"), (ce,"inbox") )
   
   Axon.Scheduler.scheduler.run.runThreads()  
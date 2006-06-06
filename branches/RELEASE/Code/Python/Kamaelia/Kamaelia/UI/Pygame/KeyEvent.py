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

import pygame
import Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.PygameDisplay import PygameDisplay

class KeyEvent(Axon.Component.component):
   """
   """
   
   Inboxes = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "",
               "callback" : "Receive callbacks from PygameDisplay"
             }
   Outboxes = { "outbox" : "button click events emitted here",
                "allkeys" : "Outbox that receives *every* keystroke if enabled",
                "signal" : "",
                "display_signal" : "Outbox used for communicating to the display surface" }
   
   def __init__(self, caption=None, 
                position=None, margin=8,
                bgcolour = (224,224,224),
                fgcolour = (0,0,0),
                msg=None,
                allkeys = False,
                key_events = None,
                transparent = False,
                outboxes = {}):
      """Creates and activates a button widget
         caption  = text label for the button / None for default label
         position = (x,y) pair / None
         margin   = margin size (around the text) in pixels
         bgcolour = background colour
         fgcolour = text colour
         msg      = message to be sent when this button is clicked / None for default
         """
      self.Outboxes = self.__class__.Outboxes
      self.Outboxes.update(outboxes)
      super(KeyEvent,self).__init__()

      self.allkeys = allkeys
      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.margin = margin
      self.key_events = key_events
      if self.key_events is None: self.key_events = {}
      
      if caption is None:
         caption = "Button "+str(self.id)
      
      pygame.font.init()      
#      self.buildCaption(caption)

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
                           "size": (0,0),
                           "transparency" : transparency }
      
      if not position is None:
        self.disprequest["position"] = position         

   def buildCaption(self, text):
      """Render the text to go on the button label.
      (This doesn't actually place the text onto the 'surface')
      """
      font = pygame.font.Font(None, 14)
      self.image = font.render(text,True, self.foregroundColour, )
      
      (w,h) = self.image.get_size()
      self.size = (w + 2*self.margin, h + 2*self.margin)
      self.imagePosition = (self.margin, self.margin)
      
       
   def waitBox(self,boxname):
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1

   
   def main(self):
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,
                  "display_signal")
             
      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      self.blitToSurface()
      
      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                  "surface" : self.display},
                  "display_signal")
      if (self.key_events is not None) or self.allkeys:
         message = { "ADDLISTENEVENT" : pygame.KEYDOWN,
                     "surface" : self.display,
                     "TRACE" : "ME"}
         self.send(message, "display_signal")

      if self.allkeys:
         message = { "ADDLISTENEVENT" : pygame.KEYUP,
                     "surface" : self.display,
                     "TRACE" : "METO"}
         self.send(message, "display_signal")

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
                      self.send( self.eventMsg, "outbox" )
                if event.type == pygame.KEYDOWN:
                   if event.key in self.key_events:
                      self.send( self.key_events[event.key][0] , self.key_events[event.key][1] )
                   if self.allkeys:
                      self.send(("DOWN", event.key), "allkeys")
                if event.type == pygame.KEYDOWN:
                   if self.allkeys:
                      self.send(("UP", event.key), "allkeys")
         yield 1
            
      
   def blitToSurface(self):
       try:
           self.display.fill( self.backgroundColour )
           self.display.blit( self.image, self.imagePosition )
       except:
           pass
                  
if __name__ == "__main__":
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   
   button1 = Button().activate()
   button2 = Button(caption="Reverse colours",fgcolour=(255,255,255),bgcolour=(0,0,0)).activate()
   button3 = Button(caption="Mary...",msg="Mary had a little lamb").activate()
   
   ce = consoleEchoer().activate()
   button1.link( (button1,"outbox"), (ce,"inbox") )
   button2.link( (button2,"outbox"), (ce,"inbox") )
   button3.link( (button3,"outbox"), (ce,"inbox") )
   
   Axon.Scheduler.scheduler.run.runThreads()  
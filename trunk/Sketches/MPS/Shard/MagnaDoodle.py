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

import pygame
import Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay

class MagnaDoodle(Axon.Component.component):
   Inboxes = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay"
             }
   Outboxes = { "outbox" : "not used",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
   
   def __init__(self, caption=None, position=None, margin=8, bgcolour = (124,124,124), fgcolour = (0,0,0), msg=None,
                transparent = False, size=(200,200)):
      super(MagnaDoodle,self).__init__()

      # How to represent these as dependencies... (they are dependended on by shards)

      # START SHARD : __init__ ======================================================
      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.margin = margin
      self.oldpos = None
      self.drawing = False
      self.size = size

      if transparent:
         transparency = bgcolour
      else:
         transparency = None

      if msg is None:
         msg = ("CLICK", self.id)
      self.eventMsg = msg      
      self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)
      # END SHARD : __init__ ========================================================

      # START DEPENDENCY FOR SHARD: Get Display Surface -----------------------------
      self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "inbox"),
                           "size": self.size,
                           "transparency" : transparency }
      
      if not position is None:
        self.disprequest["position"] = position         
      # END DEPENDENCY FOR SHARD: Get Display Surface -------------------------------

       
   # START FROM SHARD : Get Display Surface =========================================
   def waitBox(self,boxname):
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1
   # START FROM SHARD : Get Display Surface =========================================

   # START FROM SHARD : drawBG ======================================================
   def drawBG(self):
      self.display.fill( (255,0,0) )
      self.display.fill( self.backgroundColour, self.innerRect )
   # END FROM SHARD : drawBG ========================================================
     
   
   def main(self):
      # START SHARD : Setup Display =================================================

      # START SHARD : Get Display Surface -------------------------------------------
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest, "display_signal")
             
      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      # END SHARD : Get Display Surface ---------------------------------------------

      # START SHARD : drawBG ========================================================
      self.drawBG()
      # END SHARD : drawBG ========================================================
      # START SHARD : Blit Display --------------------------------------------------
      self.blitToSurface()
      # END SHARD : Blit Display ----------------------------------------------------
      
      # START SHARD : Set Event Options ---------------------------------------------
      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                  "surface" : self.display},
                  "display_signal")

      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                  "surface" : self.display},
                  "display_signal")

      self.send({ "ADDLISTENEVENT" : pygame.MOUSEMOTION,
                  "surface" : self.display},
                  "display_signal")
      # END SHARD : Set Event Options -----------------------------------------------
      # END SHARD : Setup Display ===================================================

      # START SHARD : mainloop ======================================================
      done = False
      while not done:
         # START SHARD : Handle Shutdown --------------------------------------------
         while self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, Axon.Ipc.producerFinished) or \
               isinstance(cmsg, Axon.Ipc.shutdownMicroprocess):
               self.send(cmsg, "signal")
               done = True
         # END SHARD : Handle Shutdown ----------------------------------------------
         
         while self.dataReady("inbox"):
            # START SHARD : Loop over Pygame Events ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            for event in self.recv("inbox"):
                # START SHARD : Handle Event ========================================
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # START SHARD : Mouse dn button 1 -------------------------------
                    if  event.button == 1:
                        self.drawing = True
                    elif event.button == 3:
                        self.oldpos = None
                        # START SHARD : drawBG ......................................
                        self.drawBG()
                        # END SHARD : drawBG ........................................
                        # START SHARD : Blit Display ................................
                        self.blitToSurface()
                        # END SHARD : Blit Display ..................................

                    # END SHARD : Mouse dn button 1 ---------------------------------
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # START SHARD : Mouse up button 1 -------------------------------
                    self.drawing = False
                    self.oldpos = None
                    # END SHARD : Mouse up button 1 ---------------------------------
                elif event.type == pygame.MOUSEMOTION:
                    # START SHARD : Mouse move --------------------------------------
                    if self.drawing and self.innerRect.collidepoint(*event.pos):
                        if self.oldpos == None:
                            self.oldpos = event.pos
                        else:
                            pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
                            self.oldpos = event.pos
                        # START SHARD : Blit Display ................................
                        self.blitToSurface()
                        # END SHARD : Blit Display ..................................
                    # END SHARD : Mouse move ----------------------------------------
                # END SHARD : Handle Event ==========================================
            # END SHARD : Loop over Pygame Events ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         self.pause()
         yield 1
      # END SHARD : mainloop ========================================================
      # START SHARD : __exit__ ======================================================
      # END SHARD : __exit__ ========================================================
            
      
   def blitToSurface(self):
       self.send({"REDRAW":True, "surface":self.display}, "display_signal")

__kamaelia_components__  = ( MagnaDoodle, )

                  
if __name__ == "__main__":
   MagnaDoodle().run()

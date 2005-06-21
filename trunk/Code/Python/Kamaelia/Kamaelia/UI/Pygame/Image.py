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

class Image(Axon.Component.component):
   """Simple 'Image display widget' for PygameDisplay"""
   
   Inboxes = { "inbox"    : "Specify (new) filename",
               "control"  : "",
               "callback" : "Receive callbacks from PygameDisplay",
               "bgcolour" : "Set the background colour"
             }
   Outboxes = { "signal" : "" }
    
   def __init__(self, image = None, bgcolour = (128,128,128), size = None):
      """Initialisation.
         image = filename of file containing image
         bgcolour = (r,g,b) pygame colour specification (defaults to grey)
         size  = None (defaults to image size, or (240,192) if no image specified)
                 or (width, height) tuple
      """
      super(Image, self).__init__()
      self.display = None
      
      self.backgroundColour = bgcolour
      self.size             = size
      self.imagePosition    = (0,0)
      
      self.fetchImage(image)
      
      if self.size is None:
         self.size = (240,192)
    
        
   def waitBox(self,boxname):
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1

            
   def main(self):
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"signal"), displayservice)
      
      # request a surface
      self.send({ "DISPLAYREQUEST" : True,
                  "callback" : (self,"callback"),
#                     "events" : (self, "events"),
                  "size": self.size},
                  "signal")
    
#      for _ in self.waitBox("callback"): yield 1
#      self.display = self.recv("callback")
#      self.blitToSurface()      
#      yield 1
      
      done = False
      change = False    
      while not done:
      
         if self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               done = True
         
         # if we're given a new surface, use that instead
         if self.dataReady("callback"):
            self.display = self.recv("callback")
            change = True

         if self.dataReady("inbox"):
            newImg = self.recv("inbox")
            self.fetchImage(newImg)
            change = True
            
         if self.dataReady("bgcolour"):
             self.backgroundColour = self.recv("bgcolour")
             change = True
            
         if change:
            self.blitToSurface()
            change = False
        
         yield 1

        
   def fetchImage(self, newImage):
      if newImage is None:
         self.image = None
    
      else:
         self.image = pygame.image.load(newImage)
        
         if self.size is None:
             self.size = self.image.get_size()
        
        
   def blitToSurface(self):
#      if not self.display is None:
#         self.display.fill( (0,128,0) )
#        
#         if not self.image is None:
#            self.display.blit(self.image, (0,0) )
       try:
           self.display.fill( self.backgroundColour )
           self.display.blit( self.image, self.imagePosition )
       except:
           pass
        
             
if __name__ == "__main__":
   
   testImageFile0 = "../../../../../../Sketches/OptimisationTest/pictures/cat.gif"
   testImageFile1 = "../../../../../../Sketches/OptimisationTest/pictures/thumb.10063680.jpg.gif"

   class IChange(Axon.Component.component):
      Outboxes = [ "outcolour", "outimage" ]
      def __init__(self, speed = 4):
         super(IChange,self).__init__()
         self.speed = speed
           
      def main(self):
         while 1:
            for g in range(0,256,self.speed):
               self.send( (0,g,0),"outcolour")
               yield 1
            self.send( testImageFile1, "outimage")
            for g in range(255,0,-self.speed):
               self.send( (0,g,0),"outcolour")
               yield 1
            self.send( testImageFile0, "outimage")

   from Kamaelia.Util.PipelineComponent import pipeline                  
                  
   for i in range(0,6):
       image = Image(image=testImageFile0).activate()
       ic    = IChange(4+i).activate()
       ic.link( (ic, "outcolour"), (image, "bgcolour") )
       ic.link( (ic, "outimage"), (image, "inbox") )
       
   
   Axon.Scheduler.scheduler.run.runThreads()   
   
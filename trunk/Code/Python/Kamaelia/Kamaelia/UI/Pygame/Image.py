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
Pygame image display
====================

Component for displaying an image on a pygame display. Uses the Pygame Display
service component.

The image can be changed at any time.



Example Usage
-------------

Display that rotates rapidly through a set of images::
    imagefiles = [ "imagefile1", "imagefile2", ... ]
    
    class ChangeImage(Axon.Component.component):
        def __init__(self, images):
            super(ChangeImage,self).__init__()
            self.images = images
            
        def main(self):
            while 1:
                for image in self.images:
                    self.send( image, "outbox")
                    print "boing",image
                    for i in range(0,100):
                        yield 1
    
    image = Image(image=None, bgcolour=(0,192,0))
    ic    = ChangeImage(imagefiles)
    
    Pipeline(ic, image).run()



How does it work?
-----------------

This component requests a display surface from the Pygame Display service
component and renders the specified image to it.

The image, and other properties can be changed later by sending messages to its
"inbox", "bgcolour" and "alphacontrol" inboxes.

Note that the size of display area is fixed after initialisation. If an initial
size, or image is specified then the size is set to that, otherwise a default
value is used.

Change the image at any time by sending a new filename to the "inbox" inbox.
If the image is larger than the 'size', then it will appear cropped. If it is
smaller, then the Image component's 'background colour' will show through behind
it. The image is always rendered aligned to the top left corner.

If this component receives a shutdownMicroprocess or producerFinished message on
its "control" inbox, then this will be forwarded out of its "signal" outbox and
the component will then terminate.
"""

import pygame
import Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class Image(Axon.Component.component):
   """\
   Image([image][,position][,bgcolour][,size][,displayExtra][,maxpect]) -> new Image component

   Pygame image display component. Image, and other properties can be changed at runtime.

   Keyword arguments:
   
   - image         -- Filename of image (default=None) 
   - position      -- (x,y) pixels position of top left corner (default=(0,0))
   - bgcolour      -- (r,g,b) background colour (behind the image if size>image size)
   - size          -- (width,height) pixels size of the area to render the iamge in (default=image size or (240,192) if no image specified)
   - displayExtra  -- dictionary of any additional args to pass in request to Pygame Display service
   - maxpect       -- (xscale,yscale) scaling to apply to image (default=no scaling)
   """
   
   Inboxes = { "inbox"    : "Filename of (new) image",
               "control"  : "Shutdown messages: shutdownMicroprocess or producerFinished",
               "callback" : "Receive callbacks from Pygame Display",
               "bgcolour" : "Set the background colour",
               "events"   : "Place where we recieve events from the outside world",
               "alphacontrol" : "Alpha (transparency) of the image (value 0..255)",
             }
   Outboxes = {
               "outbox" : "NOT USED",
               "signal" : "Shutdown signalling: shutdownMicroprocess or producerFinished",
               "display_signal" : "Outbox used for sending signals of various kinds to the display service"
             }
    
   def __init__(self, image = None,
                      position=None,
                      bgcolour = (128,128,128), 
                      size = None, 
                      displayExtra = None,
                      maxpect = 0):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Image, self).__init__()
      self.display = None
      
      self.backgroundColour = bgcolour
      self.size             = size
      self.imagePosition    = (0,0)
      self.maxpect = maxpect
      
      self.fetchImage(image)
      
      if self.size is None:
         self.size = (240,192)

      # build the initial request to send to Pygame Display to obtain a surface
      # but store it away until main() main loop is activated.
      self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "events"),
                           "size": self.size}
      if displayExtra is not None:
         self.disprequest.update(displayExtra)
      
      if not position is None:
         self.disprequest["position"] = position
    
        
   def waitBox(self,boxname):
      """Generator. yield's 1 until data is ready on the named inbox."""
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1

            
   def main(self):
      """Main loop."""
      
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)
      
      # request a surface
      self.send(self.disprequest, "display_signal")


      # main loop
      done = False
      change = False    
      alpha = 255
      dir = -10
      while not done:
         if self.dataReady("alphacontrol"):
              alpha = self.recv("alphacontrol")
              self.display.set_alpha(alpha)
         if self.dataReady("control"):
            print "we do get here..."
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               self.send(cmsg,"signal")
               done = True
         
         # if we're given a new surface, use that instead
         if self.dataReady("callback"):
            if self.display is None:
               self.display = self.recv("callback")
               change = True
               for x in xrange(15): yield 1
               message = { "ADDLISTENEVENT" : pygame.KEYDOWN,
                           "surface" : self.display}
               self.send(message, "display_signal")

         if self.dataReady("inbox"):
            newImg = self.recv("inbox")
            self.fetchImage(newImg)
            change = True
            
         if self.dataReady("bgcolour"):
             self.backgroundColour = self.recv("bgcolour")
             change = True
            
         if change:
            self.blitToSurface()
            self.send({"REDRAW":True, "surface":self.display}, "display_signal")
            change = False

         self.pause()
         yield 1
      print "HERE"
      self.display.set_alpha(0)
      self.send(Axon.Ipc.producerFinished(message=self.display), "display_signal") 
      yield 1
      print "NOT HERE"
        
   def fetchImage(self, newImage):
      """\
      Load image from specified filename.

      self.size is set to image dimensions if self.size is None.

      Image is scaled by self.maxpect if self.maxpect evaluates to True.
      """
      if newImage is None:
         self.image = None
    
      else:
         self.image = pygame.image.load(newImage)
        
         if self.maxpect:
              self.image = pygame.transform.scale(self.image, (self.maxpect[0], self.maxpect[1]))
         if self.size is None:
             self.size = self.image.get_size()
        
        
   def blitToSurface(self):
       """Blits the background colour and image file to the surface"""
       try:
           self.display.fill( self.backgroundColour )
           self.display.blit( self.image, self.imagePosition )
       except:
           pass
        
__kamaelia_components__  = ( Image, )

             
if __name__ == "__main__":
   
   filebase = "../../../Examples/SupportingMediaFiles/"
   testImageFile0 = filebase + "cat.gif"
   testImageFile1 = filebase + "thumb.10063680.jpg.gif"

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

                  
   for i in range(0,6):
       image = Image(image=testImageFile0).activate()
       ic    = IChange(4+i).activate()
       ic.link( (ic, "outcolour"), (image, "bgcolour") )
       ic.link( (ic, "outimage"), (image, "inbox") )
       
   
   Axon.Scheduler.scheduler.run.runThreads()   
   
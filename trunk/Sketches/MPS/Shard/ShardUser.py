#!/usr/bin/python

import pygame
import Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.PygameDisplay import PygameDisplay

from Shards import Shardable

class MagnaDoodle(Shardable,Axon.Component.component):
   """\
   MagnaDoodle(...) -> A new MagnaDoodle component.

   A simple drawing board for the pygame display service.

   (this component and its documentation is heaviliy based on Kamaelia.UI.Pygame.Button)

   Keyword arguments:

   - position     -- (x,y) position of top left corner in pixels
   - margin       -- pixels margin between caption and button edge (default=8)
   - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
   - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
   - transparent  -- draw background transparent if True (default=False)
   - size         -- None or (w,h) in pixels (default=None)

   """
   requires_methods = [ "blitToSurface", "waitBox", "drawBG" ]

   Inboxes = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay"
             }
   Outboxes = { "outbox" : "not used",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }

   def __init__(self, caption=None, position=None, margin=8, bgcolour = (124,124,124), fgcolour = (0,0,0), msg=None,
                transparent = False, size=(200,200)):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(MagnaDoodle,self).__init__()

      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.margin = margin
      self.oldpos = None
      self.drawing = False

      self.size = size
      self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)

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

   def main(self):
      """Main loop."""
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,
                  "display_signal")

      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      self.drawBG()
      self.blitToSurface()
      
      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                  "surface" : self.display},
                  "display_signal")

      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                  "surface" : self.display},
                  "display_signal")

      self.send({ "ADDLISTENEVENT" : pygame.MOUSEMOTION,
                  "surface" : self.display},
                  "display_signal")

      done = False
      while not done:
         while self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               self.send(cmsg, "signal")
               done = True

         while self.dataReady("inbox"):
            for event in self.recv("inbox"):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    exec InlineShards.getIShard(self.IShards["MOUSEBUTTONDOWN"])
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    exec InlineShards.getIShard(self.IShards["MOUSEBUTTONUP_conditional"])
                elif event.type == pygame.MOUSEMOTION:
                    exec InlineShards.getIShard(self.IShards["MOUSEMOTION"])
         self.pause()
         yield 1

__kamaelia_components__  = ( MagnaDoodle, )

if __name__ == "__main__":
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from pygame.locals import *

   Magna = MagnaDoodle()

   from Shards import blitToSurface
   from Shards import waitBox
   from Shards import drawBG
   from Shards import Fail
   import InlineShards

   try:
       Magna.checkDependencies()
   except Fail, e:
       print "yay, should fail before we add dependencies"
   Magna.addMethod("blitToSurface", blitToSurface)
   Magna.addMethod("waitBox", waitBox)
   Magna.addMethod("drawBG", drawBG)

   Magna.addIShard("MOUSEBUTTONDOWN", InlineShards.MOUSEBUTTONDOWN_handler)
   Magna.addIShard("MOUSEBUTTONUP_conditional", InlineShards.MOUSEBUTTONUP_conditional_handler)
   Magna.addIShard("MOUSEMOTION", InlineShards.MOUSEMOTION_handler)

   try:
       Magna.checkDependencies()
   except Fail, e:
       print "Hmm, should not fail, we've added dependencies"

   Magna.run()







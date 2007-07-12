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

   def __init__(self, **argd):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(MagnaDoodle,self).__init__()
      self.initialShards(argd.get("initial_shards",{}))
      exec self.getIShard("__INIT__")

   def main(self):
      """Main loop."""
      exec self.getIShard("RequestDisplay")
      for _ in self.waitBox("callback"):
          yield 1 # This can't be Sharded or ISharded
      exec self.getIShard("GrabDisplay")

      self.drawBG()
      self.blitToSurface()
      exec self.getIShard("SetEventOptions")
      done = False
      while not done:
         exec self.getIShard("HandleShutdown")
         exec self.getIShard("LoopOverPygameEvents")
         self.pause()
         yield 1 # This can't be Sharded or ISharded

__kamaelia_components__  = ( MagnaDoodle, )

if __name__ == "__main__":
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from pygame.locals import *
   import InlineShards
   from Shards import blitToSurface
   from Shards import waitBox
   from Shards import drawBG
   from Shards import Fail
   from Shards import addListenEvent

   Magna = MagnaDoodle(initial_shards={"__INIT__": InlineShards.__INIT__})

   try:
       Magna.checkDependencies()
   except Fail, e:
       print "yay, should fail before we add dependencies"
   Magna.addMethod("blitToSurface", blitToSurface)
   Magna.addMethod("waitBox", waitBox)
   Magna.addMethod("drawBG", drawBG)
   Magna.addMethod("addListenEvent", addListenEvent)
   Magna.addIShard("MOUSEBUTTONDOWN", InlineShards.MOUSEBUTTONDOWN_handler)
   Magna.addIShard("MOUSEBUTTONUP", InlineShards.MOUSEBUTTONUP_handler)
   Magna.addIShard("MOUSEMOTION", InlineShards.MOUSEMOTION_handler)
   Magna.addIShard("HandleShutdown", InlineShards.ShutdownHandler)
   Magna.addIShard("LoopOverPygameEvents", InlineShards.LoopOverPygameEvents)
   Magna.addIShard("RequestDisplay", InlineShards.RequestDisplay)
   Magna.addIShard("GrabDisplay", InlineShards.GrabDisplay)
   Magna.addIShard("SetEventOptions", InlineShards.SetEventOptions)

   try:
       Magna.checkDependencies()
   except Fail, e:
       print "Hmm, should not fail, we've added dependencies"

   Magna.run()

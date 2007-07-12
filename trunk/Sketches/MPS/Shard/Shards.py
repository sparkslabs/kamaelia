#!/usr/bin/python

from ShardCore import Shardable, Fail
import pygame
import Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay

class ShardedPygameAppChassis(Shardable,Axon.Component.component):
   requires_methods = [ "blitToSurface", "waitBox", "drawBG", "addListenEvent" ]
   requires_ishards = ["MOUSEBUTTONDOWN", "MOUSEBUTTONUP", "MOUSEMOTION",
                       "HandleShutdown", "LoopOverPygameEvents", "RequestDisplay",
                       "GrabDisplay", "SetEventOptions" ]

   Inboxes = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay"
             }
   Outboxes = { "outbox" : "not used",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }

   def __init__(self, **argd):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ShardedPygameAppChassis,self).__init__()
      self.initialShards(argd.get("initial_shards",{}))
      exec self.getIShard("__INIT__", "")

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

#
# Non-Reusable
#
def drawBG(self):
    self.display.fill( (255,0,0) )
    self.display.fill( self.backgroundColour, self.innerRect )

#
# Reusable Shards
#

def waitBox(self,boxname):
    """Generator. yields 1 until data ready on the named inbox."""
    waiting = True
    while waiting:
        if self.dataReady(boxname): return
        else: yield 1

def blitToSurface(self):
    self.send({"REDRAW":True, "surface":self.display}, "display_signal")

def addListenEvent(self, event):
    self.send({ "ADDLISTENEVENT" : pygame.__getattribute__(event),
                "surface" : self.display},
                "display_signal")

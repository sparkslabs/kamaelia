#!/usr/bin/python

import inspect
import re

class Fail(Exception): pass

class Shardable(object):
    def __init__(self):
        super(Shardable,self).__init__()
        print "Initialising Shardable"
        self.IShards = {}

    def addMethod(self, name, method):
        self.__dict__[name] = lambda *args: method(self,*args)

    def addIShard(self, name, method):
        self.IShards[name] = method

    def initialShards(self, initial_shards):
        for name in initial_shards:
            self.addIShard(name, initial_shards[name])

    def checkDependencies(self):
        missing_methods = []
        missing_ishards = []
        for i in self.requires_methods:
            try:
                x = self.__getattribute__(i)
            except AttributeError, e:
                missing_methods.append(i)

        for i in self.requires_ishards:
            try:
                x = self.IShards[i]
            except KeyError, e:
                missing_ishards.append(i)

        if missing_methods != [] or missing_ishards != []:
            print "Class", self.__class__.__name__, "requires the following dependencies"
            print "   Missing Methods:", missing_methods
            print "   Missing IShards:", missing_ishards
            print
            raise Fail(missing_methods+missing_ishards)

    def getIShard(self, code_object_name, backup=""):
        try:
            IShard = inspect.getsource(self.IShards[code_object_name])
        except KeyError:
            IShard = ":\n"+backup
        IShard = IShard[re.search(":.*\n",IShard).end():] # strip def.*
        lines = []
        indent = -1
        for line in IShard.split("\n"):
            if indent == -1:
                r = line.strip()
                indent = len(line) - len(r)
                lines.append(r)
            else:
                lines.append(line[indent:])
        IShard = "\n".join(lines)
        return IShard

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

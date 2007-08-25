#!/usr/bin/python

#from ShardCore import Shardable, Fail
import pygame
import Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay


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

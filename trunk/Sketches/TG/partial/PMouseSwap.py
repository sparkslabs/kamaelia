from partial import *
from MouseEventHandling import *
from PartialMagnaDoodle import *

"""
Test case to confirm subclassing can't work this way:
(meta)partial's __new__ returns the base class instead
of the partial class, so no references are held to the partial
class at all: its name becomes an alias for the base class
"""
class ClickPrint(partial, PMouseEventHandler):
    
    #@replace   # this doesn't help either, as MouseHandler object thrown away
    def handleMouseUp(self, event):
        #super(ClickPrint, self).handleMouseUp(self, event)
        MouseEventHandler.handleMouseUp(self, event)
        print 'hup!'

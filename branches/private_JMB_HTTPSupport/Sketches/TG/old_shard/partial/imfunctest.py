from partial import *
from PMouseEventHandling import *
from PartialMagnaDoodle import *

"""
Test case to confirm subclassing can't work this way:
(meta)partial's __new__ returns the base class instead
of the partial class, so no references are held to the partial
class at all: its name becomes an alias for the base class
"""
class ClickTest(partial, MouseEventHandler):
    
    @replace   # required
    def handleMouseUp(self, event):
        super(ClickPrint, self).handleMouseUp.im_func(self, event) # causes <type 'exceptions.AttributeError'>: 'NoneType' object has no attribute 'exc_info'
        #MouseEventHandler.handleMouseUp.im_func(self, event) # infinite loop
        print 'hup!'

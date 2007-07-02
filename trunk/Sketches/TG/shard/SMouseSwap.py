from SMouseEventHandling import *

"""
Test case for subclassing with shard function

Inheritance works if superclass calls name the class specifically
instead of calling super(), and call the function object rather than
the method object by using superFunc.im_func() instead of superFunc()
"""
class ClickPrint(MouseEventHandler):
    def handleMouseUp(self, event):
        #super(ClickPrint, self).handleMouseUp.im_func(self, event)   # causes <type 'exceptions.AttributeError'>: 'NoneType' object has no attribute 'exc_info'
        MouseEventHandler.handleMouseUp.im_func(self, event)
        print 'hup!'
    
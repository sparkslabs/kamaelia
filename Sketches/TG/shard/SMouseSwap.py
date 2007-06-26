from SMouseEventHandling import *

"""
Test case for subclassing with shard function
"""
class ClickPrint(MouseEventHandler):
    def handleMouseUp(self, event):
        MouseEventHandler.handleMouseUp(self, event)
        print 'hup!'
    
    # for testing function application with non-ClickPrint objects
    def test(self):
        print 'testing', repr(self)
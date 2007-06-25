from SMouseEventHandling import *

"""
Test case for subclassing with shard function

Currently broken: although dir() will list all available methods,
only those defined here are stored in dict, so inherited
methods do not get added
"""
class ClickPrint(MouseEventHandler):
    def handleMouseUp(self, event):
        super(ClickPrint, self).handleMouseUp(self, event)
        print 'hup!'

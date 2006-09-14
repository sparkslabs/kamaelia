#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
#

from AxonExceptions import noSpaceInBox, LinkageClash

class nullsink(object):
    def __init__(self):
        super(nullsink,self).__init__()
        self.size = None
        self.tag = None
        self.showtransit = None
    def append(self, data):
        if self.showtransit:
            print "Discarding Delivery via [", self.tag, "] of ", repr(data)
    def setShowTransit(self,showtransit, tag):
        self.showtransit = showtransit
        self.tag = tag
    def __len__(self):
        return 0
    def pop(self,index):
        raise IndexError("nullsink: You can't pop from an empty piece of storage!")
    
    
class realsink(list):
    def __init__(self, notify, size=None):
        super(realsink,self).__init__()
        self.notify = notify
        self.size = size
        self.tag = None
        self.showtransit = None
    def append(self,data):
        if self.showtransit:
            print "Delivery via [", self.tag, "] of ", repr(data)
        if self.size is not None:
           if len(self) >= self.size:
               raise noSpaceInBox(len(self),self.size)
        list.append(self,data)
        self.notify()
    def setShowTransit(self,showtransit, tag):
        self.showtransit = showtransit
        self.tag = tag


class postbox(object):
    """\
    postbox(storage) -> new postbox object.
    
    Creates a postbox, using the specified storage as default storage. Storage
    should have the interface of list objects.
    """
    
    def __init__(self, storage):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature."""
        super(postbox,self).__init__()
        self.storage = storage
        self.sources = []
        self._retarget()
        self.local_len = storage.__len__    # so compoent can specifically query local storage
        self.target = None
    
    def __len__(self):
        return self.__target_len__()

    def addsource(self,newsource):
        """\
        addsource(newsource) registers newsource as a source and tells it to
        'retarget' at this postbox.
        """
        self.sources.append(newsource)       # XXX assuming not already linked from that source
        newsource._retarget(self)
        
    def removesource(self,oldsource):
        """\
        removesource(oldsource) deregisters oldsource as a source and tells it
        to 'retarget' at None (nothing).
        """
        self.sources.remove(oldsource)
        oldsource._retarget(newtarget=None)
        
    def _retarget(self, newtarget=None):
        """\
        retarget([newtarget]) aims requests at to this postbox at a different
        target.
        
        If newtarget is unspecified or None, target is default lol storage.
        """
        if newtarget==None:
            self.sink = self.storage
        else:
#             if self.target != None and self.target != newtarget:
#                 raise LinkageClash("Can't create linkage going out from an inbox/outbox that already has a linkage going out from it.")
            self.sink = newtarget.sink
            # if i'm storing stuff, pass it on
            while len(self.storage):
                self.sink.append(self.storage.pop(0))
        
        self.target = newtarget
        
        # make calling these methods go direct to the sink
        self.append         = self.sink.append
        self.pop            = self.sink.pop
        self.__target_len__ = self.sink.__len__
        # propagate the change back up the chain
        for source in self.sources:
            source._retarget(newtarget=self)

    def setSize(self, size):
        self.storage.size = size
        return self.getSize()
    def getSize(self):
        return self.storage.size

    def setShowTransit(self, showtransit=False, tag=None):
        self.storage.setShowTransit(showtransit, tag)

    def isFull(self):
        return (self.sink.size != None) and (len(self) >= self.sink.size)

thenullsink = nullsink()

def makeInbox(notify, size = None):
    """Returns a postbox object suitable for use as an Axon inbox."""
    result = postbox(storage=realsink(notify=notify))
    if size is not None:
       result.setSize(size)
    return result

def makeOutbox():
    """Returns a postbox object suitable for use a an Axon outbox."""
    return postbox(storage=thenullsink)

# RELEASE: MH, MPS

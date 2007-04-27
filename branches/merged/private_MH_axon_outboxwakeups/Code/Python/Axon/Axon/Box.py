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

from AxonExceptions import noSpaceInBox

class nullsink(object):
    def __init__(self):
        super(nullsink,self).__init__()
        self.size = None
        self.tag = None
        self.showtransit = None
        self.wakeOnPop = []   # callbacks for when a pop() happens
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
        self.wakeOnPop = []   # callbacks for when a pop() happens
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
    def pop(self,index):
        item = list.pop(self, index)
        for n in self.wakeOnPop:
            n()
        return item


class postbox(object):
    """\
    postbox(storage,notify) -> new postbox object.
    
    Creates a postbox, using the specified storage as default storage. Storage
    should have the interface of list objects.
    
    Also takes optional notify callback, that will be called whenever an item is
    taken out of a postbox further down the chain.
    """
    
    def __init__(self, storage, notify=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature."""
        super(postbox,self).__init__()
        self.storage = storage
        self.sources = []
        self.myNotifyOnPop = []
        if notify != None:
            self.myNotifyOnPop.append(notify)
        self.target = None
        self._retarget()
        self.local_len = storage.__len__    # so compoent can specifically query local storage
    
    def __len__(self):
        return self.__target_len__()

    def addsource(self,newsource):
        """\
        addsource(newsource) registers newsource as a source and tells it to
        'retarget' at this postbox.
        
        Also finds out from the new source who wants to be notified when messages are taken
        out of postboxes, and updates records accordingly, and passes this info further down
        the chain of linkages.
        """
        self.sources.append(newsource)       # XXX assuming not already linked from that source
        newsource._retarget(self)
        self._addnotifys(newsource.getnotifys())
        
    def removesource(self,oldsource):
        """\
        removesource(oldsource) deregisters oldsource as a source and tells it
        to 'retarget' at None (nothing).
        
        Also finds out from the old source who was being notified when messages are taken
        out of postboxes, and updates records accordingly, and passes this info further down
        the chain of linkages.
        """
        self.sources.remove(oldsource)
        oldsource._retarget(newtarget=None)
        self._removenotifys(oldsource.getnotifys())
        
    def getnotifys(self):
        return self.myNotifyOnPop + self.storage.wakeOnPop
    
    def _addnotifys(self, newnotifys):
        """\
        Updates the local storage's list of notification callbacks for when messages are
        taken out of inboxes. Then recurses this info to this postbox's target, so it can
        update too.
        """
        self.storage.wakeOnPop.extend(newnotifys)
        if self.target != None:
            self.target._addnotifys(newnotifys)
        
    def _removenotifys(self, oldnotifys):
        """\
        Updates the local storage's list of notification callbacks for when messages are
        taken out of inboxes. Then recurses this info to this postbox's target, so it can
        update too.
        """
        for n in oldnotifys:
            self.storage.wakeOnPop.remove(n)
        if self.target != None:
            self.target._removenotifys(oldnotifys)
        
    def _retarget(self, newtarget=None):
        """\
        retarget([newtarget]) aims requests at to this postbox at a different
        target.
        
        If newtarget is unspecified or None, target is default lol storage.
        """
        if newtarget==None:
            self.target = None
            self.sink = self.storage
        else:
            self.target = newtarget
            self.sink = newtarget.sink
            # if i'm storing stuff, pass it on
            while len(self.storage):
                self.sink.append(self.storage.pop(0))
        
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
            

def makeInbox(notify, size = None):
    """Returns a postbox object suitable for use as an Axon inbox."""
    result = postbox(storage=realsink(notify=notify))
    if size is not None:
       result.setSize(size)
    return result

def makeOutbox(notify):
    """Returns a postbox object suitable for use a an Axon outbox."""
    return postbox(storage=nullsink(), notify=notify)

# RELEASE: MH, MPS

#!/usr/bin/env python
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
=====================================
Axon postboxes - inboxes and outboxes
=====================================

The objects used to implement inboxes and outboxes. They store and handle
linkages and delivery of messages from outbox to inbox.

* Components create postboxes and use them as their inboxes and outboxes.

*This is an Axon internal. If you are writing components you do not need to
understand this as you will normally not use it directly.*

Developers wishing to use Axon in other ways or understand its implementation
shoudl read on with interest!



Example Usage
-------------

Creation
~~~~~~~~

Creating an outbox::

    def outboxNotify():
        print "A message was collected from an inbox that this outbox is linked to."
    
    myOutbox = makeOutbox(outboxNotify)

Creating an inbox::

    def inboxNotify():
        print "A new message has arrived at this inbox."

    myInbox = makeInbox(inboxNotify)

Creating an inbox that is limited to holding 10 items::

    mySizeLimitedInbox = makeInbox(inboxNotify, size=10)

Alternative syntax to do the same::

    mySizeLimitedInbox = makeInbox(inboxNotify)
    mySizeLimitedInbox.setSize(10)


Adding/Removing Linkages
~~~~~~~~~~~~~~~~~~~~~~~~
    
Create outboxes A and B, and inboxes C and D, then linking them in a chain
A to B to C to D::

    boxA = makeOutbox( <notify callback> )
    boxB = makeOutbox( <notify callback> )
    
    boxC = makeInbox( <notify callback> )
    boxD = makeInbox( <notify callback> )
        
    boxB.addsource(boxA)
    boxC.addsource(boxB)
    boxD.addsource(boxC)

We can also remove one of those linkages::

    boxC.removeSource(boxB)



More detail
-----------

Call makeInbox() or makeOutbox() to make an inbox or outbox respectively.

Both inboxes and outboxes are instances of the postbox class. postboxes provide
a subset of the python list interface to let you add and remove items from it:

* **postbox.append(data)** - ie. send a message
* **postbox.pop(data)** - ie. collect a message
* **postbox.__len__()** - ie. len(myPostbox)


Inboxes
~~~~~~~

An inbox is a postbox with storage. Calling append() will put a message into
that inbox. Calling len() will report the number of items in the inbox, and
pop() will enable you to take items out.

Inboxes can be size limited. If it becomes full then trying to append() will
raise an Axon.AxonExceptions.noSpaceInBox exception.


Outboxes
~~~~~~~~

An outbox is a postbox with no storage. Calling append() will silently discard
the message. len() will report the box as containing zero items; and calling
pop() will, as expected, raise an IndexError exception.


Linking them together
~~~~~~~~~~~~~~~~~~~~~

Boxes can be wired together, so that posting a message to one actually results
in the message appearing in another. Axon does this when you make a link between
postboxes on different components. Links have direction. Messages flow only one
way along a link - from source to target/destination/sink.

Boxes can be wired up in a many-to-one tree structure - where many sources feed
their messages, along one or more hops through inbetween postboxes, towards a
single destination:

* postbox.addsource(source_postbox)
* postbox.removeSource(source_postbox)

Suppose you wire up boxes to form a tree::

    +---+       +---+
    | A | ----> | B | --,
    +---+       +---+   '--> +---+       +---+       +---+
                             | D | ----> | E | ----> | F |
                +---+   ,--> +---+       +---+       +---+
                | C | --'
                +---+

Sending a message using the append() method from A,B,C,D or E will result in
the message being sent to F. Make sure F is an outbox, otherwise the message
will be lost!

When a box is wired to another, it diverts calls to append() to the final
destination instead of its own local storage; so A,B,C,D and E can be inboxes
or outboxes - it doesn't matter.

You are not allowed to create links going from one source to two or more
destinations (one-to-many arrangements). If you try, an Axon.AxonExceptions.BoxAlreadyLinkedToDestination
exception will be raised.



How is it implemented?
----------------------

Calling makeInbox() or makeOutbox() creates an instance of the postbox class.
A postbox behaves like a simple piece of storage, accessed using the append(),
pop() and len() methods. However, if the postbox is linked to others,
then the storage that is actually accessed belongs to the target postbox (the
final destination in the chain).

This storage is therefore actually a separate object, held inside a postbox.
When postboxes are wired together, they all reconfigure themselves so that calls
to append(), len() and pop() actually access the same storage in the target
postbox. In the postbox class, where the messages actually get sent to is
referred to as the sink.

For inboxes, this is an instance of the realsink class (that actually stores
stuff). But for outboxes, it is an instance of the nullsink class (that just
discards stuff given to it, and always appears empty). This is so that messages
that end up at outboxes don't pile up, uncollected.

For example, suppose we link three postboxes in a chain::

  +-------------------+      +-------------------+      +----------------------+
  |     postbox A     | ---> |     postbox B     | ---> |      postbox C       |
  |                   |      |                   |      |                      |
  | A.target = C      |      | B.target = C      |      | C.target = None      |
  | A.sink   = C.sink |      | B.sink   = C.sink |      | C.sink   = C.storage |
  +-------------------+      +-------------------+      +----------------------+

The target of postboxes A and B is postbox C. The sinks used by all three is
the storage beloinging to postbox C. Calls to append(), pop() and len() made to
any of the three postboxes are all direected to the storage in postbox C.

The links between postboxes are represented internally as a list of sources for
each postbox. For example::

    +---+       +---+
    | A | ----> | B | --,
    +---+       +---+   '--> +---+       +---+       +---+
                             | D | ----> | E | ----> | F |
                +---+   ,--> +---+       +---+       +---+
                | C | --'
                +---+

    A.sources = []
    B.sources = [A]
    C.sources = []
    D.sources = [B,C]
    E.sources = [D]
    F.sources = [E]

Links are created an destroyed by calling addsource() or removeSource(). So
for example, to wire up postbox D in the above example, the following calls were
made::

    D.addsource(B)
    D.addsource(C)

Internally, addsource() and removeSource() calls _retarget() which recurses back
up the chain of linkages, updating any other boxes that feed into the source,
to make sure they all now point at the new target too.

addsource() also delivers any messages waiting in the source's storage to the
new destination's storage. This ensures that messages do not get lost halfway
along a chain of linkages when the chain is extended.

Because all postboxes in a chain end up redirecting calls to the target
postbox's storage; a separate self.local_len() method is provided to allow a
component to find out whether there is any items waiting in its own postbox.
A component's inbox might not be the final destination in a chain, so it is
important that if the component attempts to examine its own inbox for new items
it should not inadvertently query the final destination instead.



Notification that a message has been delivered
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When creating an inbox, you provide a notification callback that will be called
whenever a new message arrives at that box. Axon uses this to wake the component
that owns that inbox.

The realsink object keeps note of this callback, and calls it when a new message
is delivered to it (ie. its append() method is called).



Notification that a message has been collected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a message is collected; some parties in the chain of linked boxes may wish
to be notified. Axon uses this to wake owners of outboxes linked to the
destination inbox from which the message has been collected. You therefore
provide a notification callback when creating an outbox.

The realsink object keeps a 'wakeOnPop' list of callbacks to call when its pop()
method is called.

When linkages are added or removed, the storage of all inboxes downstream of
where the change has occurred must update their list of 'wakeOnPop' callbacks.
Therefore addsource() or removeSource() also call _addNotifys() or
_removeNotifys() respectively, which recurse down the chain of linkages towards
the target, updating the list of callbacks as they go.



Notifications - performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

All this climbing up and down of the chain of linkages to update lists of
callbacks takes time - O(n) where n is the number of postboxes in the chain.

Paying this cost upfront means that the overheads of actually delivering or
collecting messages is substantially less because all the data is already there
and up to date. In general, it is felt that messages are likely to be sent far
more often than linkages are created and destroyed - which should justify this
tradeoff.
"""

from AxonExceptions import noSpaceInBox
from AxonExceptions import BoxAlreadyLinkedToDestination

ShowAllTransits = False

class nullsink(object):
    """\
    nullsink() -> new nullsink object

    A dummy piece of storage for postboxes, that behaves a bit like a list.

    Discards data given to it by calling append() and always reports that it
    contains no items.
    """
    
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature."""
        super(nullsink,self).__init__()
        self.size = None
        self.tag = None
        self.showtransit = ShowAllTransits
        self.wakeOnPop = []   # callbacks for when a pop() happens

    def append(self, data):
        """\
        Append item to the list - though actually it just gets discarded.
        """
        if self.showtransit:
            print "Discarding Delivery via [", self.tag, "] of ", repr(data)

    def setShowTransit(self,showtransit, tag):
        """\
        Set showTransit to True to cause debugging output whenever a message is
        delivered to this storage. The tag can be anything you want to identify
        this occurrence.
        """
        self.showtransit = showtransit
        self.tag = tag
    
    def __len__(self):
        """Returns number of items in the list (always zero)"""
        return 0
    
    def pop(self,index):
        """Returns an item from the list (always raises IndexError"""
        raise IndexError("nullsink: You can't pop from an empty piece of storage!")
    def __repr__(self):
        return "<>"

class realsink(list):
    """\
    realsink(notify[,size]) -> new realsink object.

    A working piece of storage for postboxes, that behaves a bit like a list.

    Stores data given to it by calling append(), up to a limit after which
    Axon.AxonExceptions.noSpaceInBox exceptions are raised.

    Calls the 'notify' callback when append() is called.
    Calls any callbacks in the self.wakeOnPop list when pop() is called.

    Keyword arguments:

    - notify  -- notify() is called whenever append() is called
    - size    -- None, or the maximum number of items this storage can hold
    """
    
    def __init__(self, notify, size=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature."""
        super(realsink,self).__init__()
        self.notify = notify
        self.size = size
        self.tag = None
        self.showtransit = None
        self.wakeOnPop = []   # callbacks for when a pop() happens
        
    def append(self,data):
        """\
        Appends item to the list, or raises Axon.AxonExceptions.noSpaceInBox
        exception if the number of items already meets the size limit.

        Calls self.notify() callback
        """
        if self.showtransit or ShowAllTransits:
            print "Delivery via [", self.tag, "] of ", repr(data)
        if self.size is not None:
           if len(self) >= self.size:
               raise noSpaceInBox(len(self),self.size)
        list.append(self,data)
        self.notify()
        
    def setShowTransit(self,showtransit, tag):
        """\
        Set showTransit to True to cause debugging output whenever a message is
        delivered to this storage. The tag can be anything you want to identify
        this occurrence.
        """
        self.showtransit = showtransit
        self.tag = tag
        
    def pop(self,index):
        """\
        Returns an item from the list, or raises IndexError if there are none.

        Calls all callbacks listed in self.wakeOnPop
        """
        item = list.pop(self, index)
        for n in self.wakeOnPop:
            n()
        return item


class postbox(object):
    """\
    postbox(storage[,notify]) -> new postbox object.
    
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

        # point at self to start with (not linked to any other postboxes yet)
        self.target = None
        self._retarget()
        self.local_len = storage.__len__    # so component can specifically query local storage
    
    def __len__(self):
        """Returns number of items in the postbox"""
        return self.__target_len__()

    def addsource(self,newsource):
        """\
        addsource(newsource) registers newsource as a source and tells it to
        'retarget' at this postbox.
        
        Also finds out from the new source who wants to be notified when messages are taken
        out of postboxes, and updates records accordingly, and passes this info further down
        the chain of linkages.
        
        Raises Axon.AxonExceptions.BoxAlreadyLinkedToDestination if the newsource is already
        targetted at a destination. This is because Axon does not support one-to-many
        arrangements.
        """
        if newsource.target != None:
            raise BoxAlreadyLinkedToDestination(self, self.target, newsource)
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
        """\
        Returns list of all callbacks that should be made when messages are collected
        from a postbox using this one as a source.

        The list returned is effectively all callbacks this postbox would have to make
        *plus* the callback for the owner of this box (if there is one)
        """
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
        
        If newtarget is unspecified or None, target is default local storage.
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
        """\
        Set box size limit (use None for no limit)

        Behaviour is undefined (and not recommended!) if this call is made whilst
        there may be items in the postbox!
        """
        self.storage.size = size
        return self.getSize()

    def getSize(self):
        """Gets current box size limit"""
        return self.storage.size

    def setShowTransit(self, showtransit=False, tag=None):
        """\
        Set showTransit to True to cause debugging output whenever a message is
        delivered to this postbox. The tag can be anything you want to identify
        this occurrence.
        """
        self.storage.setShowTransit(showtransit, tag)

    def isFull(self):
        """Returns True if the destination box is full (and has a size limit)"""
        return (self.sink.size != None) and (len(self) >= self.sink.size)

    def __repr__(self):
        return repr(self.sink)

def makeInbox(notify, size = None):
    """\
    Returns a new postbox object suitable for use as an Axon inbox.

    Keyword arguments:

    - notify  -- notify() will be called whenever a message arrives at this inbox.
    - size    -- None, or a limit on the maxmimum number if items this inbox can hold (default=None)
    """
    result = postbox(storage=realsink(notify=notify))
    if size is not None:
       result.setSize(size)
    return result

def makeOutbox(notify):
    """\
    Returns a new postbox object suitable for use a an Axon outbox.

    Keyword arguments:

    - notify  -- notify() will be called whenever a message is collected from an inbox that this outbox delivers to.
    """
    return postbox(storage=nullsink(), notify=notify)

# RELEASE: MH, MPS

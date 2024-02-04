---
pagename: Docs/Axon/Axon.Box
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}
------------------------------------------------------------------------------------
:::
:::

::: {.section}
Axon postboxes - inboxes and outboxes
=====================================

::: {.container}
-   **[makeInbox](/Docs/Axon/Axon.Box.makeInbox.html){.reference}**(notify\[,
    size\])
-   **[makeOutbox](/Docs/Axon/Axon.Box.makeOutbox.html){.reference}**(notify)
-   **class [nullsink](/Docs/Axon/Axon.Box.nullsink.html){.reference}**
-   **class [postbox](/Docs/Axon/Axon.Box.postbox.html){.reference}**
-   **class [realsink](/Docs/Axon/Axon.Box.realsink.html){.reference}**
:::

-   [Example Usage](#35){.reference}
    -   [Creation](#36){.reference}
    -   [Adding/Removing Linkages](#37){.reference}
-   [More detail](#38){.reference}
    -   [Inboxes](#39){.reference}
    -   [Outboxes](#40){.reference}
    -   [Linking them together](#41){.reference}
-   [How is it implemented?](#42){.reference}
    -   [Notification that a message has been
        delivered](#43){.reference}
    -   [Notification that a message has been
        collected](#44){.reference}
    -   [Notifications - performance](#45){.reference}
:::

::: {.section}
The objects used to implement inboxes and outboxes. They store and
handle linkages and delivery of messages from outbox to inbox.

-   Components create postboxes and use them as their inboxes and
    outboxes.

*This is an Axon internal. If you are writing components you do not need
to understand this as you will normally not use it directly.*

Developers wishing to use Axon in other ways or understand its
implementation shoudl read on with interest!

::: {.section}
[Example Usage]{#example-usage} {#35}
-------------------------------

::: {.section}
### [Creation]{#creation} {#36}

Creating an outbox:

``` {.literal-block}
def outboxNotify():
    print "A message was collected from an inbox that this outbox is linked to."

myOutbox = makeOutbox(outboxNotify)
```

Creating an inbox:

``` {.literal-block}
def inboxNotify():
    print "A new message has arrived at this inbox."

myInbox = makeInbox(inboxNotify)
```

Creating an inbox that is limited to holding 10 items:

``` {.literal-block}
mySizeLimitedInbox = makeInbox(inboxNotify, size=10)
```

Alternative syntax to do the same:

``` {.literal-block}
mySizeLimitedInbox = makeInbox(inboxNotify)
mySizeLimitedInbox.setSize(10)
```
:::

::: {.section}
### [Adding/Removing Linkages]{#adding-removing-linkages} {#37}

Create outboxes A and B, and inboxes C and D, then linking them in a
chain A to B to C to D:

``` {.literal-block}
boxA = makeOutbox( <notify callback> )
boxB = makeOutbox( <notify callback> )

boxC = makeInbox( <notify callback> )
boxD = makeInbox( <notify callback> )

boxB.addsource(boxA)
boxC.addsource(boxB)
boxD.addsource(boxC)
```

We can also remove one of those linkages:

``` {.literal-block}
boxC.removeSource(boxB)
```
:::
:::

::: {.section}
[More detail]{#more-detail} {#38}
---------------------------

Call makeInbox() or makeOutbox() to make an inbox or outbox
respectively.

Both inboxes and outboxes are instances of the postbox class. postboxes
provide a subset of the python list interface to let you add and remove
items from it:

-   **postbox.append(data)** - ie. send a message
-   **postbox.pop(data)** - ie. collect a message
-   **postbox.\_\_len\_\_()** - ie. len(myPostbox)

::: {.section}
### [Inboxes]{#inboxes} {#39}

An inbox is a postbox with storage. Calling append() will put a message
into that inbox. Calling len() will report the number of items in the
inbox, and pop() will enable you to take items out.

Inboxes can be size limited. If it becomes full then trying to append()
will raise an
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
exception.
:::

::: {.section}
### [Outboxes]{#outboxes} {#40}

An outbox is a postbox with no storage. Calling append() will silently
discard the message. len() will report the box as containing zero items;
and calling pop() will, as expected, raise an IndexError exception.
:::

::: {.section}
### [Linking them together]{#linking-them-together} {#41}

Boxes can be wired together, so that posting a message to one actually
results in the message appearing in another. Axon does this when you
make a link between postboxes on different components. Links have
direction. Messages flow only one way along a link - from source to
target/destination/sink.

Boxes can be wired up in a many-to-one tree structure - where many
sources feed their messages, along one or more hops through inbetween
postboxes, towards a single destination:

-   postbox.addsource(source\_postbox)
-   postbox.removeSource(source\_postbox)

Suppose you wire up boxes to form a tree:

``` {.literal-block}
+---+       +---+
| A | ----> | B | --,
+---+       +---+   '--> +---+       +---+       +---+
                         | D | ----> | E | ----> | F |
            +---+   ,--> +---+       +---+       +---+
            | C | --'
            +---+
```

Sending a message using the append() method from A,B,C,D or E will
result in the message being sent to F. Make sure F is an outbox,
otherwise the message will be lost!

When a box is wired to another, it diverts calls to append() to the
final destination instead of its own local storage; so A,B,C,D and E can
be inboxes or outboxes - it doesn\'t matter.

You are not allowed to create links going from one source to two or more
destinations (one-to-many arrangements). If you try, an
[Axon.AxonExceptions.BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}
exception will be raised.
:::
:::

::: {.section}
[How is it implemented?]{#how-is-it-implemented} {#42}
------------------------------------------------

Calling makeInbox() or makeOutbox() creates an instance of the postbox
class. A postbox behaves like a simple piece of storage, accessed using
the append(), pop() and len() methods. However, if the postbox is linked
to others, then the storage that is actually accessed belongs to the
target postbox (the final destination in the chain).

This storage is therefore actually a separate object, held inside a
postbox. When postboxes are wired together, they all reconfigure
themselves so that calls to append(), len() and pop() actually access
the same storage in the target postbox. In the postbox class, where the
messages actually get sent to is referred to as the sink.

For inboxes, this is an instance of the realsink class (that actually
stores stuff). But for outboxes, it is an instance of the nullsink class
(that just discards stuff given to it, and always appears empty). This
is so that messages that end up at outboxes don\'t pile up, uncollected.

For example, suppose we link three postboxes in a chain:

``` {.literal-block}
+-------------------+      +-------------------+      +----------------------+
|     postbox A     | ---> |     postbox B     | ---> |      postbox C       |
|                   |      |                   |      |                      |
| A.target = C      |      | B.target = C      |      | C.target = None      |
| A.sink   = C.sink |      | B.sink   = C.sink |      | C.sink   = C.storage |
+-------------------+      +-------------------+      +----------------------+
```

The target of postboxes A and B is postbox C. The sinks used by all
three is the storage beloinging to postbox C. Calls to append(), pop()
and len() made to any of the three postboxes are all direected to the
storage in postbox C.

The links between postboxes are represented internally as a list of
sources for each postbox. For example:

``` {.literal-block}
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
```

Links are created an destroyed by calling addsource() or removeSource().
So for example, to wire up postbox D in the above example, the following
calls were made:

``` {.literal-block}
D.addsource(B)
D.addsource(C)
```

Internally, addsource() and removeSource() calls \_retarget() which
recurses back up the chain of linkages, updating any other boxes that
feed into the source, to make sure they all now point at the new target
too.

addsource() also delivers any messages waiting in the source\'s storage
to the new destination\'s storage. This ensures that messages do not get
lost halfway along a chain of linkages when the chain is extended.

Because all postboxes in a chain end up redirecting calls to the target
postbox\'s storage; a separate self.local\_len() method is provided to
allow a component to find out whether there is any items waiting in its
own postbox. A component\'s inbox might not be the final destination in
a chain, so it is important that if the component attempts to examine
its own inbox for new items it should not inadvertently query the final
destination instead.

::: {.section}
### [Notification that a message has been delivered]{#notification-that-a-message-has-been-delivered} {#43}

When creating an inbox, you provide a notification callback that will be
called whenever a new message arrives at that box. Axon uses this to
wake the component that owns that inbox.

The realsink object keeps note of this callback, and calls it when a new
message is delivered to it (ie. its append() method is called).
:::

::: {.section}
### [Notification that a message has been collected]{#notification-that-a-message-has-been-collected} {#44}

When a message is collected; some parties in the chain of linked boxes
may wish to be notified. Axon uses this to wake owners of outboxes
linked to the destination inbox from which the message has been
collected. You therefore provide a notification callback when creating
an outbox.

The realsink object keeps a \'wakeOnPop\' list of callbacks to call when
its pop() method is called.

When linkages are added or removed, the storage of all inboxes
downstream of where the change has occurred must update their list of
\'wakeOnPop\' callbacks. Therefore addsource() or removeSource() also
call \_addNotifys() or \_removeNotifys() respectively, which recurse
down the chain of linkages towards the target, updating the list of
callbacks as they go.
:::

::: {.section}
### [Notifications - performance]{#notifications-performance} {#45}

All this climbing up and down of the chain of linkages to update lists
of callbacks takes time - O(n) where n is the number of postboxes in the
chain.

Paying this cost upfront means that the overheads of actually delivering
or collecting messages is substantially less because all the data is
already there and up to date. In general, it is felt that messages are
likely to be sent far more often than linkages are created and destroyed
- which should justify this tradeoff.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[makeInbox](/Docs/Axon/Axon.Box.makeInbox.html){.reference}
================================================================================================================================================

::: {.section}
[makeInbox(notify\[, size\])]{#symbol-makeInbox}
------------------------------------------------

Returns a new postbox object suitable for use as an Axon inbox.

Keyword arguments:

-   notify \-- notify() will be called whenever a message arrives at
    this inbox.
-   size \-- None, or a limit on the maxmimum number if items this inbox
    can hold (default=None)
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[makeOutbox](/Docs/Axon/Axon.Box.makeOutbox.html){.reference}
==================================================================================================================================================

::: {.section}
[makeOutbox(notify)]{#symbol-makeOutbox}
----------------------------------------

Returns a new postbox object suitable for use a an Axon outbox.

Keyword arguments:

-   notify \-- notify() will be called whenever a message is collected
    from an inbox that this outbox delivers to.
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[nullsink](/Docs/Axon/Axon.Box.nullsink.html){.reference}
==============================================================================================================================================

::: {.section}
class nullsink(object) {#symbol-nullsink}
----------------------

::: {.section}
nullsink() -\> new nullsink object

A dummy piece of storage for postboxes, that behaves a bit like a list.

Discards data given to it by calling append() and always reports that it
contains no items.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self)]{#symbol-nullsink.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature.
:::

::: {.section}
#### [\_\_len\_\_(self)]{#symbol-nullsink.__len__}

Returns number of items in the list (always zero)
:::

::: {.section}
#### [\_\_repr\_\_(self)]{#symbol-nullsink.__repr__}
:::

::: {.section}
#### [append(self, data)]{#symbol-nullsink.append}

Append item to the list - though actually it just gets discarded.
:::

::: {.section}
#### [pop(self, index)]{#symbol-nullsink.pop}

Returns an item from the list (always raises IndexError
:::

::: {.section}
#### [setShowTransit(self, showtransit, tag)]{#symbol-nullsink.setShowTransit}

Set showTransit to True to cause debugging output whenever a message is
delivered to this storage. The tag can be anything you want to identify
this occurrence.
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[postbox](/Docs/Axon/Axon.Box.postbox.html){.reference}
============================================================================================================================================

::: {.section}
class postbox(object) {#symbol-postbox}
---------------------

::: {.section}
postbox(storage\[,notify\]) -\> new postbox object.

Creates a postbox, using the specified storage as default storage.
Storage should have the interface of list objects.

Also takes optional notify callback, that will be called whenever an
item is taken out of a postbox further down the chain.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, storage\[, notify\])]{#symbol-postbox.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature.
:::

::: {.section}
#### [\_\_len\_\_(self)]{#symbol-postbox.__len__}

Returns number of items in the postbox
:::

::: {.section}
#### [\_\_repr\_\_(self)]{#symbol-postbox.__repr__}
:::

::: {.section}
#### [\_addnotifys(self, newnotifys)]{#symbol-postbox._addnotifys}

Updates the local storage\'s list of notification callbacks for when
messages are taken out of inboxes. Then recurses this info to this
postbox\'s target, so it can update too.
:::

::: {.section}
#### [\_removenotifys(self, oldnotifys)]{#symbol-postbox._removenotifys}

Updates the local storage\'s list of notification callbacks for when
messages are taken out of inboxes. Then recurses this info to this
postbox\'s target, so it can update too.
:::

::: {.section}
#### [\_retarget(self\[, newtarget\])]{#symbol-postbox._retarget}

retarget(\[newtarget\]) aims requests at to this postbox at a different
target.

If newtarget is unspecified or None, target is default local storage.
:::

::: {.section}
#### [addsource(self, newsource)]{#symbol-postbox.addsource}

addsource(newsource) registers newsource as a source and tells it to
\'retarget\' at this postbox.

Also finds out from the new source who wants to be notified when
messages are taken out of postboxes, and updates records accordingly,
and passes this info further down the chain of linkages.

Raises
[Axon.AxonExceptions.BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}
if the newsource is already targetted at a destination. This is because
Axon does not support one-to-many arrangements.
:::

::: {.section}
#### [getSize(self)]{#symbol-postbox.getSize}

Gets current box size limit
:::

::: {.section}
#### [getnotifys(self)]{#symbol-postbox.getnotifys}

Returns list of all callbacks that should be made when messages are
collected from a postbox using this one as a source.

The list returned is effectively all callbacks this postbox would have
to make *plus* the callback for the owner of this box (if there is one)
:::

::: {.section}
#### [isFull(self)]{#symbol-postbox.isFull}

Returns True if the destination box is full (and has a size limit)
:::

::: {.section}
#### [removesource(self, oldsource)]{#symbol-postbox.removesource}

removesource(oldsource) deregisters oldsource as a source and tells it
to \'retarget\' at None (nothing).

Also finds out from the old source who was being notified when messages
are taken out of postboxes, and updates records accordingly, and passes
this info further down the chain of linkages.
:::

::: {.section}
#### [setShowTransit(self\[, showtransit\]\[, tag\])]{#symbol-postbox.setShowTransit}

Set showTransit to True to cause debugging output whenever a message is
delivered to this postbox. The tag can be anything you want to identify
this occurrence.
:::

::: {.section}
#### [setSize(self, size)]{#symbol-postbox.setSize}

Set box size limit (use None for no limit)

Behaviour is undefined (and not recommended!) if this call is made
whilst there may be items in the postbox!
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Box](/Docs/Axon/Axon.Box.html){.reference}.[realsink](/Docs/Axon/Axon.Box.realsink.html){.reference}
==============================================================================================================================================

::: {.section}
class realsink(list) {#symbol-realsink}
--------------------

::: {.section}
realsink(notify\[,size\]) -\> new realsink object.

A working piece of storage for postboxes, that behaves a bit like a
list.

Stores data given to it by calling append(), up to a limit after which
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
exceptions are raised.

Calls the \'notify\' callback when append() is called. Calls any
callbacks in the self.wakeOnPop list when pop() is called.

Keyword arguments:

-   notify \-- notify() is called whenever append() is called
-   size \-- None, or the maximum number of items this storage can hold
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, notify\[, size\])]{#symbol-realsink.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature.
:::

::: {.section}
#### [append(self, data)]{#symbol-realsink.append}

Appends item to the list, or raises
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
exception if the number of items already meets the size limit.

Calls self.notify() callback
:::

::: {.section}
#### [pop(self, index)]{#symbol-realsink.pop}

Returns an item from the list, or raises IndexError if there are none.

Calls all callbacks listed in self.wakeOnPop
:::

::: {.section}
#### [setShowTransit(self, showtransit, tag)]{#symbol-realsink.setShowTransit}

Set showTransit to True to cause debugging output whenever a message is
delivered to this storage. The tag can be anything you want to identify
this occurrence.
:::
:::

::: {.section}
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*

---
pagename: Docs/Axon/Axon.Postoffice
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Postoffice](/Docs/Axon/Axon.Postoffice.html){.reference}
--------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Axon postoffices
================

::: {.container}
-   **class
    [postoffice](/Docs/Axon/Axon.Postoffice.postoffice.html){.reference}**
:::

-   [How is this used in Axon?](#7){.reference}
-   [Example usage](#8){.reference}
-   [More detail](#9){.reference}
-   [Test documentation](#10){.reference}
:::

::: {.section}
A postoffice object looks after linkages. It can create and destroy them
and keeps records of what ones currently exist. It hands out linkage
objects that can be used as handles to later unlink (remove) the
linkage.

THIS IS AN AXON INTERNAL! If you are writing components you do not need
to understand this.

Developers wishing to understand how Axon is implemented should read on
with interest!

::: {.section}
[How is this used in Axon?]{#how-is-this-used-in-axon} {#7}
------------------------------------------------------

Every component has its own postoffice. The component\'s link() and
unlink() methods instruct the post office to create and remove linkages.

When a component terminates, it asks its post office to remove any
outstanding linkages.
:::

::: {.section}
[Example usage]{#example-usage} {#8}
-------------------------------

Creating a link from an inbox to an outbox; a passthrough link from an
inbox to another inbox; and a passthrough link from an outbox to another
outbox:

``` {.literal-block}
po = postoffice()
c0 = component()
c1 = component()
c2 = component()
c3 = component()

link1 = po.link((c1,"outbox"), (c2,"inbox"))
link2 = po.link((c2,"inbox"), (c3,"inbox"), passthrough=1)
link3 = po.link((c0,"outbox"), (c1,"outbox"), passthrough=2)
```

Removing one of the linkages; then all linkages involving component c3;
then all the rest:

``` {.literal-block}
po.unlink(thelinkage=link3)

po.unlink(thecomponent=c3)

po.unlinkAll()
```
:::

::: {.section}
[More detail]{#more-detail} {#9}
---------------------------

A postoffice object keeps creates and destroys objects and keeps a
record of which ones currently exist.

The linkage object returned when a linkage is created serves only as a
handle. It does not form any operation part of the linkage.

Multiple postoffices can (in fact, will) exist in an Axon system. Each
looks after its own collection of linkages. A linkage created at one
postoffice will *not* be known to other postoffice objects.
:::

Test documentation {#10}
==================

Tests passed:

-   All outboxes in a linkage chain sharing the same destination inbox
    will experience noSpaceInBox exceptions when and only when the
    destination inbox becomes full and any of them tries to send to it.
-   Restrict the size of an inbox to 5 and you can send 5 messages to it
    without error.
-   Send a 6th message to an inbox of size 5 and a noSpaceInBox
    exception will be thrown.
-   Setting a size limit of None mean the inbox size is unrestricted.
-   A size limited inbox that becomes the final destination in a linkage
    chain (because a link is broken) causes noSpaceInBox exceptions to
    be thrown as if it had always been the final destination.
-   A size limited inbox that isn\'t the final destination in a linkage
    chain will not cause noSpaceInBox exceptions to be thrown.
-   Setting a size limit then later changing it to None turns off inbox
    size restrictions.
-   Collecting 3 items from a full inbox and you can put 3 more in
    before a noSpaceInBox exception is thrown.
-   You can call mycomponent.inboxes\[boxname\].setSize(n) to set the
    box size.
-   Simple outox to inbox link, followed by an inbox to inbox
    passthrough, created in the opposite order
-   Outbox-\>Inbox-\>Inbox chain, then 2nd link (passthrough) is deleted
-   Simple outbox to inbox link, preceeded earlier by an outbox to
    outbox passthough
-   Simple outbox to inbox link
-   Simple outox to inbox link, followed by an inbox to inbox
    passthrough
-   Simple outbox to inbox link, preceeded later by an outbox to outbox
    passthough
-   test\_BoxAlreadyLinkedToDestinationException
    (\_\_main\_\_.postoffice\_Test)
-   postoffice can be instantiated with a debugger.
-   postoffice can be instantiated with no arguments. Defaults to no
    debugger or registered linkages.
-   \_\_str\_\_ - Checks the formatted string is of the correct format.
-   test\_componentlinksderegisters (\_\_main\_\_.postoffice\_Test)
-   test\_linkderegisters (\_\_main\_\_.postoffice\_Test)
-   test\_linkdisengages (\_\_main\_\_.postoffice\_Test)
-   test\_linkdisengages\_inboxinboxpassthrough
    (\_\_main\_\_.postoffice\_Test)
-   test\_linkdisengages\_outboxoutboxpassthrough
    (\_\_main\_\_.postoffice\_Test)
-   test\_linkestablishes (\_\_main\_\_.postoffice\_Test)
-   test\_linkestablishes\_inboxinboxpassthrough
    (\_\_main\_\_.postoffice\_Test)
-   test\_linkestablishes\_outboxoutboxpassthrough
    (\_\_main\_\_.postoffice\_Test)
-   test\_linkregistered (\_\_main\_\_.postoffice\_Test)
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Postoffice](/Docs/Axon/Axon.Postoffice.html){.reference}.[postoffice](/Docs/Axon/Axon.Postoffice.postoffice.html){.reference}
=======================================================================================================================================================================

::: {.section}
class postoffice(object) {#symbol-postoffice}
------------------------

::: {.section}
The post office looks after linkages between postboxes, thereby ensuring
deliveries along linkages occur as intended.

There is one post office per component.

A Postoffice can have a debug name - this is to help differentiate
between postoffices if problems arise.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, debugname\])]{#symbol-postoffice.__init__}

Constructor. If a debug name is assigned this will be stored as a
debugname attribute.
:::

::: {.section}
#### [\_\_str\_\_(self)]{#symbol-postoffice.__str__}

Provides a string representation of a postoffice, designed for debugging
:::

::: {.section}
#### [deregisterlinkage(self\[, thecomponent\]\[, thelinkage\])]{#symbol-postoffice.deregisterlinkage}

Stub for legacy
:::

::: {.section}
#### [islinkageregistered(self, linkage)]{#symbol-postoffice.islinkageregistered}

Returns a true value if the linkage given is registered with the
postoffie.
:::

::: {.section}
#### [link(self, source, sink, \*optionalargs, \*\*kwoptionalargs)]{#symbol-postoffice.link}

link((component,boxname),(component,boxname),\*\*otherargs) -\> new
linkage

Creates a linkage from a named box on one component to a named box on
another. See linkage class for meanings of other arguments. A linkage
object is returned as a handle representing the linkage created.

The linkage is registered with this postoffice.

Throws
[Axon.AxonExceptions.BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}
if the source is already linked to somewhere else (Axon does not permit
one-to-many).
:::

::: {.section}
#### [unlink(self\[, thecomponent\]\[, thelinkage\])]{#symbol-postoffice.unlink}

unlink(\[thecomponent\]\[,thelinkage\] -\> destroys linkage(s).

Destroys the specified linkage, or linkages for the specified component.

Note, it only destroys linkages registered in this postoffice.
:::

::: {.section}
#### [unlinkAll(self)]{#symbol-postoffice.unlinkAll}

Destroys all linkages made with this postoffice.
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

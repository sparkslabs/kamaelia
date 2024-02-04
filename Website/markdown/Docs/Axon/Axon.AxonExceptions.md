---
pagename: Docs/Axon/Axon.AxonExceptions
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}
----------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Axon Exceptions
===============

::: {.container}
-   **class
    [AccessToUndeclaredTrackedVariable](/Docs/Axon/Axon.AxonExceptions.AccessToUndeclaredTrackedVariable.html){.reference}**
-   **class
    [ArgumentsClash](/Docs/Axon/Axon.AxonExceptions.ArgumentsClash.html){.reference}**
-   **class
    [AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference}**
-   **class
    [BadComponent](/Docs/Axon/Axon.AxonExceptions.BadComponent.html){.reference}**
-   **class
    [BadInbox](/Docs/Axon/Axon.AxonExceptions.BadInbox.html){.reference}**
-   **class
    [BadParentTracker](/Docs/Axon/Axon.AxonExceptions.BadParentTracker.html){.reference}**
-   **class
    [BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}**
-   **class
    [MultipleServiceDeletion](/Docs/Axon/Axon.AxonExceptions.MultipleServiceDeletion.html){.reference}**
-   **class
    [NamespaceClash](/Docs/Axon/Axon.AxonExceptions.NamespaceClash.html){.reference}**
-   **class
    [ServiceAlreadyExists](/Docs/Axon/Axon.AxonExceptions.ServiceAlreadyExists.html){.reference}**
-   **class
    [invalidComponentInterface](/Docs/Axon/Axon.AxonExceptions.invalidComponentInterface.html){.reference}**
-   **class
    [noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}**
-   **class
    [normalShutdown](/Docs/Axon/Axon.AxonExceptions.normalShutdown.html){.reference}**
:::
:::

::: {.section}
AxonException is the base class for all axon exceptions defined here.
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[AccessToUndeclaredTrackedVariable](/Docs/Axon/Axon.AxonExceptions.AccessToUndeclaredTrackedVariable.html){.reference}
=================================================================================================================================================================================================================================

::: {.section}
class AccessToUndeclaredTrackedVariable(AxonException) {#symbol-AccessToUndeclaredTrackedVariable}
------------------------------------------------------

::: {.section}
Attempt to access a value being tracked by the coordinating assistant
tracker that isn\'t actually being tracked yet!

Arguments:

-   the name of the value that couldn\'t be accessed
-   the value that it was to be updated with (optional)

Possible causes:

-   Attempt to update or retrieve a value with a misspelt name?
-   Attempt to update or retrieve a value before it starts being
    tracked?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[ArgumentsClash](/Docs/Axon/Axon.AxonExceptions.ArgumentsClash.html){.reference}
===========================================================================================================================================================================================

::: {.section}
class ArgumentsClash(AxonException) {#symbol-ArgumentsClash}
-----------------------------------

::: {.section}
Supplied arguments clash with each other.

Possible causes:

-   meaning of arguments misunderstood? not allowed this given
    combination of arguments or values of arguments?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference}
=========================================================================================================================================================================================

::: {.section}
class AxonException(Exception) {#symbol-AxonException}
------------------------------

::: {.section}
Base class for axon exceptions.

Any arguments listed are placed in self.args
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*args)]{#symbol-AxonException.__init__}
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[BadComponent](/Docs/Axon/Axon.AxonExceptions.BadComponent.html){.reference}
=======================================================================================================================================================================================

::: {.section}
class BadComponent(AxonException) {#symbol-BadComponent}
---------------------------------

::: {.section}
The object provided does not appear to be a proper component.

Arguments:

-   the \'component\' in question

Possible causes:

-   Trying to register a service (component,boxname) with the
    coordinating assistant tracker supplying something that isn\'t a
    component?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[BadInbox](/Docs/Axon/Axon.AxonExceptions.BadInbox.html){.reference}
===============================================================================================================================================================================

::: {.section}
class BadInbox(AxonException) {#symbol-BadInbox}
-----------------------------

::: {.section}
The inbox named does not exist or is not a proper inbox.

Arguments:

-   the \'component\' in question
-   the inbox name in question

Possible causes:

-   Trying to register a service (component,boxname) with the
    coordinating assistant tracker supplying something that isn\'t a
    component?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[BadParentTracker](/Docs/Axon/Axon.AxonExceptions.BadParentTracker.html){.reference}
===============================================================================================================================================================================================

::: {.section}
class BadParentTracker(AxonException) {#symbol-BadParentTracker}
-------------------------------------

::: {.section}
Parent tracker is bad (not actually a tracker?)

Possible causes:

-   creating a coordinatingassistanttracker specifying a parent that is
    not also a coordinatingassistanttracker?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[BoxAlreadyLinkedToDestination](/Docs/Axon/Axon.AxonExceptions.BoxAlreadyLinkedToDestination.html){.reference}
=========================================================================================================================================================================================================================

::: {.section}
class BoxAlreadyLinkedToDestination(AxonException) {#symbol-BoxAlreadyLinkedToDestination}
--------------------------------------------------

::: {.section}
The inbox/outbox already has a linkage going *from* it to a destination.

Arguments:

-   the box that is already linked
-   the box that it is linked to
-   the box you were trying to link it to

Possible causes:

-   Are you trying to make a linkage going from an inbox/outbox to more
    than one destination?
-   perhaps another component has already made a linkage from that
    inbox/outbox?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[MultipleServiceDeletion](/Docs/Axon/Axon.AxonExceptions.MultipleServiceDeletion.html){.reference}
=============================================================================================================================================================================================================

::: {.section}
class MultipleServiceDeletion(AxonException) {#symbol-MultipleServiceDeletion}
--------------------------------------------

::: {.section}
Trying to delete a service that does not exist.

Possible causes:

-   Trying to delete a service (component,boxname) from the coordinating
    assistant tracker twice or more times?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[NamespaceClash](/Docs/Axon/Axon.AxonExceptions.NamespaceClash.html){.reference}
===========================================================================================================================================================================================

::: {.section}
class NamespaceClash(AxonException) {#symbol-NamespaceClash}
-----------------------------------

::: {.section}
Clash of names.

Possible causes:

-   two or more requests made to coordinating assistant tracker to track
    values under a given name (2nd request will clash with first)?
-   should have used updateValue() method to update a value being
    tracked by the coordinating assistant tracker?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[ServiceAlreadyExists](/Docs/Axon/Axon.AxonExceptions.ServiceAlreadyExists.html){.reference}
=======================================================================================================================================================================================================

::: {.section}
class ServiceAlreadyExists(AxonException) {#symbol-ServiceAlreadyExists}
-----------------------------------------

::: {.section}
A service already exists with the name you specifed.

Possible causes:

-   Two or more components are trying to register services with the
    coordinating assistant tracker using the same name?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[invalidComponentInterface](/Docs/Axon/Axon.AxonExceptions.invalidComponentInterface.html){.reference}
=================================================================================================================================================================================================================

::: {.section}
class invalidComponentInterface(AxonException) {#symbol-invalidComponentInterface}
----------------------------------------------

::: {.section}
Component does not have the required inboxes/outboxes.

Arguments:

-   *\"inboxes\"* or *\"outboxes\"* - indicating which is at fault
-   the component in question
-   (inboxes,outboxes) listing the expected interface

Possible causes:

-   [Axon.util.testInterface](/Docs/Axon/Axon.util.testInterface.html){.reference}()
    called with wrong interface/component specified?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
=======================================================================================================================================================================================

::: {.section}
class noSpaceInBox(AxonException) {#symbol-noSpaceInBox}
---------------------------------

::: {.section}
Destination inbox is full.

Possible causes:

-   The destination inbox is size limited?
-   It is a threaded component with too small a \'default queue size\'?
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[AxonExceptions](/Docs/Axon/Axon.AxonExceptions.html){.reference}.[normalShutdown](/Docs/Axon/Axon.AxonExceptions.normalShutdown.html){.reference}
===========================================================================================================================================================================================

::: {.section}
class normalShutdown(AxonException) {#symbol-normalShutdown}
-----------------------------------

::: {.section}
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference} :

-   [\_\_init\_\_](/Docs/Axon/Axon.AxonExceptions.html#symbol-AxonException.__init__){.reference}(self,
    \*args)
:::
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

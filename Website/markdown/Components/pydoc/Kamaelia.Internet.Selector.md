---
pagename: Components/pydoc/Kamaelia.Internet.Selector
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Selector](/Components/pydoc/Kamaelia.Internet.Selector.html){.reference}
==================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Selector](/Components/pydoc/Kamaelia.Internet.Selector.Selector.html){.reference}**
:::

-   [NOTIFICATION OF SOCKET AND FILE EVENTS](#115){.reference}
    -   [Example Usage](#116){.reference}
    -   [How does it work?](#117){.reference}
:::

::: {.section}
NOTIFICATION OF SOCKET AND FILE EVENTS {#115}
======================================

The Selector component listens for events on sockets and sends out
notifications. It is effectively a wrapper around the unix \'select\'
statement. Components request that the Selector component notify them
when a supplied socket or file object is ready.

The selectorComponent is a service that registers with the Coordinating
Assistant Tracker (CAT).

NOTE: The behaviour and API of this component changed in Kamaelia 0.4
and is likely to change again in the near future.

::: {.section}
[Example Usage]{#example-usage} {#116}
-------------------------------

See the source code for TCPClient for an example of how the Selector
component can be used.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#117}
--------------------------------------

Selector is a service. Obtain it by calling the static method
Selector.getSelectorService(\...). Any existing instance will be
returned, otherwise a new one is automatically created.

This component ignores anything sent to its \"inbox\" and \"control\"
inboxes. This component does not terminate.

Register socket or file objects with the selector, to receive a one-shot
notification when that file descriptor is ready. The file descriptor can
be a python file object or socket object. The notification is one-shot -
meaning you must resubmit your request every time you wish to receive a
notification.

Ensure you deregister the file object when closing the file/socket. You
may do this even if you have already received the notification. The
Selector component will be unable to handle notifications for any other
descriptors if it still has a registered descriptor that has closed.

Register for a notification by sending an one of the following messages
to the \"notify\" inbox, as returned by Selector.getSelectorService():

-   Kamaelia.KamaeliaIpc.newReader(caller, (component,inboxname),
    descriptor)
-   Kamaelia.KamaeliaIpc.newWriter(caller, (component,inboxname),
    descriptor)
-   Kamaelia.KamaeliaIpc.newExceptional(caller, (component,inboxname),
    descriptor)

Choose which as appropriate:

-   a newReader() request will notify when there is data ready to be
    read on the descriptor
-   a newWriter() request will notify when writing to the descriptor
    will not block.
-   a newExceptional() request will notify when an exceptional event
    occurs on the specified descriptor.

Selector will notify the taret component by sending the file/socket
descriptor object to the target inbox the component provided. It then
automatically deregisters the descriptor, unlinking from the target
component\'s inbox.

For a given descriptor for a given type of event
(read/write/exceptional) only one notification will be sent when the
event occurs. If multiple notification requests have been received, only
the first is listened to; all others are ignored.

Of course, once the notification as happened, or someone has requested
that descriptor be deregistered, then someone can register for it once
again.

Deregister by sending on of the following messages to the \"notify\"
inbox of Selector:

-   Kamaelia.KamaeliaIpc.removeReader(caller, descriptor)
-   Kamaelia.KamaeliaIpc.removeWriter(caller, descriptor)
-   Kamaelia.KamaeliaIpc.removeExceptional(caller, descriptor)

It is advisable to send a deregister message when the corresponding file
descriptor closes, in case you registered for a notification, but it has
not occurred.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Selector](/Components/pydoc/Kamaelia.Internet.Selector.html){.reference}.[Selector](/Components/pydoc/Kamaelia.Internet.Selector.Selector.html){.reference}
=====================================================================================================================================================================================================================================================================================

::: {.section}
class Selector([Axon.ThreadedComponent.threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}) {#symbol-Selector}
----------------------------------------------------------------------------------------------------------------------------------------------------------

Selector() -\> new Selector component

Use Selector.getSelectorService(\...) in preference as it returns an
existing instance, or automatically creates a new one.

::: {.section}
### [Inboxes]{#symbol-Selector.Inboxes}

-   **control** : Recieving a
    [Axon.Ipc.shutdown](/Docs/Axon/Axon.Ipc.shutdown.html){.reference}()
    message here causes shutdown
-   **inbox** : Not used at present
-   **notify** : Used to be notified about things to select
:::

::: {.section}
### [Outboxes]{#symbol-Selector.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self)]{#symbol-Selector.__init__}
:::

::: {.section}
#### [addLinks(self, replyService, selectable, meta, selectables, boxBase)]{#symbol-Selector.addLinks}

Adds a file descriptor (selectable).

Creates a corresponding outbox, with name based on boxBase; links it to
the component that wants to be notified; adds the file descriptor to the
set of selectables; and records the box and linkage info in meta.
:::

::: {.section}
#### [handleNotify(self, meta, readers, writers, exceptionals)]{#symbol-Selector.handleNotify}

Process requests to add and remove file descriptors (selectables) that
arrive at the \"notify\" inbox.
:::

::: {.section}
#### [main(self)]{#symbol-Selector.main}

Main loop
:::

::: {.section}
#### [removeLinks(self, selectable, meta, selectables)]{#symbol-Selector.removeLinks}

Removes a file descriptor (selectable).

Removes the corresponding entry from meta and selectables; unlinks from
the component to be notified; and deletes the corresponding outbox.
:::

::: {.section}
#### [stop(self)]{#symbol-Selector.stop}
:::

::: {.section}
#### [trackedBy(self, tracker)]{#symbol-Selector.trackedBy}
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

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*

---
pagename: Docs/Axon/Axon.Ipc
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}
------------------------------------------------------------------------------------
:::
:::

::: {.section}
IPC message classes
===================

::: {.container}
-   **class
    [WaitComplete](/Docs/Axon/Axon.Ipc.WaitComplete.html){.reference}**
-   **class
    [errorInformation](/Docs/Axon/Axon.Ipc.errorInformation.html){.reference}**
-   **class [ipc](/Docs/Axon/Axon.Ipc.ipc.html){.reference}**
-   **class
    [newComponent](/Docs/Axon/Axon.Ipc.newComponent.html){.reference}**
-   **class [notify](/Docs/Axon/Axon.Ipc.notify.html){.reference}**
-   **class
    [producerFinished](/Docs/Axon/Axon.Ipc.producerFinished.html){.reference}**
-   **class
    [reactivate](/Docs/Axon/Axon.Ipc.reactivate.html){.reference}**
-   **class [shutdown](/Docs/Axon/Axon.Ipc.shutdown.html){.reference}**
-   **class
    [shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}**
-   **class [status](/Docs/Axon/Axon.Ipc.status.html){.reference}**
-   **class
    [wouldblock](/Docs/Axon/Axon.Ipc.wouldblock.html){.reference}**
:::

-   [Shutting down components](#65){.reference}
-   [Knock-on shutdowns between microprocesses](#66){.reference}
-   [shutdown vs shutdownMicroprocess](#67){.reference}
-   [Setting off a new microprocess and waiting for it to
    complete](#68){.reference}
-   [Test documentation](#69){.reference}
:::

::: {.section}
Some standard IPC messages used by Axon. The base class for all IPC
classes is ipc.

Some purposes for which these can be used are described below. This is
not exhaustive and does *not* cover all of the Ipc classes defined here!

::: {.section}
[Shutting down components]{#shutting-down-components} {#65}
-----------------------------------------------------

-   [Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}
-   [Axon.Ipc.producerFinished](/Docs/Axon/Axon.Ipc.producerFinished.html){.reference}

If you want to order a component to stop, most will do so if you send
either of these ipc objects to their \"control\" inbox. When a component
does stop, most send on the same message they received out of their
\"signal\" outbox (or a message of their own creation if they decided to
shutdown without external prompting)

Producer components, such as file readers or network connections will
send a producerFinished() ipc object rather than shutdownMicroprocess()
to indicate that the shutdown is due to them finishing producing data.

You can therefore link up components in a chain - linking \"signal\"
outboxes to \"control\" inboxes to allow shutdown messages to cascade -
making it easier to shutdown and clean up a system.

How should components behave when they receive either of these Ipc
messages? In most cases, components simply shut down as soon as possible
and send the same message on out of their \"signal\" outbox. However
many components behave slightly more subtley to ensure the last few
items of data passing throuhg a chain of components are not accidentally
lost:

-   If the message is a producerFinished() message, then a component may
    wish to finish processing any data still left in its inboxes or
    internal buffers before terminating and passing on the
    producerFinished() message.
-   If the message is a shutdownMicroprocess() message, then a component
    should ideally try to terminate rather than finish what it is doing.

Many components therefore containg logic similar to this:

``` {.literal-block}
class MyComponent(Axon.Component.component):

    def main(self):

        while still got things to do and not received "shutdownMicroprocess":
            ..do things..
            ..check "control" inbox..
            yield 1

        if not received any shutdown message:
            self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
        else:
            self.send(message received, "signal")
```

producerFinished() can be likened to notification of a clean shutdown -
rather like a unix process closing its stdout file handle when it
finishes. shutdownMicroproces() is more like a hard termination due to a
system being interrupted.
:::

::: {.section}
[Knock-on shutdowns between microprocesses]{#knock-on-shutdowns-between-microprocesses} {#66}
---------------------------------------------------------------------------------------

-   [Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}

When a microprocess terminates, the scheduler calls its
[Axon.Microprocess.microprocess.\_closeDownMicroprocess](/Docs/Axon/Axon.Microprocess.microprocess._closeDownMicroprocess.html){.reference}()
method. This method can return an
[Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}
ipc object, for example:

``` {.literal-block}
def _closeDownMicroprocess(self):
    return Axon.Ipc.shutdownMicroprocess(anotherMicroprocess)
```

The scheduler will ensure that other microprocess is also shut down.
:::

::: {.section}
[shutdown vs shutdownMicroprocess]{#shutdown-vs-shutdownmicroprocess} {#67}
---------------------------------------------------------------------

-   [Axon.Ipc.shutdown](/Docs/Axon/Axon.Ipc.shutdown.html){.reference}
-   [Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}

You may notice that shutdownMicroprocess appears to be used for two
purposes - knock-on shutdowns and signalling component shutdown.

[Axon.Ipc.shutdown](/Docs/Axon/Axon.Ipc.shutdown.html){.reference} was
originally intended to be used rather than
[Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference};
however because most components support the latter (which was an
accidental mistake) the latter should continue to be used.

Axon may at some stage make these two Ipc classes synonyms for each
other to resolve this issue, but this decision has not been taken yet.
:::

::: {.section}
[Setting off a new microprocess and waiting for it to complete]{#setting-off-a-new-microprocess-and-waiting-for-it-to-complete} {#68}
-------------------------------------------------------------------------------------------------------------------------------

-   [Axon.Ipc.WaitComplete](/Docs/Axon/Axon.Ipc.WaitComplete.html){.reference}
-   [Axon.Ipc.reactivate](/Docs/Axon/Axon.Ipc.reactivate.html){.reference}

Used by:

-   components / microprocesses
-   [Axon.Scheduler.scheduler](/Docs/Axon/Axon.Scheduler.scheduler.html){.reference}

A microprocess can yield a WaitComplete() Ipc message to the scheduler
to ask for another microprocess to be started. When that second
microprocess completes, the original one resumes - it waits until the
second one completes.

This is a nice little way to sidestep the restriction in python that you
can\'t nest yield statements for a given generator inside
methods/functions it calls.

For example, here\'s a clean way to wait for data arriving at the
\"inbox\" inbox of a component:

``` {.literal-block}
class MyComponent(Axon.Component.component):

    def main(self):
        ...
        yield WaitComplete(self.waitForInbox())
        msg = self.recv("inbox")

    def waitForInbox(self):
        while not self.dataReady("inbox"):
            yield 1
```

Internally, the scheduler uses
[Axon.Ipc.reactivate](/Docs/Axon/Axon.Ipc.reactivate.html){.reference}
to ensure the original microprocess is resumed after the one that was
launched terminates.
:::

Test documentation {#69}
==================

Tests passed:

-   errorInformation.\_\_init\_\_ - Takes the supplied caller, and
    creates an errorInformation object. Checks errorInformation object
    is an instance of ipc.
-   errorInformation.\_\_init\_\_ - An exception & message (any object)
    in addition to the caller to provide a more meaningful
    errorInformation message where appropriate. ttbw
-   errorInformation.\_\_init\_\_ - Called without arguments fails -
    must include caller.
-   ipc - Should be derived from object.
-   newComponent.\_\_init\_\_ - Groups all the arguments as a tuple of
    components that need to be activated/added to the run queue. Order
    is unimportant, scheduler doesn\'t care.
-   newComponent.\_\_init\_\_ - Should work without problems.
-   newComponent.components - Returns a tuple of components that need to
    be added to the run queue/activated. Same test as for \_\_init\_\_
    as they are counterparts.
-   notify.\_\_init\_\_ - Creates a message from a specific caller with
    some data payload to notify part of the system of an event.
-   notify.\_\_init\_\_ - Called without arguments fails.
-   test\_SmokeTest.\_\_init\_\_ - Creates a producerFinished message
    with specified caller & shutdown \'last\' message.
-   producerFinished.\_\_init\_\_ - Called without arguments defaults to
    a caller of None, message of None. Checks producerFinished is a
    subclass of ipc
-   shutdownMicroprocess.\_\_init\_\_ - Treats all the arguments as a
    tuple of microprocesses that need to be shutdown.
-   shutdownMicroprocess.\_\_init\_\_ - Should work without problems.
-   shutdownMicroprocess.microprocesses- Returns the list of
    microprocesses that need to be shutdown. This is essentially the
    counterpart to the \_\_init\_\_ test.
-   status.\_\_init\_\_ - Stores the status message - for extraction by
    the recipient of the message. Checks object is instance of ipc.
-   status.\_\_init\_\_ - Called without arguments fails.
-   status.status - Returns the status message stored inside the status
    object. Counterpart to \_\_init\_\_ test.
-   wouldblock.\_\_init\_\_ - Stores the caller in the wouldblock
    message. Allows the scheduler to make a decision. Checks wouldblock
    is a subclass of ipc.
-   wouldblock.\_\_init\_\_ - Called without arguments fails.
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[WaitComplete](/Docs/Axon/Axon.Ipc.WaitComplete.html){.reference}
======================================================================================================================================================

::: {.section}
class WaitComplete(ipc) {#symbol-WaitComplete}
-----------------------

::: {.section}
WaitComplete(generator) -\> new WaitComplete object.

Message to ask the scheduler to temporarily suspect this microprocess
and run a new one instead based on the generator provided; resuming the
original when the new one completes.

Use within a microprocess by yielding one back to the scheduler.

Arguments:

-   the generator to be run as the separate microprocess
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*args, \*\*argd)]{#symbol-WaitComplete.__init__}
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[errorInformation](/Docs/Axon/Axon.Ipc.errorInformation.html){.reference}
==============================================================================================================================================================

::: {.section}
class errorInformation(ipc) {#symbol-errorInformation}
---------------------------

::: {.section}
errorInformation(caller\[,exception\]\[,message\]) -\> new
errorInformation ipc message.

A message to indicate that a non fatal error has occured in the
component. It may skip processing errored data but should respond
correctly to future messages.

Keyword arguments:

-   caller \-- the source of the error information. Assigned to
    self.caller
-   exception \-- Optional. None, or the exception that caused the
    error. Assigned to self.exception
-   message \-- Optional. None, or a message describing the problem.
    Assigned to self.message
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, caller\[, exception\]\[, message\])]{#symbol-errorInformation.__init__}
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[ipc](/Docs/Axon/Axon.Ipc.ipc.html){.reference}
====================================================================================================================================

::: {.section}
class ipc(object) {#symbol-ipc}
-----------------

::: {.section}
Message base class
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[newComponent](/Docs/Axon/Axon.Ipc.newComponent.html){.reference}
======================================================================================================================================================

::: {.section}
class newComponent(ipc) {#symbol-newComponent}
-----------------------

::: {.section}
newComponent(\*components) -\> new newComponent ipc message.

Message used to inform the scheduler of a new component that needs a
thread of control and activating.

Use within a microprocess by yielding one back to the scheduler.

Arguments:

-   the components to be activated
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*components)]{#symbol-newComponent.__init__}
:::

::: {.section}
#### [components(self)]{#symbol-newComponent.components}

Returns the list of components to be activated
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[notify](/Docs/Axon/Axon.Ipc.notify.html){.reference}
==========================================================================================================================================

::: {.section}
class notify(ipc) {#symbol-notify}
-----------------

::: {.section}
notify(caller,payload) -\> new notify ipc message.

Message used to notify the system of an event. Subclass to implement
your own specific notification messages.

Keyword arguments:

-   caller \-- a reference to whoever/whatever issued this notification.
    Assigned to self.caller
-   payload \-- any relevant payload relating to the notification.
    Assigned to self.object
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, caller, payload)]{#symbol-notify.__init__}
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[producerFinished](/Docs/Axon/Axon.Ipc.producerFinished.html){.reference}
==============================================================================================================================================================

::: {.section}
class producerFinished(ipc) {#symbol-producerFinished}
---------------------------

::: {.section}
producerFinished(\[caller\]\[,message\]) -\> new producerFinished ipc
message.

Message to indicate that the producer has completed its work and will
produce no more output. The receiver may wish to shutdown.

Keyword arguments:

-   caller \-- Optional. None, or the producer who has finished.
    Assigned to self.caller
-   message \-- Optional. None, or a message giving any relevant info.
    Assigned to self.message
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, caller\]\[, message\])]{#symbol-producerFinished.__init__}
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[reactivate](/Docs/Axon/Axon.Ipc.reactivate.html){.reference}
==================================================================================================================================================

::: {.section}
class reactivate(ipc) {#symbol-reactivate}
---------------------

::: {.section}
reactivate(original) -\> new reactivate ipc message.

Returned by
[Axon.Microprocess.microprocess.\_closeDownMicroprocess](/Docs/Axon/Axon.Microprocess.microprocess._closeDownMicroprocess.html){.reference}()
to the scheduler to get another microprocess reactivated.

Keyword arguments:

-   original \-- The original microprocess to be resumed. Assigned to
    self.original
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, original)]{#symbol-reactivate.__init__}
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[shutdown](/Docs/Axon/Axon.Ipc.shutdown.html){.reference}
==============================================================================================================================================

::: {.section}
class shutdown(ipc) {#symbol-shutdown}
-------------------

::: {.section}
Message used to indicate that the component recieving it should
shutdown.

Due to legacy mistakes, use shutdownMicroprocess instead.
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}
======================================================================================================================================================================

::: {.section}
class shutdownMicroprocess(ipc) {#symbol-shutdownMicroprocess}
-------------------------------

::: {.section}
shutdownMicroprocess(\*microprocesses) -\> new shutdownMicroprocess ipc
message.

Message used to indicate that the component recieving it should
shutdown. Or to indicate to the scheduler a shutdown knockon from a
terminating microprocess.

Arguments:

-   the microprocesses to be shut down (when used as a knockon)
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*microprocesses)]{#symbol-shutdownMicroprocess.__init__}
:::

::: {.section}
#### [microprocesses(self)]{#symbol-shutdownMicroprocess.microprocesses}

Returns the list of microprocesses to be shut down
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[status](/Docs/Axon/Axon.Ipc.status.html){.reference}
==========================================================================================================================================

::: {.section}
class status(ipc) {#symbol-status}
-----------------

::: {.section}
status(status) -\> new status ipc message.

General Status message.

Keyword arguments:

-   status \-- the status.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, status)]{#symbol-status.__init__}
:::

::: {.section}
#### [status(self)]{#symbol-status.status}

Returns what the status is
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[wouldblock](/Docs/Axon/Axon.Ipc.wouldblock.html){.reference}
==================================================================================================================================================

::: {.section}
class wouldblock(ipc) {#symbol-wouldblock}
---------------------

::: {.section}
wouldblock(caller) -\> new wouldblock ipc message.

Message used to indicate to the scheduler that the system is likely to
block now.

Keyword arguments:

-   caller \-- who it is who is likely to block (presumably a
    microprocess). Assigned to self.caller
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, caller)]{#symbol-wouldblock.__init__}
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

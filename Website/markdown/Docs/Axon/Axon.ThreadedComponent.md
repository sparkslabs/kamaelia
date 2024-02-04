---
pagename: Docs/Axon/Axon.ThreadedComponent
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[ThreadedComponent](/Docs/Axon/Axon.ThreadedComponent.html){.reference}
----------------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Thread based components
=======================

::: {.container}
-   **class
    [threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}**
-   **class
    [threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}**
:::

-   [Just like writing an ordinary component](#75){.reference}
-   [What can a threaded component do?](#76){.reference}
-   [Inbox and Outbox queues](#77){.reference}
-   [Regulating speed](#78){.reference}
-   [Stopping a threaded component](#79){.reference}
-   [When the thread terminates\...](#80){.reference}
-   [How is threaded component implemented?](#81){.reference}
-   [Test documentation](#82){.reference}
:::

::: {.section}
A threaded component is like an ordinary component but where the main()
method is an ordinary method that is run inside its own thread.
(Normally main() is a generator that is given slices of execution time
by the scheduler).

This is really useful if your code needs to block - eg. wait on a system
call, or if it is better off being able to run on another CPU (though
beware python\'s limited ability to scale across multiple CPUs).

If you don\'t need these capabilities, consider making your component an
ordinary
[Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}
instead.

-   threadedcomponent - like an ordinary
    [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference},
    but runs in its own thread
-   threadedadaptivecommscomponent - a threaded version of
    [Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}

::: {.section}
[Just like writing an ordinary component]{#just-like-writing-an-ordinary-component} {#75}
-----------------------------------------------------------------------------------

This is nearly identical to writing an ordinary
[Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}.
For example this ordinary component:

``` {.literal-block}
class MyComponent(Axon.Component.component):

    Inboxes = { "inbox"   : "Send the FOO objects to here",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Emits BAA objects from here",
                 "signal" : "NOT USED",
               }

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                result = ... do something to msg ...
                self.send(result, "outbox")

            yield 1
```

Can be trivially written as a threaded component simply by removing the
`yield`{.docutils .literal} statements, turning main() into a normal
method:

``` {.literal-block}
class MyComponent(Axon.ThreadedComponent.threadedcomponent):

    Inboxes = { "inbox"   : "Send the FOO objects to here",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Emits BAA objects from here",
                 "signal" : "NOT USED",
               }

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                result = ... do something to msg ...
                self.send(result, "outbox")
```
:::

::: {.section}
[What can a threaded component do?]{#what-can-a-threaded-component-do} {#76}
----------------------------------------------------------------------

Exactly the same things any other component can. The following method
calls are all implemented in a thread safe manner and function exactly
as you should expect:

-   self.link()
-   self.unlink()
-   self.dataReady()
-   self.anyReady()
-   self.recv()
-   self.send()

*self.pause()* behaves slightly differently:

-   calling self.pause() pauses immediately - not at the next yield
    statement (since there are no yield statements!)
-   self.pause() has an extra optional \'timeout\' argument to allow you
    to write timer code that can be interrupted, for example, by
    incoming messages.

In addition, threadedadaptivecommscomponent also supports the extra
methods in
[Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}:

-   self.addInbox()
-   self.deleteInbox()
-   self.addOutbox()
-   self.deleteOutbox()
-   *etc..*
:::

::: {.section}
[Inbox and Outbox queues]{#inbox-and-outbox-queues} {#77}
---------------------------------------------------

There is one difference: because the main() method runs in a different
thread it does not actually interact directly with its own inboxes and
outboxes. Internal queues are used to get data between your thread and
the component\'s actual inboxes and outboxes. This is hidden for the
most part - the method calls you make to receive and send messages are
exactly the same.

When initialising a threadedcomponent you may wish to specify the size
limit (queue length) for these queues. There is a size limit so that if
your threaded component is delivering to a size limited inbox, the
effects of the inbox becoming full propagate back to your thread.

In some ways this is a bit like nesting one component within another -
where all the parent component\'s inboxes and outboxes are forwarded to
the child:

``` {.literal-block}
  +-----------------------------------------+
  |           threaded component            |
  |                                         |
  |              +----------+               |
  |              |  main()  |               |
INBOX -------> inbox      outbox -------> OUTBOX
  |    queue     |          |     queue     |
  |              +----------+               |
  +-----------------------------------------+
```

What does this mean in practice?

-   *More messages get buffered*. - Suppose your threaded component has
    an internal queues of size 5 and is delivering messages to an inbox
    on another component with a size limit of 10. From the perspective
    of your threaded component you will actually be able to send 15
    messages before you might start to get
    [Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
    exceptions.
-   *Threaded components that output lots of messages might see
    unexpected \'box full\' exceptions* - Suppose your threaded
    component has a small internal queue size but produces lots of
    messages very quickly. The rest of the system may not be able to
    pick up those messages quickly enough to put them into the
    destination inbox. So even though the destination might not have a
    size limit you may still get these exceptions.

The secret is to choose a sensible queue size to balance between it
being able to buffer enough messages without generating errors whilst
not being so large as to render a size limited inbox pointless!
:::

::: {.section}
[Regulating speed]{#regulating-speed} {#78}
-------------------------------------

In addition to being able to pause (with an optional timeout), a
threaded component can also regulate its speed by briefly synchronising
with the rest of the system. Calling the sync() method simply briefly
blocks until the rest of the system can acknowledge.
:::

::: {.section}
[Stopping a threaded component]{#stopping-a-threaded-component} {#79}
---------------------------------------------------------------

Note that it is *not* safe to forcibly stop a threaded component (by
calling the stop() method before the microprocess in it has terminated).
This is because there is no true support in python for killing a thread.

Calling stop() prematurely will therefore kill the internal microprocess
that handles inbox/outbox traffic on behalf of the thread, resulting in
undefined behaviour.
:::

::: {.section}
[When the thread terminates\...]{#when-the-thread-terminates} {#80}
-------------------------------------------------------------

threadedcomponent will terminate - as you would expect. However, there
are some subtleties that may need to be considered. These are due to the
existence of the intermediate queues used to communicate between the
thread and the actual inboxes and outboxes (as described above).

-   When main() terminates, even if it has just recently checked its
    inqueues (inboxes) there might still be items of data at the
    inboxes. This is because there is a gap between data that arriving
    at an inbox, and it being forwarded into an inqueue going to the
    thread.
-   When main() terminates, threadedcomponent will keep executing until
    it has finished successfully sending any data in outqueues, out of
    the respective \"outboxes\". This means that anything main() thinks
    it has sent is guaranteed to be sent. But if the destination is a
    size limited inbox that has become full (and that never gets
    emptied), then threadedcomponent will indefinitely stall because it
    cannot finish sending.
:::

::: {.section}
[How is threaded component implemented?]{#how-is-threaded-component-implemented} {#81}
--------------------------------------------------------------------------------

threadedcomponet subclasses Axon.Components.component. It overrides the
activate() method, to force activation to use a method called
\_localmain() instead of the usual main(). The code that someone writes
for their main() method is instead run in a separate thread.

The code running in main() does not directly access inboxes our outboxes
and doesn\'t actually create or destroy linkages itself. \_localmain()
can be thought of as a kind of proxy for the thread - acting on its
behalf within the main scheduler run thread.

main() is wrapped by \_threadmain() which tries to trap any unhandled
exceptions generated in the thread and pass them back to \_localmain()
to be rethrown.

Internal state:

-   **\_threadrunning** - flag, cleared by the thread when it terminates
-   **queuelengths** - size to be used for internal queues between
    thread and inboxes and outboxes
-   **\_threadmainmethod** - the main method to be run as a thread
-   **\_thethread** - the thread object itself

Internal to \_localmain():

-   **running** - flag tracking if the thread is still runnning
-   **stuffWaiting** - flag tracking if there is are things that need to
    be done (if there is stuff waiting then \_localmain() should not
    pause or terminate until it finishes)

Communication between the thread and \_localmain():

-   **inqueues** - dictionary of thread safe queues for getting data
    from inboxes to the thread
-   **outqueues** - dictionary of thread safe queues for getting data
    from the thread to outboxes
-   **threadtoaxonqueue** - thread safe queue for making requests to
    \_localmain()
-   **axontothreadqueue** - thread safe queue for replies from
    \_localmain()
-   **threadWakeUp** - thread safe event flag for waking up the thread
    if sleeping
-   **\_threadId** - unique id that is given to the thread as its
    \'name\'
-   **\_localThreadId** - the thread id (name) of the thread
    \_localmain() and the scheduler run in

The relationship between \_localmain() and the main() method (running in
a separate thread) looks like this:

``` {.literal-block}
   +---------------------------------------------------------------------+
   |                         threaded component                          |
   |                                                                     |
   |           +--------------------------------------------+            |
   |           |                _localmain()                |            |
 INBOX ------> |                                            | -------> OUTBOX
   |           |    Ordinary generator based microprocess   |            |
CONTROL -----> |       in same thread as rest of system     | -------> SIGNAL
   |           |                                            |            |
   |           +--------------------------------------------+            |
   |              |          ^               ^            |              |
   |              |          |               |            |              |
   |          inqueues   outqueues   threadtoaxonqueue    |              |
   |           "inbox"    "outbox"           |            |              |
   |          "control"   "signal"           |    axontothreadqueue      |
   |              |          |               |            |              |
   |              V          |               |            V              |
   |           +--------------------------------------------+            |
   |           |                   main()                   |            |
   |           |                                            |            |
   |           |        Runs in a separate thread           |            |
   |           +--------------------------------------------+            |
   |                                                                     |
   +---------------------------------------------------------------------+
```

When a message arrives at an inbox, \_localmain() collects it and places
it into the thread safe queue self.inqueues\[boxname\] from which the
thread can collect it. self.dataReady() and self.recv() are both
overridden so they access the queues instead of the normal inboxes.

Similarly, when the thread wants to send to an outbox; self.send() is
overridden so that it is actually sent to a thread safe queue
self.outqueues\[boxname\] from which \_localmain() collects it and sends
it on.

Because all queues have a size limit (specified in at initialisation of
the threaded component) this enables the effects of size limited inboxes
to propagate up to the separate thread, via the queue. The
implementation of self.send() is designed to mimic the behaviour

For other methods such as link(), unlink() and (in the case of
threadedadaptivecommscomponent) addInbox(), deleteInbox(), addOutbox()
and deleteOutbox(), the \_localmain() microprocess also acts on the
thread\'s behalf. The request to do something is sent to \_localmain()
through the thread safe queue self.threadtoaxonqueue. When the operation
is complete, an acknowledgement is sent back via another queue
self.axontothreadqueue:

``` {.literal-block}
_localmain()                         main() [thread]
     |                                 |
     |       please call 'link()'      |
     | ------------------------------> |
     |                                 |
     |                         self.link() called
     |                                 |
     |      return value from call     |
     | <------------------------------ |
     |                                 |
```

The thread does not continue until it receives the acknowledgement -
this is to prevent inconsistencies in state. For example, a call to
create an inbox might be followed by a query to determine whether there
is data in it - the inbox therefore must be fully set up before that
query can be handled.

This is implemented by the \_do\_threadsafe() method. This method
detects whether it is being called from the same thread as the scheduler
(by comparing thread IDs). If it is not the same thread, then it puts a
request into self.threadtoaxonqueue and blocks on self.axontothreadqueue
waiting for a reply. The request is simply a tuple of a method or object
to call and the associated arguments. When \_localmain() collects the
request it issues the call and responds with the return value.

self.pause() is overridden and equivalent functionality reimplemented by
blocking the thread on a threading.Event() object which can be signalled
by \_localmain() whenever the thread ought to wake up.

The \'Adaptive\' version does *not* ensure the resource tracking and
retrieval methods thread safe. This is because it is assumed these will
only be accessed internally by the component itself from within its
separate thread. \_localmain() does not touch these resources.

XXX *TODO*: Thread shutdown - no true support for killing threads in python
:   (if ever). stop() method therefore doesn\'t stop the thread. Only
    stops the internal \_localmain() microprocess, which therefore cuts
    the thread off from communicating with the rest of the system.
:::

Test documentation {#82}
==================

Tests passed:

-   addInbox - adds a new inbox with the specified name. Component can
    then receive from that inbox.
-   addOutbox - adds a new outbox with the specified name. Component can
    then send to that inbox.
-   \_\_init\_\_ - can accept no arguments
-   \_\_init\_\_ - class constructor is called with no arguments.
-   \_\_init\_\_ - accepts one argument
-   Setting the queue size in the initializer limits the number of
    messages that can queue up waiting to be sent out by the main
    thread.
-   If a threadedcomponent outbox is linked to a size restricted inbox,
    then the thread can send at most inbox\_size+internal\_queue\_size
    messages before it receives a noSpaceInBox exception.
-   Setting the inbox size means at most
    inbox\_size+internal\_queue\_size messages can queue up before the
    sender receives a noSpaceInBox exception
-   test\_TakingFromDestinationAllowsMoreToBeDelivered
    (\_\_main\_\_.threadedcomponent\_Test)
-   There is a default limit on the number of messages that can queue up
    waiting to be sent out by the main thread.
-   main() - can receive data sent to the component\'s inbox(es) using
    the standard dataReady() and recv() methods.
-   main() - can send data to the component\'s outbox(es) using the
    standard send() method.
-   link() unlink() - thread safe when called. The postoffice link() and
    unlink() methods are not expected to be capable of re-entrant use.
-   \_localmain() microprocess also terminates when the thread
    terminates
-   threadedcomponent ensures that if the thread terminates, any
    messages still pending in outqueues (waiting to be sent out of
    outboxes) get sent, even if it is held up for a while by
    noSpaceInBox exceptions
-   threadedcomponent terminates when the thread terminates, even if
    data is clogged in one of the inqueues
-   \_\_init\_\_ - can accept no arguments
-   \_\_init\_\_ - class constructor is called with no arguments.
-   \_\_init\_\_ - accepts one argument
-   main() -runs in a separate thread of execution
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[ThreadedComponent](/Docs/Axon/Axon.ThreadedComponent.html){.reference}.[threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}
====================================================================================================================================================================================================================================

::: {.section}
class threadedadaptivecommscomponent(threadedcomponent, [Axon.AdaptiveCommsComponent.\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference}) {#symbol-threadedadaptivecommscomponent}
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

::: {.section}
threadedadaptivecommscomponent(\[queuelengths\]) -\> new
threadedadaptivecommscomponent

Base class for a version of an Axon adaptivecommscomponent that runs
main() in a separate thread (meaning it can, for example, block).

Subclass to make your own.

Internal queues buffer data between the thread and the Axon inboxes and
outboxes of the component. Set the default queue length at
initialisation (default=1000).

Like an adaptivecommscomponent, inboxes and outboxes can be added and
deleted at runtime.

A simple example:

``` {.literal-block}
class IncrementByN(Axon.ThreadedComponent.threadedcomponent):

    Inboxes = { "inbox" : "Send numbers here",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Incremented numbers come out here",
                "signal" : "NOT USED",
               }

    def __init__(self, N):
        super(IncrementByN,self).__init__()
        self.n = N

    def main(self):
        while 1:
            while self.dataReady("inbox"):
                value = self.recv("inbox")
                value = value + self.n
                self.send(value,"outbox")

            if not self.anyReady():
                self.pause()
```
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*argL, \*\*argD)]{#symbol-threadedadaptivecommscomponent.__init__}
:::

::: {.section}
#### [\_unsafe\_addInbox(self, \*args)]{#symbol-threadedadaptivecommscomponent._unsafe_addInbox}

Internal thread-unsafe code for adding an inbox.
:::

::: {.section}
#### [\_unsafe\_addOutbox(self, \*args)]{#symbol-threadedadaptivecommscomponent._unsafe_addOutbox}
:::

::: {.section}
#### [\_unsafe\_deleteInbox(self, name)]{#symbol-threadedadaptivecommscomponent._unsafe_deleteInbox}
:::

::: {.section}
#### [\_unsafe\_deleteOutbox(self, name)]{#symbol-threadedadaptivecommscomponent._unsafe_deleteOutbox}
:::

::: {.section}
#### [addInbox(self, \*args)]{#symbol-threadedadaptivecommscomponent.addInbox}

Allocates a new inbox with name *based on* the name provided. If a box
with the suggested name already exists then a variant is used instead.

Returns the name of the inbox added.
:::

::: {.section}
#### [addOutbox(self, \*args)]{#symbol-threadedadaptivecommscomponent.addOutbox}

Allocates a new outbox with name *based on* the name provided. If a box
with the suggested name already exists then a variant is used instead.

Returns the name of the outbox added.
:::

::: {.section}
#### [deleteInbox(self, name)]{#symbol-threadedadaptivecommscomponent.deleteInbox}

Deletes the named inbox. Any messages in it are lost.

Try to ensure any linkages to involving this outbox have been destroyed
- not just ones created by this component, but by others too! Behaviour
is undefined if this is not the case, and should be avoided.
:::

::: {.section}
#### [deleteOutbox(self, name)]{#symbol-threadedadaptivecommscomponent.deleteOutbox}

Deletes the named outbox.

Try to ensure any linkages to involving this outbox have been destroyed
- not just ones created by this component, but by others too! Behaviour
is undefined if this is not the case, and should be avoided.
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference} :

-   [initialiseComponent](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.initialiseComponent){.reference}(self)
-   [\_handlemessagefromthread](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._handlemessagefromthread){.reference}(self,
    msg)
-   [activate](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.activate){.reference}(self\[,
    Scheduler\]\[, Tracker\]\[, mainmethod\])
-   [mainBody](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.mainBody){.reference}(self)
-   [recv](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.recv){.reference}(self\[,
    boxname\])
-   [forwardInboxToThread](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.forwardInboxToThread){.reference}(self,
    box)
-   [closeDownComponent](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.closeDownComponent){.reference}(self)
-   [unlink](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.unlink){.reference}(self\[,
    thecomponent\]\[, thelinkage\])
-   [sync](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.sync){.reference}(self)
-   [send](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.send){.reference}(self,
    message\[, boxname\])
-   [\_threadmain](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._threadmain){.reference}(self)
-   [pause](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.pause){.reference}(self\[,
    timeout\])
-   [\_localmain](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._localmain){.reference}(self)
-   [\_do\_threadsafe](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._do_threadsafe){.reference}(self,
    cmd, argL, argD)
-   [link](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.link){.reference}(self,
    source, sink\[, passthrough\])
-   [main](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.main){.reference}(self)
-   [dataReady](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.dataReady){.reference}(self\[,
    boxname\])
:::

::: {.section}
#### Methods inherited from [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference} :

-   [\_\_str\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__str__){.reference}(self)
-   [childComponents](/Docs/Axon/Axon.Component.html#symbol-component.childComponents){.reference}(self)
-   [setInboxSize](/Docs/Axon/Axon.Component.html#symbol-component.setInboxSize){.reference}(self,
    boxname, size)
-   [anyReady](/Docs/Axon/Axon.Component.html#symbol-component.anyReady){.reference}(self)
-   [\_\_addChild](/Docs/Axon/Axon.Component.html#symbol-component.__addChild){.reference}(self,
    child)
-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Component.html#symbol-component._closeDownMicroprocess){.reference}(self)
-   [\_deliver](/Docs/Axon/Axon.Component.html#symbol-component._deliver){.reference}(self,
    message\[, boxname\])
-   [removeChild](/Docs/Axon/Axon.Component.html#symbol-component.removeChild){.reference}(self,
    child)
-   [Inbox](/Docs/Axon/Axon.Component.html#symbol-component.Inbox){.reference}(self\[,
    boxname\])
-   [addChildren](/Docs/Axon/Axon.Component.html#symbol-component.addChildren){.reference}(self,
    \*children)
:::

::: {.section}
#### Methods inherited from [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference} :

-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
-   [unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.unpause){.reference}(self)
-   [run](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.run){.reference}(self)
-   [\_isRunnable](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isRunnable){.reference}(self)
:::

::: {.section}
#### Methods inherited from [Axon.AdaptiveCommsComponent.\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference} :

-   [retrieveTrackedResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.retrieveTrackedResource){.reference}(self,
    inbox)
-   [\_newOutboxName](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable._newOutboxName){.reference}(self\[,
    name\])
-   [ceaseTrackingResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.ceaseTrackingResource){.reference}(self,
    resource)
-   [trackResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.trackResource){.reference}(self,
    resource, inbox)
-   [retrieveTrackedResourceInformation](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.retrieveTrackedResourceInformation){.reference}(self,
    resource)
-   [\_newInboxName](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable._newInboxName){.reference}(self\[,
    name\])
-   [trackResourceInformation](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.trackResourceInformation){.reference}(self,
    resource, inboxes, outboxes, information)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[ThreadedComponent](/Docs/Axon/Axon.ThreadedComponent.html){.reference}.[threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}
==========================================================================================================================================================================================================

::: {.section}
class threadedcomponent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-threadedcomponent}
---------------------------------------------------------------------------------------------------------

::: {.section}
threadedcomponent(\[queuelengths\]) -\> new threadedcomponent

Base class for a version of an Axon component that runs main() in a
separate thread (meaning it can, for example, block). Subclass to make
your own.

Internal queues buffer data between the thread and the Axon inboxes and
outboxes of the component. Set the default queue length at
initialisation (default=1000).

A simple example:

``` {.literal-block}
class IncrementByN(Axon.ThreadedComponent.threadedcomponent):

    Inboxes = { "inbox" : "Send numbers here",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Incremented numbers come out here",
                 "signal" : "NOT USED",
               }

    def __init__(self, N):
        super(IncrementByN,self).__init__()
        self.n = N

    def main(self):
        while 1:
            while self.dataReady("inbox"):
                value = self.recv("inbox")
                value = value + self.n
                self.send(value,"outbox")

            if not self.anyReady():
                self.pause()
```
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, queuelengths, \*\*argd)]{#symbol-threadedcomponent.__init__}
:::

::: {.section}
#### [\_do\_threadsafe(self, cmd, argL, argD)]{#symbol-threadedcomponent._do_threadsafe}

Internal method for ensuring a method call takes place in the main
scheduler\'s thread.
:::

::: {.section}
#### [\_handlemessagefromthread(self, msg)]{#symbol-threadedcomponent._handlemessagefromthread}

Unpacks a message containing a request to run a method of the form
(objectToCall, argList, argDict) then calls it and places the result in
the axontothreadqueue queue.

Used to execute methods on behalf of the separate thread. Results are
returned to it via the return queue.
:::

::: {.section}
#### [\_localmain(self)]{#symbol-threadedcomponent._localmain}

Do not overide this unless you reimplement the pass through of the boxes
to the threads, and state management.
:::

::: {.section}
#### [\_threadmain(self)]{#symbol-threadedcomponent._threadmain}

Exception trapping wrapper for main().

Runs in the separate thread. Catches any raised exceptions and attempts
to pass them back to \_localmain() to be re-raised.
:::

::: {.section}
#### [activate(self\[, Scheduler\]\[, Tracker\]\[, mainmethod\])]{#symbol-threadedcomponent.activate}

Call to activate this microprocess, so it can start to be executed by a
scheduler. Usual usage is to simply call x.activate().

See
[Axon.Microprocess.microprocess.activate](/Docs/Axon/Axon.Microprocess.microprocess.activate.html){.reference}()
for more info.
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-threadedcomponent.closeDownComponent}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [dataReady(self\[, boxname\])]{#symbol-threadedcomponent.dataReady}

Returns true if data is available in the requested inbox.

Used by the main() method of a component to check an inbox for ready
data.

Call this method to periodically check whether you\'ve been sent any
messages to deal with!

You are unlikely to want to override this method.
:::

::: {.section}
#### [forwardInboxToThread(self, box)]{#symbol-threadedcomponent.forwardInboxToThread}
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-threadedcomponent.initialiseComponent}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [link(self, source, sink\[, passthrough\])]{#symbol-threadedcomponent.link}

Creates a linkage from one inbox/outbox to another.

\-- source - a tuple (component, boxname) of where the link should start
from \-- sink - a tuple (component, boxname) of where the link should go
to

Other optional arguments:

-   passthrough=0 - (the default) link goes from an outbox to an inbox
-   passthrough=1 - the link goes from an inbox to another inbox
-   passthrough=2 - the link goes from an outbox to another outbox

See Axon.Postoffice.link(\...) for more information.
:::

::: {.section}
#### [main(self)]{#symbol-threadedcomponent.main}

Override this method, writing your own main thread of control as an
ordinary method. When the component is activated and the scheduler is
running, this what gets executed.

Write it as an ordinary method. Because it is run in a separate thread,
it can block.

If you do not override it, then a default main method exists instead
that will:

1.  Call self.initialiseComponent()
2.  Loop forever calling self.mainBody() repeatedly until mainBody()
    returns a False/zero result.
3.  Call self.closeDownComponent()
:::

::: {.section}
#### [mainBody(self)]{#symbol-threadedcomponent.mainBody}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [pause(self\[, timeout\])]{#symbol-threadedcomponent.pause}

Pauses the thread and blocks - does not return until the something
happens to re-awake it, or until it times out (if the optional timeout
is specified)

Must only be called from within the main() method - ie. from within the
separate thread.

Keyword arguments:

-   timeout \-- Optional. None, or the number of seconds after which
    this call should unblock itself (default=None)
:::

::: {.section}
#### [recv(self\[, boxname\])]{#symbol-threadedcomponent.recv}

returns the first piece of data in the requested inbox.

Used by the main() method to recieve a message from the outside world.
All comms goes via a named box/input queue

You will want to call this method to actually recieve messages you\'ve
been sent. You will want to check for new messages using dataReady first
though.

You are unlikely to want to override this method.
:::

::: {.section}
#### [send(self, message\[, boxname\])]{#symbol-threadedcomponent.send}

appends message to the requested outbox.

Used by the main() method to send a message to the outside world. All
comms goes via a named box/output queue

You will want to call this method to send messages.

Raises
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
if this outbox is linked to a destination inbox that is full, or if your
component is producing messages faster than Axon can pass them on.

You are unlikely to want to override this method.
:::

::: {.section}
#### [sync(self)]{#symbol-threadedcomponent.sync}

Call this from main() to synchronise with the main scheduler\'s thread.

You may wish to do this to throttle your component\'s behaviour This is
akin to posix.sched\_yield or shoving extra \"yield\" statements into a
component\'s generator.
:::

::: {.section}
#### [unlink(self\[, thecomponent\]\[, thelinkage\])]{#symbol-threadedcomponent.unlink}

Destroys all linkages to/from the specified component or destroys the
specific linkage specified.

Only destroys linkage(s) that were created *by* this component itself.

Keyword arguments:

-   thecomponent \-- None or a component object
-   thelinakge \-- None or the linkage to remove
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference} :

-   [\_\_str\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__str__){.reference}(self)
-   [childComponents](/Docs/Axon/Axon.Component.html#symbol-component.childComponents){.reference}(self)
-   [setInboxSize](/Docs/Axon/Axon.Component.html#symbol-component.setInboxSize){.reference}(self,
    boxname, size)
-   [anyReady](/Docs/Axon/Axon.Component.html#symbol-component.anyReady){.reference}(self)
-   [\_\_addChild](/Docs/Axon/Axon.Component.html#symbol-component.__addChild){.reference}(self,
    child)
-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Component.html#symbol-component._closeDownMicroprocess){.reference}(self)
-   [\_deliver](/Docs/Axon/Axon.Component.html#symbol-component._deliver){.reference}(self,
    message\[, boxname\])
-   [removeChild](/Docs/Axon/Axon.Component.html#symbol-component.removeChild){.reference}(self,
    child)
-   [Inbox](/Docs/Axon/Axon.Component.html#symbol-component.Inbox){.reference}(self\[,
    boxname\])
-   [addChildren](/Docs/Axon/Axon.Component.html#symbol-component.addChildren){.reference}(self,
    \*children)
:::

::: {.section}
#### Methods inherited from [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference} :

-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
-   [unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.unpause){.reference}(self)
-   [run](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.run){.reference}(self)
-   [\_isRunnable](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isRunnable){.reference}(self)
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

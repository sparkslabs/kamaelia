---
pagename: Docs/Axon/Axon.experimental._pprocess_support
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
likefile - file-like interaction with components
================================================

::: {.container}
-   **[addBox](/Docs/Axon/Axon.experimental._pprocess_support.addBox.html){.reference}**(names,
    boxMap, addBox)
-   **class
    [background](/Docs/Axon/Axon.experimental._pprocess_support.background.html){.reference}**
-   **class
    [componentWrapperInput](/Docs/Axon/Axon.experimental._pprocess_support.componentWrapperInput.html){.reference}**
-   **class
    [componentWrapperOutput](/Docs/Axon/Axon.experimental._pprocess_support.componentWrapperOutput.html){.reference}**
-   **class
    [dummyComponent](/Docs/Axon/Axon.experimental._pprocess_support.dummyComponent.html){.reference}**
-   **class
    [likefile](/Docs/Axon/Axon.experimental._pprocess_support.likefile.html){.reference}**
:::

-   [Using this code](#72){.reference}
-   [Advanced likefile usage](#73){.reference}
-   [Diagram of likefile\'s functionality](#74){.reference}
:::

::: {.section}
likefile is a way to run Axon components with code that is not
Axon-aware. It does this by running the scheduler and all associated
microprocesses in a separate thread, and using a custom component to
communicate if so desired.

::: {.section}
[Using this code]{#using-this-code} {#72}
-----------------------------------

With a normal kamaelia system, you would start up a component and start
running the Axon scheduler as follows, either:

``` {.literal-block}
from Axon.Scheduler import scheduler
component.activate()
scheduler.run.runThreads()
someOtherCode()
```

or simply:

``` {.literal-block}
component.run()
someOtherCode()
```

In both cases, someOtherCode() only run when the scheduler exits. What
do you do if you want to (e.g.) run this alongside another external
library that has the same requirement?

Well, first we start the Axon scheduler in the background as follows:

``` {.literal-block}
from likefile import background
background().start()
```

The scheduler is now actively running in the background, and you can
start components on it from the foreground, in the same way as you would
from inside kamaelia (don\'t worry, activate() is threadsafe):

``` {.literal-block}
component.activate()
someOtherCode()
```

\"component\" will immediately start running and processing. This is
fine if it\'s something non-interactive like a TCP server, but what do
we do if we want to interact with this component from someOtherCode?

In this case, we use \'likefile\', instead of activating. This is a
wrapper which sits around a component and provides a threadsafe way to
interact with it, whilst it is running in the backgrounded scheduler:

``` {.literal-block}
from Axon.LikeFile import likefile
wrappedComponent = likefile(component)
someOtherCode()
```

Now, wrappedComponent is an instance of the likefile wrapper, and you
can interact with \"component\" by calling get() on wrappedComponent, to
get data from the outbox on \"component\", or by calling put(data) to
put \"data\" into the inbox of \"component\" like so:

``` {.literal-block}
p = likefile( SimpleHTTPClient() )
p.put("http://google.com")
google = p.get()
p.shutdown()
print "google's homepage is", len(google), "bytes long.
```

for both get() and put(), there is an optional extra parameter boxname,
allowing you to interact with different boxes, for example to send a
message with the text \"RELOAD\" to a component\'s control inbox, you
would do:

``` {.literal-block}
wrappedComponent.put("RELOAD", "control")
wrappedComponent.get("signal")
```

Finally, likefile objects have a shutdown() method that sends the usual
Axon IPC shutdown messages to a wrapped component, and prevents further
IO.
:::

::: {.section}
[Advanced likefile usage]{#advanced-likefile-usage} {#73}
---------------------------------------------------

likefile has some optional extra arguments on creation, for handling
custom boxes outside the \"basic 4\". For example, to wrap a component
with inboxes called \"secondary\" and \"tertiary\" and an outbox called
\"debug\", You would do:

``` {.literal-block}
p = likefile( componentMaker,
              extraInboxes = ("secondary", "tertiary"),
              extraOutboxes = "debug", )
```

Either strings or tuples of strings will work.

It may be the case that the component you are trying to wrap will link
its own inbox/outbox/signal/control, and this will result in a
BoxAlreadyLinkedToDestination exception. To stop likefile from wrapping
the default 4 boxes, pass the parameter wrapDefault = False. Note that
you will need to manually wrap every box you want to use, for example to
wrap a component that has its own linkages for signal/control:

``` {.literal-block}
p = likefile( myComponent,
              wrapDefault = False,
              extraInboxes = "inbox",
              extraOutboxes = "outbox", )
```
:::

::: {.section}
[Diagram of likefile\'s functionality]{#diagram-of-likefile-s-functionality} {#74}
----------------------------------------------------------------------------

likefile is constructed from components like so:

``` {.literal-block}
     +----------------------------------+
     |             likefile             |
     +----------------------------------+
          |                      / \
          |                       |
      InQueues                 OutQueues
          |                       |
+---------+-----------------------+---------+
|        \ /                      |         |
|    +---------+               +--------+   |
|    |  Input  |   Shutdown    | Output |   |
|    | Wrapper | ------------> |        |   |
|    | (thread)|   Message     |Wrapper |   |
|    +---------+               +--------+   |
|         |                      / \        |
|         |                       |         |
|     Inboxes                 Outboxes      |
|         |                       |         |
|        \ /                      |         |
|    +----------------------------------+   |
|    |      the wrapped component       |   |
|    +----------------------------------+   |
|                                           |
|    +----------------------------------+   |
|    |       Some other component       |   |
|    |     that was only activated      |   |
|    +----------------------------------+   |
|                                           |
|  AXON SCHEDULED COMPONENTS                |
+-------------------------------------------+
```

Note 1: Threadsafeness of activate().

when a component is activated, it calls the method inherited from
microprocess, which calls \_addThread(self) on an appropriate scheduler.
\_addThread calls wakeThread, which places the request on a threadsafe
queue.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[addBox](/Docs/Axon/Axon.experimental._pprocess_support.addBox.html){.reference}
==============================================================================================================================================================================================================================================================================

::: {.section}
[addBox(names, boxMap, addBox)]{#symbol-addBox}
-----------------------------------------------

Add an extra wrapped box called name, using the addBox function provided
(either self.addInbox or self.addOutbox), and adding it to the box
mapping which is used to coordinate message routing within component
wrappers.
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[background](/Docs/Axon/Axon.experimental._pprocess_support.background.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
class background(threading.Thread) {#symbol-background}
----------------------------------

::: {.section}
A python thread which runs a scheduler. Takes the same arguments at
creation that scheduler.run.runThreads accepts.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, slowmo\]\[, zap\])]{#symbol-background.__init__}
:::

::: {.section}
#### [run(self)]{#symbol-background.run}
:::
:::

::: {.section}
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[componentWrapperInput](/Docs/Axon/Axon.experimental._pprocess_support.componentWrapperInput.html){.reference}
============================================================================================================================================================================================================================================================================================================

::: {.section}
class componentWrapperInput([Axon.ThreadedComponent.threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}) {#symbol-componentWrapperInput}
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

::: {.section}
A wrapper that takes a child component and waits on an event from the
foreground, to signal that there is queued data to be placed on the
child\'s inboxes.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, child\[, inboxes\])]{#symbol-componentWrapperInput.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-componentWrapperInput.main}
:::

::: {.section}
#### [pollQueue(self, whatInbox)]{#symbol-componentWrapperInput.pollQueue}

This method checks all the queues from the outside world, and forwards
any waiting data to the child component. Returns False if we propogated
a shutdown signal, true otherwise.
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.ThreadedComponent.threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference} :

-   [deleteOutbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent.deleteOutbox){.reference}(self,
    name)
-   [\_unsafe\_addOutbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent._unsafe_addOutbox){.reference}(self,
    \*args)
-   [\_unsafe\_deleteInbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent._unsafe_deleteInbox){.reference}(self,
    name)
-   [addInbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent.addInbox){.reference}(self,
    \*args)
-   [deleteInbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent.deleteInbox){.reference}(self,
    name)
-   [\_unsafe\_addInbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent._unsafe_addInbox){.reference}(self,
    \*args)
-   [\_unsafe\_deleteOutbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent._unsafe_deleteOutbox){.reference}(self,
    name)
-   [addOutbox](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedadaptivecommscomponent.addOutbox){.reference}(self,
    \*args)
:::

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

[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[componentWrapperOutput](/Docs/Axon/Axon.experimental._pprocess_support.componentWrapperOutput.html){.reference}
==============================================================================================================================================================================================================================================================================================================

::: {.section}
class componentWrapperOutput([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-componentWrapperOutput}
------------------------------------------------------------------------------------------------------------------------------------------------------------------

::: {.section}
A component which takes a child component and connects its outboxes to
queues, which communicate with the likefile component.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, child, inputHandler\[, outboxes\])]{#symbol-componentWrapperOutput.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-componentWrapperOutput.main}
:::

::: {.section}
#### [sendPendingOutput(self)]{#symbol-componentWrapperOutput.sendPendingOutput}

This method will take any outgoing data sent to us from a child
component and stick it on a queue to the outside world.
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference} :

-   [mainBody](/Docs/Axon/Axon.Component.html#symbol-component.mainBody){.reference}(self)
-   [\_\_str\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__str__){.reference}(self)
-   [childComponents](/Docs/Axon/Axon.Component.html#symbol-component.childComponents){.reference}(self)
-   [setInboxSize](/Docs/Axon/Axon.Component.html#symbol-component.setInboxSize){.reference}(self,
    boxname, size)
-   [send](/Docs/Axon/Axon.Component.html#symbol-component.send){.reference}(self,
    message\[, boxname\])
-   [dataReady](/Docs/Axon/Axon.Component.html#symbol-component.dataReady){.reference}(self\[,
    boxname\])
-   [initialiseComponent](/Docs/Axon/Axon.Component.html#symbol-component.initialiseComponent){.reference}(self)
-   [anyReady](/Docs/Axon/Axon.Component.html#symbol-component.anyReady){.reference}(self)
-   [\_\_addChild](/Docs/Axon/Axon.Component.html#symbol-component.__addChild){.reference}(self,
    child)
-   [closeDownComponent](/Docs/Axon/Axon.Component.html#symbol-component.closeDownComponent){.reference}(self)
-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Component.html#symbol-component._closeDownMicroprocess){.reference}(self)
-   [link](/Docs/Axon/Axon.Component.html#symbol-component.link){.reference}(self,
    source, sink, \*optionalargs, \*\*kwoptionalargs)
-   [unlink](/Docs/Axon/Axon.Component.html#symbol-component.unlink){.reference}(self\[,
    thecomponent\]\[, thelinkage\])
-   [recv](/Docs/Axon/Axon.Component.html#symbol-component.recv){.reference}(self\[,
    boxname\])
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

-   [pause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.pause){.reference}(self)
-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
-   [activate](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.activate){.reference}(self\[,
    Scheduler\]\[, Tracker\]\[, mainmethod\])
-   [unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.unpause){.reference}(self)
-   [run](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.run){.reference}(self)
-   [\_isRunnable](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isRunnable){.reference}(self)
:::

::: {.section}
#### Methods inherited from [Axon.AdaptiveCommsComponent.\_AdaptiveCommsable](/Docs/Axon/Axon.AdaptiveCommsComponent._AdaptiveCommsable.html){.reference} :

-   [retrieveTrackedResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.retrieveTrackedResource){.reference}(self,
    inbox)
-   [deleteOutbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.deleteOutbox){.reference}(self,
    name)
-   [\_newOutboxName](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable._newOutboxName){.reference}(self\[,
    name\])
-   [ceaseTrackingResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.ceaseTrackingResource){.reference}(self,
    resource)
-   [addInbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.addInbox){.reference}(self,
    \*args)
-   [trackResource](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.trackResource){.reference}(self,
    resource, inbox)
-   [retrieveTrackedResourceInformation](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.retrieveTrackedResourceInformation){.reference}(self,
    resource)
-   [deleteInbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.deleteInbox){.reference}(self,
    name)
-   [\_newInboxName](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable._newInboxName){.reference}(self\[,
    name\])
-   [trackResourceInformation](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.trackResourceInformation){.reference}(self,
    resource, inboxes, outboxes, information)
-   [addOutbox](/Docs/Axon/Axon.AdaptiveCommsComponent.html#symbol-_AdaptiveCommsable.addOutbox){.reference}(self,
    \*args)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[dummyComponent](/Docs/Axon/Axon.experimental._pprocess_support.dummyComponent.html){.reference}
==============================================================================================================================================================================================================================================================================================

::: {.section}
class dummyComponent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-dummyComponent}
------------------------------------------------------------------------------------------------------

::: {.section}
A dummy component. Functionality: None. Prevents the scheduler from
dying immediately.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [main(self)]{#symbol-dummyComponent.main}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference} :

-   [mainBody](/Docs/Axon/Axon.Component.html#symbol-component.mainBody){.reference}(self)
-   [\_\_str\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__str__){.reference}(self)
-   [childComponents](/Docs/Axon/Axon.Component.html#symbol-component.childComponents){.reference}(self)
-   [\_\_init\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__init__){.reference}(self,
    \*args, \*\*argd)
-   [setInboxSize](/Docs/Axon/Axon.Component.html#symbol-component.setInboxSize){.reference}(self,
    boxname, size)
-   [send](/Docs/Axon/Axon.Component.html#symbol-component.send){.reference}(self,
    message\[, boxname\])
-   [dataReady](/Docs/Axon/Axon.Component.html#symbol-component.dataReady){.reference}(self\[,
    boxname\])
-   [initialiseComponent](/Docs/Axon/Axon.Component.html#symbol-component.initialiseComponent){.reference}(self)
-   [anyReady](/Docs/Axon/Axon.Component.html#symbol-component.anyReady){.reference}(self)
-   [\_\_addChild](/Docs/Axon/Axon.Component.html#symbol-component.__addChild){.reference}(self,
    child)
-   [closeDownComponent](/Docs/Axon/Axon.Component.html#symbol-component.closeDownComponent){.reference}(self)
-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Component.html#symbol-component._closeDownMicroprocess){.reference}(self)
-   [link](/Docs/Axon/Axon.Component.html#symbol-component.link){.reference}(self,
    source, sink, \*optionalargs, \*\*kwoptionalargs)
-   [unlink](/Docs/Axon/Axon.Component.html#symbol-component.unlink){.reference}(self\[,
    thecomponent\]\[, thelinkage\])
-   [recv](/Docs/Axon/Axon.Component.html#symbol-component.recv){.reference}(self\[,
    boxname\])
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

-   [pause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.pause){.reference}(self)
-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
-   [activate](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.activate){.reference}(self\[,
    Scheduler\]\[, Tracker\]\[, mainmethod\])
-   [unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.unpause){.reference}(self)
-   [run](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.run){.reference}(self)
-   [\_isRunnable](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isRunnable){.reference}(self)
:::
:::
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[likefile](/Docs/Axon/Axon.experimental._pprocess_support.likefile.html){.reference}
==================================================================================================================================================================================================================================================================================

::: {.section}
class likefile(object) {#symbol-likefile}
----------------------

::: {.section}
An interface to the message queues from a wrapped component, which is
activated on a backgrounded scheduler.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_del\_\_(self)]{#symbol-likefile.__del__}
:::

::: {.section}
#### [\_\_init\_\_(self, child\[, extraInboxes\]\[, extraOutboxes\]\[, wrapDefault\])]{#symbol-likefile.__init__}
:::

::: {.section}
#### [anyReady(self)]{#symbol-likefile.anyReady}
:::

::: {.section}
#### [empty(self\[, boxname\])]{#symbol-likefile.empty}

Return True if there is no data pending collection on boxname, False
otherwise.
:::

::: {.section}
#### [get(self\[, boxname\]\[, blocking\]\[, timeout\])]{#symbol-likefile.get}

Performs a blocking read on the queue corresponding to the named outbox
on the wrapped component. raises AttributeError if the likefile is not
alive. Optional parameters blocking and timeout function the same way as
in Queue objects, since that is what\'s used under the surface.
:::

::: {.section}
#### [get\_nowait(self\[, boxname\])]{#symbol-likefile.get_nowait}

Equivalent to get(boxname, False)
:::

::: {.section}
#### [put(self, msg\[, boxname\])]{#symbol-likefile.put}

Places an object on a queue which will be directed to a named inbox on
the wrapped component.
:::

::: {.section}
#### [qsize(self\[, boxname\])]{#symbol-likefile.qsize}

Returns the approximate number of pending data items awaiting collection
from boxname. Will never be smaller than the actual amount.
:::

::: {.section}
#### [shutdown(self)]{#symbol-likefile.shutdown}

Sends terminatory signals to the wrapped component, and shut down the
componentWrapper. will warn if the shutdown took too long to confirm in
action.
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

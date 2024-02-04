---
pagename: Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[ThreadedComponent](/Docs/Axon/Axon.ThreadedComponent.html){.reference}.[threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.ThreadedComponent.html){.reference}

------------------------------------------------------------------------

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

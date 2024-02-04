---
pagename: Docs/Axon/Axon.experimental._pprocess_support.componentWrapperInput
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[componentWrapperInput](/Docs/Axon/Axon.experimental._pprocess_support.componentWrapperInput.html){.reference}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}

------------------------------------------------------------------------

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

---
pagename: Docs/Axon/Axon.experimental._pprocess_support.componentWrapperOutput
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[experimental](/Docs/Axon/Axon.experimental.html){.reference}.[\_pprocess\_support](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}.[componentWrapperOutput](/Docs/Axon/Axon.experimental._pprocess_support.componentWrapperOutput.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.experimental._pprocess_support.html){.reference}

------------------------------------------------------------------------

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

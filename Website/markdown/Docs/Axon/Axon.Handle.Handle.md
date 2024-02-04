---
pagename: Docs/Axon/Axon.Handle.Handle
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Handle](/Docs/Axon/Axon.Handle.html){.reference}.[Handle](/Docs/Axon/Axon.Handle.Handle.html){.reference}
---------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Handle.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Handle([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-Handle}
------------------------------------------------------------------------------------------------------------------------------

::: {.section}
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, someComponent)]{#symbol-Handle.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_get(self)]{#symbol-Handle._get}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Handle.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [get(self\[, boxname\])]{#symbol-Handle.get}

Return an item of data sent to an outbox of the wrapped component.

This method is non blocking and always returns immediately. If there is
no data to return, then the exception Queue.Empty is thrown

Arguments:

-   boxname \-- (optional) the name of the outbox of the wrapped
    component from which the data should be collected
    (default=\"outbox\", should be either \"outbox\" or \"signal\")
:::

::: {.section}
#### [main(self)]{#symbol-Handle.main}

Main loop.
:::

::: {.section}
#### [put(self, \*args)]{#symbol-Handle.put}

Send an item of data to one of the inboxes of the wrapped component.

The item of data is queued and sent to the inbox as soon as possible.

Arguments:

-   the item of data
-   the name of the inbox it is destined for (either \"inbox\" or
    \"control\")
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

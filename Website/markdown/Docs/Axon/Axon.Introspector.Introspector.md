---
pagename: Docs/Axon/Axon.Introspector.Introspector
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Introspector](/Docs/Axon/Axon.Introspector.html){.reference}.[Introspector](/Docs/Axon/Axon.Introspector.Introspector.html){.reference}
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Introspector.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Introspector([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Introspector}
----------------------------------------------------------------------------------------------------

Introspector() -\> new Introspector component.

Outputs topology (change) data describing what components there are, and
how they are wired inside the running Axon system.

::: {.section}
### [Inboxes]{#symbol-Introspector.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-Introspector.Outboxes}

-   **outbox** : Topology (change) data describing the Axon system
-   **signal** : Shutdown signalling
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
#### [introspect(self)]{#symbol-Introspector.introspect}

introspect() -\> components, postboxes, linkages

Returns the current set of components, postboxes and interpostbox
linkages.

-   components \-- a dictionary, containing components as keys
-   postboxes \-- a list of (component.id, type, \"boxname\") tuples,
    where type=\"i\" (inbox) or \"o\" (outbox)
-   linkages \-- a dictionary containing (postbox,postbox) tuples as
    keys, where postbox is a tuple from the postboxes list
:::

::: {.section}
#### [main(self)]{#symbol-Introspector.main}

Main loop.
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

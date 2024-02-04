---
pagename: Components/pydoc/Kamaelia.Util.OneShot.TriggeredOneShot
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[OneShot](/Components/pydoc/Kamaelia.Util.OneShot.html){.reference}.[TriggeredOneShot](/Components/pydoc/Kamaelia.Util.OneShot.TriggeredOneShot.html){.reference}
==================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.OneShot.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TriggeredOneShot([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TriggeredOneShot}
--------------------------------------------------------------------------------------------------------

OneShot(msg) -\> new OneShot component.

Waits for anything to arrive at its \"inbox\" inbox, then immediately
sends the specified message and terminates.

Keyword arguments:

``` {.literal-block}
- msg  -- the message to send out
```

::: {.section}
### [Inboxes]{#symbol-TriggeredOneShot.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Anything, as trigger
:::

::: {.section}
### [Outboxes]{#symbol-TriggeredOneShot.Outboxes}

-   **outbox** : Item is sent out here
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
#### [\_\_init\_\_(self\[, msg\])]{#symbol-TriggeredOneShot.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-TriggeredOneShot.main}

Main loop
:::
:::

::: {.section}
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

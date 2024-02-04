---
pagename: Components/pydoc/Kamaelia.Util.Splitter.PlugSplitter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}.[PlugSplitter](/Components/pydoc/Kamaelia.Util.Splitter.PlugSplitter.html){.reference}
=============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}

------------------------------------------------------------------------

::: {.section}
class PlugSplitter([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-PlugSplitter}
--------------------------------------------------------------------------------------------------------------------------------------------------------

PlugSplitter(\[sourceComponent\]) -\> new PlugSplitter component.

Splits incoming data out to multiple destinations. Send addsink(\...)
and removesink(\...) messages to the \'configuration\' inbox to add and
remove destinations.

Keyword arguments:

-   sourceComponent \-- None, or component to act as data source

::: {.section}
### [Inboxes]{#symbol-PlugSplitter.Inboxes}

-   **control** : Shutdown signalling, and signalling to be fanned out.
-   **\_control** : Internal inbox for receiving from the child source
    component (if it exists)
-   **configuration** : addsink(\...) and removesink(\...) request
    messages
-   **inbox** : Data items to be fanned out.
-   **\_inbox** : Internal inbox for receiving from the child source
    component (if it exists)
:::

::: {.section}
### [Outboxes]{#symbol-PlugSplitter.Outboxes}

-   **outbox** : Data items received on \'inbox\' inbox.
-   **signal** : Shutdown signalling, and data items received on
    \'control\' inbox.
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
#### [\_\_init\_\_(self\[, sourceComponent\])]{#symbol-PlugSplitter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_addSink(self, sink\[, sinkinbox\]\[, sinkcontrol\])]{#symbol-PlugSplitter._addSink}

Add a new destination for data.

Specify target component (sink), and target inbox (sinkinbox) and/or
target shutdown signalling inbox (sinkcontrol).
:::

::: {.section}
#### [\_delSink(self, sink\[, sinkinbox\]\[, sinkcontrol\])]{#symbol-PlugSplitter._delSink}

Remove a destination for data.

Specify target component (sink), and target inbox (sinkinbox) and/or
target shutdown signalling inbox (sinkcontrol).
:::

::: {.section}
#### [childrenDone(self)]{#symbol-PlugSplitter.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-PlugSplitter.main}

Main loop.
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

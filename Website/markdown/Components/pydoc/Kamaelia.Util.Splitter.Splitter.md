---
pagename: Components/pydoc/Kamaelia.Util.Splitter.Splitter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.Splitter.html){.reference}
=====================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Splitter([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-Splitter}
----------------------------------------------------------------------------------------------------------------------------------------------------

Splitter() -\> new Splitter component.

Splits incoming data out to multiple destinations. Send addsink(\...)
and removesink(\...) messages to the \'configuration\' inbox to add and
remove destinations.

::: {.section}
### [Inboxes]{#symbol-Splitter.Inboxes}

-   **control** : NOT USED
-   **configuration** : addsink(\...) and removesink(\...) request
    messages
-   **inbox** : Source of data items
:::

::: {.section}
### [Outboxes]{#symbol-Splitter.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED
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
#### [\_\_init\_\_(self)]{#symbol-Splitter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [createsink(self, sink\[, sinkbox\]\[, passthrough\])]{#symbol-Splitter.createsink}

Set up a new destination for data.

Creates an outbox, links it to the target (component,inbox) and records
it in self.outlist.
:::

::: {.section}
#### [deletesink(self, oldsink)]{#symbol-Splitter.deletesink}

Removes the specified (component, inbox) as a destination for data where
(component, inbox) = (oldsink.sink, oldsink.sinkbox).

Unlinks the target, destroys the corresponding outbox, and removes the
corresponding record from self.outlist.
:::

::: {.section}
#### [mainBody(self)]{#symbol-Splitter.mainBody}

Main loop body.
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

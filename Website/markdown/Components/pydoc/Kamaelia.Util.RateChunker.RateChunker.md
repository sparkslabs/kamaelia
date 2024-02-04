---
pagename: Components/pydoc/Kamaelia.Util.RateChunker.RateChunker
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.html){.reference}.[RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.RateChunker.html){.reference}
====================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.RateChunker.html){.reference}

------------------------------------------------------------------------

::: {.section}
class RateChunker([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RateChunker}
---------------------------------------------------------------------------------------------------

RateChunker(datarate,quantasize,chunkrate) -\> new Chunk component.

Alters the chunksize of incoming data to match a desired chunkrate.

Keyword arguments:

-   datarate \-- rate of the incoming data
-   quantasize \-- minimum granularity with which the data can be split
-   chunkrate \-- desired chunk rate

::: {.section}
### [Inboxes]{#symbol-RateChunker.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items
:::

::: {.section}
### [Outboxes]{#symbol-RateChunker.Outboxes}

-   **outbox** : Rechunked data items
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
#### [\_\_init\_\_(self, datarate, quantasize, chunkrate)]{#symbol-RateChunker.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkShutdown(self)]{#symbol-RateChunker.checkShutdown}
:::

::: {.section}
#### [main(self)]{#symbol-RateChunker.main}

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

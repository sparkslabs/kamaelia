---
pagename: Components/pydoc/Kamaelia.Util.Chunkifier.Chunkifier
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.html){.reference}.[Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.Chunkifier.html){.reference}
===============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Chunkifier.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Chunkifier([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Chunkifier}
--------------------------------------------------------------------------------------------------

Chunkifier(\[chunksize\]) -\> new Chunkifier component.

Flow controller - collects incoming data and outputs it only as quanta
of a given length in bytes (chunksize), unless the input stream ends
(producerFinished).

Keyword arguments: - chunksize \-- Chunk size in bytes - nodelay \-- if
set to True, partial chunks will be output rather than buffering up data
while waiting for more to arrive.

::: {.section}
### [Inboxes]{#symbol-Chunkifier.Inboxes}

-   **control** : Shut me down
-   **inbox** : Data stream to be split into chunks
:::

::: {.section}
### [Outboxes]{#symbol-Chunkifier.Outboxes}

-   **outbox** : Each message is a chunk
-   **signal** : I\'ve shut down
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
#### [\_\_init\_\_(self\[, chunksize\]\[, nodelay\])]{#symbol-Chunkifier.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-Chunkifier.main}
:::

::: {.section}
#### [sendChunk(self)]{#symbol-Chunkifier.sendChunk}
:::

::: {.section}
#### [sendPartialChunk(self)]{#symbol-Chunkifier.sendPartialChunk}
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

---
pagename: Components/pydoc/Kamaelia.Util.ChunkNamer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[ChunkNamer](/Components/pydoc/Kamaelia.Util.ChunkNamer.html){.reference}
==========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ChunkNamer](/Components/pydoc/Kamaelia.Util.ChunkNamer.ChunkNamer.html){.reference}**
:::

-   [Chunk Namer](#248){.reference}
    -   [Example Usage](#249){.reference}
:::

::: {.section}
Chunk Namer {#248}
===========

A component that labels each message with a unique filename for that
message. e.g. \"A\" \... \"B\" \... \--\> \[\"chunk1\", \"A\"\] \...
\[\"chunk2\", \"B\"\] \...

::: {.section}
[Example Usage]{#example-usage} {#249}
-------------------------------

Save each line entered to the console to a separate file:

``` {.literal-block}
pipeline(
    ConsoleReader(),
    ChunkNamer("test", ".txt"),
    WholeFileWriter()
).run()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[ChunkNamer](/Components/pydoc/Kamaelia.Util.ChunkNamer.html){.reference}.[ChunkNamer](/Components/pydoc/Kamaelia.Util.ChunkNamer.ChunkNamer.html){.reference}
===============================================================================================================================================================================================================================================================================

::: {.section}
class ChunkNamer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ChunkNamer}
--------------------------------------------------------------------------------------------------

ChunkNamer() -\> new ChunkNamer component.

Gives a filename to the chunk and sends it in the form \[filename,
contents\], e.g. to a WholeFileWriter component.

Keyword arguments: \-- basepath - the prefix to apply to the filename
\-- suffix - the suffix to apply to the filename

::: {.section}
### [Inboxes]{#symbol-ChunkNamer.Inboxes}

-   **control** : Shut me down
-   **inbox** : Chunks to be saved
:::

::: {.section}
### [Outboxes]{#symbol-ChunkNamer.Outboxes}

-   **outbox** : List: \[file name, file contents\]
-   **signal** : signal when I\'ve shut down
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
#### [\_\_init\_\_(self\[, basepath\]\[, suffix\])]{#symbol-ChunkNamer.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-ChunkNamer.main}
:::
:::

::: {.section}
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

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*

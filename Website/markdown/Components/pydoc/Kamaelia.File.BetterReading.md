---
pagename: Components/pydoc/Kamaelia.File.BetterReading
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[BetterReading](/Components/pydoc/Kamaelia.File.BetterReading.html){.reference}
================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [IntelligentFileReader](/Components/pydoc/Kamaelia.File.BetterReading.IntelligentFileReader.html){.reference}**
:::

-   [Intelligent File Reader](#708){.reference}
:::

::: {.section}
Intelligent File Reader {#708}
=======================

This component reads the filename specified at its creation and outputs
it as several messages. When a certain number of messages in its outbox
have not yet been delivered it will pause to reduce memory and CPU
usage. To wake it, ideally [Axon](/Docs/Axon/Axon.html){.reference}
should unpause it when the outbox has less than a certain number of
messages (i.e. when some are delivered) but for now you can send it an
arbitrary message (to \"inbox\") which will wake the component.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[BetterReading](/Components/pydoc/Kamaelia.File.BetterReading.html){.reference}.[IntelligentFileReader](/Components/pydoc/Kamaelia.File.BetterReading.IntelligentFileReader.html){.reference}
==============================================================================================================================================================================================================================================================================================================

::: {.section}
class IntelligentFileReader([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-IntelligentFileReader}
-------------------------------------------------------------------------------------------------------------

IntelligentFileReader(filename, chunksize, maxqueue) -\> file reading
component

Creates a file reader component. Reads a chunk of chunksize bytes, using
the Selector to avoid having to block, pausing when the length of its
send-queue exceeds maxqueue chunks.

::: {.section}
### [Inboxes]{#symbol-IntelligentFileReader.Inboxes}

-   **control** : for shutdown signalling
-   **inbox** : wake me up by sending anything here
-   **\_selectorready** : ready to read
:::

::: {.section}
### [Outboxes]{#symbol-IntelligentFileReader.Outboxes}

-   **debug** : information designed to aid debugging
-   **outbox** : data output
-   **signal** : outputs \'producerFinished\' after all data has been
    read
-   **\_selectorask** : ask the Selector to notify readiness to read on
    a file
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
#### [\_\_init\_\_(self, filename\[, chunksize\]\[, maxqueue\])]{#symbol-IntelligentFileReader.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [debug(self, msg)]{#symbol-IntelligentFileReader.debug}
:::

::: {.section}
#### [main(self)]{#symbol-IntelligentFileReader.main}

Main loop
:::

::: {.section}
#### [makeNonBlocking(self, fd)]{#symbol-IntelligentFileReader.makeNonBlocking}
:::

::: {.section}
#### [openFile(self, filename)]{#symbol-IntelligentFileReader.openFile}
:::

::: {.section}
#### [selectorWait(self, fd)]{#symbol-IntelligentFileReader.selectorWait}
:::

::: {.section}
#### [tryReadChunk(self, fd)]{#symbol-IntelligentFileReader.tryReadChunk}
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

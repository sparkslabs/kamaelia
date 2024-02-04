---
pagename: Components/pydoc/Kamaelia.File.Writing
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Writing](/Components/pydoc/Kamaelia.File.Writing.html){.reference}
====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SimpleFileWriter](/Components/pydoc/Kamaelia.File.Writing.SimpleFileWriter.html){.reference}**
:::

-   [Simple File Writer](#716){.reference}
    -   [Example Usage](#717){.reference}
    -   [More detail](#718){.reference}
    -   [Development history](#719){.reference}
:::

::: {.section}
Simple File Writer {#716}
==================

This component writes any data it receives to a file.

::: {.section}
[Example Usage]{#example-usage} {#717}
-------------------------------

Copying a file:

``` {.literal-block}
from Kamaelia.File.Writing import SimpleFileWriter

Pipeline(RateControlledFileReader("sourcefile",rate=1000000),
         SimpleFileWriter("destinationfile")
        ).activate()
```
:::

::: {.section}
[More detail]{#more-detail} {#718}
---------------------------

Any data sent to this component\'s inbox is written to the specified
file. Any existing file with the same name is overwritten.

The file is opened for writing when the component is activated, and is
closed when it shuts down.

This component terminates, closing the file, if it receives a
shutdownMicroprocess or producerFinished message on its \"control\"
inbox. The message is passed on out of its \"signal\" outbox.
:::

::: {.section}
[Development history]{#development-history} {#719}
-------------------------------------------

SimpleFileWriter - prototyped in
/Sketches/filereading/WriteFileAdapter.py
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Writing](/Components/pydoc/Kamaelia.File.Writing.html){.reference}.[SimpleFileWriter](/Components/pydoc/Kamaelia.File.Writing.SimpleFileWriter.html){.reference}
==================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleFileWriter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleFileWriter}
--------------------------------------------------------------------------------------------------------

SimpleFileWriter(filename) -\> component that writes data to the file

Writes any data sent to its inbox to the specified file.

::: {.section}
### [Inboxes]{#symbol-SimpleFileWriter.Inboxes}

-   **control** : to receive shutdown/finished messages
-   **inbox** : data to write to file
:::

::: {.section}
### [Outboxes]{#symbol-SimpleFileWriter.Outboxes}

-   **outbox** : not used
-   **signal** : shutdown/finished signalling
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
#### [\_\_init\_\_(self, filename\[, mode\])]{#symbol-SimpleFileWriter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-SimpleFileWriter.closeDownComponent}

Closes the file handle
:::

::: {.section}
#### [main(self)]{#symbol-SimpleFileWriter.main}

Main loop
:::

::: {.section}
#### [shutdown(self)]{#symbol-SimpleFileWriter.shutdown}

Returns True if a shutdownMicroprocess or producerFinished message is
received.

Also passes the message on out of the \"signal\" outbox.
:::

::: {.section}
#### [writeData(self, data)]{#symbol-SimpleFileWriter.writeData}

Writes the data to the file
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

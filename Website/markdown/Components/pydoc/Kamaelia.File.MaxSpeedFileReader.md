---
pagename: Components/pydoc/Kamaelia.File.MaxSpeedFileReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.html){.reference}
==========================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.MaxSpeedFileReader.html){.reference}**
:::

-   [Reading a file as fast as possible](#713){.reference}
    -   [Example Usage](#714){.reference}
    -   [More details](#715){.reference}
:::

::: {.section}
Reading a file as fast as possible {#713}
==================================

MaxSpeedFileReader reads a file in bytes mode as fast as it can; limited
only by any size limit on the inbox it is sending the data to.

This component is therefore useful for building systems that are self
rate limiting - systems that are just trying to process data as fast as
they can and are limited by the speed of the slowest part of the chain.

::: {.section}
[Example Usage]{#example-usage} {#714}
-------------------------------

Read \"myfile\" in in chunks of 1024 bytes. The rate is limited by the
rate at which the consumer component can consume the chunks, since its
inbox has a size limit of 5 items of data:

``` {.literal-block}
consumer = Consumer()
consumer.inboxes["inbox"].setSize(5)

Pipeline( MaxSpeedFileReader("myfile", chunksize=1024),
          consumer,
        ).run()
```
:::

::: {.section}
[More details]{#more-details} {#715}
-----------------------------

Specify a filename and chunksize and MaxSpeedFileReader will read bytes
from the file in the chunksize you specified and send them out of its
\"outbox\" outbox.

If the destination inbox it is sending chunks to is size limited, then
MaxSpeedFileReader will pause until space becomes available. This is how
the speed at which the file is ingested is regulated - by the rate at
which it is consumed.

When the whole file has been read, this component will terminate and
send a producerFinished() message out of its \"signal\" outbox.

If a producerFinished message is received on the \"control\" inbox, this
component will complete sending any data that may be waiting. It will
then send the producerFinished message on out of its \"signal\" outbox
and terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
this component will immediately send it on out of its \"signal\" outbox
and immediately terminate. It will not complete sending on any pending
data.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.html){.reference}.[MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.MaxSpeedFileReader.html){.reference}
=======================================================================================================================================================================================================================================================================================================================

::: {.section}
class MaxSpeedFileReader([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-MaxSpeedFileReader}
----------------------------------------------------------------------------------------------------------

MaxSpeedFileReader(filename\[,chunksize\]) -\> new MaxSpeedFileReader
component.

Reads the contents of a file in bytes mode; sending it out as fast as it
can in chunks from the \"outbox\" outbox. The rate of reading is only
limited by any size limit of the destination inbox to which the data is
being sent.

Keyword arguments:

-   filename \-- The filename of the file to read
-   chunksize \-- Optional. The maximum number of bytes in each chunk of
    data read from the file and sent out of the \"outbox\" outbox
    (default=32768)

::: {.section}
### [Inboxes]{#symbol-MaxSpeedFileReader.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-MaxSpeedFileReader.Outboxes}
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
#### [\_\_init\_\_(self, filename\[, chunksize\])]{#symbol-MaxSpeedFileReader.__init__}
:::

::: {.section}
#### [canStop(self)]{#symbol-MaxSpeedFileReader.canStop}
:::

::: {.section}
#### [handleControl(self)]{#symbol-MaxSpeedFileReader.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-MaxSpeedFileReader.main}
:::

::: {.section}
#### [mustStop(self)]{#symbol-MaxSpeedFileReader.mustStop}
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-MaxSpeedFileReader.waitSend}
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

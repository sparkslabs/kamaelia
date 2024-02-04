---
pagename: Components/pydoc/Kamaelia.File.MaxSpeedFileReader.MaxSpeedFileReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.html){.reference}.[MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.MaxSpeedFileReader.html){.reference}
=======================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.html){.reference}

------------------------------------------------------------------------

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

---
pagename: Components/pydoc/Kamaelia.File.Reading.PromptedFileReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[PromptedFileReader](/Components/pydoc/Kamaelia.File.Reading.PromptedFileReader.html){.reference}
======================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.Reading.html){.reference}

------------------------------------------------------------------------

::: {.section}
class PromptedFileReader([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PromptedFileReader}
----------------------------------------------------------------------------------------------------------

PromptedFileReader(filename\[,readmode\]) -\> file reading component

Creates a file reader component. Reads N bytes/lines from the file when
N is sent to its inbox.

Keyword arguments:

-   readmode \-- \"bytes\" or \"lines\"

::: {.section}
### [Inboxes]{#symbol-PromptedFileReader.Inboxes}

-   **control** : for shutdown signalling
-   **inbox** : requests to \'n\' read bytes/lines
:::

::: {.section}
### [Outboxes]{#symbol-PromptedFileReader.Outboxes}

-   **outbox** : data output
-   **signal** : outputs \'producerFinished\' after all data has been
    read
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
#### [\_\_init\_\_(self, filename\[, readmode\])]{#symbol-PromptedFileReader.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-PromptedFileReader.closeDownComponent}

Closes the file handle
:::

::: {.section}
#### [main(self)]{#symbol-PromptedFileReader.main}

Main loop
:::

::: {.section}
#### [readNBytes(self, n)]{#symbol-PromptedFileReader.readNBytes}

readNBytes(n) -\> string containing \'n\' bytes read from the file.

\"EOF\" raised if the end of the file is reached and there is no data to
return.
:::

::: {.section}
#### [readNLines(self, n)]{#symbol-PromptedFileReader.readNLines}

readNLines(n) -\> string containing \'n\' lines read from the file.

\"EOF\" raised if the end of the file is reached and there is no data to
return.
:::

::: {.section}
#### [shutdown(self)]{#symbol-PromptedFileReader.shutdown}

Returns True if a shutdownMicroprocess message is received.

Also passes the message on out of the \"signal\" outbox.
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

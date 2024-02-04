---
pagename: Components/pydoc/Kamaelia.File.WholeFileWriter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[WholeFileWriter](/Components/pydoc/Kamaelia.File.WholeFileWriter.html){.reference}
====================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [WholeFileWriter](/Components/pydoc/Kamaelia.File.WholeFileWriter.WholeFileWriter.html){.reference}**
:::

-   [Whole File Writer](#677){.reference}
:::

::: {.section}
Whole File Writer {#677}
=================

This component accepts file creation jobs and signals the completion of
each jobs. Creation jobs consist of a list \[ filename, contents \]
added to \"inbox\". Completion signals consist of the string \"done\"
being sent to \"outbox\".

All jobs are processed sequentially.

This component does not terminate.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[WholeFileWriter](/Components/pydoc/Kamaelia.File.WholeFileWriter.html){.reference}.[WholeFileWriter](/Components/pydoc/Kamaelia.File.WholeFileWriter.WholeFileWriter.html){.reference}
========================================================================================================================================================================================================================================================================================================

::: {.section}
class WholeFileWriter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-WholeFileWriter}
-------------------------------------------------------------------------------------------------------

WholeFileWriter() -\> component that creates and writes files

Uses \[ filename, contents \] structure to file creation messages in
\"inbox\"

::: {.section}
### [Inboxes]{#symbol-WholeFileWriter.Inboxes}

-   **control** : UNUSED
-   **inbox** : file creation jobs
:::

::: {.section}
### [Outboxes]{#symbol-WholeFileWriter.Outboxes}

-   **outbox** : filename written
-   **signal** : UNUSED
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
#### [\_\_init\_\_(self)]{#symbol-WholeFileWriter.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-WholeFileWriter.main}

Main loop
:::

::: {.section}
#### [writeFile(self, filename, data)]{#symbol-WholeFileWriter.writeFile}

Writes the data to a new file
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

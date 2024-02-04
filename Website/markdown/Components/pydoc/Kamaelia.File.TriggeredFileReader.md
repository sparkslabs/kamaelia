---
pagename: Components/pydoc/Kamaelia.File.TriggeredFileReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[TriggeredFileReader](/Components/pydoc/Kamaelia.File.TriggeredFileReader.html){.reference}
============================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TriggeredFileReader](/Components/pydoc/Kamaelia.File.TriggeredFileReader.TriggeredFileReader.html){.reference}**
:::

-   [Triggered File Reader](#721){.reference}
:::

::: {.section}
Triggered File Reader {#721}
=====================

This component accepts a filepath as an \"inbox\" message, and outputs
the contents of that file to \"outbox\". All requests are processed
sequentially.

This component does not terminate.

Drawback - this component uses blocking file reading calls but does not
run on its own thread.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[TriggeredFileReader](/Components/pydoc/Kamaelia.File.TriggeredFileReader.html){.reference}.[TriggeredFileReader](/Components/pydoc/Kamaelia.File.TriggeredFileReader.TriggeredFileReader.html){.reference}
============================================================================================================================================================================================================================================================================================================================

::: {.section}
class TriggeredFileReader([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TriggeredFileReader}
-----------------------------------------------------------------------------------------------------------

TriggeredFileReader() -\> component that reads arbitrary files

::: {.section}
### [Inboxes]{#symbol-TriggeredFileReader.Inboxes}

-   **control** : Shut me down
-   **inbox** : filepaths to read
:::

::: {.section}
### [Outboxes]{#symbol-TriggeredFileReader.Outboxes}

-   **outbox** : file contents, 1 per message
-   **signal** : Signal my shutdown with producerFinished
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
#### [\_\_init\_\_(self)]{#symbol-TriggeredFileReader.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-TriggeredFileReader.main}

Main loop
:::

::: {.section}
#### [readFile(self, filename)]{#symbol-TriggeredFileReader.readFile}

Read data out of a file
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

---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.Minimal
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[Handlers](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.html){.reference}.[Minimal](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.Minimal.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Minimal](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.Minimal.Minimal.html){.reference}**
:::

-   [Minimal](#586){.reference}
    -   [Example Usage](#587){.reference}
:::

::: {.section}
Minimal {#586}
=======

A simple HTTP request handler for HTTPServer. Minimal serves files
within a given directory, guessing their MIME-type from their file
extension.

::: {.section}
[Example Usage]{#example-usage} {#587}
-------------------------------

See HTTPResourceGlue.py for how to use request handlers.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[Handlers](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.html){.reference}.[Minimal](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.Minimal.html){.reference}.[Minimal](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.Minimal.Minimal.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Minimal([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Minimal}
-----------------------------------------------------------------------------------------------

A simple HTTP request handler for HTTPServer which serves files within a
given directory, guessing their MIME-type from their file extension.

Arguments: \-- request - the request dictionary object that spawned this
component \-- homedirectory - the path to prepend to paths requested \--
indexfilename - if a directory is requested, this file is checked for
inside it, and sent if found

::: {.section}
### [Inboxes]{#symbol-Minimal.Inboxes}

-   **control** : UNUSED
-   **\_filecontrol** : Signals from file reader
-   **\_fileread** : File data
-   **inbox** : UNUSED
:::

::: {.section}
### [Outboxes]{#symbol-Minimal.Outboxes}

-   **\_fileprompt** : Get the file reader to do some reading
-   **outbox** : Response dictionaries
-   **signal** : UNUSED
-   **\_filesignal** : Shutdown the file reader
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
#### [\_\_init\_\_(self, request\[, indexfilename\]\[, homedirectory\])]{#symbol-Minimal.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-Minimal.main}

Produce the appropriate response then terminate.
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

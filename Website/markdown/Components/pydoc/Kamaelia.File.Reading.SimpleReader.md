---
pagename: Components/pydoc/Kamaelia.File.Reading.SimpleReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[SimpleReader](/Components/pydoc/Kamaelia.File.Reading.SimpleReader.html){.reference}
==========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.Reading.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SimpleReader([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleReader}
----------------------------------------------------------------------------------------------------

SimpleReader(filename\[,mode\]\[,buffering\]) -\> simple file reader

Creates a \"SimpleReader\" component.

Arguments:

-   filename \-- Name of the file to read
-   mode \-- This is the python readmode. Defaults to \"r\". (you may
    way \"rb\" occasionally)
-   buffering \-- The python buffer size. Defaults to 1. (see
    <http://www.python.org/doc/2.5.2/lib/built-in-funcs.html>)

::: {.section}
### [Inboxes]{#symbol-SimpleReader.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleReader.Outboxes}
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
#### [\_\_init\_\_(self, filename, \*\*argd)]{#symbol-SimpleReader.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-SimpleReader.main}

Main loop Simply opens the file, loops through it (using \"for\"),
sending data to \"outbox\". If the recipient has a maximum pipewidth it
handles that eventuallity resending by pausing and waiting for the
recipient to be able to recieve.

Shutsdown on shutdownMicroprocess.
:::

::: {.section}
#### [shutdown(self)]{#symbol-SimpleReader.shutdown}

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

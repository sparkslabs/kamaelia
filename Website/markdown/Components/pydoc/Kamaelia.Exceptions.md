---
pagename: Components/pydoc/Kamaelia.Exceptions
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Exceptions](/Components/pydoc/Kamaelia.Exceptions.html){.reference}
============================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [General Kamaelia Exceptions](#532){.reference}
    -   [The exceptions](#533){.reference}
:::

::: {.section}
General Kamaelia Exceptions {#532}
===========================

This module defines a set of standard exceptions generally useful in
Kamaelia. They are all based on the
[Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException.html){.reference}
base class.

::: {.section}
[The exceptions]{#the-exceptions} {#533}
---------------------------------

-   **BadRequest(request, innerexception)** - signalling that a request
    caused an exception\`\`self.request\`\` is the original request and
    `self.exception`{.docutils .literal} is the exception that it caused
    to be thrown
-   **socketSendFailure()** - signalling that a socket failed trying to
    send
-   **connectionClosedown()** - singalling that a connection closed down
-   **connectionDied()** - signalling that a connection died \*
    connectionDiedSending() \* connectionDiedReceiving() \*
    connectionServerShutdown()
:::
:::

------------------------------------------------------------------------

::: {.section}
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

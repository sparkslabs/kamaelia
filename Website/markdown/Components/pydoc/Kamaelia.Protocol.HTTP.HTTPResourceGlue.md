---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.HTTPResourceGlue
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPResourceGlue](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPResourceGlue.html){.reference}
=========================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [What does it do?](#596){.reference}
:::

::: {.section}
HTTP Resource Glue

::: {.section}
[What does it do?]{#what-does-it-do} {#596}
------------------------------------

It picks the appropriate resource handler for a request using any of the
request\'s attributes (e.g. uri, accepted encoding, language, source
etc.)

Its basic setup is to match prefixes of the request URI each of which
have their own predetermined request handler class (a component class).

HTTPResourceGlue also creates an instance of the handler component,
allowing complete control over its \_\_init\_\_ parameters. Feel free to
write your own for your webserver configuration.
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

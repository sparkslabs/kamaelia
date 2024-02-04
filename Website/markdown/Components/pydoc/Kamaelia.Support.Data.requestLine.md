---
pagename: Components/pydoc/Kamaelia.Support.Data.requestLine
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Data](/Components/pydoc/Kamaelia.Support.Data.html){.reference}.[requestLine](/Components/pydoc/Kamaelia.Support.Data.requestLine.html){.reference}
===========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Parsing for URI request lines](#50){.reference}
    -   [Example](#51){.reference}
:::

::: {.section}
Parsing for URI request lines {#50}
=============================

This object parses a URI request line, such as those used in HTTP to
request data from a server.

::: {.section}
[Example]{#example} {#51}
-------------------

``` {.literal-block}
>>> r = requestLine("GET http://foo.bar.com/fwibble PROTO/3.3")
>>> print parser.debug__str__()
METHOD          :GET
PROTOCOL        :PROTO
VERSION         :3.3
Req Type        :http
USER            :
PASSWORD        :
DOMAIN          :foo.bar.com
URL             :/fwibble
>>> print r.domain
foo.bar.com
```
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

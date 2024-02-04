---
pagename: Components/pydoc/Kamaelia.File.Reading.FixedRateControlledReusableFileReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[FixedRateControlledReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.FixedRateControlledReusableFileReader.html){.reference}
============================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.Reading.html){.reference}

------------------------------------------------------------------------

::: {.section}
prefab: FixedRateControlledReusableFileReader {#symbol-FixedRateControlledReusableFileReader}
---------------------------------------------

FixedRateControlledReusableFileReader(readmode, rateargs) -\> reusable
file reader component

A file reading component that can be reused. Based on a carousel - send
a filename to the \"next\" or \"inbox\" inboxes to start reading from
that file.

Data is read at the specified rate.

Keyword arguments: - readmode = \"bytes\" or \"lines\" - rateargs =
arguments for ByteRate\_RequestControl component constructor
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

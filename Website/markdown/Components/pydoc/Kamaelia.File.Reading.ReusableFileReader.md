---
pagename: Components/pydoc/Kamaelia.File.Reading.ReusableFileReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[ReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.ReusableFileReader.html){.reference}
======================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.Reading.html){.reference}

------------------------------------------------------------------------

::: {.section}
prefab: ReusableFileReader {#symbol-ReusableFileReader}
--------------------------

ReusableFileReader(readmode) -\> reusable file reader component.

A file reading component that can be reused. Based on a Carousel - send
a filename to the \"next\" inbox to start reading from that file.

Must be prompted by another component - send the number of bytes/lines
to read to the \"inbox\" inbox.

Keyword arguments: - readmode = \"bytes\" or \"lines\"
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

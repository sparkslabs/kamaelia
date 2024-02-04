---
pagename: Components/pydoc/Kamaelia.Support.Data.bitfieldrec
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Data](/Components/pydoc/Kamaelia.Support.Data.html){.reference}.[bitfieldrec](/Components/pydoc/Kamaelia.Support.Data.bitfieldrec.html){.reference}
===========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Bit Field Record Support](#52){.reference}
:::

::: {.section}
Bit Field Record Support {#52}
========================

1.  subclass bfrec

2.  Define a class var \"fields\"

3.  The value for this field should be a list of \"field\"s, created by
    calling the static method field.mkList. This takes a list of tuples,
    one tuple per field. (fieldname, bitwidth, None or list)

    See testBFR for an example.

Usage:

``` {.literal-block}
>> import bitfieldrec
>> bfrec,field = bitfieldrec.bfrec,bitfieldrec.field
>> reload(bitfieldrec)
```

Currently only supports packing. Does not support unpacking (yet).
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

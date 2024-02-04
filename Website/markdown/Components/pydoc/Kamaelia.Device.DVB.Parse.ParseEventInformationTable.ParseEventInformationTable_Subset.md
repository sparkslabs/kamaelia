---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable_Subset
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}.[ParseEventInformationTable\_Subset](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable_Subset.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}

------------------------------------------------------------------------

::: {.section}
prefab: ParseEventInformationTable\_Subset {#symbol-ParseEventInformationTable_Subset}
------------------------------------------

ParseEventInformationTable\_Subset(\[actual\_presentFollowing\]\[,other\_presentFollowing\]\[,actual\_schedule\]\[,other\_schedule\]
) -\> new ParseEventInformationTable component

Returns a ParseEventInformationTable component, configured to parse the
table types specified, and ignore all others.

Keyword arguments:

``` {.literal-block}
- actual_presentFollowing  -- If True, parse 'present-following' data for this multiplex (default=True)
- other_presentFollowing   -- If True, parse 'present-following' data for other multiplexes (default=False)
- actual_schedule          -- If True, parse 'schedule' data for this multiplex (default=False)
- other_schedule           -- If True, parse 'schedule' data for other multiplexes (default=False)
```
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

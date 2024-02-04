---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}
========================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   **[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}**
    (
    [ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable.html){.reference},
    [ParseEventInformationTable\_Subset](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable_Subset.html){.reference},
    [SimplifyEIT](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.SimplifyEIT.html){.reference}
    )
-   **[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}**
    (
    [ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable.html){.reference},
    [ParseNetworkInformationTable\_ActualAndOtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualAndOtherNetwork.html){.reference},
    [ParseNetworkInformationTable\_ActualNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualNetwork.html){.reference},
    [ParseNetworkInformationTable\_OtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_OtherNetwork.html){.reference}
    )
-   **[ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.html){.reference}**
    (
    [ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.ParseProgramAssociationTable.html){.reference}
    )
-   **[ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.html){.reference}**
    (
    [ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.ParseProgramMapTable.html){.reference}
    )
-   **[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}**
    (
    [ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable.html){.reference},
    [ParseServiceDescriptionTable\_ActualAndOtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualAndOtherTS.html){.reference},
    [ParseServiceDescriptionTable\_ActualTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualTS.html){.reference},
    [ParseServiceDescriptionTable\_OtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_OtherTS.html){.reference},
    [SDT\_to\_SimpleServiceList](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.SDT_to_SimpleServiceList.html){.reference}
    )
-   **[ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.html){.reference}**
    (
    [ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.ParseTimeAndDateTable.html){.reference}
    )
-   **[ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.html){.reference}**
    (
    [ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.ParseTimeOffsetTable.html){.reference}
    )
-   **[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}**
    (
    [PrettifyEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyEventInformationTable.html){.reference},
    [PrettifyNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyNetworkInformationTable.html){.reference},
    [PrettifyProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramAssociationTable.html){.reference},
    [PrettifyProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramMapTable.html){.reference},
    [PrettifyServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyServiceDescriptionTable.html){.reference},
    [PrettifyTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeAndDateTable.html){.reference},
    [PrettifyTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeOffsetTable.html){.reference}
    )
-   **[ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}**
    (
    [ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITables.html){.reference},
    [ReassemblePSITablesService](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITablesService.html){.reference}
    )

```{=html}
<!-- -->
```
-   [Components for parsing PSI data in DVB MPEG Transport
    Streams](#483){.reference}
:::

::: {.section}
Components for parsing PSI data in DVB MPEG Transport Streams {#483}
=============================================================

DVB MPEG Transport Streams carry, on certain PIDs, tables of data. Some
tables contain data explaining the structure of services (channels)
being carried, and what PIDs to find their component audio and video
streams being carried in.

Others carry ancilliary data such as electronic programme guide
information and events, or time and date information or the frequencies
on which other multiplexes can be found.

Tables are delivered in \'sections\'.

The parsing process is basically:

> -   Use appropriate
>     [Kamaelia.Device.DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}
>     component(s) to receive and demultiplex and appropriate PID
>     containing table(s) from a broadcast multiplex (transport stream)
> -   Use
>     [Kamaelia.Device.DVB.Parse.ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}
>     to extract the table sections from a stream of TS packets
> -   Feed these raw sections to an appropriate table parsing component
>     to parse the table. These components typically convert the table
>     from its raw binary form to python dictionary based data
>     structures containing the same information, but parsed into a more
>     convenient form.

For a detailed explanation of the purposes and details of tables, see:

-   ISO/IEC 13818-1 (aka \"MPEG: Systems\") \"GENERIC CODING OF MOVING
    PICTURES AND ASSOCIATED AUDIO: SYSTEMS\" ISO / Motion Picture
    Experts Grou7p
-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)
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

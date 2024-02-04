---
pagename: Components/pydoc/Kamaelia.Protocol.RTP.RTCPHeader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}.[RTCPHeader](/Components/pydoc/Kamaelia.Protocol.RTP.RTCPHeader.html){.reference}
==========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [RTP Header](#633){.reference}
:::

::: {.section}
RTP Header {#633}
==========

This class provides a representation of the fixed RTP Headers as per
section 5.1 of RFC1889. The following attributes on an RTPHeader object
represent the fields in the header:

> version,padding, extension, CSRCCount, marker, payloadtype
> sequencenumber, timestamp, SSRC, CSRC

The order of the fields and sizes are defined in the variable
\"struct\".
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

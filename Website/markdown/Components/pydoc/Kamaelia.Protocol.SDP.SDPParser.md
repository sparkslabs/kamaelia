---
pagename: Components/pydoc/Kamaelia.Protocol.SDP.SDPParser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SDP](/Components/pydoc/Kamaelia.Protocol.SDP.html){.reference}.[SDPParser](/Components/pydoc/Kamaelia.Protocol.SDP.SDPParser.html){.reference}
========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.SDP.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SDPParser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SDPParser}
-------------------------------------------------------------------------------------------------

SDPParser() -\> new SDPParser component.

Parses Session Description Protocol data (see RFC 4566) sent to its
\"inbox\" inbox as individual strings for each line of the SDP data.
Outputs a dict containing the parsed data from its \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-SDPParser.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : SDP data in strings, each containing a single line
:::

::: {.section}
### [Outboxes]{#symbol-SDPParser.Outboxes}

-   **outbox** : Parsed SDP data in a dictionary
-   **signal** : Shutdown signalling
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
#### [handleControl(self)]{#symbol-SDPParser.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-SDPParser.main}
:::

::: {.section}
#### [readline(self)]{#symbol-SDPParser.readline}
:::

::: {.section}
#### [sendOutParsedSDP(self, session)]{#symbol-SDPParser.sendOutParsedSDP}
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

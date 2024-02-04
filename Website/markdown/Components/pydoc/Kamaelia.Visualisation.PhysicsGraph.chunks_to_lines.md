---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[chunks\_to\_lines](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [chunks\_to\_lines](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.chunks_to_lines.html){.reference}**
:::

-   [Text line splitter](#444){.reference}
    -   [Example usage](#445){.reference}
    -   [How does it work?](#446){.reference}
:::

::: {.section}
Text line splitter {#444}
==================

This component takes chunks of text and splits them at line breaks into
individual lines.

::: {.section}
[Example usage]{#example-usage} {#445}
-------------------------------

A system that connects to a server and receives fragmented text data,
but then displays it a whole line at a time:

``` {.literal-block}
Pipeline( TCPClient(host=..., port=...),
  chunks_to_lines(),
  ConsoleEcho()
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#446}
--------------------------------------

chunks\_to\_lines buffers all text it receives on its \"inbox\" inbox.
If there is a line break (\"n\") in the text it has buffered, then it
extracts that line of text, including the line break character and sends
it on out of its \"outbox\" outbox.

It also removes any \"r\" characters in the text.

If a producerFinished() or shutdownMicroprocess() message is received on
this component\'s \"control\" inbox, then it will send it on out of its
\"signal\" outbox and immediately terminate. It will not flush any whole
lines of text that may still be buffered.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[chunks\_to\_lines](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.html){.reference}.[chunks\_to\_lines](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.chunks_to_lines.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class chunks\_to\_lines([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-chunks_to_lines}
---------------------------------------------------------------------------------------------------------

chunks\_to\_lines() -\> new chunks\_to\_lines component.

Takes in chunked textual data and splits it at line breaks into
individual lines.

::: {.section}
### [Inboxes]{#symbol-chunks_to_lines.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Chunked textual data
:::

::: {.section}
### [Outboxes]{#symbol-chunks_to_lines.Outboxes}

-   **outbox** : Individual lines of text
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
#### [main(self)]{#symbol-chunks_to_lines.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-chunks_to_lines.shutdown}

Returns True if a shutdownMicroprocess or producerFinished message was
received.
:::
:::

::: {.section}
:::
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

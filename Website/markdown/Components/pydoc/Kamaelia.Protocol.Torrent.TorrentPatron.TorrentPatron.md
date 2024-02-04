---
pagename: Components/pydoc/Kamaelia.Protocol.Torrent.TorrentPatron.TorrentPatron
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent.html){.reference}.[TorrentPatron](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentPatron.html){.reference}.[TorrentPatron](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentPatron.TorrentPatron.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentPatron.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TorrentPatron([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TorrentPatron}
-----------------------------------------------------------------------------------------------------

Inboxes/outboxes and message behaviour identical to TorrentClient but
thread-safe so you can create many of these.

::: {.section}
### [Inboxes]{#symbol-TorrentPatron.Inboxes}

-   **torrent-inbox** : Received feedback from TorrentClient
-   **control** : Shut me down
-   **inbox** : Commands for the TorrentClient
:::

::: {.section}
### [Outboxes]{#symbol-TorrentPatron.Outboxes}

-   **outbox** : Forward feedback from TorrentClient out of
-   **torrent-outbox** : Talk to TorrentClient with
-   **signal** : producerFinished sent when I\'ve shutdown
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
#### [main(self)]{#symbol-TorrentPatron.main}

Main loop of TorrentPatron
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

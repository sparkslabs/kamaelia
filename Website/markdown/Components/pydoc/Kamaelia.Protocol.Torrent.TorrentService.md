---
pagename: Components/pydoc/Kamaelia.Protocol.Torrent.TorrentService
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent.html){.reference}.[TorrentService](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentService.html){.reference}
==============================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TorrentService](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentService.TorrentService.html){.reference}**
:::

-   [BitTorrent Sharing Service](#651){.reference}
    -   [How does it work?](#652){.reference}
:::

::: {.section}
BitTorrent Sharing Service {#651}
==========================

The TorrentService component provides a service that allows the sharing
of a single BitTorrent Client with more than one component that might
want to use it.

Use the TorrentPatron component to make use of BitTorrent through this
service.

Generally, you should not create a TorrentService yourself. If one is
needed, one will be created by TorrentPatron. If a TorrentService
already exists, creating one yourself may crash Python (see the effects
of creating two TorrentClient components in TorrentClient.py)

The shutting down of this component (when it is no longer in use) is
very ugly.

::: {.section}
[How does it work?]{#how-does-it-work} {#652}
--------------------------------------

This component forwards messages from TorrentPatrons to a single
TorrentClient it creates and also delivers responses from TorrentClient
to the TorrentPatron appropriate to the response content.

TorrentClient handles new torrent requests sequentially, so as long as
we keep a record of what order the requests of TorrentPatrons were
forwarded, we can work out who to send TorrentClient\'s response to.
Then, since all further messages are assigned a torrentid by
TorrentClient, we can route all messages labelled with a particular id
to to the TorrentPatron that started that torrent.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent.html){.reference}.[TorrentService](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentService.html){.reference}.[TorrentService](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentService.TorrentService.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class TorrentService([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-TorrentService}
----------------------------------------------------------------------------------------------------------------------------------------------------------

TorrentService() -\> new TorrentService component

Use TorrentService.getTorrentService(\...) in preference as it returns
an existing instance, or automatically creates a new one.

::: {.section}
### [Inboxes]{#symbol-TorrentService.Inboxes}

-   **control** : Recieving a
    [Axon.Ipc.shutdown](/Docs/Axon/Axon.Ipc.shutdown.html){.reference}()
    message here causes shutdown
-   **\_torrentcontrol** : Notice that TorrentClient has shutdown
-   **inbox** : Connects to TorrentClient (the BitTorrent code)
-   **notify** : Used to be notified about things to select
:::

::: {.section}
### [Outboxes]{#symbol-TorrentService.Outboxes}

-   **debug** : Information that may aid debugging
-   **outbox** : Connects to TorrentClient (the BitTorrent code)
-   **signal** : Not used
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
#### [\_\_init\_\_(self)]{#symbol-TorrentService.__init__}
:::

::: {.section}
#### [addClient(self, replyService)]{#symbol-TorrentService.addClient}

Registers a TorrentPatron with this service, creating an outbox
connected to it
:::

::: {.section}
#### [debug(self, msg)]{#symbol-TorrentService.debug}
:::

::: {.section}
#### [initTorrentClient(self)]{#symbol-TorrentService.initTorrentClient}
:::

::: {.section}
#### [main(self)]{#symbol-TorrentService.main}

Main loop
:::

::: {.section}
#### [removeClient(self, replyService)]{#symbol-TorrentService.removeClient}

Deregisters a TorrentPatron with this service, deleting its outbox
:::

::: {.section}
#### [sendToClient(self, msg, replyService)]{#symbol-TorrentService.sendToClient}

Send a message to a TorrentPatron
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

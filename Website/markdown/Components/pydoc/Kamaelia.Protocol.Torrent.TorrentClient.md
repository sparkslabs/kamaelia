---
pagename: Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent.html){.reference}.[TorrentClient](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.html){.reference}
============================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [BasicTorrentExplainer](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.BasicTorrentExplainer.html){.reference}**
-   **component
    [TorrentClient](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.TorrentClient.html){.reference}**
:::

-   [TorrentClient - a BitTorrent Client](#656){.reference}
    -   [Use TorrentPatron instead!](#657){.reference}
    -   [How does it work?](#658){.reference}
:::

::: {.section}
TorrentClient - a BitTorrent Client {#656}
===================================

This component is for downloading and uploading data using the
peer-to-peer BitTorrent protocol. You MUST have the Mainline (official)
BitTorrent client installed for any BitTorrent stuff to work in
Kamaelia.

NOTE: This code has only been successfully tested with version 4.20.8.
Problems have been experienced with other more recent versions regarding
a missing or misplaced language translations file. See
<http://download.bittorrent.com/dl/?M=D> and download the appropriate
version 4.20.8 package for for your platform.

::: {.section}
[Use TorrentPatron instead!]{#use-torrentpatron-instead} {#657}
--------------------------------------------------------

I should start by saying \"DO NOT USE THIS COMPONENT YOURSELF\"!

This component wraps the Mainline (official) BitTorrent client, which
unfortunately is not thread-safe (at least with the latest version -
4.20). If you run two instances of this client simultaneously, Python
will die with an exception, or if you\'re really unlucky, a segfault.

But despair not! There is a solution - use TorrentPatron instead.
TorrentPatrons will organise the sharing of a single TorrentClient
amongst themselves and expose exactly the same interface (except that
the tickInterval optional argument cannot be set) with the key advantage
that you can run as many of them as you want.

For a description of the interfaces of TorrentClient see TorrentPatron
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#658}
--------------------------------------

TorrentClient is a threadedcomponent that uses the libraries of the
Mainline (official) BitTorrent client to provide BitTorrent
functionality. As Mainline was designed to block (use blocking function
calls) this makes it incompatible with the normal structure of an
[Axon](/Docs/Axon/Axon.html){.reference} component - it cannot yield
regularly. As such it uses a threadedcomponent, allowing it to block
with impunity.

Each torrent is assigned a unique id (currently equal to the count of
torrents seen but don\'t rely on it). Inboxes are checked periodically
(every tickInterval seconds, where tickInterval is 5 by default)
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent.html){.reference}.[TorrentClient](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.html){.reference}.[BasicTorrentExplainer](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.BasicTorrentExplainer.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: BasicTorrentExplainer {#symbol-BasicTorrentExplainer}
-----------------------------

BasicTorrentExplainer is component useful for debugging
TorrentClient/TorrentPatron. It converts each torrent IPC messages it
receives into human readable lines of text.
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent.html){.reference}.[TorrentClient](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.html){.reference}.[TorrentClient](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.TorrentClient.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class TorrentClient([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-TorrentClient}
-------------------------------------------------------------------------------------------------------------------------------------

TorrentClient(\[tickInterval\]) -\> component capable of
downloading/sharing torrents.

Initialises the Mainline client. Uses threadedcomponent so it doesn\'t
have to worry about blocking I/O or making Mainline yield periodically.

Keyword arguments:

-   tickInterval \-- the interval in seconds at which TorrentClient
    checks inboxes (default=5)

::: {.section}
### [Inboxes]{#symbol-TorrentClient.Inboxes}

-   **control** : Shut me down
-   **inbox** : Torrent IPC - add a torrent, stop a torrent etc.
:::

::: {.section}
### [Outboxes]{#symbol-TorrentClient.Outboxes}

-   **outbox** : Torrent IPC - status updates, completion, new torrent
    added etc.
-   **signal** : Say when I\'ve shutdown
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
#### [\_\_init\_\_(self\[, tickInterval\])]{#symbol-TorrentClient.__init__}
:::

::: {.section}
#### [\_create\_torrent(self, metainfo, save\_incomplete\_as, save\_as)]{#symbol-TorrentClient._create_torrent}
:::

::: {.section}
#### [\_start\_torrent(self, metainfo, torrentid)]{#symbol-TorrentClient._start_torrent}
:::

::: {.section}
#### [decodeTorrent(self, data)]{#symbol-TorrentClient.decodeTorrent}

Converts bencoded raw metadata (as one would find in a .torrent file)
into a metainfo object (which one can then get the torrent\'s properties
from).
:::

::: {.section}
#### [handleMessages(self)]{#symbol-TorrentClient.handleMessages}
:::

::: {.section}
#### [main(self)]{#symbol-TorrentClient.main}

Start the Mainline client and block indefinitely, listening for
connectons.
:::

::: {.section}
#### [sendStatusUpdates(self)]{#symbol-TorrentClient.sendStatusUpdates}

Send a TIPCTorrentStatusUpdate for each running torrent.
:::

::: {.section}
#### [startTorrent(self, metainfo, save\_incomplete\_as, save\_as, torrentid)]{#symbol-TorrentClient.startTorrent}

startTorrent causes MultiTorrent to begin downloading a torrent
eventually. Use it instead of \_start\_torrent as it retries repeatedly
if Mainline is busy.
:::

::: {.section}
#### [tick(self)]{#symbol-TorrentClient.tick}

Called periodically\... by itself (gets rawserver to call it back after
a delay of tickInterval seconds). Checks inboxes and sends a
status-update message for every active torrent.
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

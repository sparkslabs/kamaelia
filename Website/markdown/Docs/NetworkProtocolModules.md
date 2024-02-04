---
pagename: Docs/NetworkProtocolModules
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Network Protocol Modules]{style="font-size: 24pt; font-weight: 600;"}
======================================================================

[Kamaelia.Protocol](/Components/pydoc/Kamaelia.Protocol)

-   AudioCookieProtocol\
-   EchoProtocol
-   FortuneCookieProtocol
-   HTTP
-   RTP
-   SimpleReliableMulticast
-   SimpleVideoCookieServer
-   Torrent (bittorrent)

**Echo protocol and Fortune Cookies**\

[EchoProtocol](/Components/pydoc/Kamaelia.Protocol.EchoProtocol) is the
simplest protocol and forms a simple loopback protocol useful for
integration testing. In practice this component is really a [data pass
through ]{style="font-style: italic;"}component since all data recieved
on its inbox is passed on directly to its outbox.
[Kamaelia.Util.PassThrough](/Components/pydoc/Kamaelia.Util.PassThrough)
is a similar component.

[FortuneCookieProtocol](/Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol)
is one step above EchoProtocol. It runs the fortune program on the
server and sends the result to its outbox. In a networked environment
what this means is the server will simply blat the fortune cookie to a
client that connects to the server.

[AudioCookieProtocol](/Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol)
is a further logical extension. Similar to FortuneCookieProtocol it too
runs an external program and sends the result to its outbox. In this
case however rather than a short piece of text, it is a short snippet of
audio.\

[SimpleVideoCookieServer](/Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer)
is essentially the same but his time with a short piece of video.\

**HTTP**\

-   [Kamaelia.Protocol.HTTP.HTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient)
-   [Kamaelia.Protocol.HTTP.HTTPServer](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer)
-   [Kamaelia.Protocol.HTTP.IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient)
    (SHOUTcast)\

[Kamaelia.Protocol.HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP) is a
collection of components implementing an extensible HTTP server and an
HTTP Client. There is also an implementation of a SHOUTcast/Icecast
client.\

**RTP**

[Kamaelia.Protocol.RTP](/Components/pydoc/Kamaelia.Protocol.RTP) is a
set of modules for implementing RTP.\

**Simple Reliable Multicast**

[Kamaelia.Protocol.SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast)
module contains a simple collection of components that can be pipelined
together to create a simple protocol for reliable transfer of data over
multicast - designed to cope with duplicated, lost and
delivered-out-of-order packets.\

**Bit Torrent**

[Kamaelia.Protocol.Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent)
is a set of modules that wrap the mainline bittorrent code adding
bit-torrent components to Kamaelia. Specifically the
[TorrentPatron](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentPatron)
component provided shared access to bittorrent functionality.\
**\
Support: Packetisation, Framing, MIME types, etc**

-   [Kamaelia.Protocol.Framing](/Components/pydoc/Kamaelia.Protocol.Framing)
-   [Kamaelia.Protocol.MimeRequestComponent](/Components/pydoc/Kamaelia.Protocol.MimeRequestComponent)
-   [Kamaelia.Protocol.Packetise](/Components/pydoc/Kamaelia.Protocol.Packetise)

These components don\'t implement fully fledged protocols, but provide
useful support that many protocols may wish to use.\

The [Framing](/Components/pydoc/Kamaelia.Protocol.Framing) module
contains components that implement a simple protocol for framing chunks
of data and combining them with an associated \'tag\' - making it easy
to add things like sequence numbers to a stream of chunks of data.

[MimeRequestComponent](/Components/pydoc/Kamaelia.Protocol.MimeRequestComponent)
module unpacks MIME request headers into a python dict object.

[Packetise](/Components/pydoc/Kamaelia.Protocol.Packetise) contains a
simple component for ensuring that data chunks do not exceed a specified
size - particularly useful, for example, for ensuring UDP payloads fit
within a packet size limit.\

\

\-- Michael, December 2004; updated by Matt, April 2007\

\

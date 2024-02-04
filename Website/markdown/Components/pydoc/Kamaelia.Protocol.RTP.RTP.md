---
pagename: Components/pydoc/Kamaelia.Protocol.RTP.RTP
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.html){.reference}
============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [RTPDeframer](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPDeframer.html){.reference}**
-   **component
    [RTPFramer](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPFramer.html){.reference}**
:::

-   [RTP Packet Framing and Deframing](#636){.reference}
    -   [Example Usage](#637){.reference}
    -   [RTPFramer behaviour](#638){.reference}
    -   [RTPDeframer Behaviour](#639){.reference}
:::

::: {.section}
RTP Packet Framing and Deframing {#636}
================================

Send a dict specifying what needs to go into the RTP packet and
RTPFramer will output it as a RTP frame.

RTPDeframer parses an RTP packet in binary string format and outputs a
(seqnum, packet) tuple containing a sequence number and a dict structure
containing the payload and metadata of the RTP packet. The format is the
same as that used by RTPFramer.

These components simply format the data into the RTP packet format or
take it back out again. They do not understand the specifics of each
payload type. You must determine for yourself the correct values for
each field (eg. payload type, timestamps, CSRCS, etc).

See [RFC 3550](http://tools.ietf.org/html/rfc3550){.reference} and [RFC
3551](http://tools.ietf.org/html/rfc3551){.reference} for information on
the RTP speecification and the meaning and formats of fields in RTP
packets.

::: {.section}
[Example Usage]{#example-usage} {#637}
-------------------------------

Read MPEG Transport Stream packets (188 bytes each) from a file in
groups of 7 at a time (to fill an RTP packet) and send them in RTP
packets over multicast to 224.168.2.9 on port 1600:

``` {.literal-block}
class PrePackage(Axon.Component.component):
    def main(self):
        SSRCID = random.randint(0,(2**32) - 1)      # random unique ID for this source
        while 1:
            while self.dataReady("inbox"):
                recvData = self.recv("inbox")
                self.send(
                  { 'payloadtype' : 33,             # type 33 for MPEG 2 TS
                    'payload'     : recvData,
                    'timestamp'   : time.time() * 90000,
                    'ssrc'        : SSRCID,
                  },
                  "outbox")
            yield 1


Pipeline( RateControlledFileReader("transportstream",chunksize=7*188),
          PrePackage(),
          RTPFramer(),
          Multicast_Transceiver(("0.0.0.0", 0, "224.168.2.9", 1600)
```

Timestamps for MPEG TS in RTP are integers at 90KHz resolution (hence
the x90000 scaling factor). A random value is chosen for the unique
source identifier (ssrc).

Save the payload from a stream of RTP packets being received from
multicast address 224.168.2.9 on port 1600 down to a file:

``` {.literal-block}
Pipeline( Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
          SimpleDetupler(1),                      # discard the source address
          RTPDeframer(),
          RecoverOrder(bufsize=64, modulo=65536), # reorder packets
          SimpleDetupler(1),                      # discard the sequence number
          SimpleDetupler("payload"),
          SimpleFileWriter("received_stream"),
        )
```
:::

::: {.section}
[RTPFramer behaviour]{#rtpframer-behaviour} {#638}
-------------------------------------------

Send to RTPFramer\'s \"inbox\" inbox a dictionary. It must contain these
fields:

``` {.literal-block}
{
    'payloadtype' : integer payload type
    'payload'     : binary string containing the payload
    'timestamp'   : integer timestamp (32 bit, unsigned)
    'ssrc'        : sync source identifier (32 bit, unsigned)
```

\...and these fields are optional:

``` {.literal-block}
    'csrcs'        : list of contributing source identifiers (default = [])
    'bytespadding' : number of bytes of padding to be added to the payload (default=0)
    'extension'    : binary string of any extension data (default = "")
    'marker'       : True to set the marker bit, otherwise False (default=False)
}
```

RTPFramer automatically adds a randomised offset to the timestamp, and
generates the RTP packet sequence numbers, as required in the
specification (RFC 3550).

RTPFramer constructs an RTP packet matching the fields specified and
sends it as a binary string out of the \"outbox\" outbox.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It is immediately sent on out of the \"signal\"
outbox and the component then immediately terminates.
:::

::: {.section}
[RTPDeframer Behaviour]{#rtpdeframer-behaviour} {#639}
-----------------------------------------------

Send to RTPDeframer\'s \"inbox\" inbox a binary string of an RTP packet,
and the packet will be parsed, resulting in a (seqnum, packet\_contents)
tuple being sent to the \"outbox\" outbox. It will have this structure:

``` {.literal-block}
( sequence_number,
  {
    'payloadtype'  : integer payload type
    'payload'      : binary string containing the payload
    'timestamp'    : integer timestamp (32 bit, unsigned)
    'ssrc'         : sync source identifier (32 bit, unsigned)
    'csrcs'        : list of contributing source identifiers, [] if empty
    'extension'    : binary string of any extension data, "" if none
    'marker'       : True if marker bit was set, otherwise False
  }
)
```

See RFC 3550 for an explanation of the precise purposes of these fields.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It is immediately sent on out of the \"signal\"
outbox and the component then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.html){.reference}.[RTPDeframer](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPDeframer.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class RTPDeframer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RTPDeframer}
---------------------------------------------------------------------------------------------------

RTPDeframer() -\> new RTPDeframer component.

Deconstructs an RTP packet, outputting (seqnum, dict) tuple where seqnum
is for recovering the order of packets, and dict contains the fields
from the RTP packet.

::: {.section}
### [Inboxes]{#symbol-RTPDeframer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RTPDeframer.Outboxes}
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
#### [main(self)]{#symbol-RTPDeframer.main}
:::

::: {.section}
#### [parsePacket(self, packet)]{#symbol-RTPDeframer.parsePacket}
:::

::: {.section}
#### [shutdown(self)]{#symbol-RTPDeframer.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}.[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.html){.reference}.[RTPFramer](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPFramer.html){.reference}
================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class RTPFramer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RTPFramer}
-------------------------------------------------------------------------------------------------

RTPFramer() -\> new RTPFramer component.

Creates a complete RTP packet based on a dict structure describing the
packet.

::: {.section}
### [Inboxes]{#symbol-RTPFramer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RTPFramer.Outboxes}
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
#### [constructPacket(self, content)]{#symbol-RTPFramer.constructPacket}
:::

::: {.section}
#### [main(self)]{#symbol-RTPFramer.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-RTPFramer.shutdown}
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

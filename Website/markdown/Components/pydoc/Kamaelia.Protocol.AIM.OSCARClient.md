---
pagename: Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}
============================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARClient.html){.reference}**
-   **component
    [OSCARProtocol](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARProtocol.html){.reference}**
-   **component
    [SNACExchanger](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger.html){.reference}**
:::

-   [Kamaelia OSCAR interface](#613){.reference}
    -   [Explanation of Terms](#614){.reference}
    -   [How does it work?](#615){.reference}
    -   [Example Usage](#616){.reference}
:::

::: {.section}
Kamaelia OSCAR interface {#613}
========================

NOTE: These components implement the OSCAR protocol at the lowest level
and require a fairly good knowledge of OSCAR to use them. For a
high-level interface, see AIMHarness.py.

-   The OSCARProtocol component provides a Kamaelia interface for the
    FLAP level of OSCAR protocol. You should not be linking to
    OSCARProtocol directly, but to OSCARClient.
-   The OSCARClient prefab returns an OSCARProtocol component wired up
    to a TCPClient.
-   SNACExchanger is the base class for all components that deal with
    the SNAC layer of OSCAR protocol.

::: {.section}
[Explanation of Terms]{#explanation-of-terms} {#614}
---------------------------------------------

NOTE: A \"byte\" in the following documentation refers to an ASCII char,
an unsigned char in C.

OSCAR messages are transmitted in discrete units called FLAPs, which
take the following form:

``` {.literal-block}
-------------------------------------------
|FLAP-header                              |
|   message start character (*) -- 1 byte |
|   channel -- 1 byte                     |
|   sequence number -- 2 bytes            |
|   length of following data -- 2 bytes   |
|-----------------------------------------|
| ------------                            |
||FLAP payload|                           |
| ------------                            |
-------------------------------------------
```

The sequence number is incremented with every FLAP sent. AOL is very
strict about in-order sequence numbers and servers may even disconnect a
client for not sending the right sequence numbers.

The majority of FLAP payloads (everything except new connection
notifications, really serious errors, shutdown notifications, and
keepalives) are units called SNACs and are transmitted over channel 2.

The structure of a SNAC:

``` {.literal-block}
--------------------------
|SNAC-header             |
|  family -- 2 bytes     |
|  subtype -- 2 bytes    |
|  request ID -- 2 bytes |
|  flags -- 4 bytes      |
|------------------------
|  --------------        |
| | SNAC payload |       |
|  --------------        |
--------------------------
```

All SNAC payloads must follow a prescribed format unique to the
particular type of SNAC, but all SNAC headers must follow the format
described above. Each different (family, subtype) performs a different
function. For example, SNAC (04, 07) (meaning family 0x04, subtype 0x07)
carries AIM messages from the server to the client, SNAC (01, 11)
reports client idle times to the server, and (04, 06) carries a message
from one user to another.

Yet another type of OSCAR datatype is a type-length-value (TLV) unit.

The structure of a TLV:

``` {.literal-block}
------------------------------------------
|TLV-header                              |
|   type -- 2 bytes                      |
|   length of following data -- 2 bytes  |
|----------------------------------------|
|  ---------                             |
| |TLV data |                            |
|  ---------                             |
-----------------------------------------
```

TLVs may appear inside SNACs or just inside FLAPs.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#615}
--------------------------------------

OSCARProtocol receives messages on its \"talk\" inbox in (channel, flap
body) format and retransmits them to \"outbox\" as true FLAPs. It
receives FLAPs on its \"inbox\" inbox and retransmits them to its
\"heard\" outbox in the format (channel, flap body). It also keeps track
of sequence numbers.

OSCARClient returns a Graphline with an OSCARProtocol component\'s
inbox/outbox connected to a TCPClient\'s outbox/inbox. The Graphline\'s
inbox and outbox are l inked to the OSCARProtocol component\'s \"talk\"
and \"heard\" boxes, respectively. Send (channel, flap body) tuples to
its inbox and receive (channel, flap body) tuples from the outbox.

SNACExchanger provides specialized methods for dealing with SNACs. You
must subclass it, as it does not have a main method.
:::

::: {.section}
[Example Usage]{#example-usage} {#616}
-------------------------------

To get an MD5 key from the authorization server during login:

``` {.literal-block}
class LoginHandler(SNACExchanger):
    def main(self):
        self.send((CHANNEL_NEWCONNECTION,
                   struct.pack('!i', 1)))
        while not self.dataReady():
            yield 1
        reply = self.recv() # server ack of new connection
        zero = struct.pack('!H', 0)
        request = TLV(0x01, "kamaelia1") + TLV(0x4b, zero) + TLV(0x5a, zero)
        self.sendSnac(0x17, 0x06, request)
        for reply in self.waitSnac(0x17, 0x07): yield 1
        md5key = reply[2:]
        print ("%02x " * len(md5key)) % unpackSingles(md5key)

Graphline(osc = OSCARClient('login.oscar.aol.com', 5190),
          login = LoginHandler(),
          linkages = {("login", "outbox") : ("osc", "inbox"),
                      ("osc", "outbox") : ("login", "inbox"),
                      }
          ).run()
```

For a more complete example, see LoginHandler.py
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}.[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARClient.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: OSCARClient {#symbol-OSCARClient}
-------------------

OSCARClient(server, port) -\> returns an OSCARProtocol component
connected to a TCPClient.

User input goes into OSCARClient\'s \"inbox\" in the form (channel, flap
body) and useable output comes out of \"outbox\" in the same form.
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}.[OSCARProtocol](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARProtocol.html){.reference}
================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class OSCARProtocol([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-OSCARProtocol}
-----------------------------------------------------------------------------------------------------

OSCARProtocol() -\> new OSCARProtocol component.

Provides a Kamaelia interface to the lowest level of OSCAR protocol, the
FLAP level.

For more information on FLAPs, see module level docs.

::: {.section}
### [Inboxes]{#symbol-OSCARProtocol.Inboxes}

-   **control** : shutdown handling
-   **inbox** : receives binary data from the AIM server
-   **talk** : receives messages in the format (channel, FLAP payload)
:::

::: {.section}
### [Outboxes]{#symbol-OSCARProtocol.Outboxes}

-   **outbox** : sends binary data to the AIM server.
-   **signal** : shutdown handling
-   **heard** : resends messages from \'outbox\' in the form (channel,
    FLAP payload)
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
#### [\_\_init\_\_(self)]{#symbol-OSCARProtocol.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkBoxes(self)]{#symbol-OSCARProtocol.checkBoxes}

checks for data in all our boxes, and if there is data, then call the
appropriate function to handle it.
:::

::: {.section}
#### [handlecontrol(self)]{#symbol-OSCARProtocol.handlecontrol}
:::

::: {.section}
#### [handleinbox(self)]{#symbol-OSCARProtocol.handleinbox}

receives data coming in through the wire, reformats it into a
Python-friendly form, and retransmits it to its \"heard\" outbox.
:::

::: {.section}
#### [handletalk(self)]{#symbol-OSCARProtocol.handletalk}

checks that incoming messages from the \"talk\" inbox are in a (channel,
flap data) tuple. If not, exceptions are raised. If so,
OSCARProtocol.sendFLAP is called.
:::

::: {.section}
#### [main(self)]{#symbol-OSCARProtocol.main}

main loop
:::

::: {.section}
#### [sendFLAP(self, data\[, channel\])]{#symbol-OSCARProtocol.sendFLAP}

constructs FLAPs and sends them
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}.[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}.[SNACExchanger](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger.html){.reference}
================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SNACExchanger([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SNACExchanger}
-----------------------------------------------------------------------------------------------------

SNACExchanger() -\> component that has methods specialized for sending
and receiving FLAPs over Channel 2 (FLAPs whose payloads are SNACs).

For a more thorough discussion on SNACs, see module level docs.

::: {.section}
### [Inboxes]{#symbol-SNACExchanger.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SNACExchanger.Outboxes}
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
#### [\_\_init\_\_(self)]{#symbol-SNACExchanger.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [recvSnac(self)]{#symbol-SNACExchanger.recvSnac}

receives FLAPs containing SNACs and parses the SNAC data.
:::

::: {.section}
#### [sendSnac(self, fam, sub, body)]{#symbol-SNACExchanger.sendSnac}

constructs a SNAC by calling self.makeSnac and sends it out the
\"outbox\".

FIXME: It would be extremely helpful to have a predefined set of SNAC
constants or perhaps even classes to pass to this method. For example,
self.sendSnac(04, 06, data) is a lot less clear than something like
self.sendSnac(MESSAGE\_TO\_USER, data).
:::

::: {.section}
#### [waitSnac(self, fam, sub)]{#symbol-SNACExchanger.waitSnac}

Yields 1 until a SNAC of the requested family and subtype is received.
The last value yielded is the payload of the requested SNAC.

Usage::
:   for result in self.waitSnac(family, subtype): yield 1.

The body of the requested SNAC will be assigned to \"result\".
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

---
pagename: Components/pydoc/Kamaelia.Protocol.SDP
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SDP](/Components/pydoc/Kamaelia.Protocol.SDP.html){.reference}
========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SDPParser](/Components/pydoc/Kamaelia.Protocol.SDP.SDPParser.html){.reference}**
:::

-   [Session Description Protocol (SDP) Support](#609){.reference}
    -   [Example Usage](#610){.reference}
    -   [Behaviour](#611){.reference}
    -   [Format of parsed output](#612){.reference}
:::

::: {.section}
Session Description Protocol (SDP) Support {#609}
==========================================

The SDPParser component parses Session Description Protocol (see [RFC
4566](http://tools.ietf.org/html/rfc4566){.reference}) data sent to it
as individual lines of text (not multiline strings) and outputs a
dictionary containing the parsed session description.

::: {.section}
[Example Usage]{#example-usage} {#610}
-------------------------------

Fetch SDP data from a URL, parse it, and display the output:

``` {.literal-block}
Pipeline( OneShot("http://www.mysite.com/sessiondescription.sdp"),
          SimpleHTTPClient(),
          chunks_to_lines(),
          SDPParser(),
          ConsoleEchoer(),
        ).run()
```

If the session description at the URL provided is this:

``` {.literal-block}
v=0
o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5
s=SDP Seminar
i=A Seminar on the session description protocol
u=http://www.example.com/seminars/sdp.pdf
e=j.doe@example.com (Jane Doe)
c=IN IP4 224.2.17.12/127
t=2873397496 2873404696
a=recvonly
m=audio 49170 RTP/AVP 0
m=video 51372 RTP/AVP 99
a=rtpmap:99 h263-1998/90000
```

Then parsing will return this dictionary:

``` {.literal-block}
{ 'protocol_version': 0,
  'origin'     : ('jdoe', 2890844526, 2890842807, 'IN', 'IP4', '10.47.16.5'),
  'sessionname': 'SDP Seminar',
  'information': 'A Seminar on the session description protocol',
  'connection' : ('IN', 'IP4', '224.2.17.12', '127', 1),
  'time'       : [(2873397496L, 2873404696L, [])],
  'URI'        : 'http://www.example.com/seminars/sdp.pdf',
  'email'      : 'j.doe@example.com (Jane Doe)',
  'attribute'  : ['recvonly'],
  'media':
      [ { 'media'     : ('audio', 49170, 1, 'RTP/AVP', '0'),
          'connection': ('IN', 'IP4', '224.2.17.12', '127', 1)
        },
        { 'media'     : ('video', 51372, 1, 'RTP/AVP', '99'),
          'connection': ('IN', 'IP4', '224.2.17.12', '127', 1),
          'attribute' : ['rtpmap:99 h263-1998/90000']
        }
      ],
}
```
:::

::: {.section}
[Behaviour]{#behaviour} {#611}
-----------------------

Send individual lines as strings to SDPParser\'s \"inbox\" inbox.
SDPParser cannot handle multiple lines in the same string.

When SDPParser receives a producerFinished() message on its \"control\"
inbox, or if it encounter another \"v=\" line then it knows it has
reached the end of the SDP data and will output the parsed data as a
dictionary to its \"outbox\" outbox.

The SDP format does *not* contain any kind of marker to signify the end
of a session description - so SDPParser only deduces this by being told
that the producer/data source has finished, or if it encounters a \"v=\"
line indicating the start of another session description.

SDPParser can parse more than one session description, one after the
other.

If the SDP data is malformed AssertionError, or other exceptions, may be
raised. SDPParser does not rigorously test for exact compliance - it
just complains if there are glaring problems, such as fields appearing
in the wrong sections!

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox then, once any pending data at the \"inbox\" inbox has
been processed, this component will terminate. It will send the message
on out of its \"signal\" outbox.

Only if the message is a producerFinished message will it output the
session description is has been parsing. A shutdownMicroprocess message
will not result in it being output.
:::

::: {.section}
[Format of parsed output]{#format-of-parsed-output} {#612}
---------------------------------------------------

The result of parsing SDP data is a dictionary mapping descriptive names
of types to values:

> Session Description
:::
:::
:::

Type

Dictionary key

Format of the value

v

\"protocol\_version\"

version\_number

o

\"origin\"

(\"user\", session\_id, session\_version, \"net\_type\", \"addr\_type\",
\"addr\")

s

\"sessionname\"

\"session name\"

t & r

\"time\"

(starttime, stoptime, \[repeat,repeat, \...\])
:   where repeat = (interval,duration,\[offset,offset, \...\])

a

\"attribute\"

\"value of attribute\"

b

\"bandwidth\"

(mode, bitspersecond)

i

\"information\"

\"value\"

e

\"email\"

\"email-address\"

u

\"URI\"

\"uri\"

p

\"phone\"

\"phone-number\"

c

\"connection\"

(\"net\_type\", \"addr\_type\", \"addr\", ttl, groupsize)

z

\"timezone adjustments\"

\[(adj-time,offset), (adj-time,offset), \...\]

k

\"encryption\"

(\"method\",\"value\")

m

\"media\"

\[media-description, media-description, \... \]
:   see next table for media description structure

Note that \'t\' and \'r\' lines are combined in the dictionary into a
single \"time\" key containing both the start and end times specified in
the \'t\' line and a list of any repeats specified in any \'r\' lines
present.

The \"media\" key contains a list of media descriptions. Like for the
overall session description, each is parsed into a dictionary, that will
contain some or all of the following:

> Media Descriptions

Type

Dictionary key

Format of the value

m

\"media\"

(\"media-type\", port-number, number-of-ports, \"protocol\", \"format\")

c

\"connection\"

(\"net\_type\", \"addr\_type\", \"addr\", ttl, groupsize)

b

\"bandwidth\"

(mode, bitspersecond)

i

\"information\"

\"value\"

k

\"encryption\"

(\"method\",\"value\")

a

\"attribute\"

\"value of attribute\"

Some lines are optional in SDP. If they are not included, then the
parsed output will not contain the corresponding key.

The formats of values are left unchanged by the parsing. For example,
integers representing times are simply converted to integers, but the
units used remain unchanged (ie. they will not be converted to unix time
units).

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SDP](/Components/pydoc/Kamaelia.Protocol.SDP.html){.reference}.[SDPParser](/Components/pydoc/Kamaelia.Protocol.SDP.SDPParser.html){.reference}
========================================================================================================================================================================================================================================================================

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

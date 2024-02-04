---
pagename: SimpleReliableMulticast
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Protocol: Simple Reliable
Multicast]{style="font-size:24pt;font-weight:600"}

This page describes a simple protocol overlaid on top of multicast to
give a thin layer of reliability. It is [not
]{style="font-weight:600"}intended to replace existing reliable
multicast protocols, but to show how they can be developed and
integrated into a Kamaelia based system. For the basis of this
discussion it is referred to here generally as SRM - simply short for
\"Simple Reliable Multicast\".

[Background]{style="font-weight:600"}

Multicast is an unreliable protocol. It is also rarely implemented over
the wide area internet, despite its age and only slightly more often
inside company networks. However where it is available - such as the
BBC\'s trial multicast peering system used for the 2004 Olympics and
others - it provides the benefit that broadcast television can be made
available over the internet. (Note: multicast is
[not]{style="font-style:italic"} broadcast - the \"multi\" part denotes
that [anyone]{style="font-style:italic"} may send and receive, not just
one source)

As well as a lack of deployment multicast has a number of specific
characteristics that cause problems for any protocol you wish to send
over multicast:

-   It does not guarantee delivery. Indeed due to it\'s nature it
    [may]{style="font-style:italic"} be considered to have a lesser
    likelihood of delivery than plain UDP. Why? Because if I send you a
    UDP packet there is a good chance, unless you\'re behind a NAT\'ing
    firewall, and possibly even then, that you will receive it. If
    however I send you a multicast packet, there are many more obstacles
    along the way to stop a packet reaching you.
-   It does not guarantee order of delivery.
-   We do not generally speaking have the ability to say \"please
    resend\" (which we can manually do with plain UDP, and TCP does
    automatically). If we try, we risk something called a \"NAK
    implosion\". That is a very large number of
    \"[N]{style="font-weight:600"}egative
    [A]{style="font-weight:600"}c[K]{style="font-weight:600"}nowldgements\"
    coming in at once. It\'s essentially like broadcasting BBC1, having
    a momentary power glitch and the entire audience of 10 million
    people phoning in to say \"there was a glitch\" - it\'s an approach
    that simply doesn\'t scale.

As a result we need a system that can essentially perform a \"as good as
it can\" attempt at cleaning up the resulting \"mess\" we are left with.
This might seem strong words, but even over a wireless link inside the
home sending multicast data from one room to another can result in all 3
of these issues interfering heavily with any higher level protocol.

[Example Setup]{style="font-weight:600"}

Take Example 4 - a simple multicast system for example. This contains a
system version with the following two pipelines:

Server:

<div>

[pipeline(]{style="font-family:Courier"}

</div>

<div>

[)]{style="font-family:Courier"}

</div>

Client:

<div>

[pipeline(]{style="font-family:Courier"}

</div>

<div>

[)]{style="font-family:Courier"}

</div>

(I\'ve removed the calls to these pipelines\' .activate() and .run()
methods)

Running these together on a single host (eg via the
[MulticastStreamingSystem.py]{style="font-style:italic"} script
provided) results in the single file being transmitted, and recieved and
played back. However if we split this across two scripts, run one on a
server machine, one on a client and place an unreliable network in
between (such as an 802.11b network), then we instantly hit audio
problems due to out of order delivery and data loss.

[Protocol Design]{style="font-weight:600"}

The protocol does the following:

-   Attempt to detect and skip data loss.
-   Be able to inform of data loss
-   Aim to be able to resync to any framing the application chooses.
-   Aim to be able to perform out of order delivery correction within a
    limited window of correction
-   Assume that the data it is sending is non-terminating

The protocol will [not do ]{style="font-weight:600"}the following:

-   Aim to correct data
-   Aim to fill in missing data
-   Provide a mechanism for indicating \"end of stream\". This is up to
    a higher layer to decide.

[Usage]{style="font-weight:600"}

The directory containing Example 4 now also contains an SRM based
version called [MulticastStreamingSystem\_SRM.py
]{style="font-style:italic"}. The client and server pipelines now looks
like this: (additions in [bold
blue]{style="font-family:Courier;font-weight:600;color:#0000cc"})

Client:

<div>

[pipeline(]{style="font-family:Courier"}

</div>

<div>

[)]{style="font-family:Courier"}

</div>

Server:

<div>

[pipeline(]{style="font-family:Courier"}

</div>

<div>

[)]{style="font-family:Courier"}

</div>

[Underlying Approach]{style="font-weight:600"}

The underlying appraoch is as follows:

On the way out from the server:

Annotate the chunks of data to send with a sequence number

Create frames containing the data, sequence numbers and lengths

Provide a means of resynchronising[ ]{style="font-weight:600"}the data
stream by adding in restart markers. The data between these markers
generally form chunks.

-   For this to work, the data inside the chunks is escaped such that
    joining chunks cannot create spurious markers, and to preserve the
    existance of the marker in the original transferred data

Limit the resulting data\'s size[ ]{style="font-weight:600"}in terms of
actual data blocks sent, to reduce the likelihood that they will get
thrown away by the multicast layer [(this is done outside the actual SRM
components because the SRM components don\'t know where the data they
create is being sent).]{style="font-style:italic"}

On the way into the client:

-   Join the recieved blocks of data forming chunks detected based on
    restart markers.
-   Decode these chunks to frames.
-   Parse the frames to a tuple containing sequence numbers and data
-   Append the tuple onto the end of a buffer
-   When the buffer is full have a one-in, one-out basis for retrieving
    tuples - always choosing the tuple with the lowest sequence number.

[Details]{style="font-weight:600"}

Unsuprisingly this all maps to a collection of components, and it\'s
simplest to show the 2 pipelines from the code:

Sending:

::: {dir="ltr"}
[def SRM\_Sender():]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[return pipeline(]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[)]{style="font-family:Courier"}
:::

Receiving:

::: {dir="ltr"}
[def SRM\_Receiver():]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[return pipeline(]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[)]{style="font-family:Courier"}
:::

For those interested a full test suite for framing and data chunking can
be found in [Kamaelia.Protocol.test]{style="font-style:italic"} , and
also Kamaelia.Data.Escape (along with tests). A frame is created as
follows:

Note that this allows for a variable length header terminated by a
carriage return, with the header consisting of two numbers - one is a
sequence number, the other is a length. Both are expressed as strings
and are expected to be parsed. The data is passed through unchanged by
the Framer.

Chunking is essentially the same process. The chunker simply takes data
(usually frames, but it doesn\'t not require frames), does the
following:

Inserts a restart marker - defaulting to \"XXXXXXXXXXXXXXXXXXXXXXXX\"
(24 \'X\' characters) into the data stream. The marker is considered to
precede a data chunk, hence for a specific data stream it will start
with this marker, but not terminate with it.

The contents of chunks (ie the original data stream) is escaped such
that the restart marker cannot exist accidentally. The approach taken is
as follows:

Escape any % charcter as %25 before performing any other escaping

For every character in the restart marker

-   Ensure that every occurance of that character is replaced by a
    hexademical representation of the ordinal value of that character,
    preceded by a % character. For example, \"hello\" would be represent
    as %68%65%6c%6c%6f

Unescaping follows the same approach, but in reverse order.

[Implementation]{style="font-weight:600"}

Initial implementation was by [Tom
Gibson](mailto:apexmerridian@users.sourceforge.net), a vacation trainee
at BBC R&D during the Summer of 2005. The robustness of the algorithm
was subsequently increased by
[Michael](mailto:ms_@users.sourceforge.net), up to the limits described
above.

The implementation can be found in the following files & components:

Kamaelia.Protocol.SimpleReliableMulticast:

Annotator

RecoverOrder

Two component factories:

-   SRM\_Sender
-   SRM\_Receiver

Kamaelia.Protocol.Framing:

-   Framer
-   DeFramer
-   DataChunker
-   DataDeChunker
-   Also : SimpleFrame, though this will probably move to Kamaelia.Data
    due to being data used in the system, but not being a component

Kamaelia.Data.Escape - contains two functions used by DataChunker&
DataDeChunker:

-   escape(message,substring = None) (substring is the restart message
    from the DataChunker\'s perspective)
-   unescape(message,substring = None)

[Boundary Issues]{style="font-weight:600"}

-   Do not try and make the restart marker or sync message include a %
    symbol. This is untested, and will probably break, eventually if not
    immediately
-   The DeChunker maintains a buffer, which can be flushed
-   The Re-Ordering code maintains a buffer which can be flushed
-   Since the SRM\_Reciever wrapper does not provide access to these,
    you will need to build your own version of the SRM Reciever pipeline
    if you need this functionality. (But as can be seen from above this
    should be simple to do)

[Relationship to Other Reliable Multicast Work]{style="font-weight:600"}

Making multicast reliable is not a new idea. This protocol is simply
designed to be \"the simplest thing that can possibly work\", and
that\'s it. Essentially it\'s provided to allow a basis for testing
other reliable multicast delivery systems, and to show how they can be
layered into existing pipelines with relative ease. It is of course
immediately useful in it\'s own right.

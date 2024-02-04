---
pagename: Challenges/P2PandMulticastTogether
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[P2P and Multicast, Together]{style="font-size:24pt;font-weight:600"}

Multicast is similar to traditional broadcast in that the BBC sends a
single stream of data out onto the Internet. The underlying networks
copy it to the interested clients. This can allow for additional
traditional style live services over the Internet.

Peer to peer (P2P) allows home users to query the network to find
content that exists on the network, and retrieve that content from as
many sources as necessary to get a good download speed. This can allow
access to a huge range of content that is already in the network. Also
since clients do not need to return to the BBC it minimises license fee
payer costs.

No documents match your search

When taken alone, neither multicast delivery nor peer to peer (P2P) are
able to deliver the full vision in Building Public Value. Multicast lets
us offer higherquality streams of live content as long as the audience
is all watching same thing. P2P is very well suited when the audience
chooses to watch different things.

However when we look at the problems both approaches have we note that
the weaknesses of one are the strengths of the other.

Issues with multicast: (potential strengths in P2P)

-   It is limited by the size of your smallest consumer\'s connection
-   It is not generally deployed on the wide area Internet for both
    technical and business reasons
-   Losing content can result in either breakage or thousands (and
    potentially millions) of clients saying \"please resend\".

Issues with P2P: (potential strengths in multicast)

-   The network cannot be trusted - viruses, spam, defacement
-   Distributed search and navigation systems are difficult and are only
    in their nascent stage of development.
-   P2P relies on delivery between homes. How can we deliver 8Tbit/s
    downlink from a 4Tbit/s uplink?

Despite the issues with both, a solution based on
[both]{style="font-style:italic"} appears to hold great possibilities.
P2P can deal with the problems of Multicast and Multicast can deal with
the problems of P2P.

We have the desire to make available this choice to every home in the
UK. Clearly not everyone would choose to receive it, this is be feasible
in terms of home storage. Multicast is however available now for a
subset of our audience, thanks to work done for the 2004 Olympics.

In this scenario the entire P2P network becomes a large intelligent
cache which is able to fill in missing blanks and missing chunks without
needing to return to the BBC.

Seeding a P2P system is often a slow process. Initially one person adds
content and on demand usage grows. If however we wish to seed a P2P
system, as a broadcaster we have other options worth consideration:

-   We can broadcast our content specifically flagged for caching into a
    P2P system with associated meta data
-   We can multicast our content, as it is digitised from the archive,
    over a network connection for people to store and cache in their
    local P2P systems.
-   Any requests for content that come back to the BBC can be sent out
    also on the multicast channel, so that the number of sources in the
    network becomes very large very fast for our audience that does not
    have multicast available.

This has a number of advantages - P2P can bridge the gap between
multicast islands or multicast deserts by rebroadcasting locally.
Clients receiving our content via multicast can ask for missing content
via the P2P network, rather than all simultaneously clogging the central
server.

Since the network becomes inherently untrusted, mechanisms for trust (by
users) need to be added to this system, which deals with a number of
security issues in both multicast and P2P systems.

[Challenges: ]{style="font-weight:600"}We need to build new
Collaborative ClientHub protocols, allowing integration between
broadcast, multicast, P2P systems and our archives. P2P and multicast
systems need to be adapted to allow and take advantage of thousands of
P2P sources becoming simultaneously active. Security mechanisms such
that the audience can trust content is a key issue in such a system.

---
pagename: Projects/Soc2006/PeerToPeerStreaming
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Projects : Peer To Peer Streaming
=====================================

There was one project application in this area that is summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.

### Peer-to-Peer streaming architecture using Kamaelia 

\*Project motivation\*\
In recent years the concept of peer-to-peer streaming has received
increased attention from the academic and\
research communities, partly because the Internet doesn\'t widely
support multicast, and because of the need for\
a large scale content distribution system.\
\
The project I would like to work on is an experiment with such an
architecture. The core idea is that each peer\
that takes part in such an architecture can receive data segments from
several other peers, aggregate and play them,\
and also server data segments (at various rates), to other peers. The
Kamaelia-based approach is to have a component\
that receives media streaming segments from a number of similar
components, and can also serve a number of other components with the
media it receives. It should be able to take advantage of local
multicast facilities.\
\
From the perspective of the challenges that BBC Research is facing, this
project would be an attempt to integrate\
P2P and Multicast, because it provide a way to deliver media streaming
information between smaller multicast islands,\
where effective communication will be achieved by more efficient,
lower-level, mechanisms.\
\
Here is a selected list of papers regarding these topics:\
\
http://citeseer.ist.psu.edu/xu02peertopeer.html\
http://citeseer.ist.psu.edu/575162.html\
http://www-unix.mcs.anl.gov/fl/flevents/wace/wace2005/papers/eetemadhi.pdf\
\
\*Architecture\*\
\
The core component to the architecture is a component that can receive
data segments from N other components, aggregate them, and send them to
a \"player\" component. Also, based on the underlying allocation
algorithm, it can serve data segments to other peers itself. For the
beginning the streaming data will be a simple integer stream, and the
\"player\" a checker for consistency (mainly, whether the segments are
in the right order, and whether there are missing segments).\
\
A subset of peers will have only one input, from a component named a
\"seeder\", which will generate the data. The discovery and the process
of building the architecture still present some challenges, and I will
probably start with a statically specified architecture; using a
\"building\" utility, that reads this topology\'s description from a
file and builds its logical structure in Python by interconnecting the
\"peer\" components. Also, I will try to explore different algorithms
and strategies for initial building of the topology, and its
maintenance.\
\
A special case is that of the multicast islands. Because they support
more efficient ways of communication, it is reasonable that they are
treated as a single peer by the external network. This possibility
suggests the following architecture choice: each peer can be linked to
its own Multicast\_transceiver, that communicates to the multicast
island this peer takes part in. This separation allows us to receive
data \"into\" the multicast island through more than one peers, a more
realistic approach to a high demand network.\
\
To sum up we have:\
\* seeders, that generate the data\
\* peers, that have a sense of the topology surrounding them; they
receive streaming data from several other peers and feed it into the
player; moreover, it can be connected to a Multicast\_transceiver in
case it takes part in a multicast island, and can relay streaming data
to a number of other peers\
\* player, which will aggregate the data segments in the correct order,
perform buffering, if required, and \"play\" the data, depending on its
type\
\
Problems that need to be addressed:\
\* initial topology setup\
\* topology maintenance\
\* multicast islands identification\
\* from a peer\'s point of view, the network discovery\
\
Finally, I would like to try some experiments using \"real\" audio or
video streaming, as opposed to simplified mock-up data.\
\
\*Timeline\*\
\
\* 20 June - detailed specifications for the architecture and the peer
component\
\* 30 June - implementation of the peer, seeder and player components,
for a simplified data stream\
\* 20 July - multicast and support for audio or video data\
\* 1 August - automatic topology discovering, using one or more
directories\
\* 20 August - documentation, testing, experimenting\
\
\*Deliverables\*\
\
\* the implementation of the \"peer\", \"seeder\" and \"player\"
components, with documentation\
\* the utilities used to set up a topology\
\* a detailed report describing the approach and algorithms used\
\* a tutorial for using the components\
\

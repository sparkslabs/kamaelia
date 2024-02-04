---
pagename: Projects/Soc2006/GeneralisedEventsBackplane
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Soc Project : Generalised Events Backplane
==========================================

There were 2 project applications in this area that are summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.\

### Project Title: Collaborative Sketching Server: A P2P events backplane application

\
Benefits to Kamaelia and to the developer community:\
\
Kamaelia is a framework for building concurrent systems. By building
this sketching server Kamaelia will have an improved collaboration tool
with audio and video sharing capabilities, better protocols for
transmission (jingle extension of XMPP and if possible RSTP),
introduction of virtual backplane to have multiple groups of peers
editing different sketches, an abstraction of virtual backplane
component and a capability of being used outside of sketcher in other
concurrent and distributed applications.\
\
While other applications such as AccessGrid \[1\] can be deployed to
achieve similar functionality, doing so would require corresponding
hardware infrastructures and would also require additional tools, such
as Globus. However, these would not only decrease cost efficiency, tools
such as Globus also bring along lot more features, GSI authentication
for example, than required for a simple application. On the other hand,
Kamaelia can be effectively put to use with simple hardware, such as
personal webcams for sharing videos.\
\
As other sample applications, MSN and Yahoo messengers bundle various
tools that facilitate sharing \[2\]. Yahoo pool and MSN\'s drawing board
are popular examples. However, programmers can not enhance the
capabilities of these tools. Kamaelia once again presents itself as an
excellent alternative.\
\
Deliverables:\
\
In this project i will be involved in improving the current version of
collaborative sketching tool and adding more functionality, improved
transmission protocols and reusable code by abstracting components for
future use in other applications.\
\
The following components shall be included in order to do so:\
\
(X) I will enhance the existing sketcher tool to share audio and video.
For doing that I will be integrating audio/video players into the
sketcher application and and also certain codecs that would enable
trasmittance of compressed audio and video.\
\
(x) I will implement virtual backplane component to have multiple
sessions having different peers or overlapping set of peers. I need to
also manage the creation and closure of virtual backplane as the session
begins and ends respectively.\
\
(X) Tracking Component. This would determine the existence of a virtual
backplane based on the connections between peers.\
\
(x) Initially I will test the application using UDP protocol component.
The present sketcher implementation uses TCP. UDP is better suited for
transmission of shared audio/video. As an addition, I shall be
implementing a component based on jingle and jingle audio extensions for
XMPP in order to transmit audio. These libraries were primarily targeted
at p2p applications, and hence fits Kamaelia\'s requirements. I will be
building \'speex\', a codec for the same.\
\
(x) I will be abstracting the virtual backplane implementation and
implement logical backplane components so that they can be used outside
the sketcher application. These components would help in making groups
of peers in a virtual backplane sub-grouped according to the logical
backplane they belong to and ensuring that messages get routed
appropriately.\
\
(X)An event logger that would enable restoring data across sessions.\
\
(X)Providing documentation for the implemented codecs and transmission
protocol components.\
\
Time permitting, I intend to do the following\
\
(X)Try to test the same application with RTSP streaming protocol. This
would be beneficial if a single server is streaming and others are
purely behaving as clients, commonly encountered in broadcasting
scenario.\
\
(X) Building a GUI to facilitate easier operation, targeted at end
users.\
(X) Widgets, in order to increase its usability\
\
Project Details:\
\
In order to accomplish the above mentioned deliverables, I will be
building some wrappers and components of the same to be added to
kamaelia and also create other components. I will also being using some
existing components which are part of packages provided with kamaelia
installation.\
\
In order to enhance the existing sketcher implementation with additional
capabilities to share audio and video I will be using the
kamelia.vorbisDecodeComponent module for clients who will be listening
to what is sent over the network. The servers, also peers, send audio
over UDP using Kamaelia.Internet.UDP.\
\
For the purpose of video sharing, dirac video codec services will be
utilized. The libraries which will be used for this purpose are the
Kamaelia.Codec.RawYUVFramer, Kamaelia.Codec.Dirac,
Kamaelia.UI.Pygame.VideoOverlay modules. Even in this case transmission
would be using UDP and above mentioned modules.\
\
Even though datagram protocol like UDP is simple and efficient for
transmitting audio and video media, there are other protocols which are
very efficient for P2P settings. One such protocol is XMPP. The jingle
and jingle-audio extensions provide for transmission over XMPP. In
trying to implement this I will be using the libjingle \[3\] library
provided by Google. I will use libsip \[6\] for generating python
bindings for the libjingle c++ library and will also write a component
for utilizing this protocol for transmission. The jingle extensions will
also require having the speex codec component for kamaelia. I will be
using pySpeex \[5\] python bindings for the same. I realize that the
hardest part is going to be understanding the jingle protocol, and hence
a significant amount of time is devoted for the same.\
\
I will need to write a virtual backplane component so that multiple
sessions connected to a single headless server exist at the same time
and each virtual backplane has different or overlapping set of peers as
part of it. In the present implementation there is no concept of virtual
backplane and all peers are part of the same group. With the
implementation in place, virtual backplane can support multiple
sessions.\
\
Other facilities to be added would be an event logger. This will help in
saving sessions and restarting them as when required. It also helps in
role-back. Simple implementation would be writing all the events to a
file using the Kamaelia.File.Writing module. In future it would be
better to come up with a better implementation and have a universal
format (preferably using XML) for saving different kinds of events.\
\
If time permits the other components to be built for this collaborative
sketcher application are RTSP component to stream video/audio. In order
to build this I will be using livemedia-utils C library from Debian
\[4\]. I will generate python bindings for it using libsip. Using the
python bindings, the Kamaelia component to support RTSP streaming
protocol will be written. As presently this library doesn\'t support all
codecs, some additional code should be written.\
\
Other aspects that will be developed if time permits are improving the
user interface of the sketcher, building a GUI showing all the
rendezvous services available and within reach to a peer (as firewalls
might be restrictive) and also as to which virtual backplane and
particular logical backplane the services belong to.\
\
\
Refernces:\
\
\[1\] www.accessgrid.com\
\[2\] pager.yahoo.com/games.php\
\[3\] http://code.google.com/apis/talk/about.html\
\[4\] http://packages.debian.org/unstable/net/livemedia-utils\
\[5\] http://www.freenet.org.nz/python/pySpeex/\
\[6\] http://www.riverbankcomputing.co.uk/sip/\

------------------------------------------------------------------------

\

### p2p Events Backplane - Collaborative Sketching Server

\
Benefits to Kamaelia:\
\
This project will provide the Kamaelia project with a strong p2p
backplane component to compliment their existing suite of networking
components. This will provide anyone leveraging Kamaelia components with
capable p2p components to develop flexible networking applications.\
\
Synopsis:\
\
This project is predominantly focused on creating a p2p backplane, with
a collaborative whiteboard application developed as a proof-of-concept
to the p2p components.\
The p2p backplane is designed around nodes that have no distinction
between clients and servers. A p2p network of \'clients\' can be
established either dynamically, or with \'servers\' that clients can
connect to as a starting point \-- in both cases, any client can provide
the functionality of a server passively. This provides a very flexible
network model of nodes that can dynamically form groups to share
information.\
In this project, the application will be a collaborative whiteboard.
Clients will be able to discover, edit, and store shared whiteboards as
well as provide this functionality as a server. Groups of clients can
work on the same whiteboard, with the changed being shared between them
and stored on each of them \-- such that new clients can edit existing
whiteboards, and old clients discover changes in their whiteboards.\
\
Deliverables:\
\
Will Deliver:\
o p2p networking components\
Components that provide simple p2p networking, client/server discovery,
and data sharing (see project details).\
o Collaborative whiteboard application\
Application that builds on the p2p networking components to provide a
collaborative whiteboard (see project details).\
o Documentation\
API documentation on how to use the p2p networking components, and
development documentation on how the whiteboard uses the API.\
o Tests\
Unit tests for both the p2p components and whiteboard application, and
system tests to test the integrity of the network and function of the
whiteboard application.\
\
Given Sufficient Time:\
o Advanced p2p services\
These include more advanced client discovery routines, client/server
management, data persistence, network searching, and task
allocation/division.\
o Advanced whiteboard services\
These include taking advantage of advanced p2p services such as
whiteboard searching, distributed whiteboard storage, live media
streaming between whiteboards, and application sharing.\
\
Project Details:\
This project will build up the existing Kamaelia components to provide
connectivity and basic data sharing between clients/servers.\
\
p2p networking components:\
\
The p2p networking components will provide the basis for p2p networking
applications. The primary method of communication for this network will
be unicast (and potentially multicast) messages (aka. events) sent and
received by peers on the network. These events are shared between all
interested parties on the network (in some cases this will be all peers,
but more application-specific communication may be limited to a group of
peers).\
\
Peers will dynamically form groups on the network based on common
features. This grouping will allow distribution of information to occur
far more effectively. For example, bulk data could be handled by forming
a group of interested parties (those with, and those requesting the
data) and the group would work to push the data to requesting clients
\-- as opposed to the model of clients seeking and pulling data
independently, this model brings all peers together to both distribute
and re-distribute the bulk data to all parties.\
\
Collaborative whiteboard application:\
\
The collaborative whiteboard application will not just be a
proof-of-concept for the p2p components, but will also be a fully
capable whiteboard application that takes advantage of the features of
the p2p components in a sensible and rational way.\
\
This whiteboard will allow for a whiteboard to be created between a
number of peers - any number of whiteboards can be created by any peer
and whiteboards can either be discovered dynamically, or via. a
bootstrap to another peer on the network that has pre-existing knowledge
of whiteboards. Using the grouping features of the p2p components, all
users participating on a particular whiteboard will be grouped together,
and event messages of drawing instructions will be quickly distributed
to all interested peers.\
\
Additional whiteboard features include attaching and embedding documents
and media to whiteboards - this will demonstrate bulk data transfer over
the network to multiple peers, as well as serving as an extension to the
whiteboards capabilities.\
\
Project Schedule:\
May 23 - Project work commences.\
Design of components, and network architecture.\
June 13 - Alpha of networking components.\
Design is feature-complete, and components are usable for testing.\
June 26 - Half-way mark.\
Beta of networking components.\
Components are feature-complete (in code) and ready to be used for
application development.\
July 18 - Alpha of whiteboard application using p2p components.\
August 8 - Beta of whiteboard application.\
p2p components completed.\
August 21 - Project end.\
Whiteboard application complete.\
\
I have given this timeline wide flexibility, as it will most likely
change as the features of the p2p components and whiteboard application
are discussed either before, or during the initial phase of the project.
As more features are exposed, the stronger this timeline will become.\
\

\

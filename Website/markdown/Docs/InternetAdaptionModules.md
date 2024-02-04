---
pagename: Docs/InternetAdaptionModules
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Internet Modules]{style="font-size: 24pt; font-weight: 600;"}

Kamaelia has a wide selection of components to allow you to implement
TCP and UDP based systems, including Multicast capabilities and simple
chassis or making servers. These are mostly found in
[Kamaelia.Internet](/Components/pydoc/Kamaelia.Internet).

These components implement the low level functionality for making and
maintaining connections - they do not implement any particular network
protocols. [Other components do that](NetworkProtocolModules) and can be
used with these to construct more capable servers and clients.

[]{style="font-weight: bold;"}

[Making a TCP socket connection to a
server]{style="font-weight: bold;"}\

-   [Kamaelia.Internet.TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient)\
-   [Kamaelia.Internet.TCPThreadedClient](/Components/pydoc/Kamaelia.Internet.TCPThreadedClient)

The [TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient) component
simply makes a connection to a server. Its inboxes and outboxes receive
and send data from/to that server. This is very easy to use.\
\
[TCPThreadedClient](/Components/pydoc/Kamaelia.Internet.TCPThreadedClient)
is identical to use, but differs in implementation. It run its own
thread and so doesn\'t need the
[Selector](/Components/pydoc/Kamaelia.Internet.Selector) component)\
\
[Being a TCP socket server]{style="font-weight: bold;"}\

-   [Kamaelia.Internet.SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer)
-   [Kamaelia.Chassis.ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer)
-   [Kamaelia.Internet.TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer)

[SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer) is the
simplest kind of server to use - it allows one client to connect at a
time, and its inbox and outbox communicate with that client.\
\
[ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer) is
more powerful - it can handle lots of clients simultaneously. It is a
kind of factor component: every time a client connects it spawns a
component (known as the protocol handler) to deal with that connection.\
\
ConnectedServer is built ontop of
[TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer) which
provides the underlying handling of the socket connections. By spawning
[ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter)
components to manage the socket for each connection.\
\
[]{style="font-weight: bold;"}[Sending and receiving UDP datagrams\
]{style="font-weight: bold;"}The
[Kamaelia.Internet.UDP](/Components/pydoc/Kamaelia.Internet.UDP) module
contains components for sending and receiving datarams.\
\
\
[Multicast]{style="font-weight: bold;"}\

-   [Kamaelia.Internet.Multicast\_receiver](/Components/pydoc/Kamaelia.Internet.Multicast_receiver)
-   [Kamaelia.Internet.Multicast\_sender](/Components/pydoc/Kamaelia.Internet.Multicast_sender)
-   [Kamaelia.Internet.Multicast\_transceiver](/Components/pydoc/Kamaelia.Internet.Multicast_transceiver)

These components provide a simple way to send and receive (or both send
and receive) multicast datagrams.\
\
[Network simulation]{style="font-weight: bold;"}\
\
The
[Kamaelia.Internet.Simulate](/Components/pydoc/Kamaelia.Internet.Simulate)
module contains components that simulate the kinds of problems you might
get on a network - out of order packet delivery, lost packets etc.\
[\
Supporting components]{style="font-weight: bold;"}\

-   [Kamaelia.Internet.ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter)
-   [Kamaelia.Chassis.Selector](/Components/pydoc/Kamaelia.Chassis.Selector)

[ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter)
(CSA) components are spawned by the TCP client and server components to
look after actual communication with the TCP socket.\
\
[Kamaelia.Chassis.Selector](/Components/pydoc/Kamaelia.Chassis.Selector)
is designed for dealing with checking to see if any network connections
are active, and notifying CSAs that they can send/receive data. This
allows individual CSAs to pause when idle - without having to block up
the system or waste processor cycles by constantly polling.\
\
If you are just using the facilities provided for implementing clients
and server you don\'t need to worry about these components!\
\
\
\-- Matt Hammond, April 2007[]{style="font-weight: bold;"}

---
pagename: Developers/Projects/MulticastProxyTools
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
\

Project Task Page: Multicast Proxy Tools
----------------------------------------

Description
-----------

::: {.boxright}
**Status:** Stasis\
**Current active developer:**\
**Current dev locations:** /Sketches/MPS/Systems/MulticastProxying\
**Start Date:** 9 June 2006\
**Expected date:** n/a\
**end date:** n/a\
**This page last updated:** 27th Nov 2006\
**Estimated effort so far:** 1/2 man day\
:::

This task aims to produce tools to make it simpler to join multicast
islands together - in essence tools for proxying multicast over
non-multicast enabled networks.

A direct end result of this is that it would enable someone to take a
multicast stream, send it to a proxying hub, allow clients to connect to
this multicast hub, and those clients would then remulticast that stream
within a local (eg corporate intranet) network for local availability.\
This task was created because it was deemed to be hopefully useful to a
particular internal client at the BBC.\
Some specific benefits of working on this include:\
\

### Inputs

Task Sponsor: (for BB)\
Task Owner: Michael (mps)\
Developers:\

-   Michael

Users:\

-   BB (potential)\

Interested Third Parties\

-   na

Requirements:\

> The expected scenario for these components is that there are
> situations as follows:\

-   A single source which is desirable to multicast to a large
    population (mps)
-   A large population has many sources in which it wishes to multicast
    to itself (mps)
-   The population consists of many disaparate multicast islands which
    need joining (mps)
-   They desire having a central hub, to join islands together (mps)
-   They wish to join multiple islands together directly and in a
    distibuted fashion and route between islands. (mps)

> This is a non-exhaustive set of input states.\

Relevant Influencing factors:\

-   *eg release of a tool doing the same sort of thing that renders this
    non-relevant*
-   *people joining/leaving project*
-   *change of sponsorship*
-   *growth in users/thirdparties*
-   *tool dependency suitablility*
-   *unexpected complications*

Outputs
-------

### **Expected**

-   Tools to allow multicast data and data sources to be proxied between
    locations effectively. The tools can be assumed at this level to not
    have to deal with any automated mesh set up or autodiscovery -
    merely to allow such higher level systems to be created.

### **Actual**

**Code Produced:**\
These tools already exist in the subversion repository in
/Sketches/MPS/Systems/MulticastProxying. Files in that directory and
purpose:\

***config.py***\
Defines the following config options\

> mcast\_group, mcast\_port - The multicast group/port to be proxied\
> mcast\_tcp\_splitter\_ip, mcast\_tcp\_splitter\_port - IP/port of a
> simple TCP Splitter that serves the contents of a given multicast
> group to people who connect\
> tcp\_tcp\_splitter\_ip, tcp\_tcp\_splitter\_port - IP/port of a TCP
> Splitter that accepts a data source from a single TCP client\
> tcp\_splitter\_client\_ip, tcp\_splitter\_client\_port - IP/port of
> the TCP Splitter where clients can connect to recieve that data source

***MulticastTCPClientRelay.py***

-   This is a simple proxy to relay multicast data from a given
    multicast group and port to a TCP server which may choose to do
    something with the data (eg split and forward).\

***MulticastTCPRelay.py***

-   This is a simple proxy to relay multicast data from a given
    multicast group and port as a TCP Service on a given port. It\'s
    worth noting that this is one way - any data from the TCP connection
    is discarded.\

***SplittingServer.py***

-   Splitting server. This expects a single inbound connection on one
    port and spits it out to all recipients who connect on another port.
    This can be\
    used as an alternate server for the TCPRelayMulticast to connect to,
    and it would expect to be fed using MulticastTCPClientRelay.\

***TCPRelayMulticast.py***

-   A TCP Client that connects to the splitting server, and takes any
    data it receives a resends it as a multicast stream

### ****Realistic possibilities arising as a result of activity on this task ****

The creation of tools that allow for automated mesh setup building on
this allow for the realistic possibility of merging application layer
multicast with IP level multicast.\
**Tasks that could benefit from or build on this work:**\

-   Whiteboard - specifically P2P Events Backplane (An extraction
    exercise)\

Related Tasks
-------------

### Tasks that directly enable this task

-   Multicast Transciever
-   Internet Subsystem

### Sub tasks

-   Coding each of the types of server, client and relay. (each of these
    is too small to be worth while)\

### Task Log

-   Initial version of the code developed, uploaded, and feedback sought
    from potential sponsor. This page created and project placed into
    **stasis.** (ie can be reactivated at any later point in time).\
    \
    Time working on code \~ 1/2 day\
    Time working on this page \~ 1/2 hour\
    Entry made: Michael, 27th November 2006\

Discussion
----------

Potential future implementation approaches could see\

-   Automated mesh creation.
-   Transport over other mechanisms - such as UDP, STCP, etc
-   Authentication before joining the mesh
-   Integration with the implicit P2P events backplane in the Whiteboard

\-- Michael Sparks, 27th November 2006

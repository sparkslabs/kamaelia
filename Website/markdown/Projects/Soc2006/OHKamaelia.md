---
pagename: Projects/Soc2006/OHKamaelia
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Project: \"OH Kamaelia!\"
=============================

There was one project application in this area that is summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.\

::: {align="right"}
*As an aside, this was possibly the most entertaining project
[title]{.underline}! Well, at least the short form. Never thought of
Kamaelia as an* expletive *before\... :-)*\
:::

### Project Title: OH-Kamaelia (\[O\]DMRP based Ad \[H\]oc extensions to \[Kamaelia\])

\
Benefits to Kamaelia: Extend Kamaelia framework to mobile ad hoc
networks (MANETS) and make immediate content sharing possible in MANETS
through Kamaelia framework.\
\
Synopsis:\
\
Abstract:\
Kamaelia is a framework for online content delivery. Currently Kamaelia
does not support mobile ad hoc wireless networks (MANETS). However, the
proliferation of networking enabled mobile devices calls for ad hoc
networking capabilities to overcome the lack of dedicated networking
infrastructure. On-Demand Multicast Routing Protocol (ODMRP) is a
leading multicast protocol for ad hoc networks. Simplicity, high-packet
delivery ratio and non-dependency on a specific unicast protocol are the
strengths of ODMRP. Based on ODMRP, this project extends Kamaelia
framework to mobile ad hoc networks.\
\
Problem Overview\
Kamaelia content delivery framework does not support ad hoc networking.
However, more and more networking enabled devices are found in
environments without dedicated networking infrastructure. Despite such
limitations, the proliferation of the mobile devices continue at a
staggering pace. In the first quarter of 2006 alone Apple has recorded
over 8.8 million iPod sales. Although iPods lack networking
capabilities, the possible usability improvements and daily decreasing
hardware costs make networking an attractive option. On the other hand,
other mobile devices such as PDAs and digital cameras already have built
in networking. Such devices rely on Bluetooth or Infrared based
protocols to overcome infrastructure limitations. But those protocols
require specialized hardware and also have limited communication
capabilities.\
ODMRP based on network broadcasting is a leading ad hoc network
multicasting protocol. The broadcast nature of ODMRP ensures high packet
delivery ratios. In addition, the simplicity of the protocol makes it
particularly suitable for mobile devices with limited hardware.
Extending Kamaelia framework to ad hoc networking based on ODMRP has
immediate benefits. It makes immediate availability of content possible
(i.e. imagine the opening ceremony of 2012 London Olympics. There will
be millions of digital cameras taking pictures of the event. The
Kamaelia framework, with ad hoc networking can make such content
immediately available to BBC online community)\
\
Deliverables:\
Will deliver:\
Implement core ODMRP protocol\
Integrate ODMRP multicasting with existing Kamaelia Internet multicast
component\
Define API for ODMRP multicast layer\
Develop a proof of concept/demo application\
\
Would like to haves:\
Make all components fully cross platform compliant (depending on
availability of hardware). Interested platforms are Windows, OS X and
Linux\
Port existing multicast applications\
\
Project Details:\
ODMRP protocol will be implemented as an application layer protocol for
ad hoc networks. The protocol implementation will be based on IP
broadcasting and raw sockets.\
The initial development will be done in a Linux environment with cross
platform portability in mind.\
\
Project Schedule:\
Tentative Schedule (activities may overlap)\
Familiarize with current Kamaelia multicast API (2 Weeks)\
Design and develop ODMRP protocol layer (2 Weeks)\
Integrate ODMRP layer to Kamaelia multicasting API (1 Week)\
Testing and documentation of the API (1 Week)\
Demo application development (2 Weeks)\
\
References:\
ODMRP protocol\
http://www.hpl.hp.com/personal/Sung-Ju\_Lee/abstracts/papers/wcnc99.pdf\
IETF draft on ODMRP\
http://www.hpl.hp.com/personal/Sung-Ju\_Lee/abstracts/papers/draft-ietf-manet-odmrp-02.txt\
\

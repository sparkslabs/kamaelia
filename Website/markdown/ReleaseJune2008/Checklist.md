---
pagename: ReleaseJune2008/Checklist
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
ReleaseJune2008: Checklist
==========================

Stuff specifically checked and any actions/decisions result.

**Release tool:** - pulls in all major dependencies

**Tools**

Show.py

-   Minor issue in MultiClick - fixed

VideoPlayer.py - passed

-   Confirmed working

AxonVisualiser.py - passed

-   Confirmed working

kamaelia\_logo.png

-   New version of logo in place

axonshell.py - passed

-   Probably to be deprecated in favour of likefile, but works

VideoShotChangeDetector - passed

-   Works with random video file :-)

Whiteboard.py - passed (speex issue dealt with by Tools branch)\

Compose.py

**Breaks in this release**

**Will remove from this release, but put out as a separate release**

-   Ala Kamaelia-ERModeller.
-   Makes tool still usable/useful.

Only major problem in the release at present - and the fact that it
actually causes a C stack trace rather than python would tend to imply
it\'s not actually a Kamaelia issue, but rather a dependency.\

Examples

Axon

**likefile** - passed BUT **Rewritten and renamed \"Handle\" as per
numerous discussions - passed\
**

Simple -\

-   all.py - passed
-   README.py - passed

SynchronousLinks

-   basic\_syncLinksAcceptanceTest.py - passed

DVB\_Systems

-   all - passed

GraphVisualisation

-   BasicGraphVisualisation.py - passed
-   TopologyVisualiser.py - passed

Introspection - all passed ( kamaelia\_logo.png issue resolved )\

Likefile

-   ./LikeTicker.py -passed\
-   mediumtcpclient.py - passed
-   ./simplehttpclient.py - passed
-   ./simpleoggdecoder.py - passed (used supported version)\
-   ./simplemp3encoder.py - **removed**\
-   ./simpleoggradioplayer.py - checked ok (relies on a service not
    always available)\
-   ./simpletcpclient.py - passed
-   simpletorrentclient.py - assumed OK (requires Bit Torrent installed)

multicast - passed\

SimpleGraphicalApps -passed (BouncingCatGame pictures replaced with
\"better\" ones)\

SoC2006

RJL

-   Not tested - no change from last release - assumed OK

THF

-   passed

TCP\_Systems - passes\

UDP\_Systems - passes\

Chassis - passe

Dirac

-   Would help if I\'d installed dirac(!)

**Otherwise OK :-)\
**

\

---
pagename: Developers/Projects/KamaeliaMacro
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Kamaelia Macro
=================================

Description 
-----------

::: {.boxright}
**Status:** Blocked since June \'06 *-* Awaiting access to hardware\
**Current Developers:** n/a\
**Current \"inflight\" dev location:**
/Code/Python/Kamaelia/Examples/DVB\_Systems\
**Start Date:** January 2006\
**Major Milestone date:** May 2006\
**Expected End Date:** September 2006\
**End Date:** na\
**Date this page last updated:** 27th November 2006\
**Estimated effort so far:** 9 man months\
**Owner:** Michael\
:::

A system for taking DTT - DVB-T - of all BBC channels, transcoding &
dumping to disk for serving by a front end, 24x7, 365 days a year.

This will create a large resource of BBC programmes for internal
experimentation (only). A previous system existed that provided a
similar capability, but failed and support was an issue. This task
replaces that system.\

Benefits include:

-   Provides motivation for optimisations to be performed.
-   Exemplar project
-   Provides a useful outcome/resource for the business
-   Expands capabilities of Kamaelia to deal with DVB & databases making
    Kamaelia a more generally useful tool.
-   Long term soak test of Kamaelia in a production environment.
-   This system would also end up being a continually/indefinitely
    running system that internal users (only) would have the potential
    to be able to take programmes and experiment with new formats based
    on a previous record of transmission.\

Inputs
------

Task Sponsor: TL

Task Owner: Michael (MPS)\

Developers:

-   Michael. (MPS)\
-   Matt. (MH)

Users:\

-   TL, MPS, MH, etc

Interested Third Parties:\

-   NT - Request for demonstration at EuroOSCON & OSCON
-   MB - Creation of the original Radio based system that proved (in
    principle) that Kamaelia was suitable for this task
-   HW\

Requirements:\

-   MUST be able to record DVB (TV) 24x7, 365 days a year\
-   MUST support transcoding of content\
-   MUST segment at least at the programme level, automatically\
-   MUST be stable (eg leavable alone for months at a time)
-   MUST be maintainable (ie able for new eyes to come in and take over
    project & code relatively easily)
-   MUST have a working demonstrator (of MUSTs) for XTech (May 2006)
-   WOULD LIKE subprogramme segmentation, approach TBD
-   WOULD LIKE multiple format transcoding.
-   WOULD LIKE metadata inserted into a database
-   WOULD LIKE a protocol/API for more granular access than \'just\'
    programme level

Influencing factors:\

Already done by MB for radio

B2 has kit needed for large scale system, but not been able to get at
kit

TL reassigned to other large scale (higher priority) projects

Interest by FLOSS community for public presentation at OSCON/etc

MS has decided (Nov 2006) to potentially reassign manchester research
lab machines to this task

-   Issue if that\'s done: Storage\

Outputs
-------

### Expected 

-   A server as a demonstrator of the core system for a single channel &
    simple demo frontend
-   Document for access protocol (API)\
-   Server farm for full system inc DB. (requires access to existing
    Macro Kit)
-   Documentation for maintenance
-   New components implementing the given requirements
-   Presentations (XTech & OSCON)
-   First production Kamaelia system\

### Actual

-   6 months (as of Nov 2006) of TV transcoded on demonstrator system (2
    weeks storage capacity). (This marks a Kamaelia system running
    reliably consistently with a high data rate (8Mbit/s) flowing
    through it whilst also processor intensive (transcoding).
-   Demonstrator system & simple demo front end

**\
Code Produced:**

-   Axon Optimisations
-   DVB Tools
-   Macro Code
-   UnixProces
-   TCP/IP throughput/CPU optimisations
-   Quiessence

**Documentation:**

-   [Web page describing Macro from a high level](/KamaeliaMacro)

**Presentations**

-   XTech - TL - May 06\
-   OSCON - MPS - July 06\
-   EuroOSCON - MPS - Sept 06\
-   Internal research board - MPS, MH - Oct 06\

**Releases:**

-   Core time shifting code included in Kamaelia Bundles 1.2 & 1.4

**Event:**

-   Brussels open space @ fo.am

### Realistic possibilities arising as a result on activity on this task

-   Ability to pipe data through external transcoders and a stable
    UnixProcess component allow many more interesting apps. (essentially
    opens up traditional unix pipes to be usable from within a Kamaelia
    system)
-   Command line PVR tool
-   IRC/webcontrol of a TV agent
-   Complete toolset for most tasks people would want for handling DVB
-   Components for OCR of subtitles would now be a realistically useful
    task to work on
-   Quiessence has opened up lots of applications due to simply freeing
    up CPU - especially for desktop apps (such as the
    [Whiteboard](/Whiteboard))\

Related Tasks
-------------

### Tasks that directly enable this task 

-   Co-ordinating assistant Tracker
-   Selector Service\

### Sub Tasks 

**Done:**\

-   [Axon box delivery
    optimisations](/Developers/Projects/AxonBoxDeliveryOptimisations)\
-   Selector Optimisations
-   UnixProcess
-   UnixProcess Rewrite
-   Python DVB Tools
-   Basic DVB components
-   Demuxer
-   Optimised Pyrex Demuxer
-   TCP/IP subsystem partial rewrite
-   Threading changes to allow quiessence
-   XTech Ready Kamaelia Macro Demonstrator\
-   Kamaelia Macro Presentation for OSCON
-   Kamaelia Macro Presentation for EuroOSCON

**Todo:**

-   Database Tools
-   Macro Database schema creation
-   Video segmentation protocol
-   Macro API design for content access

Task Log
--------

Log started 27th November. The inputs/outputs and status represent a
snapshot at that point in time. \-- Michael, 27th November 2006\

Discussion
----------

Any comments welcome\

\

\

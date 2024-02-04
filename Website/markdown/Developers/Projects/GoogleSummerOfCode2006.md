---
pagename: Developers/Projects/GoogleSummerOfCode2006
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: GoogleSummerOfCode2006
=========================================

*To be filled in now. (The template form for this was created after GSOC
finished. Why? This template form was invented some months later!)*\

**Description **
----------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** Michael Sparks\
**Current \"inflight\" dev location:** /Sketches/{RJL\|THF\|AM\|DL}\
**Start Date:** May 2006\
**Expected End Date:** Aug 2006\
**End Date:** Aug 2006\
**Date this page last updated:** 31 December 2006\
**Estimated effort so far:** 9 man months\
:::

Kamaelia & Dirac were involved with Google\'s summer of code this year -
the core aims of this task were to introduce students to open source in
the context of useful Kamaelia & Dirac based projects.\
\
**NB, this page largely discusses Kamaelia\'s involvement in SoC.**\
\
The end result of involvement is twofold. For the students, there is a
general aim in becoming a better software engineer rather than \"just\"
a coder). For Kamaelia & Dirac there is an aim to generate a collection
of useful code, & documentation increasing the usefulness of Kamaelia &
Dirac overall, increasing the project\'s utility and toolset. Ideally, a
good outcome would be for the students to become fully fledged
developers taking part in directing development of the project and
taking ownership of their code. (This is an ideal however, not an
expectation!)\
\
Google have now run summer of code now for 2 years. This year, google
invited organisations running open source projects to apply to be mentor
organisations. BBC Research applied and was accepted. We were granted 6
student slots for Summer of Code. 4 of which were allocated to Kamaelia
and 2 to Dirac. This split represented the fact that the bulk of
applications were for Kamaelia rather than Dirac.\
\
Historically, BBC research has mentored summer/pre-university students
in the past. Furthermore, Kamaelia has an aim of being usable and useful
to the average novice developer - as a result having relatively
inexperienced developers is useful (in practice there was a range of
experience).\
*\
*Benefits:\

Students gain experience of participation in an open source project and
seeing how an open source project can be run.

Students learn the difference/discipline of software engineering, rather
than just coding.\

Increased understanding of aims & ways of working between Google & BBC
Research. (I seriously think this is something that has happened - so
far perhaps only between the two teams on either side, but that\'s a
good start!)

An increased set of components for Kamaelia, increasing it\'s
attractiveness to all users

An opportunity to test the ease of use (vs learn) for Kamaelia by
relative novices.

-   Hypothesis appears confirmed. Novices seem to find Kamaelia easier
    to pick up and develop than traditional approaches, whereas
    experienced developers (*except* those used to piping data around)
    find it slightly harder, but useful.

An expansion of the problem space which Kamaelia can be used for.

Further development of lightweight project management processes/crossed
with open source best practice. (these project task pages are in a way a
direct descendant of our way of working, combined with the way we asked
students to detail their work)\

Inputs
------

Task Sponsor: Michael Sparks

Task Owner: Michael Sparks

Developers involved in the task at some point\

-   Michael Sparks (primary Kamaelia Mentor)
-   Matt Hammond (backup/secondary Kamaelia Mentor)
-   Ryan Lothian (Significant amount of useful code now included in
    distribution)
-   Thomas Flanitzer (Significant amount of useful code now included in
    distribution)
-   Devendra Laulkar (Useful code now included in distribution, proof of
    concept for inter component trusted comms)
-   Anagha Mudigonda (proof of concept for trusted comms infrastructure)

Users:

-   Developers above (however since there have been users for the bit
    torrent, webserving & web client code)\

Interested third parties

-   Google

Requirements

-   See below.\

The following is the student\'s own synopsis of their work prior to
starting.\
\
**Creation of an integrated BitTorrent component for Kamaelia**\

::: {align="right"}
*Ryan Lothian*\
:::

Kamaelia currently lacks a P2P toolset for content delivery. Adding
BitTorrent client functionality to Kamaelia would allow BitTorrent to
act as an end-point for a component chain.\
\
Eventually this could lead to the BBC being able to distribute many
terabytes of its TV and radio archive without incurring massive
bandwidth requisites.\
\
**3D widget framework**\

::: {align="right"}
*Thomas Flanitzer*\
:::

The project will provide a framework for a 3D user interface for
Kamaelia. Several 3D widgets as well as a space manager will be
implemented as components. Using these, a basic 3D user interface will
be easy to create. If there is sufficient time, I will also experiment
with more advanced components, to see in what direction the whole idea
could develop.\
\
An example application that uses all developed components will also be
written. This will most likely be an image browser or video viewer,
dependent on which components will be realized. It will help to collect
experience with 3D interfaces and their use for Kamaelia.\
\
**Trusted Communications for Kamaelia Components**\

::: {align="right"}
*Devendra Laulkar*\
:::

The aim of the project is to provide a Security Framework for Kamaelia
components. Specifically to build a security component to provide
services like Authentication and Integrity to Kamaelia components. This
can help ensure the privacy of the users of the system. Ensuring privacy
would result in an increased trust in the system.\
\
**Key Predistribution Infrastructure (KPI) base trusted communication
framework for Kamaelia**\

::: {align="right"}
*Anagha Mudigonda*\
:::

Kamaelia is set of components that can be assembled to create
media/network apps. However there are no components that address trusted
communication. By developing KPI based trusted communication framework,
BBC Research team can easily enable secure communication for online or
offline media transfers.\
\
Trusted communications project requires a set of components that address
authentication, integrity and privacy. These components will be built
using Kamaelia component architecture principles. These components would
expose high level security abstractions to applications like video
multicast, video mail, whiteboard messaging etc.\

Outputs
-------

This section is largely about WHAT has been produced, normally by WHO
(in order to provide a point of contact)\

### Expected

*In the student\'s own words\...\
\
***Creation of an integrated BitTorrent component for Kamaelia**\

Creation of an Kamaelia component or components able to

1.  Be controlled by other Kamaelia components
2.  Download data using the BitTorrent protocol
3.  Upload data using the BitTorrent protocol
4.  Create .torrent files for serving based on messages from other
    components

Documentation for the new components /ongoing until end of project/\
\
Given sufficient time the following extra features will also be
implemented\
\

Tracker interaction

1.  Automatic upload of .torrent files to a webserver for distribution
2.  Automatic download of new .torrent files from a webserver

\...

1.  Deconstruction of a data stream into separate blocks
2.  Reconstruction of downloaded blocks a single logical stream

User interface that abstracts the process from users, presenting a
simple stream/programme selection, reconstructed the stream as the
earlier parts are played\

\
**3D widget framework**\
Will deliver\

-   A framework for a 3D user interface
-   Component for managing an amount of space
-   Interactive component (like a button)
-   Component that is capable of displaying text on a surface in 3D
-   Component that is capable of displaying images on a surface in 3D
-   An example application for the created components

given sufficient time\

-   Translucency and other nice looking effects
-   Component that is capable of displaying moving images on a surface
    in 3D
-   Interaction with existing 2d pygame components
-   More interactive widgets (text entry, scrollbar, checkboxes, \...)
-   Component that handles complex 3D meshes

**Trusted Communications for Kamaelia Components**\

-   A collection of components that will provide security services to
    other components.
-   A security framework for Kamaelia.
-   Sample code and tutorial on using the security framework.
-   A blog on the progress and experiences of working with Kamaelia
    project.

Core Deliverables:\

-   Security component providing at least authentication and integrity
    services.
-   Documentation on above component.

**Key Predistribution Infrastructure (KPI) base trusted communication
framework for Kamaelia**\

-   Overall Architecture document
-   Three fully tested *(high level)* components (1 authentication, 2
    encryption)
-   Developer guide and sample apps using the components.
-   The student also proposed to work on this project till the year end
    during which they would provide the complete set of KPI framework
    components. *(this did not happen)*

### *Actual*

*To be filled in.*

### *Realistic possibilities arising as a result of activity on this task*

*To be filled in.*

*Related Tasks*
---------------

### *Tasks that directly enable this task (dependencies) *

-   *To be filled in.*

### *Sub Tasks*

-   *To be filled in.*

*Task Log*
----------

*To be filled in.* *Probably cadge the data from the weekly \"done\"
reports.\
*

-   *Created the PTP page for the project,Michael. December 31st 2006.*

*Discussion*
------------

*This page is a work in progress to capture work on Kamaelia over the
past 12 months. It\'s difficult to ignore GSOC, but this page was
missing, hence why its been added.\
*

*\-- Michael Sparks, December 31st 2006*

\

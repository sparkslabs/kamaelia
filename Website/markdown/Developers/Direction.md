---
pagename: Developers/Direction
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Direction, Goals, and Mission 
-------------------------------------

Mission
-------

> *\"To make software systems as capable, manipulable and future proof
> as the best in science fiction, without waiting 4 centuries, using
> concurrency as a tool to make them easier and more natural\"\
> *

OK, this is a recent change, and needs to change again, but is slightly
less cheesy than:

> Kamaelia is an open source project that has as it\'s less than obvious
> goal creating the computer systems that you\'d find on next gen
> version of the USS Enterprise, just not waiting 4 centuries for it.\

And definitely less teeth jarring than:

> *\"To do for software systems what IKEA has done for furniture, and
> spreadsheets have done for traditional business, but for the BBC\'s
> business of story telling & distribution.\"*\

This reflects the fact the project lead works at, and Kamaelia
originated at the BBC.\

Practical Goals
---------------

In concrete terms this mission means:

***Kamaelia systems should be creatable, eventually, by a user with a
similar level of ease as using a speadsheet***.\
Why? This would make it a much more creative tool, and useful for the
average non-programmer in a creative environment, where they don\'t need
to wait for a programmer to help them envisage their goal. Our
[Compose](/Compose/) tool is beginning to push capabilities upwards.\

***Kamaelia needs to support the various ways stories can be told and
distributed***

-   Either through creation of subsystems, or better - by integrating
    external best of breed systems where possible.\

```{=html}
<!-- -->
```
-   This includes tools for manipulation of traditional content (audio,
    video) from traditional sources (cameras, broadcast, files) as well
    as user interfaces (traditional, modern, games 2/3D, web), etc
-   This implies that networking systems must be adaptable & malleable.
    Furthermore it means that any and all online distribution mechanisms
    need to be explored for suitability, preferably through integration
    in subsystem form.\

***Kamaelia*** must ***work for the average programmer as well as the
uber-programmer.***\
Given the goal of parallelism this is unsual. In order is to allow the
non-programmer to use their systems, subsystems must *inherently* and
*easily* be able to be used/created in this way. Not as a bolt on, or
odious, but because it naturally falls out of the way the system works.\

***Systems should be future proofed - this is our starting point,
driving many design decisions***\
In practical terms, hardware is (finally, as long predicted) going
multicore and parallel. Parallel systems programming is currently
considered hard. Kamaelia aims to make concurrent/parallel systems as
simple as possible from a maintenance perspective. *Kamaelia\'s approach
comes from this perspective, however it is part of a larger picture.*\

***This all needs to be as cross platform as possible***

Kamaelia 0.5.0 seems to point that these goals are achievable.\
\

Project Direction
-----------------

Concrete, ongoing aspects of the project that show direction:\

-   [Compose](../../../Compose/): To build and extend graphical tools
    for creating software systems.
-   [Axon](../../../Docs/Axon): To make software created now relevant in
    the future - this means making concurrency actually usable.
-   [Whiteboard](../../../Whiteboard/): To build the tools that are
    repurposable, that are networked distribution tools in their own
    right, and are useful for collaboration, communicators and
    storytellers

The project is typically driven by projects and aims originating inside
the BBC. This is then used to stimulate development of both those
projects & Kamaelia itself. You are welcome to do the same.\
The current project direction is aimed at improving the toolset to allow
high quality realtime efficient communication and collaboration, whilst
extracting useful subsystems that can reused in novel ways, along with
consolidating existing work for reusability. As a result tools enabling

High quality audio & video capture

Audio/video manipulation

Integration with common systems & tools (eg Databases, XML, RSS/Atom
sources/sinks)

Tools for organisation of materials for collaboration

Areas which can be enhanced

-   Graphline editors - such as compose or the nascent 360 degree tool
-   AV capture
-   Pygame & Open GL support
-   Protocols for communicating data as well as control information
    across the network (both obvious and non obvious)

Are all of interest, but preferably driven by real world problems. This
list is non-exhaustive.\

Eh?
---

I know, I know. Very american, very un-european. Sorry :) Some of it
grates for me as much as you, but it\'s useful to know what we\'re doing
and why? I hope :-)

Knowing where the developers are headed or being lead is useful to know.
See \"Eh?\" below if you find this page painful! If you\'re interested
in developing Kamaelia, please take a peek at [Visions of
Kamaelia](Visions), and add your thoughts.\

What do we mean by Mission, Goals, Direction above?\

A mission is essentially one vision from [Visions of Kamaelia](Visions),
based on the project leads\' view. Goals are wider in scope and can
support that mission or any of the other [Visions of Kamaelia](Visions).
Project Direction reflects current developer priorities. New developers
will bring their own priorities. The mission currently reflects that the
project lead works at, and the project originated at the BBC. There is
no expectation that you share these aims, visions or goals. Sharing your
personal vision expands the project, benefitting everyone.

\-- Michael Sparks, November 2006 (updated lightly May 2008)\

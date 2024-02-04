---
pagename: TheMightyBoosh
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Mini Project: The Mighty Boosh]{style="font-size:24pt;font-weight:600"}

[Multicast streaming system]{style="font-weight:600"}

A simple kamaelia based system to multicast stream programmes. Aiming to
stream carousel(s) to clients containing 1/2 hour programme episodes
(pre-recorded, pre-compressed to files)

System consisting of:

-   playout system
-   client \'tuner\' application

[Target schedule]{style="font-weight:600"}

Highly aggressive schedule to see what can be done in a short space of
time. Expected to actually take a little longer.

-   Mon 11th July 2005 - Project start
-   Wed 13th July 2005 - code written
-   Mon 18th July 2005 - testing begins

[Achieved Schedule]{style="font-weight:600"}

Multicast Carousel work completed:

-   Friday 15th July 2005

Basic client side tuner interface completed:

-   Friday 15th July 2005

Simple Reliable Multicast Protocol completed:

-   Tues 19th July 2005

[Server pipeline:]{style="font-weight:600"}

CRON (MH) [Done]{style="font-style:italic"}

-   system cron, eventually to be a \'component\' cron, probably a
    combination of both for a while
-   determine shape of text file \'scripts\' for component cron

DATA SOURCE (MH) [Done]{style="font-style:italic"}

-   improved file reader. sequence of files to read coming from a new
    CHOOSER component, separate out bitrate limiting

SERVER (MS) [Done]{style="font-style:italic"}

Implementation of more robust [Simple Reliable
Multicast](SimpleReliableMulticast.html) protocol.

Took longer than anticipated due to boundary conditions in the sending
side.

Provide factory interface for MH to do testing (wasn\'t
necessary/needed)

-   Bypassed - MH used an basic alternative.

INTEGRATION

-   In progress

[Client pipeline]{style="font-weight:600"}

Implementation of more robust [Simple Reliable
Multicast](SimpleReliableMulticast.html) protocol.

-   Took longer than anticipated due to boundary conditions in the
    sending side.

HTTP Server (MS)

[Over optimistic for such a short time frame. Currently reviewing
approach.]{style="font-style:italic"}

-   [VLC will happily take data on stdin on linux, so let\'s do that
    /first/]{style="font-style:italic"}

restreaming locally

must be turned into threaded component

Client player (eg. VLC, [not our
responsibility]{style="text-decoration:underline"})

-   receiving locally restreamed HTTP

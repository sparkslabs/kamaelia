---
pagename: OldHome
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Snap Together Software\
]{style="font-size: 24pt; font-weight: 600"}

[A Programmer\'s Toybox for network apps\
]{style="font-size: 16pt"}

::: {.boxright}
[Getting Started]{style="font-weight:600"}

-   [Single Page Kamaelia Introduction](Introduction.html)
-   [[Setup and
    Quickstart!]{style="font-weight:600"}](/GettingStarted.html)
-   [How to write
    components?](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&postid=1113495151)
-   [How does Kamaelia Work?](/MiniAxon/)

[Recent Changes]{style="font-weight: 600"}

-   [developers/projects/webserverconsolidation.html](developers/projects/webserverconsolidation.html)
-   [index.html](index.html)
-   [Docs/Axon/Axon.util.testInterface.html](Docs/Axon/Axon.util.testInterface.html)
-   [Docs/Axon/Axon.util.safeList.html](Docs/Axon/Axon.util.safeList.html)
-   [Docs/Axon/Axon.util.removeAll.html](Docs/Axon/Axon.util.removeAll.html)
-   [Docs/Axon/Axon.util.logError.html](Docs/Axon/Axon.util.logError.html)
-   [Docs/Axon/Axon.util.listSubset.html](Docs/Axon/Axon.util.listSubset.html)
-   [Docs/Axon/Axon.util.html](Docs/Axon/Axon.util.html)
-   [Docs/Axon/Axon.util.axonRaise.html](Docs/Axon/Axon.util.axonRaise.html)
:::

[A toy box, a toolkit, a library of components you can take and bolt
together, customise and create your own. This includes components for
TCP/multicast clients and servers, backplanes, chassis, Dirac video
encoding & decoding, Vorbis decoding, pygame & Tk based user interfaces
and Tk, visualisation tools, presentation tools, games tools\... A
networked unix pipe for the 21st century - a way of making general
concurrency easy to work with, and fun.]{style="font-style: italic"}

But what is it?\

A framework providing the [nuts and bolts](/Docs/Axon.html) for building
components. A [library of components](/Components.html) built using that
framework. Components are implemented at the lowest level as python
generators, and communicate by message passing. Components are composed
into [systems](/Systems.html) in a manner similar to Unix pipelines, but
with some twists that are relevent to modern computer systems rather
than just file-like systems.

[Why?]{style="font-weight: 600"}

To enable programmers of all skill levels with playing with components
in a networked environment. Network systems are naturally concurrent,
and concurrency is often hard. Kamaelia is trying to make concurrency
natural and easy to work with, because we are trying to solve some
specific [challenges](/Challenges/) regarding putting (some or all of)
the [BBC](http://www.bbc.co.uk/) Archive online. Lego, K\'Nex and
building blocks are great metaphors for systems like unix pipelines that
have made concurrency easy (in a constrained way) for 30 years.

[[]{style="font-weight: 600"}](Licensing.html)

[Upcoming Events]{style="font-weight: 600;"}

-   **Next IRC Meeting: Thursday 12th June 2008, 4pm UK Time**
-   [**BBC
    Mashed**](http://backstage.bbc.co.uk/news/archives/2008/05/mashed_got_a_ti.html)
    **- 21st/22nd June 2008, London\
    **

\

### Current Status

::: {align="right"}
***Last updated:** Nov 11, 2006, Michael Sparks*\

::: {align="left"}
Axon - Core Concurrency framework- version 1.5.1 - overview of status\

-   API Stable for generator components
-   Beta status API for Thread based components
-   Non-CPU-greedy capable (scheduler can sleep and be awoken by
    threads)
-   Production ready (\>6 months on a running system)\

Kamaelia - the toy box - version 0.5.0\

Full coverage of [core aims](/Developers/Direction) (introspection,
network, graphics & codec capable, graphical systems composer, large
examples)

API is subject to change (hence 0.5.0 status), but includes:\

-   Network - beta production ready (TCP/UDP/Multicast clients/servers)\

```{=html}
<!-- -->
```
-   Graphics/GUI capabilities - Pygame, OpenGL, Tkinter (stable)\

```{=html}
<!-- -->
```
-   Protocols - HTTP, BitTorrent - beta status

```{=html}
<!-- -->
```
-   Codec support - Dirac (encode/decode), Vorbis(decode),
    Speex(encode/decode), MP3 (decode - via pymedia)

```{=html}
<!-- -->
```
-   PyMedia based support for some audio codecs & audio capture\

```{=html}
<!-- -->
```
-   Devices:

```{=html}
<!-- -->
```
-   Alsa, DVB (digital TV broadcast)

```{=html}
<!-- -->
```
-   Unix Shell outs

```{=html}
<!-- -->
```
-   eg to call transcoding tools

Larger scale systems in the distribution\

-   Kamaelia Macro (timeshift & transcode what\'s broadcast for viewing
    at a more convenient time)
-   P2P Whiteboard (supporting multiple pages, linked whiteboards, audio
    mixing and retransmission, etc)

```{=html}
<!-- -->
```
-   Compose - a graphical composition tool for creating pipelines
-   Axon Shell - a specialised command line allowing the launch of
    components as well as programs
-   Axon Visualiser - a pygame based system for visualising what\'s
    going on inside a Kamaelia system (uses a physics model (based on a
    lava lamp(!) )for layout that we\'ve had repeated comments looks
    fun/attractive :)\
-   Show - a presentation tool\

[Examples](/Cookbook) for many major subsystems

Extensive [Documentation](/Components.html) (at minimum detailed module
level docs - ala pydoc)\
:::
:::

Ongoing [Projects](/Developers/Projects)\
[Developer Console](/Developers/)\
\

### Mailing lists 

General discussion:

We have moved the mailing list to Google Groups - group name
\"**[Kamaelia](http://groups.google.com/group/kamaelia)**\"\

-   <http://groups.google.com/group/kamaelia>

~~<http://lists.sourceforge.net/lists/listinfo/kamaelia-list>~~

~~kamaelia-list\@lists.sourceforge.net~~

Announcements:

-   <http://lists.sourceforge.net/lists/listinfo/kamaelia-announce>
-   kamaelia-announce\@lists.sourceforge.net

Subversion commits: (high traffic)\

-   <http://lists.sourceforge.net/lists/listinfo/kamaelia-commits>
-   kamaelia-commits\@lists.sourceforge.net

\

### News

-   **May 2008** - Project revamp - the project has continued under
    active development since the last news updates. Specifically a new
    iteration of the website is planned for release which should pull in
    more dynamic information more obviously. This is to coincide with a
    new release in June 2008, based on merging work currently sitting in
    Kamaelia branches.\
    \
-   **April 2008** - Project Mailing Lists have moved to Google Groups.
    You can find the **[Kamaelia group
    here](http://groups.google.com/group/kamaelia)**\
    \
-   **November 2006 - Website Revamp**\
    The website is undergoing a revamp at present - mainly to be online
    edittable rather than just offline. This should start to have some
    positive effects :-)\
    \
-   **October 2006 - Kamaelia in December\'s [Linux
    Format](http://www.linuxformat.co.uk/)**\
    Michael has written an article on Kamaelia for this month\'s Linux
    Format - on sale October 19th. It covers how to install and use the
    [Whiteboard](../../../Whiteboard/) application as well as basics of
    how to write components when building systems. The article will
    appear on this website when the magazine goes off sale!\
    \
-   **October 2006 - Kamaelia Mega Bundle 1.4 released!**\
    The Kamaelia Mega Bundle has been updated for Kamaelia 0.5 and Axon
    1.5.1. It includes the key dependencies that we\'ve tested the code
    with, specifically for components that make use of these external
    libraries. (Kamaelia is usable without these, but they are nice :-)\
    \
    Libraries included: Axon, Kamaelia, BitTorrent, dirac, Dirac (python
    bindings), Imaging, libao, libogg, libvorbis, pyao, pycrypto,
    pygame, pymedia, PyOpenGL, Pyrex, pySpeex, python-dvb3, speex,
    vorbissimple\
    \
-   **October 2006 - Kamaelia 0.5.0 Released!**\
    \
    Kamaelia 0.5.0 marks a major stepping point for the Kamaelia
    project. It means we officially have half the capabilities we see
    ourselves expecting to have when we hit version 1.0, and also marks
    the first release where the number of external contributors to the
    release outweighs developers from inside the BBC, meaning this
    release really does belong to the Google summer of code of code
    students who worked on it.\
    \
    Key highlights of this release:\
    Bit Torrent support; Open GL support; Nascent seaside style
    webserver (sessions controllable by resumable
    components/coroutines), massively enhanced DVB support,
    collaborative whiteboarding with audio (via speex) supporting
    daisychaining of whiteboards (since whiteboards are servers &
    clients), and enhanced visual system composition (ability to compose
    arbitrary graphs now). All of these include examples, including an
    Open GL interface to bit torrent, a bit torrent based simple
    (non-robust yet) streaming system, and a \"record for me\" PVR that
    you give the channel, and programme names to and it figures out the
    rest.\
    \
-   **October 2006 - Axon 1.5.1 Released!**\
    Highlights include:\
    Useful changes for a number of threaded components in the Kamaelia
    0.5.0 release. Synchronous boxes (size limited) are now supported by
    threaded components. Furthermore, synchronous boxes can now also
    pause themselves should the need arise.\
    \
-   [September 2006 - Meet us at ]{style="font-weight: 600;"}[[Euro
    OSCON]{style="font-weight: 600;"}](http://conferences.oreillynet.com/euos2006/)[!]{style="font-weight: 600;"}

[]{style="font-size: 12pt; font-weight: 600;"}\

[]{style="font-weight: 600"}

[[Licensing:]{style="font-weight: 600"}](Licensing.html)

-   See [COPYING](COPYING) for complete details, but as a
    [guide]{style="font-style: italic"}: Kamaelia is released under the
    Mozilla trilicense scheme (MPL/GPL/LGPL). This essentially means
    that if you change any files released you must license them under
    the same terms, but if you merely [use
    ]{style="font-style: italic"}the files, you only have to pass on the
    files you use. We view inheritance from classes in Axon as usage
    since this is generally how the component classes are intended to be
    used. Alternatively licensing [may]{style="font-style: italic"} also
    be granted if appropriate.

\

---
pagename: SummerOfCode2008
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Google Summer Of Code 2008
==========================

::: {#__ss_289017 style="float: right; width: 425px; text-align: left;"}
::: {style="font-size: 11px; font-family: tahoma,arial; height: 26px; padding-top: 2px;"}
[![SlideShare](http://static.slideshare.net/swf/logo_embd.png)](http://www.slideshare.net/?src=embed)
\|
[View](http://www.slideshare.net/kamaelian/sociable-software?src=embed "View 'Sociable Software' on SlideShare")
\| [Upload your own](http://www.slideshare.net/upload?src=embed)
:::
:::

**We\'ve been accepted as mentor org for Google Summer of Code 2008!
([BBC Research](http://www.bbc.co.uk/rd/))\
\
**[This is primarily our ideas page, you really ought to read our
overall summer of code page as well. This details expectations, how to
apply, what we\'re looking for, who we\'re looking for (YOU), and a
whole bunch of notes on stuff students have done in previous
years.](/SummerOfCode.html)\
**\
Previous years ideas pages( [2007](/SummerOfCode2007.html),
[2006)](/cgi-bin/projects/blog.cgi) landing pages(**
**[2007](/SummerOfCode.html),** **[2006](/SummerOfCode2006.html)
)**\

Ideas!
======

Please note that we\'re likely to give significant weight to Kamaelia
based exemplar projects. If you\'re wondering what we mean by that, the
Whiteboard, Greylisting and ER Modelling systems are all useful tools in
their own right, but also very useful exemplars showing how to build
large systems. Community systems like Bucker are similarly really cool
exemplars. The difference really between exemplars in Kamaelia and
exemplars in other projects is that you will often result in creating a
large number of reusable components.\
**\
Exemplar Related**\
\
In previous years we\'ve taken a couple of different approaches to the
ideas list. The first year was based around idea of distribution, (user)
security and visual interfaces. That worked pretty well. Last year we
really looked at an approach largely based around the idea of targetted
simple thing which would make kamaelia useful in particular targetted
ways, which achieved around 75% of our goals. This year though, we\'d
actually be much more interested in a systems view. ie rather than
building small bits and pieces we\'d be interested to see what **you**
can build in 2-3 months of work that\'s a real living breathing system.
For an idea of the sort of thing that that can entail, the visual system
builder was around 4 weeks of work all told and the P2P whiteboard was
actually around 2 -3 weeks all told. By contrast, [Kamaelia
Grey](/KamaeliaGrey.html) was literally a few days work.\
\
This list of possible exemplars is still being fleshed out, but really
interesting, useful exemplars are something that would get a high
priority this time round. Suprise us with a really exciting idea of
something you\'d like to build, and we might surprise you by accepting
it.\

-   A neat exemplar of the multiprocess idea above would be a
    **[multiwindow pygame](http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1196129474)
    based paint program** (or even post production tool). This could and
    should go to town in dealing with stacks of images. This could
    ideally build on the whiteboard, to the extent of allowing the
    simple creation of animated shorts. Ideally this would build on the
    whiteboard, ideally build on the video whiteboard even, to allow the
    creation, extension and annotation of video with simple (limited)
    video editting functionality.\
-   **Extend the [ER modelling](http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1195955570)
    tool to be a full database front end** for
    [WSGI](http://www.python.org/dev/peps/pep-0333/) based web systems.
    (This would require the creation of comtponents for managing
    databases of course)
-   **Small children friendly version of Compose**. At present a basic
    [Kamaelia based Logo interpreter](http://kamaelia.svn.sourceforge.net/viewvc/kamaelia/trunk/Sketches/MPS/KamaeliaKids.py?view=markup)
    exists (with pygame interface). Extending this to be a full,
    reliable Logo interpretation capable of building basic kamaelia
    pipelines or even graphlines would be extremely awesome. This should
    include support for espeak (on linux), speak (on Mac OSX) and pyTTS
    (on windows) based speech synthesis for feedback. Bonus points would
    come from integrating with the [gesture recognition
    code](http://kamaelia.svn.sourceforge.net/viewvc/kamaelia/trunk/Sketches/MH/GestureRecognition/)
    to allow usage without using the keyboard.
-   **Extend the [XMPP implementation](http://trac.defuze.org/wiki/headstock) code,**
    documentation and example so that the core and some common XMPP
    extensions are implemented
-   Tools for working with SQL Databases. Build a Kamaelia interface for
    SQL so that databases can be linked to other Kamaelia components.
-   **3D Social Network Visualisation tool**. This builds on 2 core
    project ideas. The assumption is that the social network will be
    embedded in some kind of SQL database, which can be extracted by a
    component. Then, extend topologyVisualiser in the Kamaelia
    distribution to work in 3D. This will allow complex datasets to be
    viewed as 3D shapes with nodes and connectors. Imagine that a
    database contains a set of relationships with assocated data (such
    as you might find on facebook), extend topologyVisualiser to allow
    relationships to be clearly explored and viewed.
-   **Kamaelia, [Jython](http://www.jython.org/Project/index.html)** **&
    [Processing](http://processing.org/)** **integration.** ([Processing
    on Jython has been done](http://itp.nyu.edu/blogs/drawingmachines/2008/02/10/jythonprocessing-fun/))
    For something completely different, howabout getting Kamaelia
    working with Jython using the processing library? This should work,
    though require a bit of effort. The neat thing about this though
    would be the ability to have great visualisations in a browser (due
    to processing), which have all the fun and extensibility of Kamaelia
    (due to jython). This could actually be a much nicer way of
    visualising databases using kamaelia (as suggested by the social
    network visualisation project idea)
-   **Simple Video conferencing tool.** You\'ll need to wrap some webcam
    bindings and wrap those. You\'d expect to take those images for
    display, but also change them to pipe into (say) the Dirac
    compression components, send over a link, decompress and display.
    This would actually be an exemplar of showing what happens when a
    new component for handling a new device comes into play since the
    communications/compression & decompression work pretty much already
    exist, as does the display tools. The webcam bindings idea actually
    comes from [pygame\'s GSOC ideas list](http://www.pygame.org/wiki/gsoc2008ideas) and is more of an
    example application of said bindings.
-   **Swarming P2P / layer 5 multicast radio system.** Last year at [LUG
    Radio Live](http://www.lugradio.org/live/2007/index.php/Main_Page)
    Michael demonstrated/explained how a simple swarming radio system
    could be built using Kamaelia. It consisted of two main parts - a
    [radio source](http://kamaelia.svn.sourceforge.net/viewvc/kamaelia/trunk/Sketches/MPS/LUGRadio/SimpleSwarmRadioSource.py?revision=3294&view=markup)
    and [a swarm peer](http://kamaelia.svn.sourceforge.net/viewvc/kamaelia/trunk/Sketches/MPS/LUGRadio/SimpleSwarm.py?revision=3293&view=markup).
    It would be interesting to see this extended to be a robust P2P
    swarming radio system. One of the more interesting ways this could
    be made more robust would be to allow the P2P tree created to
    actually turn into a P2P mesh that forms a Layer 5 Multicast overlay
    network. One particular approach that would work well when sitting
    on top of this would be a [scattercast type](http://research.chawathe.com/people/yatin/publications/)
    system, which could work extremely well when constructed in a P2P
    fashion. ([see the tail of this presentation for more
    detail](http://www.slideshare.net/kamaelian/building-systems-with-kamaelia))\

\
**Core project related**\

Integrate Kamaelia with\...

-   **Integrate kamaelia with Stackless** - provide mappings from the
    stackless world of tasklets & channels to components and
    in/outboxes. This should be idiomatic for both stackless and
    kamaelia. One way to do this would be to implement a
    \"TaskletComponent\" like we have Component, ThreadedComponent and
    ProcessComponent.
-   **Integrate Kamaelia with Twisted** - We have kinda partially done
    this before in the BitTorrent code, but it would be really nice to
    be able to write a TwistedComponent, and to be able to use Twisted
    from Kamaelia and to be able to run the Kamaelia scheduler from
    Twisted. The LikeFile backgrounding code may be useful here.
-   **Integrate Kamaelia with gstreamer** - similar dance ! :-)\

**WSGI-ify the Kamaelia Web Server** - Extend & make more user friendly
the Kamaelia Web Server, including
[WSGI](http://www.python.org/dev/peps/pep-0333/) compliance, to enable
clientside mashups based around (say) django or pylons

**Tools for working with SQL Databases.** Build a Kamaelia interface for
SQL so that databases can be linked to other Kamaelia components.

A **Testing Framework** for Kamaelia Systems

**Improved Multicore support:** Extend python
[pprocess](http://www.boddie.org.uk/python/pprocess.html) to enable full
duplex channel communications (or multichannel communications with
processes) for multicore/multiprocess comms (eg
[1,](http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1196029230)
[2](http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1196129474)
)\

**Extensions to the [co-ordinating assistant
tracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html)** :

-   Modify the [co-ordinating assistant
    tracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html)
    to use the minimal [STM](/STM.html) code

```{=html}
<!-- -->
```
-   Make [co-ordinating assistant
    tracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html)
    environments inheritable

**Change the [topology
visualiser](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html)
to work in full 3D** - this would relate to changing the implementation
from using the pygame code and replacing it with open GL code. Most of
the physics engine would still work. This would then turn into an
exemplar you you extended to allow the construction of models this way.
This sounds difficult, but should be relatively simple\

**Extend Kamaelia\'s [Dirac](http://dirac.sourceforge.net/) support to
include** support for the optimsed version of
[Dirac](http://dirac.sourceforge.net/) called
**[Schoedinger.](http://schrodinger.sourceforge.net/ideas.php)** (Rather
amusingly you\'d be working on schoedinger\'s cat (sorry))

**Improve Kamaelia\'s support on Windows** - come up with windows
equivalents of the mega bundles or better the app bundles

See how much of **Kamaelia** can run **on IronPython 2** (notably see
how many tests can pass)

**Projects tend to succeed if you** **discuss them upfront with the mentor organisation.**
------------------------------------------------------------------------------------------

*So, if you\'re interested in any of these ideas, please discuss them
with either Michael Sparks or Matt Hammond over email -
kamaelia-list\@lists.sourceforge.net ( or anyone else on the list).
You\'ll also find us in \#kamaelia on
[freenode\'s](http://freenode.net/) IRC network.*\
\

Project Introductions
---------------------

Think \"lego for software\", and \"concurrency made easy\" if you\'re
after a soundbite. The presentation above should give you the basic
idea\
\
**More Technical intros:**\

-   <http://tinyurl.com/2hl8kj> - App focussed description on the P2P
    networked whiteboard with local remixing of audio (written for Linux
    Format)
-   <http://tinyurl.com/yp7crf> - general light technical intro (written
    for Linux Magazin germany)
-   <http://www.slideshare.net/kamaelian/building-systems-with-kamaelia>
    the first half of a talk given at LUG Radio - given as a standalone
    at pycon UK last year. Includes how to build a P2P streaming system
    for audio off DVB. (sans buffering & error handling)

**Fluffy:**\

-   [Introduction](/Introduction.html) - v short overview
-   [/Challenges/](/Challenges/) -
    a *slightly* tongue in cheese document for the open days in 2005
    based around describing the context of the projects Kamaelia was
    then being developed around. (times move on)

**Tutorials**\

-   [/MiniAxon/](/MiniAxon/) -
    I\'m a firm believer in showing people how to make their own version
    of the core of the system.
-   <http://tinyurl.com/2p9zku> - example of how go from concept to
    component

See also the [Cookbook](/Cookbook.html) &
[Components](/Components.html) links above!

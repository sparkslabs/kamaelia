---
pagename: Developers/Roadmap
last-modified-date: 2009-05-23
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
\

Development Roadmap
===================

The path to Kamaelia 1.0 {#the-path-to-kamaelia-1.0 align="right"}
------------------------

\

Timeline
--------

-   [0.6.0 - Released](http://www.kamaelia.org/ReleaseAnnouncement060)

Note: the version numbering below is changing to date based versioning.\
\
Releases to happen:\

-   0.9.5, Target: 31st May 2009
-   0.9.7, Freeze: 6th July 2009, Target: 13th July 2009
-   0.9.9, Freeze: 7th Sept 2009, Target: 14th Sept 2009
-   0.9.11, Freeze: 2nd Nov 2009, Target: 9th Nov 2009

Beyond that date, this release schedule - which is based on \"freeze on
the first monday of every other month, and full release the following
monday\" - will probably need reviewing. If it seems appropriate, and if
code has reached an appropriate stage, the release cycle will probably
be this:\

-   **1.0.2 -** **Probable Full Release, Freeze: 1st Feb 2010, Target
    release: 8th Feb 2010**
-   1.0.4 - Freeze: 5th April 2010, Target: 12th April 2010
-   1.0.6 - Freeze: 7th June 2010, Target release: 14th June 2010

Reaching beyond that sort of timeline seems foolish, so I\'m not going
to try.\
\

Feature Roadmap
---------------

Things that would be useful to go into releases\... This section is a
work in progress and will take time to dump out the various ideas people
have had. Please bear with us and [discuss this on the mailing
list.](http://groups.google.com/group/kamaelia/post?subject=Features+Roadmap+on+http://www.kamaelia.org/Developers/Roadmap)\

**Overall aims:**

Performance, Performance, Performance. Fibra shows that this is doable,
and we should either match fibra, beat fibra, or join with fibra. (the
last option is probably most fun :)\

Frame work for enabling greater contribution - through Kamaelia.Apps.\*
namespace

Larger, more comprehensive examples - based around existing real world
apps.

Website goals:

-   To make overall clearer & greater/clearer separation of:

```{=html}
<!-- -->
```
-   Axon

```{=html}
<!-- -->
```
-   Kamaelia

```{=html}
<!-- -->
```
-   Kamaelia Apps

```{=html}
<!-- -->
```
-   Ongoing development area\

**Aspirations:**

-   Merged of Chong\'s Google Summer of code project - [3D visualisation
    work](http://www.kamaelia.org/Developers/Projects/3DTopologyVisualiser)
    (since this is something I actually need sooner rather than later)
-   Flesh out http://www.kamaelia.org/Presentations somewhat\...
-   Packaging up of the
    [whiteboard](http://www.kamaelia.org/t/TN-LinuxFormat-Kamaelia.pdf)
    (pdf) as a standalone app
-   Packaging up of the [batch file
    processor](http://code.google.com/p/kamaelia/source/browse/branches/private_MPS_Participate/Apps/FileProcessor/App/BatchFileProcessor.py)
    (image/video transcoder) as a standalone app (or better packaging
    than
    [this](http://http//www.kamaelia.org/release/Kamaelia-FileProcessor-0.1.0.tar.gz))
-   A mirror of the Ben\'s [Kamaelia
    AWS](http://code.google.com/p/kamaelia-aws/) code into
    Kamaelia.Apps.AWS, if it\'s at a stage where it\'s ready. (aside
    from reviews etc)

```{=html}
<!-- -->
```
-   Merge of Jason\'s google summer of code on on
    extensions/improvements to the HTTP server code, including a better
    example of the seaside like functionality. (I think [Kamaelia
    Publish](http://www.kamaelia.org/Developers/Projects/KamaeliaPublish)
    itself should probably wait until 0.8.12 or 0.9.X) Probably after it
    gets a clearer name.

Perhaps initial work on [integration of the STM code into the
CAT](http://groups.google.com/group/kamaelia/browse_frm/thread/7c9fe6a4202303e5).
(The what? [The STM and CAT tools were discussed at pycon
uk](http://www.slideshare.net/kamaelian/sharing-data-and-services-safely-in-concurrent-systems-using-kamaelia-presentation/))
Though I suspect this will get started now, and merged in 0.8.12

2.6 cleanups (probably based on hinting from 2to3), and work started on
a 3.0 autoconversion/build system.

Other stuff I\'d like to see includes : work started on rationalising
Kamaelia.File, Full review and merge of UDP\_ng code in place of current
UDP code, basic \"connected\" UDP server support (perhaps) (ie such that
it can be used as a drop in replacement for TCPServer in ServerCore)

Better graphline shutdown [as discussed on the
list.](http://groups.google.com/group/kamaelia/msg/dd78c6c1a8125236)

Tyson\'s extended version of the file appender,

SuSE packaging for
[Axon](http://rpm.pbone.net/index.php3/stat/4/idpl/9272711/com/python-axon-1.5.1-1.1.i586.rpm.html)
&
[Kamaelia](http://rpm.pbone.net/index.php3/stat/4/idpl/9308970/com/python-kamaelia-0.5.0-1.1.i586.rpm.html)
updated from 0.5.0 to K0.6.0 & A1.6.0

-   And future packaging changes automated, ideally. (enabling 0.7.0
    easily)

Nanowrimo examples! & results of Nanowrimo example writing\...

Merge of other Summer of code projects.

Probably Dave\'s paint program

Rest of Jason\'s code, esp WSGI support

Start scavenging Joe\'s project for mergeable components.

Could consider merging code from Pablo\'s abortive planet code, since
may have useful scavengeable code.

Start extracting Matt\'s testing framework from graphline tests, to see
what we can do.

-   Will better graphline shutdown help here?

[Start work on merging CAT with STM
code](http://groups.google.com/group/kamaelia/browse_frm/thread/7c9fe6a4202303e5#)

[Aim to have started the path to python 3.0. (hence 0.9.3 would
hopefully be alpha quality python
3.0](http://groups.google.com/group/kamaelia/browse_frm/thread/fb61e380c3e8a0c9#)

Would be nice to have a Threaded\* Chassis - for taking normal Kamaelia
components and slinging them into seperate threads.

-   Requires CAT+STM to be completed

```{=html}
<!-- -->
```
-   If done, rewrite threaded components to use this chassis
-   If done, potentially deprecate threadedcomponent. (maybe, needs
    thought)\

**Aspiration:**

-   **Compatible with python 3.0 through a combination of using 2to3 and
    automated patches**
-   Requires a framework to be started to assist with this.

**1.0.2 -** **Probable Full Release**

-   Kamaelia 1.0 Release
-   Axon 2.0 Release
-   Python 3.0 compatible release (non alpha, non beta, actual release)\

Other Aspiration Features
-------------------------

If you want to add features you\'d like to see, please [add to this
thread on the mailing
list](http://groups.google.com/group/kamaelia/post?subject=Possible+Roadmap+Feature+Your+Idea),
we can then reference the thread back here for discussion purposes.
**PLEASE** remember to replace \"Your Idea\" in the subject line with
your feature idea!\

Possible Questions, Answers
---------------------------

### Version numbers.

Kamaelia\'s version number is pre-1.0 for good reasons (as of Nov 2008)
- there are specific things that (at least) Michael would like to see in
a full version 1.0. However, many projects are switching to a more date
based approach. Since we figure that we\'re about a year away from being
\"feature complete\" in Kamaelia (in terms of graphical creation tools,
full set of appropriate chassis, potential for shard support, etc) it
seems reasonable to switch to a versioning of **Y**.**Y**.**MM**.\
\
This is the reason for 2 releases before the end of the year - 0.7.0
being the next logical one after 0.6.0, and the one after 0.7.0 being
0.8.12, with 0.8.12 being the first release matching the new versioning
scheme.\
\
If the project keeps running then, then I would also expect the
following:\

-   Y.Y.MM to be used as version number in 2009
-   Y.Y.MM to be used as version number in 2010
-   1.MM to be used as version number in 2011
-   Y.MM to be used as version number 2012 - 2019(last digit of year
    only)

It seems really odd to be planning version numbers that far out, but
it\'s worth realising the first release of Kamaelia was in 2004, so 2012
is the same timeframe (or so) forwards. Not only that, but Kamaelia\'s
model does seem to have longevity.\

### Timing? 6 Weeks? Bi-Monthly? 

These target dates are deliberately far enough to be doable, but not so
far that the planning for each stage to become unrealistic. Also,
they\'re specifically designed to prevent \"mega\" releases being
planned with \"one more thing\" preventing actual release.\
\
\-- Last updated November 2008\
\
That didn\'t work. Shifting to 2 monthly cycles instead, since it feels
more \"humane\" :-)\
\
\-- May 2009\
\
As of the [0.6.0
release](http://www.kamaelia.org/ReleaseAnnouncement060) the project is
moving through a transition stage.\
\
Future releases will be based on a bi-monthly release cycle, with
version numbers based on dates, rather than arbitrary(!) version
numbers.\

---
pagename: ReleaseJune2008
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Target for next release: June 2008
==================================

It\'s been too long since the last release, for a variety of valid,
practical reasons. The aim is to restart the build/release process,
basing it on the newer packaging style used by Kamaelia { Logger, Grey,
Modeller }.\
\
Recent comments on various blogs suggest packaging can be improved, and
whilst the newer packaging style is an improvement, more \*concrete\*
suggestions for improvement are welcome - whether they\'re to do with
\"don\'t stop this\" \"stop doing this\" \"start doing this\" etc.\
\
Davbo queried why a significant amount of code from
private\_MPS\_Scratch hasn\'t been merged to trunk yet \-- Michael
replied it was largely time related, and extra help with merging would
be useful, and also what\'s important to merge from there. It\'s worth
noting that branches with specific sets of features now need claiming,
and that there\'s still a ton of work to do in merging code.\
**\
Branches (most recently) Merged**\

> private\_MPS\_JL\_PygameText/\
> private\_MPS\_JL\_AIMSupport/\
> private\_MPS\_ERModeller/\
> private\_MPS\_JL\_IRCSupport/\
> private\_MPS\_KamaeliaLogger\
> private\_MPS\_STM\
> private\_MPS\_TCPServerImprovments\
> private\_MPS\_Tools2AppsConsolidation\
> \
> *private\_MPS\_TickerFix\_mashed\
> private\_MPS\_LikeFileRewrite*\
> *private\_MPS\_PygameImprovements*\
> *private\_MPS\_AxonCoreImprovements\_mashed\
> Multicore/multiprocess code merged as Axon.experimental - [expect this
> to change\
> ]{.underline}*..*[\
> ]{.underline}***\
> **

**Branches Merged Prior to Mashed\
**Branches created (branch point rev included) **pre-mashed** to allow
rollback if unstable\

-   4496 - private\_MPS\_TickerFix\_mashed
-   4500 - private\_MPS\_LikeFileRewrite
-   4530 - private\_MPS\_AxonCoreImprovements\_mashed
-   4538 - private\_MPS\_PygameImprovements
-   r4556 - private\_MPS\_HTTPImprovements

**Branches That Need Merging**\
These branches need claiming for merge:\

> ***None at present!***\

**Things that can go in the release if time.**\

-   Kamaelia Grey merge
-   Filereading improvements
-   TCPClient enhancements
-   TPipe Chassis (maybe)
-   Support.Data.Repository changes
-   PureTransformer enhancements
-   Shutdown improvements to a variety of components
-   Improvements to protect memory (hard limits in rate filtering)
-   Improvements to the topology visualiser core
-   Fixes/improvements to chunks\_to\_lines
-   PyMedia runtime protection
-   Initialisation/Configuration improvements (merged)\
-   Axon enhancements ***\--***
    ***private\_MPS\_AxonCoreImprovements\_mashed/ - r4530***
-   Likefile replacement/reversion/reimplementation -
    ***private\_MPS\_LikeFileRewrite/ -r4500** **(merged)***\
-   [HTTP subsystem improvements](ReleaseJune2008/PossibleHTTPMerge.html) -
    ***private\_MPS\_HTTPImprovements - 4556 (merged)***\
-   Ticker fixes - ***private\_MPS\_TickerFix\_mashed** **- 4496
    (merged)\
    ***
-   Pygame.Image, Pygame.Display enhancements ***-
    private\_MPS\_PygameImprovements - 4538 (merged)***\
-   More examples\...

**Todo list beyond that, if time, in no particular order**\

From discussion:

MoreComplexServer should go in (named better - perhaps as ServerCore) -
**DONE**\

Experimental WSGI server needs to go in (under Experimental) - **first
iteration of this has actually gone in as an \*example\* rather than as
something intended for easy reuse.**\

Matt wants to sort:

sort out DVB bindings

refresh dirac/schroedinger bindings

j\_baker may:

-   refactor the HTTPParser code some.

Push for website to be sorted by then. - *didn\'t happen, but hey, code
comes first, website will get a revamp for the non-beta release.*\

Lots of support from people on the channel :-)

Need a more formal wishlist to know the goal posts.

Starting point: a working wiki (done), but mailing list suffices Target
release date: By Midsummer\'s day (coincides with BBC \"Mashed\" )\
\
Ideas for stuff to go into the release:\

runtime profiler - /Sketches/MH/Introspection/Profiling.py (needs
tidying up first)

Merge as much of private\_MPS\_Scratch onto trunk - **This has worked
really really well - massively there**\

Website update - **TBD**\

Packaging up major Kamaelia apps - **TBD**\

mhrd:

-   I\'m hoping to have a few more DVB components or example ready
    before then which I\'d hope can make it into the release too (all a
    bit dependent on how much time I can devote to that tho)

UDP components (including multicast) using Selector - **MERGED**\

The WSGI stuff should hopefully be able to go in in time (albeit
possibly under Experimental) -Jason - **Parts actually under
\"examples\"**\

Release notes - **Partial release notes in michael\'s blog**\

Detailed changelog - **Needs more detail**\

Documentation review

**Things can be very helpful:**\

-   review and merge of branches (review includes running code if you
    have the hardware of course)

Current Changelog notes (since last release)
--------------------------------------------

This is turning into a very large/substantial release. This implies a
bump from 0.5.X to 0.6.0\
\

>        * Kamaelia.UI.Pygame.Text Added - (similar to Ticker, but input as well
>
>          as output. Line oriented rather than word)
>
>        * Added minor bugfix for Windows support for TCP clients
>
>        * Fix to reliability of DVB support
>
>        * Basic SSL support added - allow, for example, HTTPS components
>
>        NEW TOOLS:
>
>        Simple Video Player:
>
>         * plays the sound and pictures from a video file
>
>        Video Reframer:
>
>         * applies an XML edit decision list to cut, crop and scale a video sequence;
>
>           reframing the content for other use.
>
>        Video Shot Change Detector:
>
>         * outputs an XML file describing the frame indices at which shot changes
>
>           probably occur in a sequence of video
>
>        NEW COMPONENTS:
>
>         * WAV format parsing and writing
>
>         * YUV4MPEG2 format parsing and writing
>
>         * Additional UnixProcess component with named pipe support
>
>         * Various simple utility components
>
>         * Pygame Video Surfaces (as opposed to overlays)
>
>         * YUV to/from RGB video frame pixel format conversion
>
>         * SDP parsing
>
>         * RTP packet parsing and writing
>
>         * Out of order packet reordering
>
>         * "Maximum speed" file reading
>
>         * Simple XML parsing
>
>         * Video shot change detection
>
>         * Video frame cropping and scaling
>
>         * Experimental Pipeline/Graphline/Carousel support for size limited inboxes
>
>         * Sequencing of tasks (Seq component)
>
>        Changed the CSA such that it no longer has internal buffering. This means
>
>        that if you make the link *TO* the CSA synchronous that you will be able
>
>        to send to the link as fast as the link will handle without causing over
>
>        buffering.
>
>        Bugfixes to:
>
>         * Kamaelia.Chassis.Carousel component - rewrite to fix shutdown behaviour.
>
>        Bugfixes to:
>
>         * Kamaelia.UI.Pygame.BasicSprite component.
>
>         * Kamaelia.Util.RateFilter.ByteRate_RequestControl component.
>
>         * Kamaelia.Protocol.HTTP.HTTPClient.SimpleHTTPClient component.
>
>        Added Documentation generation tools for generating Axon and Kamaelia
>
>        reference documentation - see their docstrings for more information.
>
>        Enhanced Kamaelia.Support.Data.Repository to support fuller introspection
>
>        of components, prefabs, classes and methods in the repository, including
>
>        their arguments and documentation. The "Compose" tool now uses this,
>
>        instead of trying to import all components.
>
>        Dirac 0.6.0 release now supported by Dirac components (through 0.6.0
>
>        bindings)
>
>        Bugfixes to:
>
>         * Kamaelia.Audio.PyMedia.Input component now works on win32
>
>         * Kamaelia.UI.Pygame.Display no longer freezes up on win32 & MacOSX
>
>         * "Show" example correctly now instantiates XML parser on win32 & MacOSX
>
>           including Kamaelia.Support.Data.Experimental XML graph parser
>
>           component
>
>         * Kamaelia.Util.Chooser components are now all quiescent when idle
>
>        Bugfixes to:
>
>         * Various example programs in /Code/Python/Kamaelia/Tools and Examples
>
>           to remove use of deprecated components.

Please add to the top of this. Rationalising things together and
correcting welcome.\
\
\

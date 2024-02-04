---
pagename: Developers/Branches
last-modified-date: 2008-10-06
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Branches & Status 
=================

### Branches Ready For Merge 

-   \

### General branches under active development 

**py2.6\_fixes/**

-   Created by JMB - purpose is to fork /trunk/Code/Python to deal with
    any 2.6 related fixes
-   Not intended for new feature development

### Personal Branches 

***Michael***\

**private\_MPS\_Scratch/**

-   This branch is in the process of having a fair amount of
    functionality and changes merged onto mainline. See also [0.6.0
    planning page](/ReleaseJune2008)
-   branch will not be merged directly but have code spun out to be
    merged.\
    \

**private\_MPS\_Games4Kids/**

-   This is a collection of tools for developing simple/silly games for
    small kids. Work in progress. Some parts will be merged sooner
    rather than later.\
    \

**private\_MPS\_SpeakNLearn/**

-   Developed as a hack for mashed, this is an application that works
    and is useful, and merges in stroke/handwriting recognition onto
    mainline. Again, this will be merged sooner rather than later\
    \

**private\_MPS\_Participate/**

-   Michael\'s day work is currently on Participate. One of the major
    systems built for this is a file processor - which is inside this
    branch. It is likely that this will be put up for merge sooner
    rather than later.\
    \
    \

**private\_MPS\_MiniKamaelia\_Networking/**

-   Intended as a micro-distribution of Kamaelia to work around the idea
    that Kamaelia can be viewed as a swiss army knife, when it fact the
    \"toy box\" metaphor is perhaps better.\
    \

***Matt***

**private\_MH\_20080523\_dvbNewStuff/**

-   Status unknown\

### GSOC Branches

**Likely to have some sort of merge due to happen\...\
**

-   private\_CL\_Topology3D/
-   private\_CL\_Topology3D\_gsoc2008/
-   private\_DK\_PaintDev/
-   private\_DK\_Paint\_gsoc08/
-   private\_JMB\_PublishWebServe\_gsoc2008/
-   private\_JMB\_Wsgi/
-   private\_JT\_JamDev/
-   private\_JT\_Jam\_gsoc2008/
-   private\_JT\_PygameDisplayImprovements/
-   private\_JT\_SelectorUDP\_mashed/

**Likely not to be merged:**

-   private\_PO\_Tests/

### Special Branches

**merged/**\

-   Branches that have been merged are moved here initially before
    deletion. (the delay is to simplify reversion if needed)

**rejected/**\

-   Branches that have been rejected are moved here initially before
    deletion. (just in case we change our minds!)\

### /merged/ Branches Pending delete

Branches that have been merged, but could be deleted, but haven\'t been
deleted yet

-   bp\_vorbis\_simple\_0\_0\_2/
-   Kamaelia\_0\_4\_0\_Deprecations/
-   Kamaelia-private\_MPS\_SelectorRewrite/
-   private\_JL\_SOC2007/
-   private\_JMB\_AddedIndexCapabilityToMimimal/
-   private\_JMB\_HTTPFixes/
-   private\_MPS\_AxonCoreImprovements\_mashed/
-   private\_MPS\_HTTPImprovements/
-   private\_MPS\_KamaeliaLogger/
-   private\_MPS\_LikeFileRewrite/
-   private\_MPS\_PygameImprovements/
-   private\_MPS\_STM/
-   private\_MPS\_TCPServerImprovments/
-   private\_MPS\_TickerFix\_mashed/
-   private\_MPS\_Tools2AppsConsolidation/
-   private\_MPS\_KamaeliaGrey/ - Merged - contains KamaeliaGrey

### /rejected/ Branches Pending delete

Branches that have been rejected, but could be deleted, but haven\'t
been deleted yet

private\_JMB\_MinimalFix/

private\_JMB\_Packager/

private\_RJL\_InternetChanges/

**private\_MPS\_HalfCloseSupport/**

Purpose: Branch created for redoin the half closed connection support.\

Branch point: r2983 (old)\

Current status: stalled - unclear what the application level logic would
be that makes sense. Needs review as to worthwhile or not.

Changes are obscured due to complaints regarding the copyright notice at
one point\...

-   Likely way forward : delete and redo if needed - especially
    considering we do have partial half close support on /trunk already\
-   svn diff -r2983:2994 \-- change is relatively small.

### Deleted Merged Branches

Branches in revision 4274:\
\

-   bp\_vorbis\_simple\_0\_0\_2/
-   Kamaelia\_0\_4\_0\_Deprecations/
-   Kamaelia-private\_MPS\_SelectorRewrite/
-   private\_JMB\_AddedIndexCapabilityToMimimal/
-   private\_MH\_20070423\_kamaelia\_bugfixes/
-   private\_MH\_20070424\_kamaelia\_deprecationfixes/
-   private\_MH\_20070425\_spritebugfix/
-   private\_MH\_20070429\_newcomponents/
-   private\_MH\_20070509\_axonwarnings/
-   private\_MH\_20070522\_threadedcomponent\_bugfixes/
-   private\_MH\_20070618\_docgen\_improvements/
-   private\_MH\_20080518\_DvbFixes/
-   private\_MH\_axon\_flowcontrolinversion/
-   private\_MH\_axon\_optimisations/
-   private\_MH\_axon\_outboxwakeups/
-   private\_MH\_axon\_syncboxesforthreadedcomponent/
-   private\_MH\_axon\_threading/
-   private\_MH\_axon\_threads/
-   private\_MPS\_AxonIdea/
-   private\_MPS\_ERModeller/
-   private\_MPS\_JL\_AIMSupport/
-   private\_MPS\_JL\_IRCSupport/
-   private\_MPS\_JL\_PygameText/
-   private\_MPS\_SynchronousBoxes2/
-   private\_MPS\_UnbufferedCSASupport/
-   private\_PT\_SOC2007/
-   private\_PT\_WindowsTCPClientFix/
-   private\_SH\_SSLCSA/
-   private\_MH\_20070425\_dirac0.6.0bindings/

### Legacy Branches

RELEASE/\
AXON\_1\_0/\
BITTORRENT\_4\_4\_0/\
\
\

---
pagename: ReleaseProgress070
last-modified-date: 2008-11-23
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Release Progress: 0.7.0
=======================

This page is for tracking 0.7.0 from planning through to release
**Current status:\
[ FROZEN ]{style="background-color: rgb(51, 255, 51);"}**\
Freeze Target: 2008/11/23\
Release Target: w/e 2008/11/30\
**If you\'re looking for the current release**, please go to the [Get Kamaelia](GetKamaelia.html) page since it always links to the current version

Draft Release Notes
-------------------

SuSE packaging for
[Axon](http://rpm.pbone.net/index.php3/stat/4/idpl/9272711/com/python-axon-1.5.1-1.1.i586.rpm.html)
&
[Kamaelia](http://rpm.pbone.net/index.php3/stat/4/idpl/9308970/com/python-kamaelia-0.5.0-1.1.i586.rpm.html)
in done

Repackaging for a new release seems relatively simple

-   grab the SRPM, do a rpmbuild -bp *specfile*
-   copy the new tar ball into the SOURCES directory
-   edit the specfile to update it to point at the new tarball, and
    update the change log\
-   Then rebuild the binary rpm using rpmbuild -bb *specfile*
-   Test it, by installing the new binary file
-   Assuming you\'re happy with the results, build a source RPM as well
    using: rpmbuild -bs *specfile*
-   Upload, announce, be happy.
-   Tell the nice people at suse that you\'ve done this :-)

DVB\_Multiplex component changed to support multiple adapters (ie not
just adapter0)

DVB/Core.py, DVB/Tuner.py changed to automatically pick up which DVB
tuning class. Now supports DVB-C (in holland) as well.\

-   python\_dvb3 bindings updates to 0.0.5 - added in a support
    function.\

Extended Kamaelia.Util.Console.ConsoleReader to have clean shutdown

Tyson\'s File Append component:

-   Merged onto branch private\_MPS\_FileAppender
-   Cleaned up, documentation added, extended slightly

Implemented better graphline shutdown on branch
private\_MPS\_ImprovedGraphlineShutdown:

It extended Graphline slightly such that, when a message is received on
the Graphline\'s \"control\" inbox, that the message is copied to all
subcomponents\' \"control\" inbox, as long as they don\'t already have
anything linking there already.

If a shutdown message is sent to the graphline, the graphline will now
terminate normally, after having passed on that message to
subcomponents.

Example of usage here:
[DemoShutdown.py](http://kamaelia.googlecode.com/svn/branches/private_MPS_ImprovedGraphlineShutdown/Kamaelia/Examples/UsingChassis/Graphline/DemoShutdown.py)

Also now has a decent test suite.

-   Worth investigating how to extract and generalise the general test
    pattern from this.

Work in progress - Bumped to 0.8.12 
-----------------------------------

**Note:** *\"if not done by\"* is a means of timing out ownership of an
item. It makes no judgement other than that.\

Awaiting review/merge

-   review/merge
    [[private\_CL\_Topology3DCore]{#thread_subject_site}](http://groups.google.com/group/kamaelia/browse_frm/thread/599eefa8ee835b5b)[
    (27/10)]{#thread_subject_site}

```{=html}
<!-- -->
```
-   [Reclaimed by Michael 2/11/08. If not merged by 5/11/08, becomes
    unclaimed again.\
    ]{#thread_subject_site}

Bumped to 0.8.12 
----------------

Current outline plans discussed:\

-   Merged of Chong\'s Google Summer of code project - [3D visualisation work](/Developers/Projects/3DTopologyVisualiser.html)
    (since this is something I actually need sooner rather than later)
-   Flesh out http://www.kamaelia.org/Presentations somewhat\...\
-   Packaging up of the
    [whiteboard](http://www.kamaelia.org/t/TN-LinuxFormat-Kamaelia.pdf)
    (pdf) as a standalone app
-   Packaging up of the [batch file
    processor](http://code.google.com/p/kamaelia/source/browse/branches/private_MPS_Participate/Apps/FileProcessor/App/BatchFileProcessor.py)
    (image/video transcoder) as a standalone app (or better packaging
    than
    [this](http://http//www.kamaelia.org/release/Kamaelia-FileProcessor-0.1.0.tar.gz))
-   A mirror of the Ben\'s [Kamaelia AWS](http://code.google.com/p/kamaelia-aws/) code into
    Kamaelia.Apps.AWS, if it\'s at a stage where it\'s ready. (aside from reviews etc)
-   Merge of Jason\'s google summer of code on on
    extensions/improvements to the HTTP server code, including a better
    example of the seaside like functionality. (I think [Kamaelia Publish](/Developers/Projects/KamaeliaPublish.html)
    itself should probably wait until 0.8.12 or 0.9.X) Probably after it
    gets a clearer name.
-   Perhaps initial work on [integration of the STM code into the
    CAT](http://groups.google.com/group/kamaelia/browse_frm/thread/7c9fe6a4202303e5).
    (The what? [The STM and CAT tools were discussed at pycon
    uk](http://www.slideshare.net/kamaelian/sharing-data-and-services-safely-in-concurrent-systems-using-kamaelia-presentation/))
    Though I suspect this will get started now, and merged in 0.8.12
-   2.6 cleanups (probably based on hinting from 2to3), and work started
    on a 3.0 autoconversion/build system.
-   Other stuff I\'d like to see includes : work started on
    rationalising Kamaelia.File, Full review and merge of UDP\_ng code
    in place of current UDP code, basic \"connected\" UDP server support
    (perhaps) (ie such that it can be used as a drop in replacement for
    TCPServer in ServerCore)

\...\
\

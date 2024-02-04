---
pagename: GettingStarted
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Getting Started]{style="font-size: 24pt; font-weight: 600;"}

[How to set up your environment for Kamaelia]{style="font-size: 18pt;"}

::: {.boxright}
[Feedback sought!]{style="font-weight: 600;"}
:::

Assumption:

-   You are using a modern linux distribution with development tools for
    C and python installed, along with some common libraries for music &
    perhaps video.
-   That you have root access on the system, and use sudo. If you don\'t
    use sudo mentally skip that below.

[Quickstart Instructions]{style="font-size: 14pt; font-weight: 600;"}

[[Download]{style="font-weight: 600;"}](http://prdownloads.sourceforge.net/kamaelia/KamaeliaMegaBundle-1.0.1.tar.gz?download)
the files you need (you might need less than this link gives you)

[Install]{style="font-weight: 600;"} the core packages (Axon & Kamaelia)

[Start playing]{style="font-weight: 400;"}[
]{style="font-weight: 600;"}with the examples, which are also in the
[cookbook](/Cookbook.html).

[Detailed Instructions]{style="font-size: 14pt; font-weight: 600;"}

[1. Download the files you
need]{style="font-size: 14pt; font-weight: 600;"}

Preferably as a bundle with everything in:

-   [KamaeliaMegaBundle-1.4.0](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=183774&release_id=451251)
    (5.7MB)

Or as individual files:

<div>

Core files you need:

</div>

-   [Axon](http://prdownloads.sourceforge.net/kamaelia/Axon-1.1.2.tar.gz?download) -
    Kernel of the system
-   [Kamaelia](http://prdownloads.sourceforge.net/kamaelia/Kamaelia-0.3.0.tar.gz?download) -
    the large collection of components.

<div>

Optional files:

</div>

-   Highly recommended:
    [pygame](http://www.pygame.org/ftp/pygame-1.7.1release.tar.gz)
    (1.3MB)
-   C libraries used by some components :
    [dirac](http://prdownloads.sourceforge.net/dirac/dirac-0.5.4.tar.gz?download),
    [libogg](http://downloads.xiph.org/releases/ogg/libogg-1.1.3.tar.gz),
    [libvorbis](http://downloads.xiph.org/releases/vorbis/libvorbis-1.1.2.tar.gz),
    [libao](http://downloads.xiph.org/releases/ao/libao-0.8.6.tar.gz)
-   Tool needed for building python bindings:
    [pyrex](http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/Pyrex-0.9.5.1a.tar.gz)
-   Python bindings for above C libraries:
    [pyao](http://www.andrewchatham.com/pyogg/download/pyao-0.82.tar.gz),
    [vorbissimple](http://prdownloads.sourceforge.net/kamaelia/vorbissimple-0.0.1.tar.gz?download),
    [dirac](http://prdownloads.sourceforge.net/kamaelia/Dirac-0.0.1.tar.gz?download),
    [DVB3](http://prdownloads.sourceforge.net/kamaelia/python-dvb3-0.0.4.tar.gz?download)

[Note: ]{style="font-weight: 600;"}If you just want to play and get
started, just get the two core files, install the core system and work
from there. A number of the examples, which you\'ll find in the cookbook
use the libraries above, but you should be able to get the gist of how
to do things without needing the optional files.

For convenience in the below I assume you\'ve downloaded all the above
files into the same directory, or downloaded a bundle and unpacked it.

[2. Install the Core]{style="font-size: 14pt; font-weight: 600;"}

[Install Axon]{style="font-weight: 600;"}

[Unpack\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

[Install Kamaelia]{style="font-weight: 600;"}

[Unpack\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

[2.1 Install Optional C
libraries]{style="font-size: 14pt; font-weight: 600;"}

You might notice a pattern with all of these \... :-) If you want dirac
support, you only need to install Dirac. If you want vorbis support, you
need to have libogg, libvorbis and libao installed. With a modern linux
distribution these are probably already included. If they\'re not,
they\'re simple to build - see below. You might want to skip to the next
section before deciding whether to install these. Personally though,
I\'d recommend installing them because these are what we\'re currently
developing with.

[Installing Dirac]{style="font-weight: 600;"}

[Unpack\....]{style="font-style: italic;"}

[Build\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

Homepage for Dirac: http://dirac.sourceforge.net/

[Installing libogg]{style="font-weight: 600;"}

[Unpack\....]{style="font-style: italic;"}

[Build\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

Homepage for Ogg: http://www.xiph.org/

[Installing libvorbis]{style="font-weight: 600;"}

[Unpack\...]{style="font-style: italic;"}

[Build\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

Homepage for Vorbis: http://www.xiph.org/

[Installing libao]{style="font-weight: 600;"}

[Unpack\....]{style="font-style: italic;"}

[Build\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

Homepage for libao: http://www.xiph.org/

[2.2 Installing Optional Python
Bindings]{style="font-size: 14pt; font-weight: 600;"}

Note that for some of these you will need to have installed the
appropriate C libraries described in 3.

[Installing pygame ]{style="font-weight: 600;"}(If you don\'t have
pygame already installed!)

[Unpack\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

Homepage for pygame: http://www.pygame.org/

[Installing pyao]{style="font-weight: 600;"}

If you want to use the vorbis examples, then you need something to
output the audio. PyAO wraps libao which is an audio output library.
This is generally included in most linux distributions, but PyAO
generally isn\'t. Installation:

[Unpack\....]{style="font-style: italic;"}

[Configure\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

Homepage for pyao: http://www.andrewchatham.com/pyogg/

[Installing Pyrex ]{style="font-weight: 600;"}(important)

Many of the other python bindings described here are built using a great
python tool called pyrex. As a result you need to install this if you
want to use the vorbis, dirac or DVB bindings. Installation:

[Unpack\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

Hompage: http://www.cosc.canterbury.ac.nz/\~greg/python/Pyrex/

[Installing Python support for VorbisSimple]{style="font-weight: 600;"}

This is a simple wrapper around libvorbis to make it easier to work
with. This also includes python bindings for this wrapper. As a result
you installed the simple wrapper first, then install the python
bindings. If you\'re interested, it also includes a document called
\"BytesToBeeps\" which describes how libvorbis and libogg are used by
this library. Installation:

[Unpack\....]{style="font-style: italic;"}

[Build & Install the C library
wrapper\....]{style="font-style: italic;"}

[Install the python bindings\....]{style="font-style: italic;"}

[Installing Python support for Dirac]{style="font-weight: 600;"}

[Unpack\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

[Installing Python support for DVB]{style="font-weight: 600;"} (Digital
TV, for timeshifting components)

[Unpack\....]{style="font-style: italic;"}

[Install\....]{style="font-style: italic;"}

These bindings have only been tested against a freecom DVB-T USB stick,
but should work with other DVB cards quite happily.

[3. Play with the examples!]{style="font-size: 14pt; font-weight: 600;"}

At this point, you\'ve got everything installed. Depending on whether
you installed various bindings, you will be able to play with different
examples. [These are all in the cookbook as well.](/Cookbook.html)

Have fun!

------------------------------------------------------------------------

Michael, March 2006, minor updates November 2006\

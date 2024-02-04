---
pagename: Download
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Downloads]{style="font-size: 20pt; font-weight: 600;"}

Kamaelia\'s main download site is the Kamaelia project page on
sourceforge:

-   <http://sourceforge.net/projects/kamaelia>

[You are highly recommended to look at the
]{style="font-weight: 600;"}[[download, setup and quickstart
page]{style="font-weight: 600;"}](/GettingStarted.html)[ for
instructions on getting started quickly!]{style="font-weight: 600;"}

Kamaelia is divided into two portions - Axon and Kamaelia. Axon forms
the core concurrency toolkit, like a kernal. Kamaelia is a collection a
components that use Axon to run (like user apps). You need BOTH in order
to run Kamaelia based systems.

-   Kamaelia\'s main release currently stands at 0.5.0, and requires
    Axon 1.5.1 for full functionality.
-   Axon\'s main release currently stands at 1.5.1
-   The preferred way for ensuring you have all the dependencies is to
    use the [Kamaelia Mega
    Bundle](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=183774&release_id=451251)

Installation of these packages is the usual dance:

-   [sudo python setup.py install]{style="font-family: Courier;"}

The following packages are up to date:

-   [Kamaelia-0.5.0](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=133714&release_id=451253)
-   [Axon-1.5.1](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=139298&release_id=451254)
-   [KamaeliaMegaBundle-1.4.0](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=183774&release_id=451251)
-   [python-dvb3-0.0.4](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=176999&release_id=387737)
-   [vorbissimple-0.0.2](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=145510&release_id=427115)
-   [python-dirac-0.0.1](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=163564&release_id=356353)

The following packages need updating:\

-   [debian-python-2.4-axon-1.1.1](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=158831&release_id=344740)
-   [debian-python-2.4-kamaelia-0.2.0](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=158832&release_id=344745)
-   [KamaeliaBundle-1.2.0](http://sourceforge.net/project/showfiles.php?group_id=122494&package_id=183773&release_id=427118)

[SVN]{style="font-weight: 600;"}

Developers are particularly welcome to play with the SVN tree.\

This always has more in than the releases! In the following
[\$root]{style="font-family: Courier;"} refers to the directory in which
you\'ve done a checkout of the main trunk. (kamaelia/trunk)

The development approach taken is this:

New ideas are developed in
[\$root/Sketches.]{style="font-family: Courier;"} Most new stuff is
developed under
[\$root/Sketches/]{style="font-family: Courier;"}[DI]{style="font-family: Courier; font-style: italic;"}
(Where DI stands for [D]{style="font-weight: 600;"}eveloper
[I]{style="font-weight: 600;"}nitials.)

After they have proven useful for some purpose, a position is chosen in
the main tree.

-   If the sketch extends Axon, the locatiion will be below
    [\$root/Code/Python/Axon/\....]{style="font-family: Courier;"}
-   If the sketch is a collection of Kamaelia components it will be
    below:
    [\$root/Code/Python/Kamaelia/Kamaelia\...]{style="font-family: Courier;"}
-   If the sketch simply glues together existing components, if it\'s
    unlikely to be extended further or is trivial is will go
    below:[\$root/Code/Python/Kamaelia/Examples\...]{style="font-family: Courier;"}
-   If the sketch is a useful application of some kind related to
    Kamaelia, it will go in
    [\$root/Code/Python/Kamaelia/Tools.]{style="font-family: Courier;"}

After using the resulting components in their new location, once we\'re
sure these components are useful and in a good place, they\'re added
into the RELEASE branch.

New releases of Axon are created by doing the following: (NB, the
scripts need updating due to change to SVN)

New releases of Kamaelia are created by doing the following: (NB, the
scripts need updating due to change to SVN)

Updated: Michael, November 2006 (Needs updating)

\

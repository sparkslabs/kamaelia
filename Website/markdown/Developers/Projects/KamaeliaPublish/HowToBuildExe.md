---
pagename: Developers/Projects/KamaeliaPublish/HowToBuildExe
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Developers/Projects/KamaeliaPublish/HowToBuildExe
=================================================

This page describes the process for changing the toolchain to use
different scripts.  There are two important files that you may need to
edit to alter this behavior:  zipheader.unix and
scripts/Publish.prepare.sh.  To build an executable, you will need at
minimum the following files from
private\_JMB\_DescartesComponentsAdded/Apps/Kamaelia-Publish:\

-   zipheader.unix
-   make-unix.sh
-   scripts/Publish.prepare.sh\

make-unix.sh
------------

There is not currently any part of make-unix.sh that needs to be
customized.\
\

zipheader.unix
--------------

This file won\'t need to be changed if you have a module main with a
main function in it (which is to be the main entry point to your
application). Otherwise, these lines will need to be changed:
[]{#line-52 .anchor}[]{#line-53 .anchor}

[]{#line-54 .anchor}[]{#line-55 .anchor}[]{#line-56 .anchor}[]{#line-57
.anchor}

    import main

    main.main()

[]{#line-58 .anchor}This is plain old python code, so you can put
whatever you want here. My advice would be to have it import and run
your main module.\
\

scripts/publish.prepare.sh
--------------------------

This file is only responsible for moving all the files into the assembly
directory.  Thus, all you really have to do is move all the files that
you want built into the executable into the assembly directory.\

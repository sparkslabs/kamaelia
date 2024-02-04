---
pagename: Developers/PlatformSpecificHints
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Developers/Platform Specific Hints
==================================

### Mac OS X

Mac OS X ships with a case insensitive filesystem on the hard disk.
Clashing filenames, eg. passThrough.py and PassThrough.py in the
repository will cause subversion client to fail when trying to check out
a working copy.\
\

C/pyrex code: malloc.h is in a different location: malloc/malloc.h For
cross platform compatibility, use \#include \<stdlib.h\> instead.

\
Here is an [Apple technical
note](http://developer.apple.com/technotes/tn2002/tn2071.html%20) on
porting unix (command line) apps to OS X.\
\

### Windows (win32)

The filesystem is case insensitive. Clashing filenames, eg.
passThrough.py and PassThrough.py in the repository will cause
subversion client to fail when trying to check out a working copy.

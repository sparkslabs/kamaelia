---
pagename: Developers/Projects/KamaeliaPublish
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia: Publish {#head-c56d7c932f5d44641046aae5892bb3342b553c19}
-----------------

What is it? {#head-cb43cfbe3084966a3a3d76039ca664b41579c854}
-----------

Kamaelia Publish as of right now aims to be a system that will let users
publish themselves on their own terms. The goal is to allow a person to
host their own web services without being beholden to anyone else for
web space.

**Who wrote it?**

It\'s developed by Jason Baker. It builds on HTTP work by Michael Sparks
& Ryan Lothian

**Who\'s interested in it?**

Michael Sparks, \... you?\

Where do I get it & install it? {#head-4ae61e667b2c73bd4538b78f2443acaacfb3a7e7}
-------------------------------

**developers**

-   svn co
    <https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/branches/private_JMB_Wsgi>

-   [Build the executable](./KamaeliaPublish/BuildForUnix)

**Mac/Linux**

1.  Download <http://www.coderspalace.com/downloads/kpublish.zip>

2.  Unzip the file.

3.  Run the executable.

4.  Go to <http://127.0.0.1:8082/simple> to try it out.

Planned Schedule: {#head-ab982e78aa80eb65225e149907cae69c7abf9889}
-----------------

-   June 6 - Build local tool chain for packaging up the webserver as it
    stands at that instant using py2app, py2exe, distutils.
-   June 20 - Fix POST support with the server. Simplify URL routing and
    possibly include Paste, werkzeug, etc for more advanced URL routing.
    Make a WSGI application or use a pre-made one for serving static
    content and remove reliance on Minimal.
-   July 4 - Convert the server to be an XMPP client instead of using
    HTTP.
-   July 18 - Make an XMPP gateway to convert HTTP requests to XMPP that
    the WSGI server can understand.
-   Aug 1 - Work on package manager to easily install WSGI software.
    This is intended to be an easy to use graphical interface for
    installing and configuring WSGI software.
-   Aug 18 - I\'ll leave the last two weeks as a giant Miscellaneous.
    Tie up any loose ends with any of the apps I\'ve written. Implement
    some of the would be nices that didn\'t make it into the final
    schedule. Examples include:
    -   Create a FOAF database of some kind so that Google\'s
        [SocialGraph](http://wsgi.coderspalace.com/kcwiki/SocialGraph){.nonexistent}
        API can be used to build friends lists.

    -   Make the server more user friendly and create some good
        administration tools for idiots either using a native
        application or some kind of web app (the latter is preferable).

    -   Make a basic plugin system based on mako templating. It\'s kind
        of hard to put this one into words, but the basic idea is to
        have a system that end users can design their own webpages with
        pre-made widgets that can be inserted as mako expression
        substitution.

Progress (dates related to the weekly meeting - these are the \"DONE\" lines) {#head-38c970225e454db55841fa5cd8c542a5e0948c10}
-----------------------------------------------------------------------------

-   Fixed some more stuff with the Minimal request handler, got
    [MoinMoin](http://wsgi.coderspalace.com/kcwiki/MoinMoin) working

See Also {#head-105aec3df2ff0e4fd9e666bbf89cba1902e148a1}
--------

[How to use my toolchain for other
projects](./KamaeliaPublish/HowToBuildEXE)\
**\
Project sub pages:** (by last change)\

-   [kpgate\_ini](/Developers/Projects/KamaeliaPublish/kpgate_ini)      (*Sat
    Sep 20 22:31:56 2008*)
-   [kp\_ini](/Developers/Projects/KamaeliaPublish/kp_ini)      (*Sat
    Sep 20 22:31:56 2008*)
-   [index](/Developers/Projects/KamaeliaPublish/index)      (*Sat Sep
    20 22:31:56 2008*)
-   [UrlsFile](/Developers/Projects/KamaeliaPublish/UrlsFile)      (*Sat
    Sep 20 22:31:56 2008*)
-   [Review](/Developers/Projects/KamaeliaPublish/Review)      (*Sat Sep
    20 22:31:56 2008*)
-   [RequestReference](/Developers/Projects/KamaeliaPublish/RequestReference)      (*Sat
    Sep 20 22:31:56 2008*)
-   [Pylons](/Developers/Projects/KamaeliaPublish/Pylons)      (*Sat Sep
    20 22:31:56 2008*)
-   [OpenIssues](/Developers/Projects/KamaeliaPublish/OpenIssues)      (*Sat
    Sep 20 22:31:56 2008*)
-   [MoinMoin](/Developers/Projects/KamaeliaPublish/MoinMoin)      (*Sat
    Sep 20 22:31:56 2008*)
-   [HowToBuildExe](/Developers/Projects/KamaeliaPublish/HowToBuildExe)      (*Sat
    Sep 20 22:31:56 2008*)
-   [Files](/Developers/Projects/KamaeliaPublish/Files)      (*Sat Sep
    20 22:31:56 2008*)
-   [Django](/Developers/Projects/KamaeliaPublish/Django)      (*Sat Sep
    20 22:31:56 2008*)
-   [CrossTalk](/Developers/Projects/KamaeliaPublish/CrossTalk)      (*Sat
    Sep 20 22:31:56 2008*)
-   [BuildForUnix](/Developers/Projects/KamaeliaPublish/BuildForUnix)      (*Sat
    Sep 20 22:31:56 2008*)

\

Log/Discussion {#head-105aec3df2ff0e4fd9e666bbf89cba1902e148a1}
--------------

Just tested the \"executable\" under linux with python 2.5. Works
perfectly fine. Really impressive - worked straight out the box.\
\
Also just tested under Mac OS 10.. That comes with python2.3 which
doesn\'t include wsgiref, which means I get the following failure:\
\
Traceback (most recent call last):\
File \" stdin \", line 9, in ?\
File \"./kpublish/main.py\", line 5, in ?\
File \"./kpublish/Kamaelia/Experimental/Wsgi/WsgiHandler.py\", line 9,
in ?\
ImportError: No module named wsgiref.validate\
\
Which isn\'t the least bit surprising - that machine doesn\'t have
wsgiref installed. It may be worth considering re-packaging this to
include a copy of wsgiref.\
\
Still despite that, impressive :-)\
\

-   FIXED:  wsgiref should be included in the bundle now.\

\
\-- Michael, 7 June 2008\
\

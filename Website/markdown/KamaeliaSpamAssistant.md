---
pagename: KamaeliaSpamAssistant
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia Spam Assistant
=======================

::: {.boxright}
If you run your own SMTP server, you can stop a lot of spam before it
hits your mailbox by using [KamaeliaGrey](/KamaeliaGrey.html)
:::

This tool is a work in progress and has already assisted in the deletion
of several thousand spams repaying it\'s development cost immediately.\
It\'s purposes is to delete spam on a POP3 server before downloading the
spam. It does this by examining headers. It is currently a first pass
designed to assist clearing my current inbox which has reach silly
proportions.\
The code is nowhere near perfect Kamaelia code and does things Kamaelia
systems shouldn\'t really, but that\'s not the point - these things can
(and will) be tidied up. The site hosting the phrases.txt file also
needs to provide a mechanism of allowing for shared (trusted) updates of
the phrases.txt file.\

**Getting it**
--------------

It is not yet packaged up - you\'ll need to use SVN to grab it.\
<https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/MPS/POP3/spam_deletion_assistant.py>\
svn co
https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/MPS/POP3\
To install and use it you\'ll need a copy of Kamaelia & Axon. The
easiest way is to grab a copy of [Kamaelia Grey](/KamaeliaGrey.html) (link on
that page :-) )\

**Running it **
---------------

Usage: spam\_deletion\_assistant.py username password pop3\_server port\
\[port is usually 110\]\

**Improving it **
-----------------

29th May 2008 - First version written, used for deletion of \~3000 spams
and checked into SVN\
30th May 2008 - This page created.\
\
\
Michael, 30 May 2008\
\
\

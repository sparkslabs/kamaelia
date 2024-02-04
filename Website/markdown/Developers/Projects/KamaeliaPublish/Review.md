---
pagename: Developers/Projects/KamaeliaPublish/Review
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Code to review
==============

This is going here for Dave\'s purposes because I think a little bit of
formatting will make this easier to read.  :)  If you want to just get a
list of the files ready to merge, check here: 
[http://www.kamaelia.org/Developers/Projects/KamaeliaPublish/Files](../../../Developers/Projects/KamaeliaPublish/Files)\
\
If you\'re ready to start reviewing some of my code, here is a list of
what you can start on (I tried to group everything by the functionality
it provides).  I\'ll start with the standard branch data:\
\

Branch Details
--------------

branch:  private\_JMB\_Wsgi\
branch point:  r4433\
to review (although it would probably not be feasible to go through the
diff for the entire branch):\
    cd branches/private\_JMB\_Wsgi\
    svn diff -r4433:HEAD .\
\

### What does it do?

This branch aims to add several improvements to Kamaelia\'s HTTP
handling including WSGI support.  It is also the branch that contains
Kamaelia Publish and Kamaelia WebServe.\
\
**Kamaelia WebServe** - This is a Kamaelia web server for running WSGI
applications and static content (support for more Kamaelia handlers is
currently in TODO status).\
**Kamaelia Publish** - Kamaelia Publish aims to break a couple of the
biggest barriers for starting your own webpage.  Typically, you have to
have a domain name, a static ip, etc.  Kamaelia Publish aims to improve
web page serving by removing these requirements.  For more information
on Kamaelia Publish, see this topic on the mailing list: 
<http://groups.google.com/group/kamaelia/browse_thread/thread/c17ebe5a31a94caf>
(The status of my project as of now)\

Examples:
---------

I\'m starting with examples, because this is probably the best place to
start familiarizing yourself with Kamaelia\'s HTTP code and to get an
idea of how my code changes the use of the HTTP functionality.\
\

### Files:

Kamaelia/Examples/TCP\_Systems/HTTP/cookbook\_1.py

Kamaelia/Examples/TCP\_Systems/HTTP/cookbook\_2.py\

(These are how the cookbook examples would look if my code were merged. 
To see how they look now, go here: 
[http://www.kamaelia.org/Cookbook/HTTPServer](../../../Cookbook/HTTPServer))\

\
Kamaelia/Examples/TCP\_Systems/HTTP/WSGI/simple\_wsgi\_example.py\
Kamaelia/Examples/TCP\_Systems/HTTP/WSGI/wsgi\_example.py\
(These examples show how to use my WSGI handler with the HTTP Server and
ServerCore)\
\

### Review:

Looked through both HTTP examples, all the code is fine. Documentation
is a bit light to say they\'re supposed to be cookbook examples. However
I especially appreciate the way you handle routing, very nice solution.
The echoHandler and usage of Pipelines is good to see too :-)\

-   I agree that the documentation was a little light on the second
    example, so I went back and added some more comments.  Let me know
    if that helps. -Jason\

\
Kamaelia/Examples/TCP\_Systems/HTTP/WSGI/simple\_wsgi\_example.py\
Does what it says on the tin.\
\
Kamaelia/Examples/TCP\_Systems/HTTP/WSGI/wsgi\_example.py\
Unclear what exactly this is supposed to do, I get 404 errors on
anything but /simple which yields \"Page found, but app object
missing.\" I that\'s correct, but not sure. I wonder if the 404 is
appropriate if the page exists but the app doesn\'t?? Perhaps a more
relevant error here.\

-   The error\'s been fixed.  It was a result of me changing the URL
    routing to test some of the error messages and then forgetting to
    change it back.  The functionality this uses may end up going into
    Kamaelia.Apps, but I\'ll let you give the WSGI code a look before I
    change it.  -Jason\

\

HTTP Support code:
------------------

Most of this stuff is miscellaneous utility functions that make using
the HTTP Server a little less repetitive.  Probably the most important
change is the requestHandlers function and the HTTPProtocol function,
which is what allowed me to cut the HTTPServer cookbook example almost
in half.  There\'s only one file to look at here:\
\

### Files:

Kamaelia/Kamaelia/Support/Protocol/HTTP.py\
\

### Review:

I see what you mean by \"miscellaneous utility functions\", I don\'t see
anything inherently wrong with the code. I mean, if it does what you
want for your purposes then it\'s fair enough. Will come back to this
later maybe when I see the usage.\

WSGI code:
----------

Essentially, WSGI was a standard that was invented to allow Python web
programs to run in a variety of webservers and to allow multiple
frameworks to co-exist on the same server.  One of the things that my
code does is allow Kamaelia\'s HTTP Server to run WSGI code by making a
WSGI handler.  If you need some extra links for learning about WSGI,
these may be helpful (otherwise, skip on to the code):\
\
<http://ivory.idyll.org/articles/wsgi-intro/what-is-wsgi.html>\
<http://www.wsgi.org/wsgi/>\
\
(this is more of reference value than it is of learning value, but it\'s
a pretty important link to know if you plan on doing anything
non-trivial with WSGI)\
<http://www.python.org/dev/peps/pep-0333/>\
\

### Dependencies:

You will need wsgiref to run these files (which is included in Python
2.5).\

### Files:

Kamaelia/Kamaelia/Protocol/HTTP/Handlers/WSGI/\_\_init\_\_.py\
Kamaelia/Kamaelia/Protocol/HTTP/Handlers/WSGI/\_factory.py\
Kamaelia/Kamaelia/Protocol/HTTP/Handlers/WSGI/\_WSGIHandler.py\
(Note that I doubt this will be a directory layout that Michael will
want to merge due to code being in \_\_init\_\_.py and there being
private source files, so any feedback on a better directory structure is
welcome)\
\

### Review:

WSGIHandler code is rather confusing for me (especially since i\'m not
familiar with the PEP), but I\'ve gone through it. Error handling seems
extensive however your exceptions just pass and don\'t even seem to log
the exception thrown? I\'m not 100% on python\'s exceptions but it seems
odd to me.\

-   As discussed in IRC, the errors are logged, it just wasn\'t very
    clear where that was.  I\'ll comment the code a little better.
    -Jason\

WSGI Apps:
----------

These are a few WSGI applications that are included for a variety of
reasons (some make working with a framework easier, Simple is a basic
\"demonstration\" app, there is also a file just for test WSGI
applications, etc).  Admittedly, testing some of these out can be
cumbersome, so some of these may not make it into the trunk until
they\'ve been tested more thoroughly.\
\
I have my doubts about some of these being merged into trunk at this
point simply for maintainability reasons, so the primary ones to look at
will be ErrorHandler.py and Simple.py..  PasteApp is an application that
will simplify working with Paste Deploy, a sort of \"framework\'s
framework.\"  It aims to simplify things like URL routing and deploying
WSGI apps.  Thus, I think that making it easy to use should be a
priority.  For more info on Paste Deploy, see here: 
<http://pythonpaste.org/deploy/>.

### Dependencies:

These vary from file to file and will be noted in the file.\
\

### Files:

Kamaelia/Kamaelia/Apps/WSGI/CpyApp.py\
Kamaelia/Kamaelia/Apps/WSGI/ErrorHandler.py\
Kamaelia/Kamaelia/Apps/WSGI/Moin.py\
Kamaelia/Kamaelia/Apps/WSGI/PasteApp.py\
Kamaelia/Kamaelia/Apps/WSGI/Simple.py\
Kamaelia/Kamaelia/Apps/WSGI/Static.py\
Kamaelia/Kamaelia/Apps/WSGI/Test.py\
\

### Review:

Once I\'ve got the Kamaelia WebServe running how do I get these to work,
Simple seems to be on by default. Is that intended? (sorry for asking
annoying questions)\

-   Yes, simple is supposed to be on by default.  The error handler is
    also configured by default (it\'s what gives you a 404 page if you
    pull up the wrong webpage).  I think that I\'ll have to hold off on
    the others for now.  I think that the Kamaelia repository won\'t be
    the best place for this.  At some point, I would like to add a
    \"Package manager\" that will set everything up for you
    automatically. -Jason\

Kamaelia WebServe:
------------------

This is a Kamaelia web server for running WSGI applications and static
content (support for more Kamaelia handlers is currently in TODO
status).  Building and running WebServe is (intended to be) simple and
easy.  When you first run the server, it will install the necessary
files to run to your home directory (the ability to customize this is in
TODO status).  You may also want to read about customizing a [URLs
file](../../../Developers/Projects/KamaeliaPublish/UrlsFile) and a
[kp.ini file](../../../Developers/Projects/KamaeliaPublish/kp_ini)
(which will be generated for you).  By default, if you go to
http://127.0.0.1:8080/simple, it will bring up the demonstration
application.  All you have to do to start the server is the following:\
\
    cd branches/private\_JMB\_Wsgi/Apps/Kamaelia-WebServe\
    ./make-unix.sh \#this builds the executable, so is only necessary
the first time and any time you change the source\
    dist/kwserve\
\

### Files:

Apps/make-unix.sh\
Apps/prepare.sh\
Apps/zip-header.unix\
Apps/data/kp.ini\
Apps/data/kpuser/urls.ini\
Apps/data/kpuser/kp.log\
Apps/data/kpuser/www/index.html\
Apps/scripts/main.py\
Kamaelia/Kamaelia/Apps/Web\_common/auto\_install.py\
Kamaelia/Kamaelia/Apps/Web\_common/ConfigFile.py\
Kamaelia/Kamaelia/Apps/Web\_common/Console.py\
Kamaelia/Kamaelia/Apps/Web\_common/ServerSetup.py\
Kamaelia/Kamaelia/Apps/Web\_common/Structs.py\
Kamaelia/Kamaelia/Apps/Web\_common/UrlConfig.py\
\

### Review:

Does this install Kamaelia Publish too? What are the differences\...I
seem to have a kpuser folder in \~ after installing this? (I might have
installed Publish at an earlier date)\

-   This leads me to believe that \"install\" might have been a poor
    choice of naming in creating the kpuser file.  Perhaps \"configure\"
    is a better word.  To answer your question more directly though, the
    data that\'s in kpuser can be used by both Kamaelia WebServe and the
    Kamaelia Publish Peer.  You just have to add your XMPP information
    for Kamaelia Publish to work. -Jason\

Kamaelia Publish:
=================

To begin with, you\'ll need two XMPP accounts to test this.  If you have
a GMail account, then you already have one XMPP account.  You can also
register for accounts with other servers (like jabber.org) via most XMPP
chat clients like Pidgen or Gajim.  Kamaelia Publish consists of two
parts:  a gateway and a peer.  The gateway is what takes the HTTP
request and sends it to the peer, which generates the webpage to be sent
to the person requesting the webpage.\
\
Running both of these is pretty similar to running Kamaelia WebServe. 
To build and run them, you do the following:\
\
**Gateway:**\
cd branches/private\_JMB\_Wsgi/Apps/Kamaelia-Publish/Gateway\
./make-unix.sh\
dist/kpublish\
\
**Peer:**\
cd branches/private\_JMB\_Wsgi/Apps/Kamaelia-Publish/Peer\
./make-unix.sh\
dist/kpublish\
\
You\'ll also need
a [kp.ini](../../../cgi-bin/Wiki/edit/Developers/Projects/KamaeliaPublish/kp_ini)
and
[kpgate.ini](../../../cgi-bin/Wiki/edit/Developers/Projects/KamaeliaPublish/kpgate_ini)\
\

### Dependencies

You will need the following:\
\
simplejson - you can install this just by using \"easy\_install
simplejson\"\
headstock and bridge - you\'ll need to check out and install from the
latest version in the repository.  Check out
[defuze.org](www.defuze.org) (which is down at the time of this post)
for instructions on installing these.\
sqlalchemy - You must download and install version 4.7p1 from
[www.sqlalchemy.org](www.sqlalchemy.org).  The version in the cheeseshop
is a beta, and the version in Synaptic is oudated.\

### Files:

Apps/Kamaelia-Publish/Gateway/make-unix.sh\
Apps/Kamaelia-Publish/Gateway/prepare.sh\
Apps/Kamaelia-Publish/Gateway/zipheader.unix\
Apps/Kamaelia-Publish/Gateway/scripts/\_\_init\_\_.py\
Apps/Kamaelia-Publish/Gateway/scripts/BoxManager.py\
Apps/Kamaelia-Publish/Gateway/scripts/http.py\
Apps/Kamaelia-Publish/Gateway/scripts/interface.py\
Apps/Kamaelia-Publish/Gateway/scripts/jabber.py\
Apps/Kamaelia-Publish/Gateway/scripts/main.py\
Apps/Kamaelia-Publish/Gateway/util/kpgate.db\
Apps/Kamaelia-Publish/Peer/make-unix.sh\
Apps/Kamaelia-Publish/Peer/prepare.sh\
Apps/Kamaelia-Publish/Peer/zipheader.unix\
Apps/Kamaelia-Publish/Peer/scripts/\_\_init\_\_.py\
Apps/Kamaelia-Publish/Peer/scripts/main.py\
Apps/Kamaelia-Publish/Peer/scripts/transactions.py\
Kamaelia/Apps/Publish/\_\_init\_\_.py\
Kamaelia/Apps/Publish/Gateway/\_\_init\_\_.py\
Kamaelia/Apps/Publish/Gateway/consts.py\
Kamaelia/Apps/Publish/Gateway/JIDLookup.py\
Kamaelia/Apps/Publish/Gateway/translator.py\
Kamaelia/Apps/Publish/Gateway/UserDatabase.py\
Kamaelia/Apps/Publish/Peer/\_\_init\_\_.py\
Kamaelia/Apps/Publish/Peer/translator.py\
Everything in Kamaelia/Apps/Web\_common that was mentioned in Kamaelia
WebServe\
Kamaelia/Kamaelia/IPC.py\
Axon/Axon/Ipc.py\

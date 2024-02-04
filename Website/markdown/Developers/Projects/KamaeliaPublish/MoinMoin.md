---
pagename: Developers/Projects/KamaeliaPublish/MoinMoin
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
How do I use MoinMoin with Kamaelia Publish?
--------------------------------------------

Installation of MoinMoin can be a complex subject and is in a large
degree outside the scope of this wiki.  This page exists to document
some of the Kamaelia Publish specific items of installing MoinMoin.  For
more information about installing MoinMoin, please visit their
HelpOnInstalling page:  <http://www.moinmo.in/HelpOnInstalling>\
\
To begin with, you must have a moin WSGI script.  MoinMoin includes a
file called moin.wsgi in its server directory.  This must be in a
location where it may be imported in python.  That means that it may be
built into your executable file (usually under plugins/WsgiApps) or
located elsewhere on your python path.\
\
Please note that you **may not** build the main MoinMoin files into your
executable.  It is possible to do so in theory, but isn\'t a good idea
in practice because it also includes some static files that must be
accessed at run time.\
\
You must also place Moin\'s static files somewhere where the static file
handler can get at them.  I usually copy Moin\'s included htdocs into my
static directory as moin-htdocs.\
\
\

### Please note that MoinMoin 1.6.3 is the only version of Moin that has been tested with Kamaelia Publish. 

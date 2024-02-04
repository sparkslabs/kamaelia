---
pagename: Developers/Projects/KamaeliaPublish/kp_ini
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia Publish and WebServe config file
=========================================

Both the Kamaelia Publish Peer and Kamaelia WebServe use the same format
for a config file.  The files were designed so that you may use one
config file for both applications (albeit possibly with minor
modifications).  This is a breakdown of what goes in each individual
section and what the keys mean.  Note that case isn\'t important in
setting the keys up (so ignore any inconsistencies you see in case here
and in the file in the repository).\
\
\

SERVER
------

This section holds most of the data required to configure the server in
general.\
\

-   **Port** - This is the port that Kamaelia WebServe will listen on
    for HTTP requests.  Note that using port 80 (typically used for
    HTTP) will require elevated privileges on most \*NIX systems.  **It
    is not recommended that you use port 80 currently as this is a
    potential security problem since Kamaelia WebServe does not
    de-escalate privileges.**
-   **pypath\_append** - This is a list of entries to add to the python
    path, separated by colons (:).  Entries added here will be added to
    the end of the python path.  This is useful if you would like to put
    WSGI applications somewhere where the system can get to them.
-   **pypath\_prepend** - This is a list of entries to be added to the
    front of the python path, separated by colons.  You probably don\'t
    need to use this except for testing and debugging purposes.
-   **log** - This is the location where the log will go.  Note that you
    may get errors if this file does not already exist.

STATIC
------

This section holds the data necessary to configure server to handle
static content (javascript, images, HTML, etc).  **NOTE:  This is likely
to either be changed or moved elsewhere (likely the urls file) to
simplify URL routing.**\
\

-   **url** - The url prefix that will handle static content (set to
    \'/static\' by default).
-   **indexfilename** - If no filename is specified in the URI, this is
    what to assume (set to \'index.html\' by default).
-   **homedirectory** - The directory to look in for static content in. 
    The \"root\" of the static handler\'s \"file system.\"

WSGI
----

This section holds the configuration data for the WSGI handler.  Most of
the keys are self explanitory, but are explained here for
completeness\'s sake.\
\

-   **SERVER\_SOFTWARE** - Currently set to \'Kamaelia WSGI Server v
    0.0.1\'
-   **SERVER\_ADMIN** - The person who runs the server.
-   **WSGI\_VER** - You want to leave this at 1.0 unless you have a
    really, really good reason for changing it.
-   **URL\_LIST** - The URLs file to use to route URLs.  For more info
    on URLs files, see
    [http://www.kamaelia.org/Developers/Projects/KamaeliaPublish/UrlsFile](../../../Developers/Projects/KamaeliaPublish/UrlsFile)

XMPP
----

This section is relevant only in the Kamaelia Publish Peer.  For this
section, we\'ll assume that we\'re using the JID
kamaelia\_user\@jabber.org.\

-   **username** - This is your username (the part of your JID before
    the @ symbol).  For kamaelia\_user\@jabber.org, you would put
    kamaelia\_user.
-   **domain** - This is the domain of your JID (the part after the @,
    but before the / if there is one).  For the above example, this
    would be jabber.org.
-   **server** - This depends on which server you\'re using.  For the
    above example, it will be jabber.org:5222.\
-   **resource** - This key is optional.  It represents the resource in
    your jid (the part after the /).  This is typically used to indicate
    the instant messenging program you\'re using and is useful if you
    want to be logged into the same jabber account on two different
    computers or programs.
-   **password** - You should know this one already.  :) 
-   **usetls** - This will also be dependent on the server.  This is a
    boolean value, so it doesn\'t matter what you set it to.  If it\'s
    present and the value is anything but a blank key, it will evaluate
    to True.\

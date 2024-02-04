---
pagename: Developers/Projects/KamaeliaPublish/kpgate_ini
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia Publish Gateway config file
====================================

The config file format is very similar to the one used by [Kamaelia
WebServe and the Kamaelia Publish
peer](../../../cgi-bin/Wiki/edit/Developers/Projects/KamaeliaPublish/kp_ini).

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
-   **db** - This is URI of the database to connect to.  See [this
    page](http://www.sqlalchemy.org/docs/05/dbengine.html#dbengine_establishing)
    for more info.  Note that there is a sample database file in
    private\_JMB\_Wsgi/Apps/Kamaelia-Publish/Gateway/util named
    kpgate.db.  You will probably have to edit in the JID that you\'re
    wanting to use in the Peer in manually (Ubuntu has sqlitebrowser in
    its package management system that can be used to do this).[\
    ](http://www.sqlalchemy.org/docs/05/dbengine.html#dbengine_establishing)

\

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
completeness\'s sake.  **NOTE: This section currently doesn\'t do
anything.  But it may do something when a website where people can
register is set up.**\
\

-   **SERVER\_SOFTWARE** - Currently set to \'Kamaelia WSGI Server v0.0.1\'
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

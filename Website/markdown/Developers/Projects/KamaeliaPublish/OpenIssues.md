---
pagename: Developers/Projects/KamaeliaPublish/OpenIssues
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia Publish Open Issues
----------------------------

This page is intended to be a big \"todo\" list for Kamaelia Publish. 
It may or may not a lot of items that I would like to get done but may
not have time for.  So this page shouldn\'t be construed as being a part
of my GSoC work (but some of it will be).\
\

### Bugs

The software still needs much more testing, so this really only
represents a list of known bugs:\
\

-   When the gateway logs in, sometimes it receives messages indicating
    which users are online, sometimes it doesn\'t.  The gateway should
    check a user\'s online status with the server before assuming they
    are offline.\

### Enhancements

~~Make static content able to be served.~~

-   Static content is now served by the gateway.  The peer is capable of
    serving such files, but such would be REALLY slow and somewhat more
    complicated.\

Add the capability to look up registered and possibly logged in users in
a database.

-   Partially completed:  Registered users and whether they are logged
    in or not can be stored in a SQLite database.
-   sub-issue:  Get the gateway able to use more different kinds of
    databases like MySQL, PostgreSQL, etc.
-   sub-issue:  Having to look up whether or not a user is online EVERY
    time will probably affect performance.  Some kind of caching system
    should be in place.\

Add the capability to send data between the Gateway and serving peer
directly.  This can be done by either doing an XMPP file transfer or
possibly bypassing XMPP altogether.

Look into getting the Peer to work on Python 2.2.  Being able to run a
webserver on Symbian would be Pretty Damn Cool (tm).

-   This is definitely a \"would be nifty\" idea.  I have no idea if
    this is even feasible or how much work would be involved in this.\

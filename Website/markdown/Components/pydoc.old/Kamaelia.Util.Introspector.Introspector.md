---
pagename: Components/pydoc.old/Kamaelia.Util.Introspector.Introspector
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Introspector.Introspector
=======================================

class Introspector(Axon.Component.component)
--------------------------------------------

Introspector() -\> new Introspector component.

Outputs topology (change) data describing what components there are, and
how they are wired inside the running Axon system.

#### Inboxes

-   control : Shutdown signalling
-   inbox : NOT USED

#### Outboxes

-   outbox : Topology (change) data describing the Axon system
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### introspect(self)

introspect() -\> components, postboxes, linkages

Returns the current set of components, postboxes and interpostbox
linkages.

-   components \-- a dictionary, containing components as keys
-   postboxes \-- a list of (component.id, type, \"boxname\") tuples,
    where type=\"i\" (inbox) or \"o\" (outbox)
-   linkages \-- a dictionary containing (postbox,postbox) tuples as
    keys, where postbox is a tuple from the postboxes list

### main(self)

Main loop.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

---
pagename: Components/pydoc.old/Kamaelia.Util.Graphline.Graphline
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Graphline.Graphline
=================================

class Graphline(Axon.Component.component)
-----------------------------------------

Graphline(linkages,\*\*components) -\> new Graphline component

Encapsulates the specified set of components and wires them up with the
specified linkages.

Keyword arguments: - linkages \-- dictionary mapping
(\"componentname\",\"boxname\") to (\"componentname\",\"boxname\") -
components \-- dictionary mapping names to component instances (default
is nothing)

#### Inboxes

-   control :
-   inbox :

#### Outboxes

-   outbox :
-   signal :

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, linkages)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### addExternalPostboxes(self)

Adds to self.Inboxes and self.Outboxes any postboxes mentioned in
self.layout that don\'t yet exist

### childrenDone(self)

Unplugs any children that have terminated, and returns true if there are no
:   running child components left (ie. their microproceses have
    finished)

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

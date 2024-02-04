---
pagename: Components/pydoc.old/Kamaelia.Util.Fanout.fanout
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Fanout.fanout
===========================

class fanout(Axon.Component.component)
--------------------------------------

fanout(boxnames) -\> new fanout component.

A component that copies anything received on its \"inbox\" inbox to the
named list of outboxes.

Keyword arguments: - boxnames \-- list of names for the outboxes any
input will be fanned out to.

#### Inboxes

-   control : Shutdown signalling
-   inbox : Data to be fanned out

#### Outboxes

-   outbox : NOT USED
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, boxnames)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

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

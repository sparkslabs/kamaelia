---
pagename: Components/pydoc.old/Kamaelia.Util.ToStringComponent.ToStringComponent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.ToStringComponent.ToStringComponent
=================================================

class ToStringComponent(Axon.Component.component)
-------------------------------------------------

ToStringComponent() -\> new ToStringComponent.

A component that converts data items received on its \"inbox\" inbox to
strings and sends them on out of its \"outbox\" outbox.

#### Inboxes

-   control : NOT USED
-   inbox : Data items to convert to string

#### Outboxes

-   outbox : Data items converted to strings
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### mainBody(self)

Main loop body.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

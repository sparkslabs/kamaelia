---
pagename: Components/pydoc.old/Kamaelia.Util.Marshalling.DeMarshaller
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Marshalling.DeMarshaller
======================================

class DeMarshaller(Axon.Component.component)
--------------------------------------------

DeMarshaller(klass) -\> new DeMarshaller component.

A component for demarshalling data (deserialising it from a string).

Keyword arguments: - klass \-- a class with static method:
demarshall(data) that returns the data, demarshalled.

#### Inboxes

-   control : Shutdown signalling
-   inbox : data to be demarshalled

#### Outboxes

-   outbox : demarshalled data
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, klass)

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

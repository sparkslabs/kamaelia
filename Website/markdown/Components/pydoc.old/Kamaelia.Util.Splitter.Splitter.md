---
pagename: Components/pydoc.old/Kamaelia.Util.Splitter.Splitter
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Splitter.Splitter
===============================

class Splitter(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent)
------------------------------------------------------------------

Splitter() -\> new Splitter component.

Splits incoming data out to multiple destinations. Send addsink(\...)
and removesink(\...) messages to the \'configuration\' inbox to add and
remove destinations.

#### Inboxes

-   control : NOT USED
-   configuration : addsink(\...) and removesink(\...) request messages
-   inbox : Source of data items

#### Outboxes

-   outbox : NOT USED
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### createsink(self, sink, sinkbox, passthrough)

Set up a new destination for data.

Creates an outbox, links it to the target (component,inbox) and records
it in self.outlist.

### deletesink(self, oldsink)

Removes the specified (component, inbox) as a destination for data where
(component, inbox) = (oldsink.sink, oldsink.sinkbox).

Unlinks the target, destroys the corresponding outbox, and removes the
corresponding record from self.outlist.

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

---
pagename: Components/pydoc.old/Kamaelia.Util.Splitter.PlugSplitter
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Splitter.PlugSplitter
===================================

class PlugSplitter(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent)
----------------------------------------------------------------------

PlugSplitter(\[sourceComponent\]) -\> new PlugSplitter component.

Splits incoming data out to multiple destinations. Send addsink(\...)
and removesink(\...) messages to the \'configuration\' inbox to add and
remove destinations.

Keyword arguments: - sourceComponent \-- None, or component to act as
data source

#### Inboxes

-   control : Shutdown signalling, and signalling to be fanned out.
-   \_control : Internal inbox for receiving from the child source
    component (if it exists)
-   configuration : addsink(\...) and removesink(\...) request messages
-   inbox : Data items to be fanned out.
-   \_inbox : Internal inbox for receiving from the child source
    component (if it exists)

#### Outboxes

-   outbox : Data items received on \'inbox\' inbox.
-   signal : Shutdown signalling, and data items received on \'control\'
    inbox.

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, sourceComponent)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### \_addSink(self, sink, sinkinbox, sinkcontrol)

Add a new destination for data.

Specify target component (sink), and target inbox (sinkinbox) and/or
target shutdown signalling inbox (sinkcontrol).

### \_delSink(self, sink, sinkinbox, sinkcontrol)

Remove a destination for data.

Specify target component (sink), and target inbox (sinkinbox) and/or
target shutdown signalling inbox (sinkcontrol).

### childrenDone(self)

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)

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

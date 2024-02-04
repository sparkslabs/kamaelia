---
pagename: Components/pydoc.old/Kamaelia.Util.Splitter.Plug
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Splitter.Plug
===========================

class Plug(Axon.Component.component)
------------------------------------

Plug(splitter,component) -\> new Plug component.

A component that \'plugs\' the specified component into the specified
splitter as a destination for data.

Keyword arguments: - splitter \-- splitter component to plug into (any
component that accepts addsink(\...) and removesink(\...) messages on a
\'configuration\' inbox - component \-- component to receive data from
the splitter

#### Inboxes

-   control : Incoming control data for child component, and shutdown
    signalling
-   inbox : Incoming data for child component

#### Outboxes

-   outbox : Outgoing data from child component
-   signal : Outgoing control data from child component, and shutdown
    signalling
-   splitter\_config : Used to communicate with the target splitter

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, splitter, component)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

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

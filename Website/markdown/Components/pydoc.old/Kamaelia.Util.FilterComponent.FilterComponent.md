---
pagename: Components/pydoc.old/Kamaelia.Util.FilterComponent.FilterComponent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.FilterComponent.FilterComponent
=============================================

class FilterComponent(Axon.Component.component)
-----------------------------------------------

FilterComponent(\[filter\]) -\> new FilterComponent component.

Component that can modify and filter data passing through it. Plug your
own \'filter\' into it.

Keyword arguments: - filter \-- an object implementing a filter(data)
method (default=NullFilter instance)

#### Inboxes

-   control : Shutdown signalling
-   inbox : Data to be filtered

#### Outboxes

-   outbox : Filtered data
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, filter)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### closeDownComponent(self)

Flush any data remaining in the filter before shutting down.

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

---
pagename: Components/pydoc.old/Kamaelia.Util.RateFilter.OnDemandLimit
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.RateFilter.OnDemandLimit
======================================

class OnDemandLimit(Axon.Component.component)
---------------------------------------------

OnDemandLimit() -\> new OnDemandLimit component.

A component that receives data items, but only emits them on demand, one
at a time, when \"NEXT\" messages are received on the \"slidecontrol\"
inbox.

#### Inboxes

-   control : Shutdown signalling
-   inbox : Data items to be passed on, on demand.
-   slidecontrol : \'NEXT\' requests to emit a data item.

#### Outboxes

-   outbox : Data items, when requested.
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

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

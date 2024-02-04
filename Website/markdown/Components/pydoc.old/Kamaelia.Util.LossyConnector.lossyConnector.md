---
pagename: Components/pydoc.old/Kamaelia.Util.LossyConnector.lossyConnector
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.LossyConnector.lossyConnector
===========================================

class lossyConnector(Axon.Component.component)
----------------------------------------------

lossyConnector() -\> new lossyConnector component

Component that forwards data from inbox to outbox, but discards data if
destination is full.

#### Inboxes

-   control : Shutdown signalling
-   inbox : Data to be passed on

#### Outboxes

-   outbox : Data received on \'inbox\' inbox
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

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

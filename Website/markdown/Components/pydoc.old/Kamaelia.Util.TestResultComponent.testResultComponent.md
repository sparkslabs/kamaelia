---
pagename: Components/pydoc.old/Kamaelia.Util.TestResultComponent.testResultComponent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.TestResultComponent.testResultComponent
=====================================================

class testResultComponent(Axon.Component.component)
---------------------------------------------------

testResultComponent() -\> new testResultComponent.

Component that raises an AssertionError if it receives data on its
\"inbox\" inbox that does not test true. Or raises a StopSystemException
if a StopSystem message is received on its \"control\" inbox.

#### Inboxes

-   control : StopSystemException messages
-   inbox : Data to test

#### Outboxes

-   outbox : NOT USED
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### mainBody(self)

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

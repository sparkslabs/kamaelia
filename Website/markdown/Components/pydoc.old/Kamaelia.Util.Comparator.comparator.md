---
pagename: Components/pydoc.old/Kamaelia.Util.Comparator.comparator
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Comparator.comparator
===================================

class comparator(Axon.Component.component)
------------------------------------------

comparator() -\> new comparator component.

Compares items received on \"inA\" inbox with items received on \"inB\"
inbox. For each pair, outputs True if items compare equal, otherwise
False.

#### Inboxes

-   control : NOT USED
-   inbox : NOT USED
-   inB : Source \'B\' of items to compare
-   inA : Source \'A\' of items to compare

#### Outboxes

-   outbox : Result of comparison
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### combine(self, valA, valB)

Returns result of (valA == valB)

Reimplement this method to change the type of comparison from equality
testing.

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

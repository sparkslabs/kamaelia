---
pagename: Components/pydoc.old/Kamaelia.Util.Chooser.Chooser
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Chooser.Chooser
=============================

class Chooser(Axon.Component.component)
---------------------------------------

Chooser(\[items\]) -\> new Chooser component.

Iterates through a finite list of items. Step by sending \"NEXT\",
\"PREV\", \"FIRST\" or \"LAST\" messages to its \"inbox\" inbox.

Keyword arguments: - items \-- list of items to be chosen from, must be
type \'list\' (default=\[\])

#### Inboxes

-   control : shutdown messages
-   inbox : receive commands

#### Outboxes

-   outbox : emits chosen items
-   signal : shutdown messages

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, items)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### getCurrentChoice(self)

Return the current choice to the outbox

### gotoFirst(self)

Goto the first item in the set. Returns True.

### gotoLast(self)

Goto the last item in the set. Returns True.

### gotoNext(self)

Advance the choice forwards one.

Returns True if successful or False if unable to (eg. already at end).

### gotoPrev(self)

Backstep the choice backwards one.

Returns True if successful or False if unable to (eg. already at start).

### main(self)

Main loop.

### shutdown(self)

Returns True if a shutdownMicroprocess message was received.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

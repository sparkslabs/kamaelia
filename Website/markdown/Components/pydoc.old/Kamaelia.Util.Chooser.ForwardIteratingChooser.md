---
pagename: Components/pydoc.old/Kamaelia.Util.Chooser.ForwardIteratingChooser
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Chooser.ForwardIteratingChooser
=============================================

class ForwardIteratingChooser(Axon.Component.component)
-------------------------------------------------------

Chooser(\[items\]) -\> new Chooser component.

Iterates through an iterable set of items. Step by sending \"NEXT\"
messages to its \"inbox\" inbox.

Keyword arguments: - items \-- iterable source of items to be chosen
from (default=\[\])

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

Return the current choice

### gotoNext(self)

Advance the choice forwards one.

Returns True if successful or False if unable to (eg. already at end).

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

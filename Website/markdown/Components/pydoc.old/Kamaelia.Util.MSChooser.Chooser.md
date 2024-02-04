---
pagename: Components/pydoc.old/Kamaelia.Util.MSChooser.Chooser
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.MSChooser.Chooser
===============================

class Chooser(Axon.Component.component)
---------------------------------------

Chooses items out of a set, as directed by commands sent to its inbox

> Emits the first item at initialisation, then whenever a command is
> received it emits another item (unless you\'re asking it to step
> beyond the start or end of the set)

#### Inboxes

-   control :
-   inbox : receive commands

#### Outboxes

-   outbox : emits chosen items
-   signal :

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, items, loop)

Initialisation.
:   items = set of items that can be iterated over. Must be finite. If
    an iterator is supplied, it is enumerated into a list during
    initialisation.

### main(self)

### shutdown(self)

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

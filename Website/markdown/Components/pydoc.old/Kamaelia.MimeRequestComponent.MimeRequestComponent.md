---
pagename: Components/pydoc.old/Kamaelia.MimeRequestComponent.MimeRequestComponent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.MimeRequestComponent.MimeRequestComponent
==================================================

class MimeRequestComponent(Axon.Component.component)
----------------------------------------------------

Component that accepts raw data, parses it into consituent
:   parts of a MIME request. Attempts no interpretation of the request
    however.

#### Inboxes

-   control : Secondary inbox often used for signals. The closest
    analogy is unix signals
-   inbox : Default inbox for bulk data. Used in a pipeline much like
    stdin

#### Outboxes

-   outbox : Default data out outbox, used in a pipeline much like
    stdout
-   signal : The default signal based outbox - kinda like stderr, but
    more for sending singal type signals

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

### checkEndOfHeader(self)

### getALine(self)

Sets the *CURRENT* line arguments

### getData(self)

### getRequestLine(self)

Sets the *REQUEST* line arguments

### handleDataAquisition(self)

This is currently clunky and effectively implements a state machine.
:   Should consider rewriting as a generator

### initialiseComponent(self)

### mainBody(self)

### nextLine(self)

### readHeader(self)

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

---
pagename: Components/pydoc.old/Kamaelia.Protocol.FortuneCookieProtocol.FortuneCookieProtocol
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Protocol.FortuneCookieProtocol.FortuneCookieProtocol
=============================================================

class FortuneCookieProtocol(Axon.Component.component)
-----------------------------------------------------

FortuneCookieProtocol(\[debug\]) -\> new FortuneCookieProtocol
component.

A protocol that spits out a random fortune cookie, then terminates.

Keyword arguments: - debug \-- Debugging output control (default=0)

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

### \_\_init\_\_(self, debug)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### initialiseComponent(self)

Initialises component. Sets up a ReadFileAdapter to read the result of
running \'fortune\'.

### mainBody(self)

Main body.

All the interesting work has been done by linking the file reader\'s
output to our output. Messages sent to control are unchecked and the
first message causes the component to exit.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

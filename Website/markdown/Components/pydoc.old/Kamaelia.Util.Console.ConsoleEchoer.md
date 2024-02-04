---
pagename: Components/pydoc.old/Kamaelia.Util.Console.ConsoleEchoer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Console.ConsoleEchoer
===================================

class ConsoleEchoer(Axon.Component.component)
---------------------------------------------

ConsoleEchoer(\[forwarder\]\[,use\_repr\]) -\> new ConsoleEchoer
component.

A component that outputs anything it is sent to standard output (the
console).

Keyword arguments: - forwarder \-- incoming data is also forwarded to
\"outbox\" outbox if True (default=False) - use\_repr \-- use repr()
instead of str() if True (default=False)

#### Inboxes

-   control : Shutdown signalling
-   inbox : Stuff that will be echoed to standard output

#### Outboxes

-   outbox : Stuff forwarded from \'inbox\' inbox (if enabled)
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, forwarder, use\_repr)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

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

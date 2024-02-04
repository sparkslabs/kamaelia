---
pagename: Components/pydoc.old/Kamaelia.Util.Console.ConsoleReader
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.Console.ConsoleReader
===================================

class ConsoleReader(Axon.ThreadedComponent.threadedcomponent)
-------------------------------------------------------------

ConsoleReader(\[prompt\]\[,eol\]) -\> new ConsoleReader component.

Component that provides a console for typing in stuff. Each line is
output from the \"outbox\" outbox one at a time.

Keyword arguments: - prompt \-- Command prompt (default=\"\>\>\> \") -
eol \-- End of line character(s) to put on end of every line outputted
(default is newline\")

#### Inboxes

-   control : NOT USED
-   inbox : NOT USED

#### Outboxes

-   outbox : Lines that were typed at the console
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, prompt, eol)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### run(self)

Main thread loop.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

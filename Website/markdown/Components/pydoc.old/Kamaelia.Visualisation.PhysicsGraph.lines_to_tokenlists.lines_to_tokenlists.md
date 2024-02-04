---
pagename: Components/pydoc.old/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.lines_to_tokenlists
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Visualisation.PhysicsGraph.lines\_to\_tokenlists.lines\_to\_tokenlists
===============================================================================

class lines\_to\_tokenlists(Axon.Component.component)
-----------------------------------------------------

lines\_to\_tokenlists() -\> new lines\_to\_tokenlists component.

Takes individual lines of text and separates them into white space
separated tokens. Tokens can be enclosed with single or double quote
marks.

#### Inboxes

-   control : Shutdown signalling
-   inbox : Individual lines of text

#### Outboxes

-   outbox : list of tokens making up the line of text
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### lineToTokens(self, line)

linesToTokens(line) -\> list of tokens.

Splits a line into individual white-space separated tokens. Tokens can
be enclosed in single or double quotes to allow spaces to be used in
them.

Escape backslash and single or double quotes by prefixing them with a
backslash *only* if used within an quote encapsulated string.

### main(self)

Main loop.

### shutdown(self)

Returns True if a shutdownMicroprocess or producerFinished message was
received.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

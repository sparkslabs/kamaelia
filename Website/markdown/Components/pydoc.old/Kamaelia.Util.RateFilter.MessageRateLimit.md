---
pagename: Components/pydoc.old/Kamaelia.Util.RateFilter.MessageRateLimit
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.RateFilter.MessageRateLimit
=========================================

class MessageRateLimit(Axon.Component.component)
------------------------------------------------

MessageRateLimit(messages\_per\_second\[, buffer\]) -\> new
MessageRateLimit component.

Buffers messages and outputs them at a rate limited by the specified
rate once the buffer is full.

Keyword arguments: - messages\_per\_second \-- maximum output rate -
buffer \-- size of buffer (0 or greater) (default=60)

#### Inboxes

-   control : NOT USED
-   inbox : Incoming items/messages

#### Outboxes

-   outbox : Items/messages limited to specified maximum output rate
-   signal : NOT USED

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, messages\_per\_second, buffer)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Main loop.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

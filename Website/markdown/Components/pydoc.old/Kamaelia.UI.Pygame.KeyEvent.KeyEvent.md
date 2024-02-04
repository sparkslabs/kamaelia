---
pagename: Components/pydoc.old/Kamaelia.UI.Pygame.KeyEvent.KeyEvent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.UI.Pygame.KeyEvent.KeyEvent
====================================

class KeyEvent(Axon.Component.component)
----------------------------------------

KeyEvent(\[allkeys\]\[,key\_events\]\[,outboxes\]) -\> new KeyEvent
component.

Component that sends out messages in response to pygame keypress events.

Keyword arguments: - allkeys \-- if True, all keystrokes send messages
out of \"allkeys\" outbox (default=False) - key\_events \-- dict mapping
pygame keycodes to (msg,\"outboxname\") pairs (default=None) - outboxes
\-- dict of \"outboxname\":\"description\" key:value pairs (default={})

#### Inboxes

-   control : Shutdown messages: shutdownMicroprocess or
    producerFinished
-   callback : Receive callbacks from PygameDisplay
-   inbox : Receive events from PygameDisplay

#### Outboxes

-   outbox : NOT USED
-   signal : Shutdown signalling: shutdownMicroprocess or
    producerFinished
-   allkeys : Outbox that receives \*every\* keystroke if enabled
-   display\_signal : Outbox used for communicating to the display
    surface

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, allkeys, key\_events, outboxes)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Main loop.

### waitBox(self, boxname)

Generator. yields 1 until data is ready on the named inbox.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

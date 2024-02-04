---
pagename: Components/pydoc.old/Kamaelia.Protocol.AudioCookieProtocol.AudioCookieProtocol
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Protocol.AudioCookieProtocol.AudioCookieProtocol
=========================================================

class AudioCookieProtocol(Axon.Component.component)
---------------------------------------------------

AudioCookieProtocol(\[debug\]) -\> new AudioCookieProtocol component.

A protocol that spits out raw audio data from a randomly selected audio
file.

Keyword arguments: - debug \-- Debugging output control (default=0)

#### Inboxes

-   control : NOT USED
-   inbox : NOT USED

#### Outboxes

-   outbox : Raw audio data
-   signal : producerFinished() at end of data

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, debug)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### initialiseComponent(self)

Initialises component. Sets up a ReadFileAdapter to read in the contents
of an audio file at 95.2kbit/s and wires it to fire the contents out

### mainBody(self)

Main body - sits and waits, as ReadFileAdapter is getting on with the
work for us

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

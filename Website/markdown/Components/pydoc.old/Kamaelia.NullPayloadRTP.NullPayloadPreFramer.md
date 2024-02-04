---
pagename: Components/pydoc.old/Kamaelia.NullPayloadRTP.NullPayloadPreFramer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.NullPayloadRTP.NullPayloadPreFramer
============================================

class NullPayloadPreFramer(Axon.Component.component)
----------------------------------------------------

Inboxes:
:   control -\> File select, file read control, framing control recvsrc
    -\> Block/Chunks of raw disk data

Outboxes:
:   activatesrc -\> Control messages to the file reading subsystem
    output -\> The framed data, payload ready

#### Inboxes

-   control : Code uses old style inbox/outbox description - no metadata
    available
-   recvsrc : Code uses old style inbox/outbox description - no metadata
    available

#### Outboxes

-   output : Code uses old style inbox/outbox description - no metadata
    available

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, sourcename, sourcebitrate, chunksize)

-   

    Name of source - at \_\_init\_\_

    :   -   Data Rate - at \_\_init\_\_
        -   Chunksize - at \_\_init\_\_

### closeDownComponent(self)

No closedown/shutdown code

### handleControl(self)

returns quit flag - True means quit

### handleShutdown(self)

### initialiseComponent(self)

No initialisation

### mainBody(self)

Loopbody:

### makeChunk(self, datatosend)

C.makeChunk(datatosend) -\> chunk : network ready data

### sendCurrentChunk(self, sendpartial)

-   

    grab first (current chunk size) bytes

    :   -   frame chunk
        -   send chunk

### updateTimestamp(self, datatosend)

C.updateTimestamp(datatosend)

> self.timestamp stores the timestamp of the end of the most recently
> transmitted data, whenever we send some data this timestamp needs to
> be updated. This method represents the calculation involved.
> (calculate the time period the data covers, and increment the
> timestamp)

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

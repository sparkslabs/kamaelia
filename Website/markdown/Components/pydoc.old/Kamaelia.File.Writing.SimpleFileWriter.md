---
pagename: Components/pydoc.old/Kamaelia.File.Writing.SimpleFileWriter
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.File.Writing.SimpleFileWriter
======================================

class SimpleFileWriter(Axon.Component.component)
------------------------------------------------

SimpleFileWriter(filename) -\> component that writes data to the file

Writes any data sent to its inbox to the specified file.

#### Inboxes

-   control : to receive shutdown/finished messages
-   inbox : data to write to file

#### Outboxes

-   outbox : not used
-   signal : shutdown/finished signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, filename)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### closeDownComponent(self)

Closes the file handle

### main(self)

Main loop

### shutdown(self)

Returns True if a shutdownMicroprocess or producerFinished message is
received.

Also passes the message on out of the \"signal\" outbox.

### writeData(self, data)

Writes the data to the file

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

---
pagename: Components/pydoc.old/Kamaelia.File.Reading.PromptedFileReader
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.File.Reading.PromptedFileReader
========================================

class PromptedFileReader(Axon.Component.component)
--------------------------------------------------

PromptedFileReader(filename\[,readmode\]) -\> file reading component

Creates a file reader component. Reads N bytes/lines from the file when
N is sent to its inbox.

Keyword arguments: - readmode = \"bytes\" or \"lines\"

#### Inboxes

-   control : for shutdown signalling
-   inbox : requests to \'n\' read bytes/lines

#### Outboxes

-   outbox : data output
-   signal : outputs \'producerFinished\' after all data has been read

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, filename, readmode)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### closeDownComponent(self)

Closes the file handle

### main(self)

Main loop

### readNBytes(self, n)

readNBytes(n) -\> string containing \'n\' bytes read from the file.

\"EOF\" raised if the end of the file is reached and there is no data to
return.

### readNLines(self, n)

readNLines(n) -\> string containing \'n\' lines read from the file.

\"EOF\" raised if the end of the file is reached and there is no data to
return.

### shutdown(self)

Returns True if a shutdownMicroprocess message is received.

Also passes the message on out of the \"signal\" outbox.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

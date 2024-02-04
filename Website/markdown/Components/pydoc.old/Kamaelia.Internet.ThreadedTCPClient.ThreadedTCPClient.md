---
pagename: Components/pydoc.old/Kamaelia.Internet.ThreadedTCPClient.ThreadedTCPClient
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.ThreadedTCPClient.ThreadedTCPClient
=====================================================

class ThreadedTCPClient(Axon.ThreadedComponent.threadedcomponent)
-----------------------------------------------------------------

ThreadedTCPClient(host,port\[,chargen\]\[,initalsendmessage\]) -\>
threaded component with a TCP connection to a server.

Establishes a TCP connection to the specified server.

Keyword arguments: - host \-- address of the server to connect to
(string) - port \-- port number to connect on - initialsendmessage \--
to be send immediately after connection is established (default=None)

#### Inboxes

-   control :
-   inbox : data to send to the socket

#### Outboxes

-   outbox : data received from the socket
-   signal : diagnostic output, errors and shutdown messages

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, host, port, chargen, initialsendmessage)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### run(self)

Main (thread) loop

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

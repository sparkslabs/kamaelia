---
pagename: Components/pydoc.old/Kamaelia.Internet.TCPClient.TCPClient
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Internet.TCPClient.TCPClient
=====================================

class TCPClient(Axon.Component.component)
-----------------------------------------

TCPClient(host,port\[,delay\]) -\> component with a TCP connection to a
server.

Establishes a TCP connection to the specified server.

Keyword arguments: - host \-- address of the server to connect to
(string) - port \-- port number to connect on - delay \-- delay
(seconds) after activation before connecting (default=0)

#### Inboxes

-   control : NOT USED
-   inbox : data to send to the socket
-   \_socketFeedback : notifications from the ConnectedSocketAdapter

#### Outboxes

-   outbox : data received from the socket
-   signal : socket errors
-   \_selectorSignal : communicating with a selectorComponent

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, host, port, delay)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### main(self)

Main loop.

### runClient(self, sock)

### safeConnect(self, sock)

Connect to socket and handle possible errors that may occur.

Returns True if successful, or False on failure. Unhandled errors are
raised as exceptions.

### setupCSA(self, sock)

setupCSA(sock) -\> new ConnectedSocketAdapter component

Creates a ConnectedSocketAdapter component for the socket, and wires up
to it. Also sends the CSA to the \"selector\" service.

### waitCSAClose(self)

Returns True if a socketShutdown message is received on
\"\_socketFeedback\" inbox.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

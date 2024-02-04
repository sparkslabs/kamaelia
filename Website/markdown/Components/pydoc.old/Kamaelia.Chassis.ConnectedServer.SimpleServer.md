---
pagename: Components/pydoc.old/Kamaelia.Chassis.ConnectedServer.SimpleServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Chassis.ConnectedServer.SimpleServer
=============================================

class SimpleServer(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent)
----------------------------------------------------------------------

SimpleServer(protocol\[,port\]) -\> new Simple protocol server component

A simple single port, multiple connection server, that instantiates a
protocol handler component to handle each connection.

Keyword arguments: protocol \-- function that returns a protocol handler
component port \-- Port number to listen on for connections
(default=1601)

#### Inboxes

-   \_oobinfo : internal use: Out Of Bounds Info - for receiving
    signalling of new and closing connections

#### Outboxes

-   

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, protocol, port)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### checkOOBInfo(self)

Check and handle Out Of Bounds info - notifications of new and closed
sockets.

### handleClosedCSA(self, data)

handleClosedCSA(data) -\> None

Terminates and unwires the protocol handler for the closing socket.

Keyword arguments: data \-- data.object is the ConnectedSocketAdapter
for socket that is closing.

### handleNewCSA(self, data)

handleNewCSA(data) -\> Axon.Ipc.newComponent(protocol handler)

Creates and returns a protocol handler for new connection.

Keyword arguments: data \-- data.object is the ConnectedSocketAdapter
component for the connection

### initialiseComponent(self)

Sets up socket binding to listen for incoming connections

### mainBody(self)

Main loop

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).

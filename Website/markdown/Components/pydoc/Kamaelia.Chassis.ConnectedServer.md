---
pagename: Components/pydoc/Kamaelia.Chassis.ConnectedServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}
=============================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ServerCore](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.ServerCore.html){.reference}**
-   **component
    [SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html){.reference}**
:::

-   [Connected Servers](#268){.reference}
    -   [Example Usage](#269){.reference}
    -   [Why is this useful?](#270){.reference}
    -   [Writing a protocol handler](#271){.reference}
    -   [How does it work?](#272){.reference}
    -   [History](#273){.reference}
    -   [To do](#274){.reference}
:::

::: {.section}
Connected Servers {#268}
=================

These \'chassis\' style components are used to implementing connected
servers. The most common example of this is a server which runs on top
of the TCP. Examples include: a web server, email server, imap server,
game protocol server, etc.

At present, there are two variants of this: *ServerCore* and
*SimpleServer* (You are generally recommended to use ServerCore)

Both of these revolve around building TCP based servers. They handle the
mechanics of creating the listening component, and when new connections
come in, creating instances of your protocol handler components to
handle the connections.

As a result, the primary arguments are the port to listen on and a
function call or class name that when called returns a component for
handling this connection.

Your protocol handler then receives data from a specific client on its
inbox \"inbox\" and sends data to that same client on its outbox
\"outbox\".

ServerCore passes additional information about the connection to the
function that creates the protocol handler. You are not required to do
anything with that information if you don\'t need to.

Aside from that, ServerCore & SimpleServer are used in the same way.
(ServerCore is just an extension, and rationalisation of the older
simple server code).

There is more information here:
<http://www.kamaelia.org/Cookbook/TCPSystems>

::: {.section}
[Example Usage]{#example-usage} {#269}
-------------------------------

A server using a simple echo protocol, that just echoes back anything
sent by the client. Becase the protocol has no need to know any details
of the connection, the SimpleServer component is used:

``` {.literal-block}
import Axon
from Kamaelia.Chassis.ConnectedServer import SimpleServer

PORTNUMBER = 12345
class EchoProtocol(Axon.Component.component):

    def main(self):
        while not self.shutdown():
            yield 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data, "outbox")

    def shutdown(self):
        if self.dataReady("control"):
            msg = self.recv("control")
            return isinstance(msg, Axon.Ipc.producerFinished)

simpleServer = SimpleServer( protocol = EchoProtocol, port = PORTNUMBER )
simpleServer.run()
```

Try connecting to this server using the telnet command, and it will echo
back to you every character you type.

A more complex server might need to inform the protocol of the IP
address and port of the client that connects, or the ip address and port
at this (the server end) to which the client has connected. For this,
ServerCore is used:

``` {.literal-block}
import Axon
from Axon.Ipc import shutdownMicroprocess
from Kamaelia.Chassis.ConnectedServer import ServerCore

PORTNUMBER = 12345
class CleverEchoProtocol(Axon.Component.component):

    def main(self):
        welcomeMessage =                 "Welcome! You have connected to %s on port %d from %s on port %d" %                 (self.localip, self.localport, self.peer, self.peerport)

        self.send(welcomeMessage, "outbox")
        while not self.shutdown():
            yield 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data, "outbox")

    def shutdown(self):
        if self.dataReady("control"):
            msg = self.recv("control")
            return isinstance(msg, Axon.Ipc.producerFinished)

myServer = ServerCore( protocol = CleverEchoProtocol, port = PORTNUMBER )
myServer.run()
```

Example output when telnetting to this more complex server, assuming
both server and telnet session are running on the same host, and the
server is listening to port number 8081:

``` {.literal-block}
$ telnet localhost 8081
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Welcome! You have connected to 127.0.0.1 on port 8081 from 127.0.0.1 on port 47316
```
:::

::: {.section}
[Why is this useful?]{#why-is-this-useful} {#270}
------------------------------------------

Provides a framework for creating generic protocol handlers to deal with
information coming in on a single port (and a single port only). This
however covers a large array of server types.

A protocol handler is simply a component that can receive and send data
(as byte strings) in a particular format and with a particular behaviour
- ie. conforming to a particular protocol.

Provide this chassis with a factory function to create a component to
handle the protocol. Whenever a client connects a handler component will
then be created to handle communications with that client.

Data received from the client will be sent to the protocol handler
component\'s \"inbox\" inbox. To send data back to the client, the
protocol handler component should send it out of its \"outbox\" outbox.

For the SingleServer component, the factory function takes no arguments.
It should simply return the component that will be used to handle the
protocol, for example:

``` {.literal-block}
def makeNewProtocolHandler():
    return MyProtocolComponent()
```

For the ServerCore component, the factory function must accept the
following arguments (with these names):

-   peer \-- the address of the remote endpoint (the client\'s address)
-   peerport \-- the port number of the remote endpoint (the port number
    from which the client connection originated)
-   localip \-- the address of the local endpoint (this end of the
    connection)
-   localport \-- the port number of the local endpoint (this end of the
    connection)

For example:

``` {.literal-block}
def makeNewProtocolHandler(peer, peerport, localip, localport):
    print "Debugging: client at address "+peer+" on port "+str(peerport)
    print " ... has connected to address "+localip+" on port "+str(localport)
    return MyProtocolComponent()
```

Do not activate the component. SingleServer or ServerCore will do this
once the component is wired up.
:::

::: {.section}
[Writing a protocol handler]{#writing-a-protocol-handler} {#271}
---------------------------------------------------------

A protocol handler component should use its standard inboxes (\"inbox\"
and \"control\") and outboxes (\"outbox\" and \"signal\") to communicate
with client it is connected to.

-   Bytes received from the client will be sent to the \"inbox\" inbox
    as a string.
-   Send a string out of the \"outbox\" outbox to send bytes back to the
    client.

If the connection is closed, a Kamaelia.IPC.socketShutdown message will
arrive at the protocol handler\'s \"control\" inbox. If this happens
then the connection should be assumed to have already closed. Any more
messages sent will not be sent to the client. The protocol handler
should react by terminating as soon as possible.

To cause the connection to close, send a producerFinished or
shutdownMicroprocess message out of the protocol handler\'s \"signal\"
outbox. As soon as this has been done, it can be assumed that the
connection will be closed as soon as is practical. The protocol handler
will probably also want to terminate at this point.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#272}
--------------------------------------

SimpleServer is based on ServerCore. It simply contains a wrapper around
the protocol handler function that throws away the connection
information instead of passing it in as arguments.

At initialisation the component registers a TCPServer component to
listen for new connections on the specified port.

You supply a factory function that takes no arguments and returns a new
protocol handler component.

When it receives a \'newCSA\' message from the TCPServer (via the
\"\_socketactivity\" inbox), the factory function is called to create a
new protocol handler. The protocol handler\'s \"inbox\" inbox and
\"outbox\" outbox are wired to the ConnectedSocketAdapter (CSA)
component handling that socket connection, so it can receive and send
data.

If a \'shutdownCSA\' message is received (via \"\_socketactivity\") then
a Kamaelia.IPC.socketShutdown message is sent to the protocol handler\'s
\"control\" inbox, and both it and the CSA are unwired.

This component does not terminate. It ignores any messages sent to its
\"control\" inbox.

In practice, this component provides no external connectors for your
use.
:::

::: {.section}
[History]{#history} {#273}
-------------------

This code is based on the code used for testing the Internet Connection
abstraction layer.
:::

::: {.section}
[To do]{#to-do} {#274}
---------------

This component currently lacks an inbox and corresponding code to allow
it to be shut down (in a controlled fashion). Needs a \"control\" inbox
that responds to shutdownMicroprocess messages.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}.[ServerCore](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.ServerCore.html){.reference}
==========================================================================================================================================================================================================================================================================================================

::: {.section}
class ServerCore([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-ServerCore}
------------------------------------------------------------------------------------------------------------------------------------------------------

ServerCore(protocol\[,port\]) -\> new Simple protocol server component

A simple single port, multiple connection server, that instantiates a
protocol handler component to handle each connection. The function that
creates the protocol must access arguments providing information about
the connection.

Keyword arguments:

-   protocol \-- function that returns a protocol handler component
-   port \-- Port number to listen on for connections (default=1601)

::: {.section}
### [Inboxes]{#symbol-ServerCore.Inboxes}

-   **control** : We expect to get serverShutdown messages here
-   **\_socketactivity** : Messages about new and closing connections
    here
:::

::: {.section}
### [Outboxes]{#symbol-ServerCore.Outboxes}

-   **\_serversignal** : we send shutdown messages to the TCP server
    here
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-ServerCore.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [handleClosedCSA(self, shutdownCSAMessage)]{#symbol-ServerCore.handleClosedCSA}

handleClosedCSA(shutdownCSAMessage) -\> None

Terminates and unwires the protocol handler for the closing socket.

Keyword arguments: shutdownCSAMessage \-- shutdownCSAMessage.object is
the ConnectedSocketAdapter for socket that is closing.
:::

::: {.section}
#### [handleNewConnection(self, newCSAMessage)]{#symbol-ServerCore.handleNewConnection}

handleNewConnection(newCSAMessage) -\>
[Axon.Ipc.newComponent](/Docs/Axon/Axon.Ipc.newComponent.html){.reference}(protocol
handler)

Creates and returns a protocol handler for new connection.

Keyword arguments:

-   newCSAMessage \-- newCSAMessage.object is the ConnectedSocketAdapter
    component for the connection
:::

::: {.section}
#### [initialiseServerSocket(self)]{#symbol-ServerCore.initialiseServerSocket}
:::

::: {.section}
#### [main(self)]{#symbol-ServerCore.main}
:::

::: {.section}
#### [mkProtocolHandler(self, \*\*sock\_info)]{#symbol-ServerCore.mkProtocolHandler}
:::

::: {.section}
#### [stop(self)]{#symbol-ServerCore.stop}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}.[SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html){.reference}
==============================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleServer(ServerCore) {#symbol-SimpleServer}
------------------------------

SimpleServer(protocol\[,port\]) -\> new Simple protocol server component

A simple single port, multiple connection server, that instantiates a
protocol handler component to handle each connection.

Keyword arguments:

-   protocol \-- function that returns a protocol handler component
-   port \-- Port number to listen on for connections (default=1601)

::: {.section}
### [Inboxes]{#symbol-SimpleServer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleServer.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-SimpleServer.__init__}
:::

::: {.section}
#### [mkProtocolHandler(self, \*\*sock\_info)]{#symbol-SimpleServer.mkProtocolHandler}
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.Chassis.ConnectedServer.MoreComplexServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.MoreComplexServer.html){.reference} :

-   [handleNewConnection](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.handleNewConnection){.reference}(self,
    newCSAMessage)
-   [stop](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.stop){.reference}(self)
-   [initialiseServerSocket](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.initialiseServerSocket){.reference}(self)
-   [handleClosedCSA](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.handleClosedCSA){.reference}(self,
    shutdownCSAMessage)
-   [main](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html#symbol-MoreComplexServer.main){.reference}(self)
:::
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*

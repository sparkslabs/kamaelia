#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
=====================
Simple Server Chassis
=====================

A simple TCP server, bound to a specified port. For each client that connects, a
protocol handler component, of your choosing, is created to send and receive
data to and from that client.



Example Usage
-------------

A server using a simple echo protocol, that just echoes back anything sent by
the client::

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
                return isinstance(msg, Axon.Ipc.producerFinished):

    def newProtocol():
        return EchoProtocol()

    simpleServer = SimpleServer( protocol = newProtocol, port = PORTNUMBER )
    simpleServer.activate()



Why is this useful?
-------------------

Provides a framework for creating generic protocol handlers to deal with
information coming in on a single port (and a single port only). This however
covers a large array of server types.

A protocol handler is simply a component that can receive and send data (as
byte strings) in a particular format and with a particular behaviour - ie.
conforming to a particular protocol. 

Provide this chassis with a factory function to create a component to
handle the protocol. Whenever a client connects a handler component will then be
created to handle communications with that client.



How does it work?
-----------------

At initialisation the component registers a TCPServer component to listen for
new connections on the specified port.

You supply a factory function that takes no arguments and returns a new
protocol handler component.

When it receives a 'newCSA' message from the TCPServer (via the "_socketactivity"
inbox), the factory function is called to create a new protocol handler. The
protocol handler's "inbox" inbox and "outbox" outbox are wired to the
ConnectedSocketAdapter (CSA) component handling that socket connection, so it can
receive and send data.

If SingleServer receives a 'shutdownCSA' message (via "_socketactivity") then a
Kamaelia.KamaeliaIpc.socketShutdown message is sent to the protocol handler's
"control" inbox, and both it and the CSA are unwired.

This component does not terminate. It ignores any messages sent to its "control"
inbox.

In practice, this component provides no external connectors for your use.



History
-------

This code is based on the code used for testing the Internet Connection
abstraction layer.



To do
-----

This component currently lacks an inbox and corresponding code to allow it to
be shut down (in a controlled fashion). Needs a "control" inbox that responds to
shutdownMicroprocess messages.
"""
import sys
import socket
import Axon
from Kamaelia.Internet.TCPServer import TCPServer
from Kamaelia.IPC import newCSA, shutdownCSA, socketShutdown, serverShutdown
from Axon.Ipc import newComponent, shutdownMicroprocess


class ServerCore(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """
    ServerCore(protocol[,port]) -> new Simple protocol server component

    A simple single port, multiple connection server, that instantiates a
    protocol handler component to handle each connection.

    Keyword arguments:

    - protocol  -- function that returns a protocol handler component
    - port      -- Port number to listen on for connections (default=1601)
    """

    Inboxes = { "_socketactivity" : "Messages about new and closing connections here",
                "control" : "We expect to get serverShutdown messages here" }
    Outboxes = { "_serversignal" : "we send shutdown messages to the TCP server here",
               }
    port = 1601
    protocol = None
    socketOptions=None
    TCPS=TCPServer
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ServerCore, self).__init__(**argd) 
        self.connectedSockets = []
        self.server = None
        if not self.protocol:
            print self.__class__, self.__class__.protocol, self.protocol
            raise "Need a protocol to handle!"

    def initialiseServerSocket(self):
        if self.socketOptions is None:
            self.server = (self.TCPS)(listenport=self.port)
        else:
            self.server = (self.TCPS)(listenport=self.port, socketOptions=self.socketOptions)

        self.link((self.server,"protocolHandlerSignal"),(self,"_socketactivity"))
        self.link((self,"_serversignal"), (self.server,"control"))
        self.addChildren(self.server)
        self.server.activate()

    def main(self):
        self.initialiseServerSocket()
        while 1:
            while not self.anyReady():
                self.pause()
                yield 1
            # Check and handle Out Of Bounds info
            # notifications of new and closed sockets
            while self.dataReady("_socketactivity"):
                data = self.recv("_socketactivity")
                if isinstance(data, newCSA):
                    self.handleNewConnection(data)
                if isinstance(data, shutdownCSA):
                    self.handleClosedCSA(data)
            if self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data, serverShutdown):
                    break
            yield 1

        self.stop() # Ensures everything shuts down as far as we can manage it

    def stop(self):
        for CSA in self.connectedSockets:
            self.handleClosedCSA(shutdownCSA(self,CSA))

        self.send(serverShutdown(), "_serversignal")
        super(ServerCore, self).stop()

    def mkProtocolHandler(self, **sock_info):

        return (self.protocol)(peer = sock_info["peer"],
                               peerport = sock_info["peerport"],
                               localip = sock_info["localip"],
                               localport = sock_info["localport"])

    def handleNewConnection(self, newCSAMessage):
        """
        handleNewConnection(newCSAMessage) -> Axon.Ipc.newComponent(protocol handler)

        Creates and returns a protocol handler for new connection.

        Keyword arguments:

        - newCSAMessage  -- newCSAMessage.object is the ConnectedSocketAdapter component for the connection
        """
        connectedSocket = newCSAMessage.object

        sock = newCSAMessage.sock
        try:
            peer, peerport = sock.getpeername()
            localip, localport = sock.getsockname()
        except socket.error, e:
            peer, peerport = "0.0.0.0", 0
            localip, localport = "127.0.0.1", self.port
        protocolHandler = self.mkProtocolHandler(peer=peer, peerport=peerport,localip=localip,localport=localport)

        self.connectedSockets.append(connectedSocket)

        outboxToShutdownProtocolHandler= self.addOutbox("protocolHandlerShutdownSignal")
        outboxToShutdownConnectedSocket= self.addOutbox("connectedSocketShutdownSignal")

        # sys.stderr.write("Wooo!\n"); sys.stderr.flush()

        self.trackResourceInformation(connectedSocket, 
                                      [], 
                                      [outboxToShutdownProtocolHandler], 
                                      protocolHandler)
        # sys.stderr.write("Um, that should've tracked something...!\n"); sys.stderr.flush()

        self.link((connectedSocket,"outbox"),(protocolHandler,"inbox"))
        self.link((protocolHandler,"outbox"),(connectedSocket,"inbox"))
        self.link((self,outboxToShutdownProtocolHandler), (protocolHandler, "control"))
        self.link((self,outboxToShutdownConnectedSocket), (connectedSocket, "control"))
        self.link((protocolHandler,"signal"),(connectedSocket, "control"))

        if "serversignal" in protocolHandler.Outboxes:
            controllink = self.link((protocolHandler, "serversignal"), (self, "control"))
        else:
            controllink = None

        self.trackResourceInformation(connectedSocket, 
                                      [], 
                                      [outboxToShutdownProtocolHandler, outboxToShutdownConnectedSocket], 
                                      ( protocolHandler, controllink ) )

        self.addChildren(connectedSocket,protocolHandler)
        connectedSocket.activate()
        protocolHandler.activate()

    def handleClosedCSA(self,shutdownCSAMessage):
        """
        handleClosedCSA(shutdownCSAMessage) -> None

        Terminates and unwires the protocol handler for the closing socket.

        Keyword arguments:
        shutdownCSAMessage -- shutdownCSAMessage.object is the ConnectedSocketAdapter for socket that is closing.
        """
        connectedSocket = shutdownCSAMessage.object
        try:
            bundle=self.retrieveTrackedResourceInformation(connectedSocket)
        except KeyError:
            # This means we've actually already done this...
            return
        resourceInboxes,resourceOutboxes,(protocolHandler,controllink) = bundle

        self.connectedSockets = [ x for x in self.connectedSockets if x != self.connectedSockets ]

        self.unlink(thelinkage=controllink)

        self.send(socketShutdown(),resourceOutboxes[0]) # This is now instantly delivered
        self.send(shutdownMicroprocess(),resourceOutboxes[1]) # This is now instantly delivered

        self.removeChild(connectedSocket)
        self.removeChild(protocolHandler)
        self.deleteOutbox(resourceOutboxes[0]) # So this is now safe
                                               # This did not used to be the case.
        self.deleteOutbox(resourceOutboxes[1]) # So this is now safe
                                               # This did not used to be the case.
        self.ceaseTrackingResource(connectedSocket)

class SimpleServer(ServerCore):
    def __init__(self, **argd):
        super(SimpleServer, self).__init__(**argd)
    def mkProtocolHandler(self, **sock_info):
        return  (self.protocol)()

# To act as a crutch during getting ready for merge.
MoreComplexServer = ServerCore

__kamaelia_components__ = ( ServerCore, SimpleServer, )


if __name__ == '__main__':

    from Axon.Scheduler import scheduler
    class SimpleServerTestProtocol(Axon.Component.component):
        def __init__(self):
            super(SimpleServerTestProtocol, self).__init__()
            assert self.debugger.note("SimpleServerTestProtocol.__init__",1, "Starting test protocol")

        def mainBody(self):
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                print "Got data", data
                assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "NetServ : We were sent data - ")
                assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "We should probably do something with it now? :-)")
                assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "I know, let's sling it straight back at them :-)")
                self.send(data,"outbox")
            if self.dataReady("control"):
                data = self.recv("control")
                return 0
            return 1

        def closeDownComponent(self):
            assert self.debugger.note("SimpleServerTestProtocol.closeDownComponent",1, "Closing down test protcol")

    SimpleServer(protocol=SimpleServerTestProtocol).activate()
    scheduler.run.runThreads(slowmo=0)

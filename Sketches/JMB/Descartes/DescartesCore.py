import Axon
from Kamaelia.Internet.TCPServer import TCPServer
from Kamaelia.IPC import newCSA, shutdownCSA, socketShutdown, serverShutdown
from Axon.Ipc import newComponent, shutdownMicroprocess

class ServerCore(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """
    MoreComplexServer(protocol[,port]) -> new Simple protocol server component

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
            print self.__class__, self.__class__.protocol, self.protocol, protocol
            raise "Need a protocol to handle!"
        else:
            pass
            # print self.protocol

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
#        for CSA in self.connectedSockets:
#            self.handleClosedCSA(shutdownCSA(self,CSA))
#
#        self.send(serverShutdown(), "_serversignal")
#        print len(self.outboxes["_serversignal"])
#        print "Simple Server Shutting Down"

    def stop(self):
        for CSA in self.connectedSockets:
            self.handleClosedCSA(shutdownCSA(self,CSA))

        self.send(serverShutdown(), "_serversignal")
        super(SimpleServer, self).stop()

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

        protocolHandler = (self.protocol)(peer = peer,
                                          peerport = peerport,
                                          localip = localip,
                                          localport = localport)
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

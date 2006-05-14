#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Simple Server Chassis.

Provides a framework for creating generic protocol handlers to deal with
information coming in on a single port (and a single port only). This however
covers a large array of server types.

A protocol handler is simply a component that can receive and send data (as
byte strings) in a particular format and with a particular behaviour - ie.
conforming to a particular protocol. 

Provide this chassis with a factory function to create a component to
handle the protocol. Whenever a client connects a handler component will then be
created to handle communications with that client.



EXAMPLE USAGE : Simple echo protocol

Using a simple echo protocol, that just echoes back anything sent by the client:

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



HOW DOES IT WORK?

At initialisation the component registers a TCPServer component to listen for
new connections on the specified port.

You supply a factory function that takes no arguments and returns a new
protocol handler component.

When it receives a 'newCSA' message from the TCPServer (via the "_oobinfo"
inbox), the factory function is called to create a new protocol handler. The
protocol handler's "inbox" inbox and "outbox" outbox are wired to the
ConnectedSocketAdapter (CSA) component handling that socket connection, so it can
receive and send data.

If SingleServer receives a 'shutdownCSA' message (via "_oobinfo") then a
Kamaelia.KamaeliaIpc.socketShutdown message is sent to the protocol handler's
"control" inbox, and both it and the CSA are unwired.

In practice, this component provides no external connectors for your use.



HISTORY

This code is based on the code used for testing the Internet Connection
abstraction layer.



TODO

This component currently lacks an inbox and corresponding code to allow it to
be shut down (in a controlled fashion). Needs a "control" inbox that responds to
shutdownMicroprocess messages.
"""

import Axon as _Axon
from Axon import AxonObject as _AxonObject
import Kamaelia.Internet.TCPServer as _ic
import Kamaelia.KamaeliaIPC as _ki
import time as _time

class simpleServerProtocol(_Axon.Component.component):
    pass

class SimpleServer(_Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """
    SimpleServer(protocol[,port]) -> new Simple protocol server component

    A simple single port, multiple connection server, that instantiates a
    protocol handler component to handle each connection.

    Keyword arguments:
    protocol -- function that returns a protocol handler component
    port -- Port number to listen on for connections (default=1601)
    """
                    
    Inboxes = { "_oobinfo" : "internal use: Out Of Bounds Info - for receiving signalling of new and closing connections" }
    Outboxes = {}
    
    def __init__(self, protocol=None, port=1601):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SimpleServer, self).__init__()
        if not protocol:
            raise "Need a protocol to handle!"
        self.protocolhandlers = None
        self.protocolClass = protocol
        self.iter = 0
        self.time = _time.time()
        self.listenport = port
    
    def initialiseComponent(self):
        """Sets up socket binding to listen for incoming connections"""
        myPLS = _ic.TCPServer(listenport=self.listenport)
        self.link((myPLS,"protocolHandlerSignal"),(self,"_oobinfo"))
        self.addChildren(myPLS)
        return _Axon.Ipc.newComponent(myPLS)
    
    def mainBody(self):
        """Main loop"""
        self.pause()
        result = self.checkOOBInfo()
        if ((_time.time() - self.time) > 1):
            self.time = _time.time()
    
        self.iter = self.iter +1
        return 1
    
    def handleNewCSA(self, data):
        """
        handleNewCSA(data) -> Axon.Ipc.newComponent(protocol handler)
         
        Creates and returns a protocol handler for new connection.

        Keyword arguments:
        data -- data.object is the ConnectedSocketAdapter component for the connection
        """
        CSA = data.object
###        print "NEW CSA", CSA
        pHandler = self.protocolClass()
    
        pHandlerShutdownOutbox= self.addOutbox("protocolHandlerShutdownSignal")
        assert self.debugger.note("SimpleServer.handleNewCSA",5,"Allocated shutdown signal box", pHandlerShutdownOutbox)
    
        self.trackResourceInformation(CSA, [], [pHandlerShutdownOutbox], pHandler)
        assert self.debugger.note("SimpleServer.handleNewCSA",5, "tracking resource")
    
        self.addChildren(CSA,pHandler)
    
        self.link((CSA,"outbox"),(pHandler,"inbox"))
        self.link((pHandler,"outbox"),(CSA,"inbox"))
        self.link((self,pHandlerShutdownOutbox), (pHandler, "control"))
    
        if "signal" in pHandler.Outboxes:
            self.link((pHandler,"signal"),(CSA, "control"))
            _Axon.Foo = CSA
    
        CSA.activate()
        pHandler.activate()

    def handleClosedCSA(self,data):
        """
        handleClosedCSA(data) -> None
        
        Terminates and unwires the protocol handler for the closing socket.

        Keyword arguments:
        data -- data.object is the ConnectedSocketAdapter for socket that is closing.
        """
        assert self.debugger.note("SimpleServer.handleClosedCSA",1,"handling Closed CSA", data)
        CSA = data.object
        bundle=self.retrieveTrackedResourceInformation(CSA)
        inboxes,outboxes,pHandler = bundle
        self.send(_ki.socketShutdown(),outboxes[0])
        assert self.debugger.note("SimpleServer.handleClosedCSA",1,"Removing ", CSA.name, pHandler.name, outboxes[0])
        self.removeChild(CSA)
        self.removeChild(pHandler)
        self.deleteOutbox(outboxes[0])
        self.ceaseTrackingResource(CSA)
        assert self.debugger.note("SimpleServer.handleClosedCSA",5, "GRRR... ARRRGG")

    def checkOOBInfo(self):
        """Check and handle Out Of Bounds info - notifications of new and closed sockets."""
        while self.dataReady("_oobinfo"):
            data = self.recv("_oobinfo")
            if isinstance(data,_ki.newCSA):
                self.handleNewCSA(data)
            if isinstance(data,_ki.shutdownCSA):
                assert self.debugger.note("SimpleServer.checkOOBInfo", 1, "SimpleServer : Client closed itself down")
                self.handleClosedCSA(data)

__kamaelia_components__ = ( SimpleServer, )

                
if __name__ == '__main__':
    
    from Axon.Scheduler import scheduler
    class SimpleServerTestProtocol(simpleServerProtocol):
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

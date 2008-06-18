#!/usr/bin/python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Simple UDP components
=====================

These components provide simple support for sending and receiving UDP packets.



Example Usage
-------------

Send console input to port 1500 of myserver.com and receive packets locally on
port 1501 displaying their contents (and where they came from) on the console::
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.Internet.UDP import SimplePeer
    
    Pipeline( ConsoleReader(),
              SimplePeer("127.0.0.1", 1501, "myserver.com", 1500),
              ConsoleEchoer(),
            ).run()


Sends data from a data source as UDP packets, changing between 3 different
destinations, once per second::

    class DestinationSelector(component):
        def main(self):
            while 1:
                for dest in [ ("server1.com",1500),
                              ("server2.com",1500),
                              ("server3.com",1500), ]:
                    self.send(dest,"outbox")
                next=time.time()+1.0
                while time.time() < next:
                    yield 1
                    
    Graphline( \
        SOURCE = MyDataSource(),
        SELECT = DestinationSelector(),
        UDP    = TargettedPeer(),
        linkages = {
            ("SOURCE", "outbox") : ("UDP", "inbox"),
            ("SELECT", "outbox") : ("UDP", "target"),
        }
    ).run()

Send UDP packets containing "hello" to several different servers, all on port
1500::
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Internet.UDP import PostboxPeer
    
    Pipeline(
        DataSource( [ ("myserver1.com",1500,"hello"),
                      ("myserver2.com",1500,"hello"),
                      ("myserver3.com",1500,"hello"),
                    ]
                    ),
        PostboxPeer(),
    ).run()



Behaviour
---------

When any of these components receive a UDP packet on the local address and port
they are bound to; they send out a tuple (data,(host,port)) out of their
"outbox" outboxes. 'data' is a string containing the payload of the packet.
(host,port) is the address of the sender/originator of the packet.

SimplePeer is the simplest to use. Any data sent to its "inbox" inbox is sent
as a UDP packet to the destination (receiver) specified at initialisation.

TargettedPeer behaves identically to SimplePeer; however the destination
(receiver) it sends UDP packets to can be changed by sending a new (host,port)
tuple to its "target" inbox.

PostboxPeer does not have a fixed destination (receiver) to which it sends UDP
packets. Send (host,port,data) tuples to its "inbox" inbox to arrange for a UDP
packet containing the specified data to be sent to the specified (host,port).

None of these components terminate. They ignore any messages sent to their
"control" inbox and do not send anything out of their "signal" outbox.



Implementation Details
----------------------

SimplePeer, TargettedPeer and PostboxPeer are all derived from the base class
BasicPeer. BasicPeer provides some basic code for receiving from a socket.

Although technically BasicPeer is a component, it is not a usable one as it
does not implement a main() method.
"""

import socket
import errno
import Axon

from Kamaelia.Internet.Selector import Selector
from Kamaelia.IPC import newReader, newWriter
from Axon.Ipc import producerFinished, shutdownMicroprocess

class BasicPeer(Axon.Component.component):
    """\
    BasicPeer() -> new BasicPeer component.
    
    Base component from which others are derived in this module. Not properly
    functional on its own and so *should not be used* directly.
    """

    Inboxes  = { "inbox"      : "Data to sent to the socket",
                 "control"    : "Recieve shutdown messages",
                 "readReady"  : "Notify that there is incoming data ready on the socket",
                 "writeReady" : "Notify that the socket is ready to send"
                }

    Outboxes = { "outbox"          : "(data,(host,port)) tuples for each packet received",
                 "signal"          : "Signals receiver is shutting down",
                 "_selectorSignal" : "For communication to the selector"
               }

    def __init__(self):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(BasicPeer, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP)
        self.receiving = False
        self.sending = False
        # Send buffer is actually a [buffer, (address, port)] list so we can
        # keep track of where things are supposed to go if they don't get sent
        # succesfully first time
        self.sendBuffer = ["", ("0.0.0.0", 0)]

    def safeBind(self, target):
        """
        Bind the socket to the target address and port, handling errors
        gracefully
        
        Arguments:

        - target -- (address, port) tuple indicating where to bind
        """
        
        #FIXME: Binding should handle errors gracefully
        self.sock.bind(target)

    def setupSelector(self):
        """ Get the selector service, and ensure it is activated and linked """

        selectorService, selectorShutdownService, newSelector = Selector.getSelectorServices()
        if newSelector:
            newSelector.activate()

        # Link to the selector's "notify" inbox
        self.link((self, "_selectorSignal"), selectorService)

    def sendLoop(self, target):
        """
        Safely send any data stored in the send buffer or waiting on the
        "inbox" inbox

        Arguments:

        - target -- (address, port) tuple indicating where to send the data
        """
        while len(self.sendBuffer[0]) != 0 or self.dataReady("inbox"):
            if len(self.sendBuffer[0]) == 0:
                self.sendBuffer = [self.recv("inbox"), target]
            bytesSent = self.safeSend(*self.sendBuffer)
            self.sendBuffer[0] = self.sendBuffer[0][bytesSent:]
            if bytesSent == 0:
                # Failed to send right now, so resend it later
                break

    def safeSend(self, data, target):
        """
        Send data over the socket, handling errors gracefully

        Arguments:

        - data   -- the data to send over the socket
        - target -- (address, port) tuple indicating where to send the data
        """

        bytesSent = 0
        try:
            bytesSent = self.sock.sendto(data, target)
            return bytesSent
        except socket.error, socket.msg:
            (errorno, errmsg) = socket.msg.args
            if errorno == errno.AGAIN or errorno == errno.EWOULDBLOCK:
                self.send(newWriter(self, ((self, "writeReady"), self.sock)),
                          "_selectorSignal")
        self.sending = False
        return bytesSent

    def recvLoop(self):
        """
        Read any data available on the socket in chunks of 1024 bytes
        """

        data = True
        while data:
            data = self.safeRecv(1024)
            if data:
                self.send(data, "outbox")

    def safeRecv(self, size):
        """
        Read data from the socket, handling errors gracefully

        Arguments:

        - size -- The number of bytes of data to request from the socket
        """

        try:
            data = self.sock.recvfrom(size)
            if data:
                return data
        except socket.error, socket.msg:
            (errorno, errmsg) = socket.msg.args
            if errorno == errno.EAGAIN or errorno == errno.EWOULDBLOCK:
                self.send(newReader(self, ((self, "readReady"), self.sock)),
                         "_selectorSignal")
        self.receiving = False
        return None 
    
class UDPReceiver(BasicPeer):
    """\
    UDPReceiver([localaddr][,localport]) -> new UDPReceiver component.
    
    A simple component for receiving UDP packets. It binds to
    the specified local address and port - from which it will receive packets.
    Packets received are sent to it "outbox" outbox.
    
    Arguments:
    
    - localaddr      -- Optional. The local addresss (interface) to bind to. (default="0.0.0.0")
    - localport      -- Optional. The local port to bind to. (default=0)
    """    
    def __init__(self, localaddr="0.0.0.0", localport=0):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(UDPReceiver, self).__init__()
        self.local = (localaddr, localport)

    def main(self):
        """ Main loop """
        self.safeBind(self.local)
        # TODO: Find out if anything is likely to bite me when setting blocking
        self.sock.setblocking(0)

        self.setupSelector()
        yield 1
        self.send(newReader(self, ((self, "readReady"), self.sock)),
                   "_selectorSignal")

        while 1:
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    break

            if self.dataReady("readReady"):
                self.recv("readReady")
                self.receiving = True

            if self.receiving:
                self.recvLoop()
            if not self.anyReady():
                self.pause()
            yield 1

class UDPSender(BasicPeer):
    """\
    UDPSender([receiver_addr][,receiver_port]) -> new UDPSender component.
    
    A simple component for transmitting UDP packets. It sends packets received
    from the "inbox" inbox to a receiver on the specified address and port.
    
    Arguments:
    
    - receiver_addr  -- Optional. The address the receiver is bound to - to which packets will be sent. (default="0.0.0.0")
    - receiver_port  -- Optional. The port the receiver is bound on - to which packets will be sent. (default=0)
    """

    def __init__(self, receiver_addr="0.0.0.0", receiver_port=0):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(UDPSender, self).__init__()
        self.remote= (receiver_addr, receiver_port)

    def main(self):
        """ Main loop """
        self.sock.setblocking(0)
        self.setupSelector()
        yield 1
        self.send(newWriter(self, ((self, "writeReady"), self.sock)),
                  "_selectorSignal")

        shutdownOnEmptyBuffer = False
        while 1:
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    shutdownOnEmptyBuffer = True
                if isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    break

            # Make sure everything which could get sent does so before we
            # exit
            if shutdownOnEmptyBuffer:
                if (not self.dataReady("inbox") and
                    len(self.sendBuffer[0]) == 0):
                    self.send(producerFinished(), "signal")
                    break

            if self.dataReady("writeReady"):
                self.recv("writeReady")
                self.sending = True

            if self.sending:
                self.sendLoop(self.remote)

            # This line is sketchy.  I have a feeling it'll lead to never
            # pausing in certain circumstances.  So far it's not happened...
            if not shutdownOnEmptyBuffer:
                if (not self.anyReady() or
                    not (self.sending and len(self.sendBuffer[0]) != 0)):
                    self.pause()
            yield 1

class SimplePeer(BasicPeer):
    """\
    SimplePeer([localaddr][,localport][,receiver_addr][,receiver_port]) -> new SimplePeer component.
    
    A simple component for receiving and transmitting UDP packets. It binds to
    the specified local address and port - from which it will receive packets
    and sends packets to a receiver on the specified address and port.
    
    Arguments:
    
    - localaddr      -- Optional. The local addresss (interface) to bind to. (default="0.0.0.0")
    - localport      -- Optional. The local port to bind to. (default=0)
    - receiver_addr  -- Optional. The address the receiver is bound to - to which packets will be sent. (default="0.0.0.0")
    - receiver_port  -- Optional. The port the receiver is bound on - to which packets will be sent. (default=0)
    """

    def __init__(self, localaddr="0.0.0.0", localport=0,
                 receiver_addr="0.0.0.0", receiver_port=0):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(SimplePeer, self).__init__()
        self.local = (localaddr, localport)
        self.remote = (receiver_addr, receiver_port)

    def main(self):
        """ Main loop """
        self.safeBind(self.local)
        self.sock.setblocking(0)

        self.setupSelector()
        yield 1
        self.send(newWriter(self, ((self, "writeReady"), self.sock)),
                  "_selectorSignal")
        self.send(newReader(self, ((self, "readReady"), self.sock)),
                  "_selectorSignal")

        while 1:
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    break

            if self.dataReady("writeReady"):
                self.recv("writeReady")
                self.sending = True
            if self.dataReady("readReady"):
                self.recv("readReady")
                self.receiving = True

            if self.sending:
                self.sendLoop(self.remote)
            if self.receiving:
                self.recvLoop()

            if (not self.anyReady() or
                not (self.sending and len(self.sendBuffer[0]) != 0)):
                self.pause()
            yield 1

class TargettedPeer(BasicPeer):
    """\
    TargettedPeer([localaddr][,localport][,receiver_addr][,receiver_port]) -> new TargettedPeer component.
    
    A simple component for receiving and transmitting UDP packets. It binds to
    the specified local address and port - from which it will receive packets
    and sends packets to a receiver on the specified address and port.
    
    Can change where it is sending to by sending the new (addr,port) receiver
    address to the "target" inbox.
    
    Arguments:
    
    - localaddr      -- Optional. The local addresss (interface) to bind to. (default="0.0.0.0")
    - localport      -- Optional. The local port to bind to. (default=0)
    - receiver_addr  -- Optional. The address the receiver is bound to - to which packets will be sent. (default="0.0.0.0")
    - receiver_port  -- Optional. The port the receiver is bound on - to which packets will be sent. (default=0)
    """

    Inboxes  = { "inbox"      : "Data to sent to the socket",
                 "control"    : "Recieve shutdown messages",
                 "readReady"  : "Notify that there is incoming data ready on the socket",
                 "writeReady" : "Notify that the socket is ready to send",
                 "target"     : "Data receieved here changes the receiver addr/port data is tuple form: (host, port)",
               }

    Outboxes = { "outbox"          : "(data,(host,port)) tuples for each packet received",
                 "signal"          : "Signals receiver is shutting down",
                 "_selectorSignal" : "For communication to the selector",
               }

    def __init__(self, localaddr="0.0.0.0", localport=0,
                 receiver_addr="0.0.0.0", receiver_port=0):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(TargettedPeer, self).__init__()
        self.local = (localaddr, localport)
        self.remote = (receiver_addr, receiver_port)

    def main(self):
        """ Main loop """
        self.safeBind(self.local)
        self.sock.setblocking(0)

        self.setupSelector()
        yield 1
        self.send(newWriter(self, ((self, "writeReady"), self.sock)),
                  "_selectorSignal")
        self.send(newReader(self, ((self, "readReady"), self.sock)),
                  "_selectorSignal")

        while 1:
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    break

            if self.dataReady("target"):
                self.remote = self.recv("target")

            if self.dataReady("writeReady"):
                self.recv("writeReady")
                self.sending = True
            if self.dataReady("readReady"):
                self.recv("readReady")
                self.receiving = True

            if self.sending:
                self.sendLoop(self.remote)
            if self.receiving:
                self.recvLoop()

            if (not self.anyReady() or
                not (self.sending and len(self.sendBuffer[0]) != 0)):
                self.pause()
            yield 1

class PostboxPeer(BasicPeer):
    """\
    PostboxPeer([localaddr][,localport]) -> new PostboxPeer component.
    
    A simple component for receiving and transmitting UDP packets. It binds to
    the specified local address and port - from which it will receive packets.
    Sends packets to individually specified destinations
    
    Arguments:
    
    - localaddr      -- Optional. The local addresss (interface) to bind to. (default="0.0.0.0")
    - localport      -- Optional. The local port to bind to. (default=0)
    """

    def __init__(self, localaddr="0.0.0.0", localport=0):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(PostboxPeer, self).__init__()
        self.local = (localaddr, localport)

    def sendLoop(self):
        """
        Safely send any data stored in the send buffer or waiting on the
        "inbox" inbox
        """
        while len(self.sendBuffer[0]) != 0 or self.dataReady("inbox"):
            if len(self.sendBuffer[0]) == 0:
                receiverAddr, receiverPort, data = self.recv("inbox")
                self.sendBuffer = [data, (receiverAddr, receiverPort)]
            bytesSent = self.safeSend(*self.sendBuffer)
            self.sendBuffer[0] = self.sendBuffer[0][bytesSent:]
            if bytesSent == 0:
                # Failed to send right now, so resend it later
                break        

    def main(self):
        """ Main loop """
        self.safeBind(self.local)
        self.sock.setblocking(0)

        self.setupSelector()
        yield 1
        self.send(newWriter(self, ((self, "writeReady"), self.sock)),
                  "_selectorSignal")
        self.send(newReader(self, ((self, "readReady"), self.sock)),
                  "_selectorSignal")

        while 1:
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    break

            if self.dataReady("writeReady"):
                self.recv("writeReady")
                self.sending = True
            if self.dataReady("readReady"):
                self.recv("readReady")
                self.receiving = True

            if self.sending:
                self.sendLoop()
            if self.receiving:
                self.recvLoop()

            if (not self.anyReady() or
                not (self.sending and len(self.sendBuffer[0]) != 0)):
                self.pause()
            yield 1

__kamaelia_components__  = ( UDPSender, UDPReceiver, SimplePeer,
                             TargettedPeer, PostboxPeer, )

if __name__=="__main__":
    class DevNull(Axon.Component.component):
        def main(self):
            while 1:
                while self.dataReady():
                    self.recv()
                yield 1

    class ConfigChargen(Axon.Component.component):
       # This should probably be rolled back into Chargen.
       #  Since this is generally useful and a backwards compatible change.
       def __init__(self, message="Hello World"):
          super(Chargen, self).__init__()
          self.message = message
       def main(self):
          while 1:
             self.send(self.message, "outbox")
             yield 1

    class LineSepFilter(Axon.Component.component):
        # Should these changes be rolled into the console echoer?
        # In some respects they're both a pretext/posttext formatter
        # Call it a formatter? Require the format to take a single string?
        # Simple formatter?
        def __init__(self, pretext=""):
            super(LineSepFilter, self).__init__()
            self.pretext = pretext
        def main(self):
            while 1:
                while self.dataReady():
                   self.send(self.pretext + str(self.recv())+"\n")
                   yield 1
                self.pause()
                yield 1

    def SimplePeer_tests():
        from Axon.Scheduler import scheduler
        from Kamaelia.Util.Console import ConsoleEchoer
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.Chargen import Chargen

        server_addr = "127.0.0.1"
        server_port = 1600

        Pipeline(
            Chargen(),
            SimplePeer(receiver_addr=server_addr, receiver_port=server_port),
        ).activate()

        Pipeline(
            SimplePeer(localaddr=server_addr, localport=server_port),
            DevNull(),
#            ConsoleEchoer()
        ).run()

    def TargettedPeer_tests():
        from Axon.Scheduler import scheduler
        from Kamaelia.Util.Console import ConsoleEchoer
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.Chargen import Chargen
        from Kamaelia.Chassis.Graphline import Graphline

        server_addrs = [ 
                         ("127.0.0.1", 1600),
                         ("127.0.0.2", 1601),
                         ("127.0.0.3", 1602),
                         ("127.0.0.4", 1603),
                       ]

        for server_addr, server_port in server_addrs:
            Pipeline(
                SimplePeer(localaddr=server_addr, localport=server_port), # Simple Servers

                LineSepFilter("SERVER:"+server_addr+" :: "),
                ConsoleEchoer()
            ).activate()

        class TargetTesterSource(Axon.Component.component):
            Outboxes = [ "changetarget", "outbox" ]
            def __init__(self, targets):
                super(TargetTesterSource, self).__init__()
                self.targets = targets
            def main(self):
                while 1:
                    yield 1
                    for target in self.targets:
                        self.send(target, "changetarget")
                        for x in xrange(5):
                            self.send("HELLO ("+str(x)+") TO " + str(target), "outbox")

        Graphline(
            TESTSOURCE = TargetTesterSource(server_addrs),
            SENDER = TargettedPeer(localaddr="127.0.0.1"),
            linkages = {
                ( "TESTSOURCE", "changetarget") : ( "SENDER", "target"),
                ( "TESTSOURCE", "outbox") : ( "SENDER", "inbox"),
            }
        ).run()


    def PostboxPeer_tests():
        from Axon.Scheduler import scheduler
        from Kamaelia.Util.Console import ConsoleEchoer
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.Chargen import Chargen
        from Kamaelia.Chassis.Graphline import Graphline
        import random

        server_addrs = [
                         ("127.0.0.1", 1601),
                         ("127.0.0.2", 1602),
                         ("127.0.0.3", 1603),
                         ("127.0.0.4", 1604),
                       ]

        for server_addr, server_port in server_addrs:
            Pipeline(
                SimplePeer(localaddr=server_addr, localport=server_port), # Simple Servers
                LineSepFilter("SERVER:"+server_addr+" :: "),
                ConsoleEchoer()
            ).activate()

        class PostboxPeerSource(Axon.Component.component):
            def __init__(self, targets):
                super(PostboxPeerSource, self).__init__()
                self.targets = targets
            def main(self):
                while 1:
                    yield 1
                    target_addr, target_port = server_addrs[random.randint(0,3)]
                    data_to_send = "HELLO ! TO " + target_addr

                    message = ( target_addr, target_port, data_to_send )

                    self.send( message, "outbox")

        Pipeline(
            PostboxPeerSource(server_addrs),
            PostboxPeer(localaddr="127.0.0.1"),
        ).run()

    print "At present, UDP.py only has manually verified test suites."
    print "This does need recifying, but at present, this is what we have!"

    SimplePeer_tests()
#    TargettedPeer_tests()
#    PostboxPeer_tests()

# RELEASE: MH, MPS


#!/usr/bin/python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

*Note* that this components are deemed somewhat experimental.



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

#
# Experimental code, not to be moved into release tree without
# documentation. (Strictly not to be moved into release tree!)
#

import socket
import Axon

# ---------------------------- # SimplePeer
class BasicPeer(Axon.Component.component):
    """\
    BasicPeer() -> new BasicPeer component.
    
    Base component from which others are derived in this module. Not properly
    functional on its own and so *should not be used* directly.
    """
    
    Inboxes = { "inbox" : "NOT USED",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "(data,(host,port)) tuples for each packet received",
                 "signal" : "NOT USED",
               }
    
    def receive_packet(self, sock):
        """\
        Tries to receive from socket. Any data received is sent out of the 
        "outbox" outbox. Any socket errors are absorbed.
        
        Arguments:
    
        - sock  -- bound socket object to receive from
        """
        try:
            message = sock.recvfrom(1024)
        except socket.error, e:
            pass
        else:
            self.send(message,"outbox") # format ( data, addr )

 

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
    
    Inboxes = { "inbox" : "Raw binary string data packets to be sent to the destination (receiver host,port)",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "(data,(host,port)) tuples for each packet received",
                 "signal" : "NOT USED",
               }
    
    def __init__(self, localaddr="0.0.0.0", localport=0, receiver_addr="0.0.0.0", receiver_port=0):
        super(SimplePeer, self).__init__()
        self.localaddr = localaddr
        self.localport = localport
        self.receiver_addr = receiver_addr
        self.receiver_port = receiver_port

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.localaddr,self.localport))
        sock.setblocking(0)

        while 1:
            while self.dataReady("inbox"):
                data = self.recv()
                sent = sock.sendto(data, (self.receiver_addr, self.receiver_port) )
                yield 1

            self.receive_packet(sock)
            yield 1

# ---------------------------- # TargetedPeer
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
    Inboxes = {
        "inbox" : "Data recieved here is sent to the reciever addr/port",
        "target" : "Data receieved here changes the receiver addr/port data is tuple form: (host, port)",
        "control" : "Not listened to", # SMELL: This is actually a bug!
    }
    Outboxes = {
        "outbox" : "Data received on the socket is passed out here, form: (data,(host, port))",
        "signal" : "No data sent to", # SMELL: This is actually a bug!
    }
    def __init__(self, localaddr="0.0.0.0", localport=0, receiver_addr="0.0.0.0", receiver_port=0):
        super(TargettedPeer, self).__init__()
        self.localaddr = localaddr
        self.localport = localport
        self.receiver_addr = receiver_addr
        self.receiver_port = receiver_port

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.localaddr,self.localport))
        sock.setblocking(0)

        while 1:
            #
            # Simple Dispatch behaviour
            # 
            if self.dataReady("target"):
                addr, port = self.recv("target")
                self.receiver_addr = addr
                self.receiver_port = port

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                sock.sendto(data, (self.receiver_addr, self.receiver_port) );
                yield 1

            self.receive_packet(sock)
            yield 1


# ---------------------------- # PostboxPeer
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
    Inboxes = {
        "inbox" : "Send (host,port,data) tuples here to send a UDP packet to (host,port) containing data",
        "control" : "Not listened to", # SMELL: This is actually a bug!
    }
    Outboxes = {
        "outbox" : "Data received on the socket is passed out here, form: ((host, port), data)",
        "signal" : "No data sent to", # SMELL: This is actually a bug!
    }
    def __init__(self, localaddr="0.0.0.0", localport=0):
        super(PostboxPeer, self).__init__()
        self.localaddr = localaddr
        self.localport = localport

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.localaddr,self.localport))
        sock.setblocking(0)

        while 1:
            if self.dataReady("inbox"):
                receiver_addr, receiver_port, data = self.recv("inbox")
                sock.sendto(data, (receiver_addr, receiver_port) );
                yield 1
            self.receive_packet(sock)
            yield 1

__kamaelia_components__  = ( SimplePeer, TargettedPeer, PostboxPeer, )

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

# FIXME: Note the header!
# FIXME: Note the header!
# FIXME: Note the header!

# RELEASE: MH, MPS

#!/usr/bin/python
#
# Experimental code, not to be moved into release tree without
# documentation. (Strictly not to be moved into release tree!)
#

import socket
import Axon

# ---------------------------- # SimplePeer
class BasicPeer(Axon.Component.component):
    def receive_packet(self, sock):
            try:
                message = sock.recvfrom(1024)
            except socket.error, e:
                pass
            else:
                self.send(message,"outbox") # format ( data, addr )
 

class SimplePeer(BasicPeer):
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
    Inboxes = {
        "inbox" : "Data recieved here is sent to the reciever addr/port",
        "target" : "Data receieved here changes the receiver addr/port data is tuple form: (addr, port)",
        "control" : "Not listened to", # SMELL: This is actually a bug!
    }
    Outboxes = {
        "outbox" : "Data received on the socket is passed out here, form: ((addr, port), data)",
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
    A postbox peer recieves messages formed of 3 parts:
        (addr, port, data)

    The postbox peer then takes care of delivery of these UDP messages to the recipient.
    """
    Inboxes = {
        "inbox" : "Data recieved here is sent to the reciever addr/port",
        "control" : "Not listened to", # SMELL: This is actually a bug!
    }
    Outboxes = {
        "outbox" : "Data received on the socket is passed out here, form: ((addr, port), data)",
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

__kamaelia_components__  = ( BasicPeer, SimplePeer, TargettedPeer, PostboxPeer, )

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

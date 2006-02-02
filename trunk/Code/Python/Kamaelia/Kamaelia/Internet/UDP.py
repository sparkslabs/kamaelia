#!/usr/bin/python
#
# Experimental code, not to be moved into release tree without
# documentation. (Strictly not to be moved into release tree!)
#

import socket
import Axon

# ---------------------------- # SimplePeer
class SimplePeer(Axon.Component.component):
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
            if self.dataReady("inbox"):
                data = self.recv()
                sock.sendto(data, (self.receiver_addr, self.receiver_port) );
                yield 1

            try:
                data, addr = sock.recvfrom(1024)
            except socket.error, e:
                pass
            else:
                message = (addr, data) 
                self.send(message,"outbox")

            yield 1

# ---------------------------- # SimplePeer
class TargettedPeer(Axon.Component.component):
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
            #
            # Simple Transform behaviour
            #
            try:
                data, addr = sock.recvfrom(1024) # SMELL: UM look below (message!)
            except socket.error, e:
                pass
            else:
                message = (addr, data)           # SMELL: UM look above (data, addr)
                self.send(message,"outbox")
            yield 1


if __name__=="__main__":
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
        from Kamaelia.Util.PipelineComponent import pipeline
        from Kamaelia.Util.Chargen import Chargen

        server_addr = "127.0.0.1"
        server_port = 1600

        pipeline(
            Chargen(),
            SimplePeer(receiver_addr=server_addr, receiver_port=server_port),
        ).activate()

        pipeline(
            SimplePeer(localaddr=server_addr, localport=server_port),
            ConsoleEchoer()
        ).run()

    def TargettedPeer_tests():
        """Not finished"""
        from Axon.Scheduler import scheduler
        from Kamaelia.Util.Console import ConsoleEchoer
        from Kamaelia.Util.PipelineComponent import pipeline
        from Kamaelia.Util.Chargen import Chargen
        from Kamaelia.Util.Graphline import Graphline

        server_addrs = [ 
                         ("127.0.0.1", 1600),
                         ("127.0.0.2", 1601),
                         ("127.0.0.3", 1602),
                         ("127.0.0.4", 1603),
                       ]

        for server_addr, server_port in server_addrs:
            pipeline(
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

    print "At present, UDP.py only has manually verified test suites."
    print "This does need recifying, but at present, this is what we have!"

#    SimplePeer_tests()
    TargettedPeer_tests()

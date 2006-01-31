#!/usr/bin/python


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

def tests():
    from Axon.Scheduler import scheduler
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
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
        consoleEchoer()
    ).run()

if __name__=="__main__":
    tests()

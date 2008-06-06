import socket
import errno
import Axon

from Kamaelia.Internet.Selector import Selector
from Kamaelia.IPC import newReader, newWriter

class UDPReceiver(Axon.Component.component):
    Inboxes  = {"inbox"   : "NOT USED",
                "control"    : "Recieve shutdown messages",
                "ReadReady"  : "Receive messages indicating data is ready to be read from the socket"}

    Outboxes = {"outbox"          : "Data received from the socket",
                "signal"          : "Signals receiver is shutting down",
                "_selectorSignal" : "For communication to the selector"}

    def __init__(self, local_addr, local_port):
        super(UDPReceiver, self).__init__(self)
        self.local = (local_addr, local_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP)
        
    def main(self):
        #TODO: Binding should handle errors gracefully
        self.sock.bind(self.local)
        self.sock.setblocking(0)
        selectorService, selectorShutdownService, newSelector = Selector.getSelectorServices()
        if newSelector:
            newSelector.activate()
        yield 1

        # Link to the selector's "notify" inbox
        self.link((self, "_selectorSignal"), selectorService)
        self.send(newReader(self, ((self, "ReadReady"), self.sock)),
                   "_selectorSignal")

        # TODO: Make me shutdown nicely
        while 1:
            if self.dataReady("ReadReady"):
                self.recv("ReadReady")
                data = True
                while data:
                    data = self.safeRecv(1024)
                    if data:
                        self.send(data, "outbox")
            if not self.anyReady():
                self.pause()
            yield 1

    def safeRecv(self, size):
        try:
            data = self.sock.recvfrom(size)
            if data:
                return data
        except socket.error, socket.msg:
            (errorno, errmsg) = socket.msg.args
            if errorno == errno.EAGAIN or errorno == errno.EWOULDBLOCK:
                self.send(newReader(self, ((self, "ReadReady"), self.sock)),
                          "_selectorSignal")
        return None

class UDPSender(Axon.Component.component):
    def __init__(self, receiver_addr, receiver_port):
        super(UDPSender, self).__init__(self)
        self.receiver = (receiver_addr, receiver_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP)

    def main(self):
        selectorService, selectorShutdownService, newSelector = Selector.getSelectorServices()
        if newSelector:
            newSelector.activate()
        self.link((self, "_selectorSignal"), selectorService)
        self.send(newWriter(self, ((self, "WriteReady"), self.sock)),
                  "_selectorSignal")
        
        # TODO: Make me shutdown nicely
        while 1:
            #TODO: Write me :D
            pass
            

                    
if __name__ == "__main__":
    UDPReceiver("127.0.0.1", 2000).run()

import socket
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
        selectorServices = Selector.getSelectorServices()
        self.link((self, "_selectorSignal"), selectorServices[0])
        self.send(newReader((self, "ReadReady"), self.sock), "_selectorSignal")

        # TODO: Make me shutdown nicely
        while 1:
            if self.dataReady("ReadReady"):
                data = True
                while data:
                    data = self.safeRecv(1024)
                    if data:
                        print "data"
                        self.send(data, "outbox")
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
                self.send(newReader(self, "ReadReady"), self.sock)
        return None

                    
if __name__ == "__main__":
    UDPReceiver("127.0.0.1", 2000).run()

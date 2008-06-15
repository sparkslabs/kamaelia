import Axon

class UDPDistributor(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    def __init__(self):
        super(UDPDistributor, self).__init__()
        self.peers = []
        self.senders = {}
        self.acceptNewPeers = True

    def createSender(address, port):
        self.addOutbox("outbox_%s" % address)
        sender = UDPSender(remote_addr=address, remote_port=port).activate()
        self.link(self, "outbox_%s" % address, sender, "inbox")
        self.senders[address] = sender

    def sendPeerList(address, port):
        # Bit ugly - means we end up creating two UDP senders then destroying
        # one of them.  Maybe OK for now...
        p = Pipeline(OneShot(("/Jam/PeerList", self.peers)),
                     Osc(), UDPSender(address, port)).activate()


    def main():
        while 1:
            if self.dataReady("addPeer"):
                address, port = self.recv("addPeer")
                if self.acceptNewPeers:
                    self.peers.append((address, port))
                    self.createSender(address, port)
                    self.sendPeerList(address, port)
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                for peer in self.peers:
                    self.send(data, "outbox_%s" % peer[0])
            if not self.anyReady():
                self.pause()
            yield 1

                
                
            

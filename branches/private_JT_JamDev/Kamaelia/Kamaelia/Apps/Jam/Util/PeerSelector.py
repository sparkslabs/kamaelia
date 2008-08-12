import sets
import Axon

class PeerSelector(Axon.Component.component):
    Inboxes = {"inbox" : "",
               "control" : "",
               "addPeer" : "",
               "peerSet" : ""
              }
    def __init__(self, localport, localaddress=None):
        super(PeerSelector, self).__init__()
        self.peers = sets.Set()
        self.connectedTo = sets.Set()
        if localaddress:
            self.local = (localaddress, localport)
        else:
            self.local = localport

    def main(self):
        while 1:
            if self.dataReady("peerSet"):
                data = self.recv("peerSet")
                self.peers.update(data)
                self.sendConnectMessages()
                self.connectedTo.update(self.peers)
            if self.dataReady("addPeer"):
                data = self.recv("addPeer")
                self.peers.add(data)
                self.sendConnectMessages()
                self.connectedTo.update(self.peers)
            if not self.anyReady():
                self.pause()
            yield 1
                
    def sendConnectMessages(self):
        for peer in self.peers.difference(self.connectedTo):
            print "Sending connect message - %s:%s" % peer
            self.send((peer[0], peer[1], ("Connect", self.local)), "outbox")
                

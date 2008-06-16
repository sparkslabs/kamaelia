import Axon
import OSC

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Apps.Jam.Protocol.Osc import Osc
from Kamaelia.Apps.Jam.Internet.NewDP import UDPSender

class UDPDistributor(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes = {"inbox" : "",
               "control" : "",
               "addPeer" : "",
              }
    Outboxes = {"outbox" : "",
                "signal" : "",
               }
    def __init__(self):
        super(UDPDistributor, self).__init__()
        # List of peers needs to exist higher up the pipeline so we can use it
        # to connect to others (i.e. peer select widget).  Maybe a backplane
        # system?
        self.peers = []
        self.senders = {}
        self.acceptNewPeers = True

    def createSender(self, address, port):
        self.addOutbox("outbox_%s" % address)
        sender = UDPSender(receiver_addr=address, receiver_port=port).activate()
        self.link((self, "outbox_%s" % address), (sender, "inbox"))
        self.senders[address] = sender

    def sendPeerList(self, address, port):
        # FIXME: Ugly - manual creation of OSC bundle = not very Kamaelia-ific
        # Better to have a pipeline here with the OSC component in
        bundle = OSC.OSCBundle("/Jam/PeerList", 0)
        bundle.append(self.peers)
        self.send(bundle.getBinary(), "outbox_%s" % address)



    def main(self):
        while 1:
            if self.dataReady("addPeer"):
                address, port = self.recv("addPeer")
                if self.acceptNewPeers:
                    self.createSender(address, port)
                    self.sendPeerList(address, port)
                    self.peers.append((address, port))
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                for peer in self.peers:
                    self.send(data, "outbox_%s" % peer[0])
            if not self.anyReady():
                self.pause()
            yield 1


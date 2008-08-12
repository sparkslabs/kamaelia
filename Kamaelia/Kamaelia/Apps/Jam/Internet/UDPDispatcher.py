import sets
import Axon
import OSC

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Apps.Jam.Protocol.Osc import Osc
from Kamaelia.Internet.UDP_ng import UDPSender

class UDPDispatcher(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes = {"inbox" : "",
               "control" : "",
               "addPeer" : "",
               "peerSet" : "",
              }
    Outboxes = {"outbox" : "",
                "signal" : "",
               }
    def __init__(self):
        super(UDPDispatcher, self).__init__()
        self.peers = sets.Set()
        self.connectedPeers = sets.Set()
        self.senders = {}
        self.acceptNewPeers = True

    def createSender(self, address, port):
        """
        Create and connect a new UDPSender component pointing to the
        address and port supplied.
        """
        boxName = "outbox_%s_%s" % (address, port)
        self.addOutbox(boxName)
        sender = UDPSender(receiver_addr=address, receiver_port=port).activate()
        self.link((self, boxName), (sender, "inbox"))
        self.senders[address] = sender

    def sendPeerList(self, address, port):
        # FIXME: Ugly - manual creation of OSC bundle = not very Kamaelia-ific
        # Better to have a pipeline here with the OSC component in
        bundle = OSC.OSCBundle("/Jam/PeerList", 0)
        bundle.append(list(self.peers))
        self.send(bundle.getBinary(), "outbox_%s_%s" % (address, port))

    def main(self):
        while 1:
            if self.dataReady("addPeer"):
                address, port = self.recv("addPeer")
                if not (address, port) in self.connectedPeers:
                    if self.acceptNewPeers:
                        print "New peer connected - %s:%s" % (address, port)
                        # Create a new component to send messages to the
                        # peer
                        self.createSender(address, port)
                        # Send them the list of peers we are connected to
                        self.sendPeerList(address, port)
                        # Add them to our peer lists
                        self.peers.add((address, port))
                        self.connectedPeers.add((address, port))
            if self.dataReady("peerSet"):
                # Add any new peers we hear about to the peer list
                self.peers.update(self.recv("peerSet"))
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                # Send the data out to all of our peers
                for peer in self.peers:
                    self.send(data, "outbox_%s_%s" % peer)
            if not self.anyReady():
                self.pause()
            yield 1


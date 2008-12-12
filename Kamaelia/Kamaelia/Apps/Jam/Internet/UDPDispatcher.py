"""
==============
UDP Dispatcher
==============

A dispatcher which keeps a list off peers which are connected to us, and sends
any messages received on the "inbox" inbox to each of them.  The list of peers
is updated either by adding an individual (by sending an (address, port) tuple
to the "addPeer" inbox), or a group (by sending a python Set of (address, port)
tuples to the "peerSet" inbox.  When a message indicating a new peer has
connected the dispatcher immediately sends its peer set as an OSC message 
to the new peer, so they can connect to the rest of the network.

Example Usage
-------------

Send two OSC messages to port 2000 on hosts 127.0.0.1, 127.0.0.2 and 127.0.0.3

Graphline(data=dataSource(("/Hello", (1, 2, 3)), ("/World", (4, 5, 6)))
          osc=Osc(),
          ap=OneShot(("127.0.0.1", 2000)),
          ps=OneShot(sets.Set((("127.0.0.2", 2000), ("127.0.0.3", 2000)))),
          dispatcher = UDPDispatcher(),
          linkages={("data", "outbox"):("osc", "inbox"),
                    ("osc", "outbox"):("dispatcher", "inbox"),
                    ("ap", "outbox"):("dispatcher", "addPeer"),
                    ("ps", "outbox"):("dispatcher", "peerSet"),
                   }
         )

How it works
------------

When the component recieves a connection message from a new peer on the
"addPeer" inbox it creates a new outbox named "outbox_[address]_[port]".  It
then creates a new UDPSender component pointing at the address and port, and
connects the outbox to it.  It then send an OSC message (currently hard-coded
to /Jam/PeerList) containing a flattened list of address, port pairs as the OSC
arguments.  The (address, port) tuple is then added to the set of peers.

When a message is received on the "peerList" inbox the component updates its
peer set with the set received.  When a message is received on the "inbox"
inbox it is forwarded through the various "outbox" outboxes to send the
message to each peer.
"""

import sets
import Axon
import OSC

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Apps.Jam.Protocol.Osc import Osc
from Kamaelia.Internet.UDP_ng import UDPSender

class UDPDispatcher(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """
    UDPDispatcher() -> new UDPDispatcher component

    Distribute messages recieved on the "inbox" inbox to an updatable list
    of peers.
    """
    Inboxes = {"inbox" : "Data to send to the peers",
               "control" : "NOT USED", # FIXME
               "addPeer" : "Data for new peers connecting to us",
               "peerSet" : "Lists of peers sent from people we are connected to",
              }
    Outboxes = {"outbox" : "NOT USED",
                "signal" : "NOT USED", #FIXME
               }
    def __init__(self):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """
        super(UDPDispatcher, self).__init__()
        self.peers = sets.Set()
        self.senders = {}

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
        """
        Send a list of the currently connected peers as an OSC message to
        the supplied address and port
        """
        # FIXME: Ugly - manual creation of OSC bundle = not very Kamaelia-ific
        # Better to have a pipeline here with the OSC component in
        # Should be Jam (and maybe OSC) independant too
        bundle = OSC.OSCBundle("/Jam/PeerList", 0)
        bundle.append(list(self.peers))
        self.send(bundle.getBinary(), "outbox_%s_%s" % (address, port))

    def main(self):
        """ Main loop """
        while 1:
            if self.dataReady("addPeer"):
                address, port = self.recv("addPeer")
                if not (address, port) in self.peers:
                    print "New peer connected - %s:%s" % (address, port)
                    # Create a new component to send messages to the
                    # peer
                    self.createSender(address, port)
                    # Send them the list of peers we are connected to
                    self.sendPeerList(address, port)
                    # Add them to our peer lists
                    self.peers.add((address, port))
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


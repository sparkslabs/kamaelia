"""
============
PeerSelector
============

Sends connection requests to any new peers supplied by messages on the
"addPeer" and "peerSet" inbox.  Send (address, port) pairs to the "addPeer"
inbox, or a set of (address, port) pairs to the "peerSet" inbox to send new
connect messages to new peers.

Connect messages are sent from the "outbox" outbox in the form of
(address, port, ("Connect", localData)), where localData is either a port, or
an (address, port) tuple if an address argument is given on construction.

Example Usage
-------------

Send OSC connect messages to ports 2000, and 2001 on the local machine.  Note
that although port 2000 is added twice it will only receive one connect message.

Graphline(osc=Osc(),
          ap=OneShot(("127.0.0.1", 2000)),
          ps=OneShot(sets.Set((("127.0.0.1", 2000), ("127.0.0.3", 2001)))),
          peerSelector=PeerSelector(),
          osc = Osc(index=2),
          postboxPeer = PostboxPeer(),
          linkages={("ap", "outbox"):("peerSelector", "addPeer"),
                    ("ps", "outbox"):("peerSelector", "peerSet"),
                    ("peerSelector", "outbox"):("osc", "inbox"),
                    ("osc", "outbox"):("postboxPeer", "inbox")}).run()
"""
import sets
import Axon

class PeerSelector(Axon.Component.component):
    """
    PeerSelector(localport, [localaddress]) -> new PeerSelector component

    Send connect messages to an updatable group of peers

    Arguments:
    - localport -- The port to inform the peer to send messages to
    - localaddress -- The address to inform the peer to send messages to (optional)
    """

    Inboxes = {"inbox" : "NOT USED",
               "control" : "NOT USED", #FIXME
               "addPeer" : "Send a connect message to a new peer if we are not already connected",
               "peerSet" : "Send a connect message to a set of peers if we are not connected to them"
              }

    def __init__(self, localport, localaddress=None):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """ 
        super(PeerSelector, self).__init__()
        self.peers = sets.Set()
        if localaddress:
            self.local = (localaddress, localport)
        else:
            self.local = localport

    def main(self):
        """ Main loop """
        while 1:
            if self.dataReady("peerSet"):
                data = self.recv("peerSet")
                for address, port in data.difference(self.peers):
                    self.sendConnectMessage(address, port)
                self.peers.update(data)
            if self.dataReady("addPeer"):
                data = self.recv("addPeer")
                if data not in self.peers:
                    self.sendConnectMessage(*data)
                    self.peers.add(data)
            if not self.anyReady():
                self.pause()
            yield 1
                
    def sendConnectMessage(self, address, port):
        """ Send a connect message to a peer at a given address and port """
        print "Sending connect message - %s:%s" % (address, port)
        self.send((address, port, ("Connect", self.local)), "outbox")
                

# -*- coding: utf-8 -*-
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sets
import Axon
import OSC

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Apps.Jam.Protocol.Osc import Osc
from Kamaelia.Apps.Jam.Internet.UDP_ng import UDPSender

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
                        self.createSender(address, port)
                        self.sendPeerList(address, port)
                        self.peers.add((address, port))
                        self.connectedPeers.add((address, port))
            if self.dataReady("peerSet"):
                self.peers.update(self.recv("peerSet"))
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                for peer in self.peers:
                    self.send(data, "outbox_%s_%s" % peer)
            if not self.anyReady():
                self.pause()
            yield 1


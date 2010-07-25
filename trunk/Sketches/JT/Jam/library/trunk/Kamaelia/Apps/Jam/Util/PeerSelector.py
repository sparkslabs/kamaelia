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
                

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
        selectorService, selectorShutdownService, newSelector = Selector.getSelectorServices()
        if newSelector:
            newSelector.activate()
        yield 1
        

        self.link((self, "_selectorSignal"), selectorService)
        self.send(newReader(self, ((self, "ReadReady"), self.sock)), "_selectorSignal")
      
        # TODO: Make me shutdown nicely
        while 1:
            if self.dataReady("ReadReady"):
#            if 1:
                data = True
                while data:
                    data = self.safeRecv(1024)
                    if data:
                        print "data", repr(data)
                        self.send(data, "outbox")
            else:
                print newSelector
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

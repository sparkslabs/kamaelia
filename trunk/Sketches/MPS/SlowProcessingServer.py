#!/usr/bin/python

import socket, time, copy
import Axon
from Kamaelia.Chassis.ConnectedServer import MoreComplexServer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient

class SlowProcessingServer(MoreComplexServer):
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    class protocol(Axon.Component.component):
        def main(self):
            i = 0
            t = time.time()
            self.setInboxSize("inbox", 1)
            while 1:
                if time.time() -t > 2:
                    if self.dataReady("inbox"):
                        t = time.time()
                        i += 1
                        d = self.recv("inbox")
                        x = d.find(".")
                        j = copy.copy(d)
                        j = j.replace(".","")
                        j = j.replace("\r\n","")
                        self.send("Thanks for :"+repr(j)+":  d:"+str(len(d))+"\r\n", "outbox")
                yield 1

class ImpatientClient(Axon.Component.component):
    request = ".........................................\r\n"*100000
    def main(self):
        t =time.time()
        i = 0
        while 1:
#            if time.time() - t >1:
            if 1:
                t = time.time()
                i = i +1
                print "sending to server", i, len(self.request)
                self.send(str(i) + self.request ,"outbox")
            while self.dataReady("inbox"):
                print "response from server: "+ str(self.recv("inbox"))
            yield 1

if 0:
    Graphline(
        IC = ImpatientClient(),
        TCPC = TCPClient("127.0.0.1", 1601),
        linkages = {
            ("IC","outbox"): ("TCPC","inbox"),
            ("TCPC","outbox"): ("IC","inbox"),
        }
    ).activate()

SlowProcessingServer().run()

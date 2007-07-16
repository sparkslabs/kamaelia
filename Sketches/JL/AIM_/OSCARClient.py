#! /usr/bin/env python

import md5
import struct
#from oscarutil import *
import pickle
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess

class OSCARProtocol(component):
    Inboxes = {"inbox" : "receives messages, usually from TCP",
               "control" : "shutdown handling",
               "SNAC" : "SNACs to be sent out to AIM. Takes data in the format ((family, subtype), data)",
               "strings" : "strings to be sent out to AIM. Takes data in the format (channel, data)"
               }

    Outboxes = {"outbox" : "sends messages to AIM, usually via TCP",
                "signal" : "shutdown handling", 
                "channel1" : "channel1",
                "channel2" : "channel2",
                "channel3" : "channel3",
                "channel4" : "channel4",
                "channel5" : "channel5",
                }
    
    def __init__(self):
        super(OSCARProtocol, self).__init__()
        self.seqnum = 0
        self.done = False

    def main(self):
        while not self.done:
            yield 1
            self.checkBoxes()

    def checkBoxes(self):
        for box in self.Inboxes:
            if self.dataReady(box):
                cmd = "self.handle%s()" % box
                exec(cmd)

    def handleinbox(self):
        data = self.recv("inbox")
        header = '!cBHH'
        while data:
            a, chan, seqnum, datalen = struct.unpack(header, data[:6])
            assert len(data) >= 6+datalen
            flapbody = data[6:6+datalen]
            self.send(flapbody, "channel%i" % chan)
            data = data[6+datalen:]

    def handlecontrol(self):
        data = self.recv("control")
        self.done = True
        self.send(shutdownMicroprocess(), "signal")

    def handleSNAC(self):
        data = self.recv("SNAC")
        snac = self.makeSNAC(*data)
        self.sendFLAP(snac)

    def handlestrings(self):
        chan, data = self.recv("strings")
        self.sendFLAP(data, chan)

    #most of method definition from Twisted's oscar.py
    def makeSNAC(self, (fam, sub), data, flags=[0,0], id=1): #currently id never changes
        header="!HHBBL"
        head=struct.pack(header,fam,sub,
                         flags[0],flags[1],
                         id)
        return head+str(data)

    #most of method definition from Twisted's oscar.py
    def sendFLAP(self,data,channel = 0x02):
        header="!cBHH"
        self.seqnum=(self.seqnum+1)%0x10000
        seqnum=self.seqnum
        head=struct.pack(header,'*', channel,
                         seqnum, len(data))
        self.send(head+str(data))


from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient

def OSCARClient(server, port):
    return Graphline(oscar = OSCARProtocol(),
                     tcp = TCPClient(server, port),
                     linkages = {
                         ("oscar", "outbox") : ("tcp", "inbox"),
                         ("tcp", "outbox") : ("oscar", "inbox"),
                         ("oscar", "signal") : ("tcp", "control"),

                         ("oscar", "signal") : ("tcp", "control"),

                         ("self", "snac") : ("oscar", "SNAC"),
                         ("self", "strings") : ("oscar", "strings"),
                         ("self", "control") : ("oscar", "control"),
                         ("oscar", "channel1") : ("self", "channel1"),
                         ("oscar", "channel2") : ("self", "channel2"),
                         ("oscar", "channel3") : ("self", "channel3"),
                         ("oscar", "channel4") : ("self", "channel4"),
                         ("oscar", "channel5") : ("self", "channel5"),
                         ("tcp", "signal") : ("self", "signal"),
                         }
                     )

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer
    
    proto = OSCARProtocol()
    flap = '*\x03\x00\x01\x00\x08flapbody' * 5
    proto._deliver(flap, "inbox")

    def unpack(data):
        fmt = '!%iB' % len(data)
        return struct.unpack(fmt, data)
    
    Graphline(proto = proto,
              pure = PureTransformer(unpack),
              echo = ConsoleEchoer(),
              linkages = {("proto", "channel3") : ("pure", "inbox"),
                          ("pure", "outbox") : ("echo", "inbox"),
                          }
              ).run()

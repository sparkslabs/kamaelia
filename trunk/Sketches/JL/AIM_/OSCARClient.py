#! /usr/bin/env python

import md5
import struct
#from oscarutil import *
import pickle
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess

class OSCARProtocol(component):
    Inboxes = {"inbox" : "receives messages, usually from TCP",
               "control" : "NOTHING",
               "SNAC" : "SNACs to be sent out to AIM. Takes data in the format ((family, subtype), data)",
               "strings" : "strings to be sent out to AIM. Takes data in the format (channel, data)"
               }

    Outboxes = {"outbox" : "sends messages to AIM, usually via TCP",
                "signal" : "NOTHING",
                "heard" : "Everything it hears, after processing",
                }
    
    def __init__(self):
        super(OSCARProtocol, self).__init__()
        self.seqnum = 0

    def main(self):
        while True:
            yield 1
            self.checkBoxes()

    def checkBoxes(self):
        for box in self.Inboxes:
            if self.dataReady(box):
                cmd = "self.handle%s()" % box
                exec(cmd)

    def handleinbox(self):
        data = self.recv("inbox")
        self.send(data, "heard")

    def handlecontrol(self):
        data = self.recv("control")

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

def OSCARClient():
    return Graphline(oscar = OSCARProtocol(),
                     tcp = TCPClient('login.oscar.aol.com', 5190),
                     linkages = {
                         ("oscar", "outbox") : ("tcp", "inbox"),
                         ("tcp", "outbox") : ("oscar", "inbox"),
                         ("oscar", "signal") : ("tcp", "control"),

                         ("oscar", "signal") : ("tcp", "control"),

                         ("self", "snac") : ("oscar", "SNAC"),
                         ("self", "strings") : ("oscar", "strings"),
                         ("self", "control") : ("oscar", "control"),
                         ("oscar", "heard") : ("self", "outbox"),
                         ("tcp", "signal") : ("self", "signal"),
                         }
                     )

if __name__ == '__main__':
    OSCARClient().run() #shouldn't do anything except make sure the code passes the barest of requirements

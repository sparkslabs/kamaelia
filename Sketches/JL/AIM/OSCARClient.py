import md5
import struct
#from oscarutil import *
import pickle
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess

class OSCARClient(component):
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
        super(OSCARClient, self).__init__()
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
        snac = self.makeSnac(*data)
        self.sendFlap(snac)

    def handlestrings(self):
        chan, data = self.recv("strings")
        self.sendFlap(data, chan)

    #most of method definition from Twisted's oscar.py
    def makeSNAC((fam, sub), data, flags=[0,0], id=1): #currently id never changes
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
Graphline(oscar = OSCARClient(),
          tcp = TCPClient('login.oscar.aol.com', 5190),
          linkages = {("oscar", "outbox") : ("tcp", "inbox"),
                      ("tcp", "outbox") : ("oscar", "inbox"),

                      ("oscar", "signal") : ("tcp", "control"),
                      }
          ).run()
          

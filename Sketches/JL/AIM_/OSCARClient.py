#! /usr/bin/env python

import struct
from oscarutil import *
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess

FLAP_HEADER_LEN = 6
class OSCARProtocol(component):
    Inboxes = {"inbox" : "receives messages, usually from TCP",
               "control" : "shutdown handling",
               "talk" : "(channel, FLAP payload)",
               }

    Outboxes = {"outbox" : "sends messages to AIM, usually via TCP",
                "signal" : "shutdown handling", 
                "heard" : "(channel, FLAP payload)",
                }
    
    def __init__(self):
        super(OSCARProtocol, self).__init__()
        self.seqnum = 0
        self.done = False

    def main(self):
        """main loop"""
        while not self.done:
            yield 1
            self.checkBoxes()

    def checkBoxes(self):
        """checks for data in all our boxes, and if there is data, then call the appropriate function
        to handle it."""
        for box in self.Inboxes:
            if self.dataReady(box):
                cmd = "self.handle%s()" % box
                exec(cmd)

    def handleinbox(self):
        """receives data coming in through the wire, reformats it into Kamaelia-and-Python-friendly forms,
        and retransmits it to its "heard" outbox."""
        data = self.recv("inbox")
        head = '!cBHH'
        while data:
            a, chan, seqnum, datalen = struct.unpack(head, data[:FLAP_HEADER_LEN])
            assert len(data) >= 6+datalen
            flapbody = data[FLAP_HEADER_LEN:FLAP_HEADER_LEN+datalen]
            self.send((chan, flapbody), "heard")  
            data = data[FLAP_HEADER_LEN+datalen:]

    def handlecontrol(self):
        data = self.recv("control")
        self.done = True
        self.send(shutdownMicroprocess(), "signal")

    def handletalk(self):
        """handles messages coming into the "talk" inbox. Expects FLAP data in the format (channel, flap body).
        If incoming messages are not in this format, we raise an error. 
        If they are in the correct format, then this method constructs the FLAPs and sends them."""
        data = self.recv("talk")
        assert len(data) == 2 #we want to call this to the developer's attention if the format of things coming into "talk" isn't right.
        assert type(data[0]) == type(1)
        self.sendFLAP(data[1], data[0])

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

                         ("self", "inbox") : ("oscar", "talk"),
                         ("oscar", "heard") : ("self", "outbox"),
                         ("self", "control") : ("oscar", "control"),
                         ("tcp", "signal") : ("self", "signal"),
                         }
                     )
    
class SNACExchanger(component):
    def __init__(self):
        super(SNACExchanger, self).__init__()
        debugSections = {"SNACExchanger.recvSnac" : 0,
                         "SNACExchanger.sendSnac" : 0,
                         }
        self.debugger.addDebug(**debugSections)
        
    def sendSnac(self, fam, sub, body):
        snac = self.makeSnac(fam, sub, body)
        self.send((CHANNEL_SNAC, snac))
        assert self.debugger.note("SNACExchanger.sendSnac", 5, "sent SNAC " + str((fam, sub)))

    def recvSnac(self):
        recvdflap = self.recv() #supported services snac
        data = readSNAC(recvdflap[1])
        assert len(data) == 2
        header, reply = data
        assert self.debugger.note("SNACExchanger.recvSnac", 5, "received SNAC" + str(header))
        return header, reply

    def waitSnac(self, fam, sub):
        done = False
        while not done:
            while not self.dataReady():
                yield 1
            header, reply = self.recvSnac()
            if header[0] == fam and header[1] == sub:
                yield reply
                done = True

    def makeSnac(self, fam,sub,data,id=1, flags=[0,0]):
        #the reqid mostly doesn't matter, unless this is a query-response situation 
        return Double(fam) + Double(sub) + Single(flags[0]) + Single(flags[1]) + Quad(id) + data



if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Chassis.Pipeline import Pipeline
    server = 'localhost'
    port = 5190

    class Terminator(component):
        def main(self):
            for i in range(10):
                print i
                self.send((i, "hi i am a string"))
                yield 1            
            self.send(shutdownMicroprocess(), "signal")

    Pipeline(Terminator(), OSCARClient(server,port)).run()
    print "Pipeline finished"

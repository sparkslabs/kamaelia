#! /usr/bin/env python

import struct
from oscarutil import *
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess

class OSCARProtocol(component):
    """\
    OSCARProtocol() -> new OSCARProtocol component.

    Provides a Kamaelia interface to the lowest level of OSCAR protocol, the FLAP level.
    """
    Inboxes = {"inbox" : "receives binary data from the AIM server",
               "control" : "shutdown handling",
               "talk" : "receives messages in the format (channel, FLAP payload)",
               }

    Outboxes = {"outbox" : "sends binary data to the AIM server.",
                "signal" : "shutdown handling", 
                "heard" : "resends messages from 'outbox' in the form (channel, FLAP payload)",
                }
    
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(OSCARProtocol, self).__init__()
        self.seqnum = 0
        self.done = False

    def main(self):
        """main loop"""
        while not self.done:
            yield 1
            self.checkBoxes()

    def checkBoxes(self):
        """checks for data in all our boxes, and if there is data, then call the
        appropriate function to handle it."""
        for box in self.Inboxes:
            if self.dataReady(box):
                cmd = "self.handle%s()" % box
                exec(cmd)

    def handleinbox(self):
        """receives data coming in through the wire, reformats it into
        Kamaelia-and-Python-friendly forms, and retransmits it to its "heard" outbox."""
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
        """checks that incoming messages from the "talk" inbox are in the form
        (channel, flap data). If not, exceptions are raised. If so,
        OSCARProtocol.sendFLAP is called. """
        data = self.recv("talk")
        assert len(data) == 2 #we want to call this to the developer's attention if the format of things coming into "talk" isn't right.
        assert type(data[0]) == type(1)
        self.sendFLAP(data[1], data[0])

    #most of method definition from Twisted's oscar.py
    def sendFLAP(self,data,channel = 0x02):
        """constructs FLAPs and sends them"""
        header="!cBHH"
        self.seqnum=(self.seqnum+1)%0x10000
        seqnum=self.seqnum
        head=struct.pack(header,'*', channel,
                         seqnum, len(data))
        self.send(head+str(data))


from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient

def OSCARClient(server, port):
    """\
    OSCARClient(server, port) -> returns an OSCARProtocol component connected to
    a TCPClient.

    User input goes into OSCARClient's "inbox" in the form (channel, flap body)
    and useable output comes out of "outbox" in the same form. 
    """
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
    """\
    SNACExchanger() -> component that has methods specialized for sending and
    receiving FLAPs over Channel 2 (FLAPs whose payloads are SNACs).

    ======================
    About SNACs
    ======================
    
    Many times the payload of a FLAP is a SNAC, which has a structure of its own:

    |------------------------|
    |SNAC-header             |
    |  Family -- 2 bytes     |
    |  Subtype -- 2 bytes    |
    |  Request ID -- 2 bytes |
    |  Flags -- 4 bytes      |
    |------------------------
    |  --------------        |
    | | SNAC payload |       |
    |  --------------        |
    |------------------------|

    
    FLAP channel 2 is reserved for SNACs. All SNAC payloads must follow a
    prescribed format, a format unique to each particular type, but all SNAC
    headers follow the format described above. Each different (family, subtype)
    performs a different function. For example, family 0x04, subtype 0x07, 
    (04, 07), carries AIM messages from the server to the client. 
    """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SNACExchanger, self).__init__()
        debugSections = {"SNACExchanger.recvSnac" : 0,
                         "SNACExchanger.sendSnac" : 0,
                         }
        self.debugger.addDebug(**debugSections)
        
    def sendSnac(self, fam, sub, body):
        """constructs a SNAC by calling self.makeSnac and sends it out the "outbox"."""
        snac = self.makeSnac(fam, sub, body)
        self.send((CHANNEL_SNAC, snac))
        assert self.debugger.note("SNACExchanger.sendSnac", 5, "sent SNAC " + str((fam, sub)))

    def recvSnac(self):
        """receives FLAPs and parses the SNAC data."""
        recvdflap = self.recv() #supported services snac
        data = readSNAC(recvdflap[1])
        assert len(data) == 2
        header, reply = data
        assert self.debugger.note("SNACExchanger.recvSnac", 5, "received SNAC" + str(header))
        return header, reply

    def waitSnac(self, fam, sub):
        """wait for a particular SNAC"""
        done = False
        while not done:
            while not self.dataReady():
                yield 1
            header, reply = self.recvSnac()
            if header[0] == fam and header[1] == sub:
                yield reply
                done = True

    def makeSnac(self, fam,sub,data,id=1, flags=[0,0]):
        """actually constructs the SNAC"""
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

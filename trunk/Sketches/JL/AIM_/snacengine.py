#! /usr/bin/env python
import pickle
import socket
import struct
from oscarutil import *
from Axon.Component import component
from Axon.Ipc import WaitComplete, shutdownMicroprocess
from Kamaelia.Internet.TCPClient import TCPClient

CHANNEL_SNAC = 2

class SNACEngine(component):
    """specialized component for sending sequences of SNACs. Standard inbox/outboxes. Base class.\
    'inbox' is for communicating with AIM, via OSCARClient or OSCARProtocol."""
    def __init__(self):
        super(SNACEngine, self).__init__()
        self.waiting = {}
        debugSections = {"SNACEngine.main" : 5,
                         "SNACEngine.handleAIMMessage" : 5,
                         }
        self.debugger.addDebug(**debugSections)

    def main(self):
        """stub method, to be overwritten"""
        pass 

    def sendout(self, (fam, sub), s_body, waitfor=None, sendback=None, postrecv=None):
        """waitfor is the (fam, sub) of the anticipated response. sendback is the (fam, sub)\
        of the response SNAC, while postrecv is the function \
        the returned SNAC body is run through. If postrecv(self, snacbody) returns a value,
        then that value is
        sent as the SNAC body. If not, then an empty SNAC is sent."""
        self.sendSNAC(fam, sub, s_body)
        if waitfor:
            self.putwait(waitfor, sendback, postrecv)

    def sendSNAC(self, fam, sub, s_body):
        self.send((CHANNEL_SNAC, SNAC(fam, sub, s_body)))

    def putwait(self, famsub, sendback, postrecv):
        self.waiting[famsub] = (sendback, postrecv or (lambda self, x: None))

    def handleAIMMessage(self, flapbody):
        """when a SNAC from OSCARProtocol is received, this method checks to see if the
        SNAC is one we have been waiting for. If so, we then apply the stored method to the response.
        Then we check if we should send a reply back to the server. If so, then we SNACify the
        result of the postrecv function and send it back to the server. """
        s_header, s_body = readSNAC(flapbody)
        sendbackData= self.waiting.get((s_header[0], s_header[1]))
        if sendbackData:
            sendback, postrecv = sendbackData
            reply_s_body = postrecv(self, s_body)
            if sendback:
                self.sendSNAC(sendback[0], sendback[1], reply_s_body)


class ServerEmulator(component):
    def main(self):
        prefix = '/home/jlei/aim/snacs/'
        for name in ['0103', '0118', '0113', '0107']:
            yield 1
            data = open(prefix+name).read()
            self.send(data)


class ProtocolNegotiator(SNACEngine):
    def main(self):
        yield 1
        standardResponse = (lambda self, x: "SNACEngine response")
        def setServiceVersions(self, x):
            self.serviceVersions = x
        self.putwait((0x01, 0x03), (0x01, 0x17), standardResponse)
        self.putwait((0x01, 0x18), None, setServiceVersions)
        self.putwait((0x01, 0x13), None, None)
        self.putwait((0x01, 0x07), (0x01, 0x08), standardResponse)        
        while True:
            yield 1
            if self.dataReady():
                data = self.recv()
                self.handleAIMMessage(data[1])
        
            
if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
    from OSCARClient import OSCARClient, OSCARProtocol
    client = Graphline(oscar = OSCARProtocol(),
                     tcp = ServerEmulator(),
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
    
    Pipeline(client, ProtocolNegotiator(), ConsoleEchoer()).run()

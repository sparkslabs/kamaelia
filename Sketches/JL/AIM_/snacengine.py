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
            del(self.waiting[(s_header[0], s_header[1])])


class ServerEmulator(component):
    def main(self):
        prefix = '/home/jlei/aim/snacs/'
        for name in ['0103', '0118', '0113', '0107']:
            yield 1
            data = open(prefix+name).read()
            self.send(data)


#define functions that SNACEngine will use
def setServiceVersions(self, reply):
        reply = unpackDoubles(reply)
        self.acceptedServices = dict(zip(reply[::2], reply[1::2]))

def makeVersionRequest(self, reply):
    desiredServiceVersions = {0x01 : 3,
                               0x02 : 1,
                               0x03 : 1,
                               0x04 : 1,
                               0x08 : 1,
                               0x09 : 1,
                               0x0a : 1,
                               0x0b : 1,
                               0x13 : 4,
                               0x15 : 1,
                               }

    supportedFamilies = unpackDoubles(reply)
    data = ""
    for family in supportedFamilies:
        if family in desiredServiceVersions:
            data += Double(family) + Double(desiredServiceVersions[family])
        self.putwait((0x01, 0x18), None, setServiceVersions)
    return data

def parseRates(self, reply):
    def parseRateInfoChunk(chunk, versionNumber=1):
        """returns a tuple (rate class : {rate class info}) for each string
        representing the info for one rate class. Imperfect."""
        tup = struct.unpack("!H8iB", chunk)
        d = {"window size" : tup[1],
             "clear level" : tup[2],
             "alert level" : tup[3],
             "limit level" : tup[4],
             "disconnect level" : tup[5],
             "current level" : tup[6],
             "max level" : tup[7],
             }
        if versionNumber != 2:
            d["last time"] = tup[8]
            d["current state"] = tup[9]

        return (tup[0], d)

    def parseRateInfo(data, numClasses):
        """saves to self.rateInfo a dict with rate class numbers as the keys and dictionaries containing their info as values."""
        rates = {}
        for i in range(numClasses):
            chunk = parseRateInfoChunk(data[i*LEN_RATE_CLASS : (i+1)*LEN_RATE_CLASS])
            rates[chunk[0]] = chunk[1]
        self.rateInfo = rates
        
    numClasses, = struct.unpack('!H', reply[:2])
    parseRateInfo(reply[2:], numClasses)
    snac_body = struct.pack("!%iH" % numClasses, *self.rateInfo.keys())
    return snac_body

    
class ProtocolNegotiator(SNACEngine):
    def main(self):
        self.putwait((0x01, 0x03), (0x01, 0x17), makeVersionRequest)
        self.putwait((0x01, 0x13), None, None)
        self.sendout((0x01, 0x06), "",
                     waitfor=(0x01, 0x07),
                     sendback=(0x01, 0x08),
                     postrecv=parseRates)
        while len(self.waiting):
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
    pn = ProtocolNegotiator()
    
    Pipeline(client, pn, ConsoleEchoer()).run()

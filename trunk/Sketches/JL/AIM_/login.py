#! /usr/bin/env python

import pickle
import struct
from oscarutil import *
from Axon.Component import component
from Axon.Ipc import WaitComplete, shutdownMicroprocess
from snacengine import SNACEngine, ServerEmulator

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
    def __init__(self, authCookie, versionNumber=1):
        super(ProtocolNegotiator, self).__init__()
        self.versionNumber = versionNumber
        self.authCookie = authCookie

    def main(self):
        for _ in self.connect(): yield 1
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

    def connect(self):
        data = struct.pack('!i', self.versionNumber)
        data += TLV(0x06, self.authCookie)
        self.send((CHANNEL_NEWCONNECTION, data))
        while not self.dataReady():
            yield 1
        serverAck = self.recv()
        assert serverAck[0] == 1

if __name__ == '__main__':
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
    pn = ProtocolNegotiator("AUTHORIZATIONCOOKEEEE")
    
    Pipeline(client, pn, ConsoleEchoer()).run()


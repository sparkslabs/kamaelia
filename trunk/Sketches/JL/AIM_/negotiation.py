#! /usr/bin/env python

import pickle
import socket
import struct
from oscarutil import *
from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import WaitComplete, shutdownMicroprocess
from Kamaelia.Internet.TCPClient import TCPClient


CLIENT_ID_STRING = "Kamaelia/AIM"
CHANNEL_NEWCONNECTION = 1
CHANNEL_SNAC = 2
CHANNEL_FLAPERROR = 3
CHANNEL_CLOSECONNECTION = 4
CHANNEL_KEEPALIVE = 5
LEN_RATE_CLASS = 2 + 8*4 + 1
        
class ProtocolNegotiator(component):
    def __init__(self, authCookie, versionNumber=1):
        super(ProtocolNegotiator, self).__init__()
        self.versionNumber = versionNumber
        self.authCookie = authCookie
        self.desiredServiceVersions = {0x01 : 3,
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
        self.debugger.addDebugSection("ProtocolNegotiator.main", 5)

    
    def main(self):
        #new connection 
        data = struct.pack('!i', self.versionNumber)
        data += TLV(0x06, self.authCookie)
        self.send((CHANNEL1, data))
        assert self.debugger.note("ProtocolNegotiator.main", 5, "sent handshake 1")
        while not self.dataReady():
            yield 1
        recvdflap = self.recv()
        assert self.debugger.note("ProtocolNegotiator.main", 5, "received FLAP " + str(recvdflap[0]))

        #get supported services
        while not self.dataReady():
            yield 1
        recvdflap = self.recv() #supported services snac
        header, reply = readSNAC(recvdflap[1])
        assert self.debugger.note("ProtocolNegotiator.main", 5, "received SNAC" + str(header))
        supportedFamilies = struct.unpack("!%iH" % (len(reply)/2), reply)

        #request service versions
        data = ""
        for family in supportedFamilies:
            if family in self.desiredServiceVersions:
                data += Double(family) + Double(self.desiredServiceVersions[family])
        self.send((CHANNEL_SNAC, SNAC(0x01, 0x17, data)))

        #get and process accepted versions
        while not self.dataReady():
            yield 1
        recvdflap = self.recv() #accepted services snac
        header, reply = readSNAC(recvdflap[1])
        assert self.debugger.note("ProtocolNegotiator.main", 5, "received SNAC" + str(header))
        reply = unpackDoubles(reply)
        self.acceptedServices = dict(zip(reply[::2], reply[1::2]))
        assert self.debugger.note("ProtocolNegotiator.main", 5, "accepted " + str(self.acceptedServices))

        #get motd
        while not self.dataReady():
            yield 1
        reply = self.recv() #motd snac
        assert self.debugger.note("ProtocolNegotiator.main", 5, "received motd")
        
        #request rate limits
        self.send((CHANNEL_SNAC, SNAC(0x01, 0x06, "", id=2)))
        while not self.dataReady():
            yield 1
        recvflap = self.recv() #rate limits
        header, reply = readSNAC(recvflap[1])
        assert self.debugger.note("ProtocolNegotiator.main", 5, "received SNAC" + str(header))

        #process rate limits
        numClasses, = struct.unpack('!H', reply[:2])
        self.parseRateInfo(reply[2:], numClasses)
##        reply = reply[2 + numClasses*LEN_RATE_CLASS:]
##        self.parseRateGroups(reply)

        snac_body = struct.pack("!%iH" % numClasses, *self.rateInfo.keys())
        self.send((CHANNEL_SNAC, SNAC(0x01, 0x08, snac_body)))
        self.send(shutdownMicroprocess(), "signal")
        
    def handshake(self):
        data = struct.pack('!i', self.versionNumber)
        data += TLV(0x06, self.authCookie)
        self.send((CHANNEL1, data))
        while not self.dataReady():
            yield False
        reply = self.recv() #should be server ack of new connection
        yield readSNAC(reply[1])
        
    def parseRateInfoChunk(self, chunk):
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
        if self.versionNumber != 2:
            d["last time"] = tup[8]
            d["current state"] = tup[9]

        return (tup[0], d)

    def parseRateInfo(self, data, numClasses):
        """saves to self.rateInfo a dict with rate class numbers as the keys and dictionaries containing their info as values."""
        rates = {}
        for i in range(numClasses):
            chunk = self.parseRateInfoChunk(data[i*LEN_RATE_CLASS : (i+1)*LEN_RATE_CLASS])
            rates[chunk[0]] = chunk[1]
        self.rateInfo = rates

    def parseRateGroups(self, data):
        """adds lists of the SNACS governed by each rate class to self.rateInfo"""
        while data:
            print len(data) 
            gid, numPairs = struct.unpack("HH", data[:4])
            pairs = struct.unpack("!%ii" % numPairs, data[4 : 4 + 4*numPairs])
            pairs = zip(pairs[::2], pairs[1::2])
            self.rateInfo[gid]["group"] = pairs
            data = data[4 + 4*numPairs:]
                              

if __name__ == '__main__':        
    from Kamaelia.Chassis.Graphline import Graphline
    from OSCARClient import OSCARClient
    import sys
    import os
    sys.path.append('..')
    from likefile import *
    from gen import AuthCookieGetter
    import pickle

    g = \
    Graphline(auth = AuthCookieGetter(),
              oscar = OSCARClient('login.oscar.aol.com', 5190),
              linkages = {("auth", "outbox") : ("oscar", "inbox"),
                          ("oscar", "outbox") : ("auth", "inbox"),
                          ("auth", "signal") : ("oscar", "control"),
                          ("auth", "_cookie") : ("self", "outbox"),
                          }
              ) 

    background = schedulerThread(slowmo=0.01).start()
    h = LikeFile(g)
    h.activate()
    BOS_server, port, auth_cookie = h.get()

    Graphline(ambassador = ProtocolNegotiator(auth_cookie),
              oscar = OSCARClient(BOS_server, port),
              linkages = {("ambassador", "outbox") : ("oscar", "inbox"),
                          ("oscar", "outbox") : ("ambassador", "inbox"),
                          ("ambassador", "signal") : ("oscar", "control"),
                          }
              ).run()

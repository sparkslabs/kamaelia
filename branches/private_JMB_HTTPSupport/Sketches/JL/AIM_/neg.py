#! /usr/bin/env python
from oscarutil import *
from Axon.Component import component
import time

screenname = 'ukelele94720'
password = '123abc'
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
        debugSections = {"ProtocolNegotiator.main" : 5,
                         "ProtocolNegotiator.recvSnac" : 5,
                         }
        self.debugger.addDebug(**debugSections)

    def sendSnac(self, fam, sub, body):
        snac = SNAC(fam, sub, body)
        self.send((CHANNEL_SNAC, snac))

    def recvSnac(self):
        recvdflap = self.recv() #supported services snac
        header, reply = readSNAC(recvdflap[1])
        assert self.debugger.note("ProtocolNegotiator.recvSnac", 5, "received SNAC" + str(header))
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
            

    def main(self):
        yield Axon.Ipc.WaitComplete(self.connect())
        yield Axon.Ipc.WaitComplete(self.setServiceVersions())
        yield Axon.Ipc.WaitComplete(self.getRateLimits())
        self.requestRights()
        yield Axon.Ipc.WaitComplete(self.getRights())
        assert self.debugger.note("ProtocolNegotiator.main", 5, "rights gotten, calling self.activateConnection()")
        self.activateConnection()
        yield 1
        
    def parseRateInfo(self, data, numClasses):
        return '\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05'

    def connect(self):
        data = struct.pack('!i', self.versionNumber)
        data += TLV(0x06, self.authCookie)
        self.send((CHANNEL_NEWCONNECTION, data))
        while not self.dataReady():
            yield 1
        serverAck = self.recv()
        assert serverAck[0] == CHANNEL_NEWCONNECTION

    def setServiceVersions(self):
        #get supported services
        for reply in self.waitSnac(0x01, 0x03): yield 1

        #request service versions
        supportedFamilies = struct.unpack("!%iH" % (len(reply)/2), reply)
        data = ""
        for family in supportedFamilies:
            if family in self.desiredServiceVersions:
                data += Double(family) + Double(self.desiredServiceVersions[family])
        self.sendSnac(0x01, 0x17, data)

        #get and process accepted versions
        for reply in self.waitSnac(0x01, 0x18): yield 1
        reply = unpackDoubles(reply)
        self.acceptedServices = dict(zip(reply[::2], reply[1::2]))
        assert self.debugger.note("ProtocolNegotiator.main", 5, "accepted " + str(self.acceptedServices))

    def getRateLimits(self):
        #request rate limits
        self.sendSnac(0x01, 0x06, "")
        for reply in self.waitSnac(0x01, 0x07): yield 1
        
        #process rate limits
        numClasses, = struct.unpack('!H', reply[:2])
        ack = self.parseRateInfo(reply[2:], numClasses)

        #ack to server
        self.sendSnac(0x01, 0x08, ack)

    def requestRights(self):
        self.sendSnac(0x01, 0x0e, "")
        self.sendSnac(0x13, 0x02, "")
        self.sendSnac(0x13, 0x04, "")
        self.sendSnac(0x02, 0x02, "")
        self.sendSnac(0x03, 0x02, "")
        self.sendSnac(0x04, 0x04, "")
        self.sendSnac(0x09, 0x02, "")
        
    def getRights(self):
        doNothing = (lambda x: None)
        expecting = {(0x01, 0x0f) : doNothing,
                     (0x13, 0x03) : doNothing,
                     (0x13, 0x06) : doNothing,
                     (0x02, 0x03) : doNothing,
                     (0x03, 0x03) : doNothing,
                     (0x04, 0x05) : doNothing,
                     (0x09, 0x03) : doNothing,
                    }
        done = False
        while not done and len(expecting):
            while not self.dataReady():
                yield 1
            header, reply = self.recvSnac()
            if (header[0], header[1]) in expecting.keys():
                del(expecting[(header[0], header[1])])
            else:
                done = True
        assert self.debugger.note("ProtocolNegotiator.main", 5, "last reply: " + str((header[0], header[1])))
                                  

    def activateConnection(self):
        """send some parameters up to the server, then signal that we're ready to begin receiving data"""
        #tell server our capabilities -- which at this point is nothing
        capabilities = TLV(0x05, "")
        self.sendSnac(0x02, 0x04, capabilities)

        #tell server we're done editing SSI data
        self.sendSnac(0x13, 0x12, "")

        #activate SSI data
        self.sendSnac(0x13, 0x07, "")

        #send up our status
        STATUS_DCDISABLED = 0x0100
        STATUS_ONLINE = 0x0000
        userStatus = TLV(0x06, struct.pack("!HH", STATUS_DCDISABLED, STATUS_ONLINE))
        self.sendSnac(0x01, 0x1e, userStatus)

        #now we're ready to begin receiving data
        body = ""
        for service, version in self.desiredServiceVersions.items():
            data = struct.pack("!HHi", service, version, 0x01100629)
            body += data
        self.sendSnac(0x01, 0x02, body)        
        
if __name__ == '__main__':
    from OSCARClient import OSCARClient
    from Kamaelia.Chassis.Graphline import Graphline
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

    

#! /usr/bin/env python
from oscarutil import *
from Axon.Component import component
from OSCARClient import OSCARClient, SNACExchanger
import time
import Axon

class LoginHandler(SNACExchanger):
    def __init__(self,screenname, password, versionNumber=1):
        super(LoginHandler, self).__init__()
        self.screenname = screenname
        self.password = password
        self.versionNumber = versionNumber
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
        self.client_id = 0x0109 #this value seems to work
        self.major_version = 0
        self.minor_version = 1
        self.lesser_version = 0
        self.build_num = 42
        self.distr_num = 0
        self.language = 'en'
        self.country = 'us'
        self.use_SSI = 1

        self.oscar = OSCARClient('login.oscar.aol.com', 5190).activate()
        self.link((self, "outbox"), (self.oscar, "inbox"))
        self.link((self.oscar, "outbox"), (self, "inbox"))

        debugSections = {"LoginHandler.main" : 5,
                         "LoginHandler.connectAuth" : 5,
                         "LoginHandler.reconnect" : 5,
                         }
        self.debugger.addDebug(**debugSections)


    def main(self):
        yield Axon.Ipc.WaitComplete(self.getBOSandCookie())
        yield Axon.Ipc.WaitComplete(self.negotiateProtocol())

    def getBOSandCookie(self):
        yield Axon.Ipc.WaitComplete(self.connectAuth())
        for reply in self.getCookie(): yield 1
        goal = self.extractBOSandCookie(reply)
        assert self.debugger.note("Loginhandler.main", 1, "Got cookie!")
        
    def negotiateProtocol(self):
        yield Axon.Ipc.WaitComplete(self.reconnect(self.server, self.port, self.cookie))
        yield Axon.Ipc.WaitComplete(self.setServiceVersions())
        yield Axon.Ipc.WaitComplete(self.getRateLimits())
        self.requestRights()
        yield Axon.Ipc.WaitComplete(self.getRights())
        assert self.debugger.note("LoginHandler.main", 5, "rights gotten, activating connection")
        self.activateConnection()
        yield 1

    def connectAuth(self):
        assert self.debugger.note("LoginHandler.connectAuth", 7, "sending new connection...")
        data = struct.pack('!i', self.versionNumber)
        self.send((CHANNEL_NEWCONNECTION, data))
        while not self.dataReady():
            yield 1
        reply = self.recv() #should be server ack of new connection
        assert self.debugger.note("LoginHandler.connectAuth", 5, "received new connection ack")

    def getCookie(self):
        #request and get MD5 key from server
        zero = struct.pack('!H', 0)
        request = TLV(0x01, self.screenname) + TLV(0x4b, zero) + TLV(0x5a, zero)
        self.sendSnac(0x17, 0x06, request)
        for reply in self.waitSnac(0x17, 0x07): yield 1
        assert self.debugger.note("AuthCookieGetter.main", 5, "received md5 key")
        md5key = reply[2:]

        #using MD5 key, request and get BOS server, port and authorization cookie
        request = TLV(0x01, self.screenname) +\
                  TLV(0x25, encryptPasswordMD5(self.password, md5key)) +\
                  TLV(0x4c, "") +\
                  TLV(0x03, CLIENT_ID_STRING) +\
                  TLV(0x16, Double(self.client_id)) +\
                  TLV(0x17, Double(self.major_version)) +\
                  TLV(0x18, Double(self.minor_version)) +\
                  TLV(0x19, Double(self.lesser_version)) +\
                  TLV(0x1a, Double(self.build_num)) +\
                  TLV(0x14, Quad(self.distr_num)) +\
                  TLV(0x0f, self.language) +\
                  TLV(0x0e, self.country) +\
                  TLV(0x4a, Single(self.use_SSI))
        self.sendSnac(0x17, 0x02, request)
        for reply in self.waitSnac(0x17, 0x03): yield 1
        assert self.debugger.note("AuthCookieGetter.main", 5, "received BOS/auth cookie")
        while not self.dataReady():
            yield 1
        recvdflap = self.recv()
        assert recvdflap[0] == 4 #close connection command
        yield reply

    def extractBOSandCookie(self, reply):  
        parsed = readTLVs(reply)
        assert parsed.has_key(0x05)
        BOS_server = parsed[0x05]
        BOS_server, port = BOS_server.split(':')
        port = int(port)    
        auth_cookie = parsed[0x06]
        self.server, self.port, self.cookie = BOS_server, port, auth_cookie

    def reconnect(self, server, port, cookie):
        self.unlink(self.oscar)
        self.oscar = OSCARClient(server, port).activate()
        self.link((self, "outbox"), (self.oscar, "inbox"))
        self.link((self.oscar, "outbox"), (self, "inbox"))
        yield 1
        assert self.debugger.note("LoginHandler.reconnect", 7, "linked, linked, and unlinked")
        
        data = Quad(self.versionNumber)
        data += TLV(0x06, cookie)
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
        assert self.debugger.note("LoginHandler.main", 5, "accepted " + str(self.acceptedServices))

    def parseRateInfo(self, data, numClasses):
        return '\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05'

    def getRateLimits(self):
        #request rate limits
        self.sendSnac(0x01, 0x06, "")
        for reply in self.waitSnac(0x01, 0x07): yield 1
        assert self.debugger.note("LoginHandler.main", 7, "parsing rate info...")
        
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
        assert self.debugger.note("LoginHandler.main", 5, "last reply: " + str((header[0], header[1])))
                                  

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
        assert self.debugger.note("LoginHandler.main", 5, "sent CLI_READY")

        
if __name__ == '__main__':
    screenname = 'ukelele94720'
    password = '123abc'

    LoginHandler(screenname, password).run()


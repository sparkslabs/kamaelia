#!/usr/bin/env python

import pickle
import md5
from Axon.Component import component
from Axon.Ipc import WaitComplete, ipc
from OSCARClient import OSCARClient
from oscarutil import *

screenname = 'ukelele94720'
password = '123abc'
CLIENT_ID_STRING = "Kamaelia/AIM"
CHANNEL_NEWCONNECTION = 1
CHANNEL_SNAC = 2
CHANNEL_FLAPERROR = 3
CHANNEL_CLOSECONNECTION = 4
CHANNEL_KEEPALIVE = 5

class AuthCookieGetter(component):
    Outboxes = {"outbox" : "outgoing messages to AIM",
                "signal" : "NOT USED",
                "_cookie" : "(BOS server, port, cookie)",
                }
                
    
    def __init__(self):
        super(AuthCookieGetter, self).__init__()
        self.versionNumber = 1
        self.debugger.addDebugSection("AuthCookieGetter.main", 5)
        
    def main(self):
        yield WaitComplete(self.connect())
        for md5key in self.getMD5key(): yield 1
        for reply in self.getBOSandAuthCookie(md5key): yield 1
        goal = self.extractBOSandCookie(reply)
        self.send(goal, "_cookie")
        assert self.debugger.note("AuthCookieGetter.main", 1, str(goal))
        
    def connect(self):
        data = struct.pack('!i', self.versionNumber)
        self.send((CHANNEL_NEWCONNECTION, data))
        while not self.dataReady():
            yield 1
        reply = self.recv() #should be server ack of new connection
        assert self.debugger.note("AuthCookieGetter.main", 5, "received new connection ack")

    def getMD5key(self):
        zero = struct.pack('!H', 0)
        snac_body = ""
        snac_body += TLV(0x01, screenname)
        snac_body += TLV(0x4b, zero)
        snac_body += TLV(0x5a, zero)
        self.send((CHANNEL_SNAC, SNAC(0x17, 0x06, snac_body)))
        # get md5 key
        while not self.dataReady():
            yield 1
        reply = self.recv() #snac (17, 07)
        snac = readSNAC(reply[1])
        assert self.debugger.note("AuthCookieGetter.main", 5, "received md5 key")
        yield snac[1][2:]

    def getBOSandAuthCookie(self, md5key):
        snac_body = ""
        snac_body += TLV(0x01, screenname)

        ### Digest password ###
        md5obj = md5.new()
        md5obj.update(md5key)
        md5obj.update(md5.new(password).digest())
        md5obj.update(AIM_MD5_STRING)
        password_hash = md5obj.digest()
        snac_body += TLV(0x25, password_hash)

        snac_body += TLV(0x4c, "")
        snac_body += TLV(0x03, CLIENT_ID_STRING)

        client_id = 0x0109 #this value seems to work
        snac_body += TLV(0x16, Double(client_id))

        major_version = 5
        snac_body += TLV(0x17, Double(major_version))

        minor_version = 1
        snac_body += TLV(0x18, Double(minor_version))

        lesser_version = 0
        snac_body += TLV(0x19, Double(lesser_version))

        build_num = 3036
        snac_body += TLV(0x1a, Double(build_num))

        distr_num = 0
        snac_body += TLV(0x14, Quad(distr_num))

        language = 'en'
        snac_body += TLV(0x0f, language)

        country = 'us'
        snac_body += TLV(0x0e, country)

        ssiflag = 1
        snac_body += TLV(0x4a, Single(ssiflag))
        self.send((CHANNEL_SNAC, SNAC(0x17, 0x02, snac_body)))
        
        while not self.dataReady():
            yield 1
        reply = self.recv()
        assert self.debugger.note("AuthCookieGetter.main", 5, "received BOS/auth cookie")
        yield reply[1]

    def extractBOSandCookie(self, data):  
        snac = readSNAC(data)
        parsed = readTLVs(snac[1])
        assert parsed.has_key(0x05)
        BOS_server = parsed[0x05]
        BOS_server, port = BOS_server.split(':')
        port = int(port)    
        auth_cookie = parsed[0x06]
        return BOS_server, port, auth_cookie



if __name__ == '__main__':
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer

    Graphline(auth = AuthCookieGetter(),
              oscar = OSCARClient('login.oscar.aol.com', 5190),
              cons = ConsoleEchoer(),
              linkages = {("auth", "outbox") : ("oscar", "inbox"),
                          ("oscar", "outbox") : ("auth", "inbox"),
                          ("auth", "signal") : ("oscar", "control"),
                          ("auth", "_cookie") : ("cons", "inbox"),
                          }
              ).run()
              

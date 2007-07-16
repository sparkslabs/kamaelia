#!/usr/bin/env python

import pickle
import md5
from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, WaitComplete, ipc
from OSCARClient import OSCARClient
from oscarutil import *

screenname = 'kamaelia1'
password = 'abc123'
CLIENT_ID_STRING = "KamaeliaAIM/0.01"

class AuthCookieGetter(component):
    Outboxes = {"outbox" : "the only thing that comes out is the auth cookie and BOS server",
                "strings" : "non-snac requests to AIM",
                "snac" : "snacs to go out to AIM",
                "signal" : "shutdown handling",
                }
    
    def __init__(self):
        super(AuthCookieGetter, self).__init__()
        self.versionNumber = 1
        self.debugger.addDebugSection("AuthCookieGetter.main", 5)
        
    def main(self):
        yield WaitComplete(self.handshake())
        for value in self.getMD5key():
            if value == 1: yield value
            else: md5key = value
        for value in self.getBOSandAuthCookie(md5key):
            if value == 1: yield value
            else: reply = value
            
        #save data, in case we need it for debugging later
        fle = open("snac1703.dat", "wb")
        pickle.dump(reply, fle)
        fle.close()
        snac_body = reply[FLAP_HEADER_LEN+SNAC_HEADER_LEN:]
        parsed = readTLVs(snac_body)
        BOS_server = parsed[0x05]
        BOS_server, port = BOS_server.split(':')
        port = int(port)    
        auth_cookie = parsed[0x06]
        self.send((BOS_server, port, auth_cookie))
        self.send(shutdownMicroprocess(), "signal")
    
    def handshake(self):
        data = struct.pack('!i', self.versionNumber)
        self.send((CHANNEL1, data), "strings")
        while not self.dataReady("inbox"):
            yield 1
        reply = self.recv() #should be server ack of new connection
        assert self.debugger.note("AuthCookieGetter.main", 5, "received new connection ack")

    def getMD5key(self):
        zero = struct.pack('!H', 0)
        snac_body = ""
        snac_body += TLV(0x01, screenname)
        snac_body += TLV(0x4b, zero)
        snac_body += TLV(0x5a, zero)
        self.send(((0x17, 0x06), snac_body), "snac")
        # get md5 key
        while not self.dataReady("inbox"):
            yield 1
        reply = self.recv()
        assert self.debugger.note("AuthCookieGetter.main", 5, "received md5 key")
        md5key = reply[18:]
        yield md5key

    def getBOSandAuthCookie(self, md5key):
        snac_body = ""
        snac_body += TLV(0x01, screenname)
        snac_body += TLV(0x03, CLIENT_ID_STRING)

        ### Digest password ###
        md5obj = md5.new()
        md5obj.update(md5key)
        md5obj.update(password)
        md5obj.update(AIM_MD5_STRING)
        password_hash = md5obj.digest()
        snac_body += TLV(0x25, password_hash)

        client_id = 0x0109 #this value seems to work
        snac_body += TLV(0x16, Double(client_id))

        major_version = 0
        snac_body += TLV(0x17, Double(major_version))

        minor_version = 0
        snac_body += TLV(0x18, Double(minor_version))

        lesser_version = 1
        snac_body += TLV(0x19, Double(lesser_version))

        build_num = 1
        snac_body += TLV(0x1a, Double(build_num))

        distr_num = 0
        snac_body += TLV(0x14, Double(distr_num))

        language = 'en'
        snac_body += TLV(0x0f, language)

        country = 'us'
        snac_body += TLV(0x0e, country)

        ssiflag = 1
        snac_body += TLV(0x4a, Single(ssiflag))
        self.send(((0x17, 0x02), snac_body), "snac")
        
        while not self.dataReady("inbox"):
            yield 1
        reply = self.recv()
        assert self.debugger.note("AuthCookieGetter.main", 5, "received BOS/auth cookie")
        yield reply


from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer

Graphline(auth = AuthCookieGetter(),
          oscar = OSCARClient(),
          echo = ConsoleEchoer(),
          linkages = {("auth", "strings") : ("oscar", "strings"),
                      ("auth", "snac") : ("oscar", "snac"),
                      ("oscar", "outbox") : ("auth", "inbox"),
                      ("auth", "outbox") : ("echo", "inbox"),
                      ("auth", "signal") : ("oscar", "control"),
                      }
          ).run()
          

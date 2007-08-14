#! /usr/bin/env python
##
## (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
##     All Rights Reserved.
##
## You may only modify and redistribute this under the terms of any of the
## following licenses(2): Mozilla Public License, V1.1, GNU General
## Public License, V2.0, GNU Lesser General Public License, V2.1
##
## (1) Kamaelia Contributors are listed in the AUTHORS file and at
##     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
##     not this notice.
## (2) Reproduced in the COPYING file, and at:
##     http://kamaelia.sourceforge.net/COPYING
## Under section 3.5 of the MPL, we are using this text since we deem the MPL
## notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
## notice is prohibited.
##
## Please contact us via: kamaelia-list-owner@lists.sourceforge.net
## to discuss alternative licensing.
## -------------------------------------------------------------------------

"""\
=========
AIM Login
=========

This component logs into to AIM with the given screenname and password. It then
sends its logged-in OSCAR connection out of its "signal" outbox, followed by a
list of any non-login-related messages it has received.



Example Usage
-------------
Login and wire the resulting OSCARClient up to a ChatManager::

    class AIMHarness(component):
        def main(self):
            self.loginer = LoginHandler('sitar63112', 'sitar63112').activate()
            self.link((self.loginer, "signal"), (self, "internal inbox"))
            self.addChildren(self.loginer)
            while not self.dataReady("internal inbox"):
                yield 1
            self.oscar = self.recv("internal inbox")
            queued = self.recv("internal inbox")
            self.unlink(self.oscar)
            
            self.chatter = ChatManager().activate()
            self.link((self.chatter, "heard"), (self, "outbox"), passthrough=2)
            self.link((self, "inbox"), (self.chatter, "talk"), passthrough=1)
            self.link((self.chatter, "outbox"), (self.oscar, "inbox"))
            self.link((self.oscar, "outbox"), (self.chatter, "inbox"))
            self.link((self, "internal outbox"), (self.chatter, "inbox"))
            while len(queued):
                self.send(queued[0], "internal outbox")
                del(queued[0])
            while True:
                yield 1

    AIMHarness().run()

You can also run LoginHandler by itself. This is useful for debugging::

    LoginHandler("kamaelia1", "abc123").run()



How it works
------------
First, LoginHandler connects to the authorization server at login.oscar.aol.com
and gets the address of the Basic Oscar Service server, the port to connect on,
and an authorization cookie. It connects to the BOS server, which after some
negotiation sends LoginHandler a list of the services it supports and their
service versions. LoginHandler then finds out rate limits and service
limitations. Then LoginHandler tells the server it is ready to begin normal
operation as an AIM client.

At this point the server recognizes us as a functioning AIM client. LoginHandler
unlinks its internal OSCARClient and passes the OSCARClient out of the "signal"
outbox. LoginHandler also collects any additional messages from OSCARClient and
sends them out of its "signal" outbox. Now any component that connects to that
OSCARClient will be able to send and receive AIM messages. 

"""

from Kamaelia.Support.OscarUtil import *
from Kamaelia.Support.OscarUtil2 import *
from Kamaelia.Protocol.AIM.OSCARClient import OSCARClient, SNACExchanger
from Axon.Component import component
import time
import Axon

__kamaelia_components__ = (OSCARClient, SNACExchanger)

class LoginHandler(SNACExchanger):
    """\
    LoginHandler(screenname, password, [versionNumber]) -> new LoginHandler
    component

    Once started, LoginHandler logs in to AIM and sends the primed connection
    out of its "signal" outbox.

    Keyword arguments:
   
    - versionNumber  -- the version of OSCAR protocol we are using. Default 1. 
    """
    def __init__(self,screenname, password, versionNumber=1):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
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

        debugSections = {"LoginHandler.main" : 0,
                         "LoginHandler.connectAuth" : 0,
                         "LoginHandler.reconnect" : 0,
                         "LoginHandler.passTheReins" : 5,
                         }
        self.debugger.addDebug(**debugSections)


    def main(self):
        """\
        Gets BOS and auth cookie, negotiates protocol, and then passes the
        connection + any non-login-related messages out.
        """
        yield Axon.Ipc.WaitComplete(self.getBOSandCookie())
        if self.error:
            self.send(self.error, "signal")
        else:
            yield Axon.Ipc.WaitComplete(self.negotiateProtocol())
            yield Axon.Ipc.WaitComplete(self.passTheReins())
        
    def getBOSandCookie(self):
        """Gets BOS and auth cookie."""
        yield Axon.Ipc.WaitComplete(self.connectAuth())
        for reply in self.getCookie(): yield 1
        self.error = self.extractBOSandCookie(reply)
        if self.error:
            assert self.debugger.note("LoginHandler.main", 1, self.error)
        else:
            assert self.debugger.note("LoginHandler.main", 1, "Got cookie!")
        
    def negotiateProtocol(self):
        """Negotiates protocol."""
        yield Axon.Ipc.WaitComplete(self.reconnect(self.server, self.port, self.cookie))
        yield Axon.Ipc.WaitComplete(self.setServiceVersions())
        yield Axon.Ipc.WaitComplete(self.getRateLimits())
        self.requestRights()
        yield Axon.Ipc.WaitComplete(self.getRights())
        assert self.debugger.note("LoginHandler.main", 5, "rights gotten, activating connection")
        self.activateConnection()
        
    def connectAuth(self):
        """
        Connects to the AIM authorization server, says hi, and waits for
        acknowledgement.
        """
        assert self.debugger.note("LoginHandler.connectAuth", 7, "sending new connection...")
        data = struct.pack('!i', self.versionNumber)
        self.send((CHANNEL_NEWCONNECTION, data))
        while not self.dataReady():
            yield 1
        reply = self.recv() #should be server ack of new connection
        assert self.debugger.note("LoginHandler.connectAuth", 5, "received new connection ack")

    def getCookie(self):
        """ Requests and waits for MD5 key. """
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
        """Extracts BOS server, port, and auth cookie from server reply."""
        parsed = readTLVs(reply)
        if parsed.has_key(0x08):
            return readTLV08(parsed[0x08])
        assert parsed.has_key(0x05)
        BOS_server = parsed[0x05]
        BOS_server, port = BOS_server.split(':')
        port = int(port)    
        auth_cookie = parsed[0x06]
        self.server, self.port, self.cookie = BOS_server, port, auth_cookie

    def reconnect(self, server, port, cookie):
        """
        Discards old connection to authorization server, connects to BOS, says
        hi, and waits for acknowledgement.
        """
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
        """
        Waits for supported services list from server, requests service
        versions, and waits for server acknowledgement of accepted service
        versions.
        """
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
        """
        Does something useful with the information about rate classes that the
        server sends us and returns the acknowledgement we are supposed to send
        back to the server.

        """
        return '\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05'

    def getRateLimits(self):
        """
        Request rate limits, wait for reply, and send acknowledgement to the
        server.
        """
        
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
        """
        Request that the server tell us our rights and limitations for the
        services that were accepted.
        """
        self.sendSnac(0x01, 0x0e, "")
        self.sendSnac(0x13, 0x02, "")
        self.sendSnac(0x13, 0x04, "")
        self.sendSnac(0x02, 0x02, "")
        self.sendSnac(0x03, 0x02, "")
        self.sendSnac(0x04, 0x04, "")
        self.sendSnac(0x09, 0x02, "")
        
    def getRights(self):
        """.
        Get the server's reply on rights and limitations
        """
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
        """
        Send some parameters up to the server, then signal that we're ready to
        begin receiving data.
        """
        #tell server our capabilities -- which at this point is nothing
        capabilities = TLV(0x05, "")
        self.sendSnac(0x02, 0x04, capabilities)

        #tell server we're done editing SSI data
        self.sendSnac(0x13, 0x12, "")

        #activate SSI data
        self.sendSnac(0x13, 0x07, "")

        #send up our status
        userStatus = TLV(0x06, struct.pack("!HH", STATUS_MISC_DCDISABLED, STATUS_ONLINE))
        self.sendSnac(0x01, 0x1e, userStatus)

        #now we're ready to begin receiving data
        body = ""
        for service, version in self.desiredServiceVersions.items():
            data = struct.pack("!HHi", service, version, 0x01100629)
            body += data
        self.sendSnac(0x01, 0x02, body)
        assert self.debugger.note("LoginHandler.activateConnection", 5, "sent CLI_READY")

    def passTheReins(self):
        """
        Unlink the internal OSCARClient and send it to "signal".
        Also collect any unused messages from OSCARClient and send them out
        through "signal".
        """
        while not self.dataReady():
            yield 1
        queued = []
        while self.dataReady(): #empty the inbox and pass it on to the next component
            queued.append(self.recv())
            yield 1
        self.unlink(self.oscar)
        self.send(self.oscar, "signal")
        self.send(queued, "signal")
        assert self.debugger.note("LoginHandler.passTheReins", 5, "Login done")
        
if __name__ == '__main__':
    screenname = 'kamaelia1'
    password = 'abc123'

    LoginHandler(screenname, password).run()


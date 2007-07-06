#!/usr/bin/python

import Axon

from likefile import *
background = schedulerThread().start()

class SimpleSwarm(Axon.Component.component):
    clients = []
    rr = 0
    maxclients = 4
    def __init__(self, port):
        super(SimpleSwarm, self).__init__()
        self.__class__.port = port
    #
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                req = data.split(" ")
                if req[0] == "REQCONNECT":
                    if len(self.clients) < self.maxclients:
                        reqfrom = req[1]
                        self.clients.append(reqfrom)
                        self.send( "CONNECT " + str(self.port) , "outbox" )
                    else:
                        reqconn = self.clients[self.__class__.rr]
                        self.__class__.rr = (self.__class__.rr+1) % self.maxclients
                        self.send( "REQCONNECT " + reqconn )
            if not self.anyReady():
                self.pause()
            yield 1

def test_SimpleSwarm():
    expect = [
        'CONNECT 1500',
        'CONNECT 1500',
        'CONNECT 1500',
        'CONNECT 1500',
        'REQCONNECT 127.0.0.1:1501',
        'REQCONNECT 127.0.0.1:1502',
        'REQCONNECT 127.0.0.1:1503',
        'REQCONNECT 127.0.0.1:1504',
        'REQCONNECT 127.0.0.1:1501',
    ]
    for i in xrange(1501,1510):
        P = LikeFile(SimpleSwarm(1500))
        P.activate()
        P.send("REQCONNECT 127.0.0.1:%d" % i)
        d = P.recv()
        expected = expect.pop(0)
        assert (repr(d) == repr(expected))
    print "Test passed"


myip = "127.0.0.1"
myport = 1501
servip = "127.0.0.1"
servport = 1500

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient

def newServer(port):
    def mySwarmer():
        return SimpleSwarm(port)
    SimpleServer(protocol=mySwarmer, port=port).activate()

newServer(1500)
time.sleep(0.1)

for myport in xrange(1501, 1506):
    port = 0
    servip = "127.0.0.1"
    servport = 1500
    while port == 0:
        print "REQUEST connecting to ", servip, servport
        l = LikeFile(TCPClient(servip, servport))
        l.activate()
        l.send("REQCONNECT %s:%d" % (myip, myport))
        resp_raw = l.recv()
        resp = resp_raw.split(" ")
        if resp[0] == "CONNECT":
            port = int(resp[1])
            ip = servip
            print "Connecting to", port
        elif resp[0] == "REQCONNECT":
            servip, servport = resp[1].split(":")
            servport = int(servport)
            print "REDIRECTED : request connecting to ", servip, servport 

    print servip, port
    print "Starting Server", myport
    newServer(myport)
    time.sleep(0.1)


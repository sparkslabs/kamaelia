#!/usr/bin/python

import Axon

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.UnixProcess import UnixProcess
from Kamaelia.Chassis.ConnectedServer import SimpleServer

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
    # Server side of the peer
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
    #
    # Client side of the peer
    @staticmethod
    def clientRequest(rootip, rootport, myip, myport):
        servip, servport = rootip, rootport
        port = 0
        while port == 0:
            l = LikeFile(TCPClient(servip, servport)) # "REQUEST connecting to ", servip, servport
            l.activate()
            l.send("REQCONNECT %s:%d" % (myip, myport))
            resp_raw = l.recv()
            resp = resp_raw.split(" ")
            if resp[0] == "CONNECT": # "Connecting to", port
                port = int(resp[1])
                ip = servip
            elif resp[0] == "REQCONNECT": #"REDIRECTED : request connecting to ", servip, servport 
                servip, servport = resp[1].split(":")
                servport = int(servport)
        return servip, port # Resulting server ip/port we can connect to

#
# Configuration
#
# We should really do this in a nicer way,
# but for a simple demo its nice
#
myip = "127.0.0.1"
myport = 1501
servip = "127.0.0.1"
servport = 1500

class ConnectToSwarm(Axon.Component.component):
    def __init__(self, rootip, rootport, myip, myport):
        super(ConnectToSwarm, self).__init__()
        self.rootip = rootip
        self.rootport = rootport
        self.myip = myip
        self.myport = myport

    def main(self):
        servip, servport = SimpleSwarm.clientRequest(self.rootip, self.rootport, self.myip, self.myport)
        yield 1
        self.send( ( servip, servport ), "outbox")
        self.pause()
        yield 1

def mkTCPClient(args): return TCPClient(*args)

Backplane("RADIO").activate()

#
# The client portion of the P2P swarm
#
Graphline(CONFIGURE= ConnectToSwarm(rootip, rootport, myip, myport),
          CLIENT = Carousel(mkTCPClient),
          PUBLISHTO = PublishTo("RADIO"),
          linkages = {
              ("CONFIGURE","outbox"):("CLIENT", "next"),
              ("CLIENT", "outbox") : ("PUBLISHTO", "inbox"),
          }
).activate()

#/-----------------------------------------------------------------
# Handle clients connecting to us:
def ServeRadio(): return SubscribeTo("RADIO")

SimpleServer(protocol=ServeRadio, port = mydataport).activate()

#\-----------------------------------------------------------------

#/-----------------------------------------------------------------
# Why not playback the data we're receiving too?
Pipeline(
    SubscribeTo("RADIO"),
    UnixProcess("mplayer -"),
).run()

#
# Cruft old code
#
if 0:
    def newServer(port):
        def mySwarmer():
            return SimpleSwarm(port)
        SimpleServer(protocol=mySwarmer, port=port).activate()

    newServer(1500)
    time.sleep(0.1)

    for myport in xrange(1501, 1505):
        servip = "127.0.0.1"
        servport = 1500
        servip, servport = SimpleSwarm.clientRequest(servip , servport,myip, myport)

        print "We've been told we can connect to here for data:", servip, servport
        print "Starting Server", myport
        newServer(myport)
        time.sleep(0.1)

#
# Test code for the server side of the swarming code
#
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

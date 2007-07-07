#!/usr/bin/python
#
# Very simple Peer to peer radio player.
#
# We have essentially 2 trees constructed - a mesh construction tree and a data tree.
# There are therefore 2 ports for each peer:
#
# control port - request to connect. Either told to connect to a
#    new port number, or given a new ip/port to request to connect to
#
# data port - connecting to here gets you the data. Its good form
#    to ask on the control port first if you can connect there.
#
# As a result that's why there's two SimpleServer instances.
#

import Axon

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.UnixProcess import UnixProcess
from Kamaelia.Chassis.ConnectedServer import SimpleServer

import dvb3
from Kamaelia.Device.DVB.Core import DVB_Multiplex

from likefile import *
background = schedulerThread().start()

#/-----------------------------------------------------------------
#  Core Control/Mesh setup Protocol
#
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
#\-----------------------------------------------------------------


#/-----------------------------------------------------------------
# Configuration
#
# We should really do this in a nicer way,
# but for a simple demo its nice
#
# Local config
myip = "127.0.0.1" # not needed
mycontrolport = 1500
mydataport = 1601
#
# Root config
#
rootip = "127.0.0.1"  # not needed
rootcontrolport = 1500  # not needed
#
#\-----------------------------------------------------------------


#/-----------------------------------------------------------------
# So we can handle requests for our control port for building
# the mesh
#
def mySwarmer():
    return SimpleSwarm(mydataport)
SimpleServer(protocol=mySwarmer, port=mycontrolport).activate()
#
#\-----------------------------------------------------------------



#/-----------------------------------------------------------------
# Mechanism to allow the audio data to be shared to all clients
#
Backplane("RADIO").activate()
#
#\-----------------------------------------------------------------



#/---------------------------------------------------------------------------
#
# Data source portion of this peer. Connect to the DVB-T
# stream for Radio 1 !
#
# (Code provided for inspection purposes, running this on the internet would
# in all likelihood mean you're in breach of copyright!)
#
# Note how similar this is to the original radio tuner code.
#
freq = 850.166670
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "coderate_HP" : dvb3.frontend.FEC_3_4,
    "coderate_LP" : dvb3.frontend.FEC_3_4,
}

Pipeline(
   DVB_Multiplex(freq, [6210], feparams), # RADIO ONE
   PublishTo("RADIO"),
).activate()
#
#\-----------------------------------------------------------------



#/-----------------------------------------------------------------
# Handle clients connecting to us:
def ServeRadio(): return SubscribeTo("RADIO")

SimpleServer(protocol=ServeRadio, port = mydataport).activate()
#
#\-----------------------------------------------------------------



#/-----------------------------------------------------------------
# Why not playback the data we're receiving off air too?
Pipeline(
    SubscribeTo("RADIO"),
    UnixProcess("mplayer -"),
).run()
#
#\-----------------------------------------------------------------

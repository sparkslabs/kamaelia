#!/usr/bin/python
#
# Initial implementation of The Matrix
#
#

import traceback
import Axon

from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import Plug
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.File.Writing import SimpleFileWriter

import sys
if len(sys.argv) > 1:
   dj1port = int(sys.argv[1])
else:
   dj1port = 1701

if len(sys.argv) > 2:
   dj2port = int(sys.argv[2])
else:
   dj2port = 1702

if len(sys.argv) > 3:
   mockserverport = int(sys.argv[2])
else:
   mockserverport = 1700

class Backplane(Axon.Component.component):
    def __init__(self, name):
        super(Backplane,self).__init__()
        assert name == str(name)
        self.name = name
        self.splitter = Splitter().activate()

    def main(self):
        splitter = self.splitter
        cat = CAT.getcat()
        try:
            cat.registerService("Backplane_I_"+self.name, splitter, "inbox")
            cat.registerService("Backplane_O_"+self.name, splitter, "configuration")
        except Axon.AxonExceptions.ServiceAlreadyExists, e:
            print "***************************** ERROR *****************************"
            print "An attempt to make a second backplane with the same name happened."
            print "This is incorrect usage."
            print 
            traceback.print_exc(3)
            print "***************************** ERROR *****************************"


            raise e
        while 1:
            self.pause()
            yield 1

class message_source(Axon.Component.component):
    def main(self):
        last = self.scheduler.time
        while 1:
            yield 1
            if self.scheduler.time - last > 1:
                self.send("message", "outbox")#
                last = self.scheduler.time

class echoer(Axon.Component.component):
    def main(self):
        count = 0
        while 1:
            self.pause()
            yield 1
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                print "echoer #",self.id,":", data, "count:", count
                count = count +1

class publishTo(Axon.Component.component):
    def __init__(self, destination):
        super(publishTo, self).__init__()
        self.destination = destination
    def main(self):
        cat = CAT.getcat()
        service = cat.retrieveService("Backplane_I_"+self.destination)
        self.link((self,"inbox"), service, passthrough=1)
        while 1:
            self.pause()
            yield 1            
            
class subscribeTo(Axon.Component.component):
    def __init__(self, source):
        super(subscribeTo, self).__init__()
        self.source = source
    def main(self):
        cat = CAT.getcat()
        splitter,configbox = cat.retrieveService("Backplane_O_"+self.source)
        Plug(splitter, self).activate()
        while 1:
            while self.dataReady("inbox"):
                d = self.recv("inbox")
                self.send(d, "outbox")
            yield 1            

class MatrixMixer(Axon.Component.component):
    debug = 0
    Inboxes = ["inbox", "control", "DJ1", "DJ2"]
    def main(self):
        source_DJ1 = subscribeTo("DJ1").activate()
        source_DJ2 = subscribeTo("DJ2").activate()
        self.link((source_DJ1, "outbox"), (self, "DJ1"))
        self.link((source_DJ2, "outbox"), (self, "DJ2"))
        data_dj1 = []
        data_dj2 = []
        count = 0
        while 1:
            self.pause()
            yield 1
            data_dj1 = []
            data_dj2 = []
            while self.dataReady("DJ1"):
                data_dj1.append(self.recv("DJ1"))
            while self.dataReady("DJ2"):
                data_dj2.append(self.recv("DJ2"))

            if data_dj1 != [] or data_dj2 != []:
                data = self.mix(data_dj1, data_dj2)
                self.send(data, "outbox")

            if self.debug and (len(data_dj1) or len(data_dj2)):
                print self.id, "echoer #1",self.id,":", data_dj1, "count:", count
                print self.id, "       #2",self.id,":", data_dj2, "count:", count
                count = count +1

    def mix(self, *sources):
        """ This is a correct, but very slow simple 2 source mixer """
        def char_to_ord(char):
            raw = ord(char)
            if raw >128:
               return (-256 + raw)
            else:
               return raw
        def ord_to_char(raw):
            if raw <0:
                result = 256 + raw
            else:
                result = raw
            return chr(result)
        raw_dj1 = "".join(sources[0])
        raw_dj2 = "".join(sources[1])
        len_dj1 = len(raw_dj1)
        len_dj2 = len(raw_dj2)
        packet_size = max( len_dj1, len_dj2 )
        pad_dj1 = "\0"*(packet_size-len_dj1)
        pad_dj2 = "\0"*(packet_size-len_dj2)
        raw_dj1 = raw_dj1 + pad_dj1
        raw_dj2 = raw_dj2 + pad_dj2
        result = []
        try:
            for i in xrange(0, packet_size,2):
                lsb2 = ord(raw_dj2[i])
                msb2 = ord(raw_dj2[i+1])

                twos_complement_X = (msb2 << 8) + lsb2
                if twos_complement_X > 32767:
                    valuefrom2 = -65536 + twos_complement_X
                else:
                    valuefrom2 = twos_complement_X

                lsb1 = ord(raw_dj1[i])
                msb1 = ord(raw_dj1[i+1])

                twos_complement_X = (msb1 << 8) + lsb1
                if twos_complement_X > 32767:
                    valuefrom1 = -65536 + twos_complement_X
                else:
                    valuefrom1 = twos_complement_X

                mixed = (valuefrom2+valuefrom1) /2
                
                if mixed < 0:
                    mixed = 65536 + mixed
                mixed_lsb= mixed %256
                mixed_msb= mixed >>8

                result.append(chr(mixed_lsb))
                result.append(chr(mixed_msb))

        except IndexError:
            print "WARNING: odd (not even) packet size"
        return "".join(result)

Backplane("DJ1").activate()
Backplane("DJ2").activate()

pipeline(
    SingleServer(port=dj1port),
    publishTo("DJ1"),
).activate()

pipeline(
    SingleServer(port=dj2port),
    publishTo("DJ2"),
).activate()

audienceout = pipeline(
    MatrixMixer(), 
    TCPClient("127.0.0.1", mockserverport)
).run()

# Controller mix
####MatrixMixer().run()
#
# Bunch of code used when debugging various bits of code.
#
#

if 0:
    pipeline(
        ReadFileAdaptor("audio.1.raw", readsize="60024"), #readmode="bitrate", bitrate =16000000),
        publishTo("DJ1"),
    ).activate()

    pipeline(
        ReadFileAdaptor("audio.2.raw", readsize="60024"), #readmode="bitrate", bitrate =16000000),
        publishTo("DJ2"),
    ).activate()

    audienceout = pipeline(
        MatrixMixer(), 
    ###    TCPClient("127.0.0.1", mockserverport)
        SimpleFileWriter("bingle.raw"),
    ).run()
    ###activate()

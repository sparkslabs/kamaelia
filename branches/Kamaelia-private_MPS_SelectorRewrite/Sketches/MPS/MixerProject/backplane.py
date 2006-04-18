#!/usr/bin/python
#
# Initial implementation of The Matrix
#
#

import traceback
import Axon
import time

from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import Plug
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists

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

if len(sys.argv) > 3:
   musicport = int(sys.argv[2])
else:
   musicport = 1703

if len(sys.argv) > 5:
   controlport = int(sys.argv[2])
else:
   controlport = 1705

class ConsoleReader(threadedcomponent):
   def __init__(self, prompt=">>> "):
      super(ConsoleReader, self).__init__()
      self.prompt = prompt

   def run(self):
      while 1:
         line = raw_input(self.prompt)
         line = line + "\n"
         self.outqueues["outbox"].put(line)

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
    Inboxes = ["inbox", "control", "DJ1", "DJ2","music","mixcontrol"]
    Outboxes = ["outbox", "signal", "mixcontrolresponse"]
    def main(self):
        self.dj1_active = 1
        self.dj2_active = 1
        self.music_active = 1
        source_DJ1 = subscribeTo("DJ1").activate()
        source_DJ2 = subscribeTo("DJ2").activate()
        source_music = subscribeTo("music").activate()
        self.link((source_DJ1, "outbox"), (self, "DJ1"))
        self.link((source_DJ2, "outbox"), (self, "DJ2"))
        self.link((source_music, "outbox"), (self, "music"))
        data_dj1 = []
        data_dj2 = []
        data_music = []
        count = 0
        while 1:
            self.pause()
            yield 1
            while self.dataReady("DJ1"):
                data_dj1.append(self.recv("DJ1"))
            while self.dataReady("DJ2"):
                data_dj2.append(self.recv("DJ2"))
            while self.dataReady("music"):
                data_music.append(self.recv("music"))

            while self.dataReady("mixcontrol"):
                command = self.recv("mixcontrol")
                result = self.handleCommand(command)+"\n"  # Response always ends with newline
                print "RESPONSE TO COMMAND", repr(result)
                self.send(result, "mixcontrolresponse")

            # Only bother mixing if the sources are active
            if self.dj1_active or self.dj2_active or self.music_active:
                mix_args = [[],[],[]]  # Mixer function expects 3 sources

                if self.dj1_active:
                   mix_args[0]= data_dj1
                if self.dj2_active:
                   mix_args[1]= data_dj2
                if self.music_active:
                   mix_args[2]= data_music

                if len(data_dj1) > 0 or len(data_dj2) > 0 or len(data_music) > 0:
                    X = time.time()
                    data = self.mix(mix_args)
#                    sys.stderr.write("mixtime ="+str( time.time() - X)+"\n")
                    self.send(data, "outbox")
                    data_dj1 = []
                    data_dj2 = []
                    data_music = []

            if self.debug and (len(data_dj1) or len(data_dj2) or len(data_music)):
                print self.id, "echoer #1",self.id,":", data_dj1, "count:", count
                print self.id, "       #2",self.id,":", data_dj2, "count:", count
                count = count +1

    def handleCommand(self, command):
        print "COMMAND RECEIVED:", repr(command)
        if len(command)>0:
            command[0] = command[0].upper()
            if command[0] == "SWITCH":
                if len(command) !=4: return "FAIL"
                command, dest, source, flag = command
                command.upper()
                dest.upper()
                source.upper()
                flag.upper()
                if flag == "ONLY":
                    if source == "DJ1":
                        self.dj1_active, self.dj2_active, self.music_active = (1,0,0)
                        return "OK"
                    elif source == "DJ2":
                        self.dj1_active, self.dj2_active, self.music_active = (0,1,0)
                        return "OK"
                    elif source == "PRERECORD":
                        self.dj1_active, self.dj2_active, self.music_active = (0,0,1)
                        return "OK"
                    elif source == "ALL":
                        self.dj1_active, self.dj2_active, self.music_active = (1,1,1)
                        return "OK"
                elif flag == "ON" or flag == "OFF":
                    if flag == "ON":
                        value = 1
                    else:
                        value = 0
                    if source == "DJ1":
                        self.dj1_active = value
                        return "OK"
                    elif source == "DJ2":
                        self.dj2_active = value
                        return "OK"
                    elif source == "PRERECORD":
                        self.music_active = value
                        return "OK"
                    elif source == "ALL":
                        self.dj1_active, self.dj2_active, self.music_active = (value,value,value)
                        return "OK"

            if command[0] == "QUERY":
                if len(command) !=3: return "FAIL"
                command, dest, source = command
                command.upper(), dest.upper(), source.upper()
                if source == "DJ1":
                    if self.dj1_active:
                        return "ON"
                    else:
                        return "OFF"
                elif source == "DJ2":
                    if self.dj2_active:
                        return "ON"
                    else:
                        return "OFF"
                elif source == "PRERECORD":
                    if self.music_active:
                        return "ON"
                    else:
                        return "OFF"
                elif source == "ALL":
                    result = []
                    if self.dj1_active: result.append("ON")
                    else:               result.append("OFF")
                    if self.dj2_active: result.append("ON")
                    else:               result.append("OFF")
                    if self.music_active: result.append("ON")
                    else:               result.append("OFF")
                    return " ".join(result)
                    
        return "FAIL"

    def mix(self, sources):
        """ This is a correct, but very slow simple 2 source mixer """
#        sys.stderr.write("sourcelen:"+str( [ len(s) for s in sources] )+"\n")
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
        raw_music = "".join(sources[2])
        len_dj1 = len(raw_dj1)
        len_dj2 = len(raw_dj2)
        len_music = len(raw_music)
        packet_size = max( len_dj1, len_dj2, len_music )
        pad_dj1 = "\0"*(packet_size-len_dj1)
        pad_dj2 = "\0"*(packet_size-len_dj2)
        pad_music = "\0"*(packet_size-len_music)
        raw_dj1 = raw_dj1 + pad_dj1
        raw_dj2 = raw_dj2 + pad_dj2
        raw_music = raw_music + pad_music
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

                lsbmusic = ord(raw_music[i])
                msbmusic = ord(raw_music[i+1])

                twos_complement_X = (msbmusic << 8) + lsbmusic
                if twos_complement_X > 32767:
                    valuefrommusic = -65536 + twos_complement_X
                else:
                    valuefrommusic = twos_complement_X

                mixed = (valuefrom2+valuefrom1+valuefrommusic) /3
                
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
Backplane("music").activate()
Backplane("destination").activate()

pipeline(
    SingleServer(port=dj1port),
    publishTo("DJ1"),
).activate()

pipeline(
    SingleServer(port=dj2port),
    publishTo("DJ2"),
).activate()

pipeline(
    SingleServer(port=musicport),
    publishTo("music"),
).activate()

livecontrol = 1
networkserve = 0
standalone = 1

datarate = 1536000

class printer(Axon.Component.component):
        def main(self):
            while 1:
                if self.dataReady("inbox"):
                    data = self.recv("inbox")
                    sys.stdout.write(data)
                    sys.stdout.flush()
                yield 1

#if standalone:
if 0:
    networkserve = 0
    pipeline(
         ReadFileAdaptor("audio.1.raw", chunkrate=1000, readmode="bitrate", bitrate=datarate),
         TCPClient("127.0.0.1", dj1port),
    ).activate()
    pipeline(
         ReadFileAdaptor("audio.2.raw", chunkrate=1000, readmode="bitrate", bitrate=datarate),
         TCPClient("127.0.0.1", dj2port),
    ).activate()
    pipeline(
         ReadFileAdaptor("audio.2.raw", chunkrate=1000, readmode="bitrate", bitrate=datarate),
         TCPClient("127.0.0.1", musicport),
    ).activate()

if networkserve:
    audiencemix = SingleServer(port=mockserverport)
else:
    audiencemix = printer() # SimpleFileWriter("bingle.raw")

if livecontrol:
    Graphline(
        CONTROL =  SingleServer(port=controlport),
        TOKENISER = lines_to_tokenlists(),
        MIXER = MatrixMixer(), 
        AUDIENCEMIX = audiencemix,
        linkages = {
           ("CONTROL" , "outbox") : ("TOKENISER" , "inbox"),
           ("TOKENISER" , "outbox") : ("MIXER" , "mixcontrol"),
           ("MIXER" , "mixcontrolresponse") : ("CONTROL" , "inbox"),
           ("MIXER", "outbox") : ("AUDIENCEMIX", "inbox"),
        }
    ).run()
else:
    Graphline(
        CONTROL = ConsoleReader("mixer desk >> "),
        CONTROL_ = consoleEchoer(),
        TOKENISER = lines_to_tokenlists(),
        MIXER = MatrixMixer(), 
        AUDIENCEMIX = audiencemix,
        linkages = {
           ("CONTROL" , "outbox") : ("TOKENISER" , "inbox"),
           ("TOKENISER" , "outbox") : ("MIXER" , "mixcontrol"),
           ("MIXER" , "mixcontrolresponse") : ("CONTROL_" , "inbox"),
           ("MIXER", "outbox") : ("AUDIENCEMIX", "inbox"),
        }
    ).run()

if 0:
    audienceout = pipeline(
        MatrixMixer(), 
        SingleServer(port=mockserverport)
    ).run()


    def dumping_server():
        return pipeline(
            SingleServer(mockserverport),
            printer(),
        )

    dumping_server().run()

    # Command line mixer control
    commandlineMixer = Graphline(
        TOKENISER = lines_to_tokenlists(),
        MIXER = MatrixMixer(), 
        FILE = SimpleFileWriter("bingle.raw"),
        linkages = {
           ("USER" , "outbox") : ("TOKENISER" , "inbox"),
           ("TOKENISER" , "outbox") : ("MIXER" , "mixcontrol"),
           ("MIXER" , "mixcontrolresponse") : ("USERRESPONSE" , "inbox"),
           ("MIXER", "outbox") : ("FILE", "inbox"),
        }
    ).run()

    # TCP Client sending
    audienceout = pipeline(
        MatrixMixer(), 
    #    SimpleFileWriter("bingle.raw"),
        TCPClient("127.0.0.1", mockserverport)
    ).run()
    #).activate()

    def dumping_server():
        return pipeline(
            SingleServer(mockserverport),
            printer(),
        )

# Controller mix
####MatrixMixer().run()
#
# Bunch of code used when debugging various bits of code.
#
#
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

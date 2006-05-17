#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Demuxer,DVB_Multiplex
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.File.UnixPipe import Pipethrough
import Axon
import struct
import dvb3

from Axon.Ipc import shutdownMicroprocess, producerFinished
from Kamaelia.Device.DVB.EIT import PSIPacketReconstructor, EITPacketParser, NowNextServiceFilter, NowNextChanges, TimeAndDatePacketParser
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Util.PipelineComponent import pipeline
import time, os

class EITDemux(Axon.Component.component):
    Outboxes = {"outbox":"",
                "signal":"",
                "_eit_" :"",
               }
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                packet = self.recv("inbox")
                pid = struct.unpack(">H", packet[1: 3])[0] & 0x1fff
                if pid != 18:
                    self.send( packet, "outbox")
                else:
                    self.send( packet, "_eit_")
#                yield 1
            else:
                self.pause()

class ProgrammeTranscoder(Axon.Component.component):
    Inboxes = { "inbox" : "TS packets containing audio and video",
                "control" : "the usual",
                "_transcodingcomplete" : "signal from the transcoder",
              }
    Outboxes = { "outbox" : "",
                 "_stop" : "stop the transcoder",
                 "signal" : "the usual",
               }
    def __init__(self, eitdata, mencoder_options, dir_prefix):
        super(ProgrammeTranscoder,self).__init__()
        self.eitdata = eitdata
        self.mencoder_options =mencoder_options
        self.dir_prefix = dir_prefix
        
    def main(self):
        # first, generate unique filename
        uid = str(time.time())
        
        encodingfile = "/data/encoding"+self.dir_prefix+"/"+uid+".avi"
        waitingEIT   = "/data/encoding"+self.dir_prefix+"/"+uid+".eit"
        
        finishedfile = "/data/finished"+self.dir_prefix+"/"+uid+".avi"
        finishedEIT  = "/data/finished"+self.dir_prefix+"/"+uid+".eit"
        
        \
print "Starting transcoding into: "+encodingfile
        transcoder = Pipethrough("mencoder -o "+encodingfile+" "+self.mencoder_options)
        
        data_linkage = self.link( (self,"inbox"), (transcoder,"inbox"), passthrough=1 )
        ctrl_linkage = self.link( (self,"_stop"), (transcoder,"control"))
        done_linkage = self.link( (transcoder,"signal"), (self,"_transcodingcomplete") )
        
        transcoder.activate()
        
        # write the eit data to a file
        eitF = open(waitingEIT,"wb")
        eitF.write( str(self.eitdata) )
        eitF.close()
        eitF = None
        
        while not self.dataReady("control"):      # wait until shutdown
            self.pause()
            yield 1
            
        \
print "shutdown received"
        while self.dataReady("control"):
            self.recv("control")                 # flush out shutdown messages
            
        # tell transcoder to stop
        \
print "Transcoding must now stop..."
        self.send(producerFinished(), "_stop")
        
        \
print "waiting for transcoder to finish"
        while not self.dataReady("_transcodingcomplete"):
            self.pause()
            yield 1
        \
print "transcoder has finished"
        while self.dataReady("_transcodingcomplete"):
            self.recv("_transcodingcomplete")
        
        # move the transcoded file and eit data to final destination
        \
print "Moving finished files"
        os.rename(encodingfile, finishedfile)
        os.rename(waitingEIT, finishedEIT)

        \
print "Unlinking transcoder"
        self.unlink(data_linkage)
        self.unlink(ctrl_linkage)
        self.unlink(done_linkage)

        \
print "Sending done signal"
        self.send(producerFinished(), "signal")
        raise "STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP!!!!"


def EITParsing(*service_ids):
    return pipeline(
        PSIPacketReconstructor(),
        EITPacketParser(),
        NowNextServiceFilter(*service_ids),
        NowNextChanges(),
    )        


def ChannelTranscoder(service_id, mencoder_options, dir_prefix): # BBC ONE
    def transcoder_factory(eit):
        \
print "transcoder factory called with eit:\n"+str(eit)+"\n"
        return ProgrammeTranscoder(eit, mencoder_options, dir_prefix)
    
    return Graphline(
        PROG_CODER = Carousel( transcoder_factory ),
        EIT_PARSE = EITParsing(service_id),
        DEMUX = EITDemux(),
        linkages = {
          ("self","inbox") : ("DEMUX","inbox"),
          ("DEMUX","outbox") : ("PROG_CODER","inbox"),   # forward video and audio packets to coder
          ("DEMUX","_eit_") : ("EIT_PARSE", "inbox"),    # forward eit packets to eit parsing
          ("EIT_PARSE", "outbox") : ("PROG_CODER", "next"), # eit programme junction events cause new transcoding to start
        }
    )

location = "london"

if location == "london":
    freq = 505.833330 # 529.833330   # 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
else: # manchester
    freq = 754
    feparams = {}

from Axon.ThreadedComponent import threadedcomponent

class SysStatus(threadedcomponent):
    def main(self):
        while 1:
            print "---",time.time()
            for mprocess in Axon.Scheduler.scheduler.run.threads:
                print mprocess._isRunnable(),mprocess.name
            print "---"
            time.sleep(10)

#SysStatus().activate()

from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.Console import ConsoleEchoer

params={}
params["LO"] = {
    "mencoder_options" : " -ovc lavc -oac mp3lame -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -",
    "dir_prefix" : "200",
    }
params["HI"] = {
    "mencoder_options" : " -ovc lavc -oac mp3lame -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=512:abitrate=128 -vf scale=640:-2 -",
    "dir_prefix" : "512"
    }

pids = { "BBC ONE" : [600,601],
         "BBC TWO" : [610,611],
         "CBEEBIES": [201,401],
         "EIT"     : [18],
       }

service_ids = { "BBC ONE": 4164,
                "BBC TWO": 4228,
                "CBEEBIES":16960,
              }

Graphline(
    SOURCE=DVB_Multiplex(freq, pids["BBC TWO"]+pids["EIT"], feparams), # BBC ONE + EIT data
#    SOURCE=ReadFileAdaptor("BBC_ONE_AND_EIT.ts",readmode="bitrate",bitrate=6000000,chunkrate=6000000/8/2048),
    DEMUX=DVB_Demuxer({
#        "600": ["BBCONE","BBCONE_2"],
#        "601": ["BBCONE","BBCONE_2"],
        "610": ["BBCTWO","BBCTWO_2"],
        "611": ["BBCTWO","BBCTWO_2"],
#        "201" : ["CBEEBIES"],
#        "401" : ["CBEEBIES"],
        "18": ["BBCTWO","BBCTWO_2"],   # BBCONE","BBCONE_2","BBCTWO","BBCTWO_2", "CBEEBIES"
#        "20": ["DATETIME"],
    }),
#    BBCONE_LO = ChannelTranscoder(4164, **params["LO"]),
#    BBCONE_HI = ChannelTranscoder(4164, **params["HI"]),
    BBCTWO_HI = ChannelTranscoder(service_ids["BBC TWO"], **params["HI"]),
#    CBEEBIES = ChannelTranscoder(service_ids["CBEEBIES"], **params["HI"]),

#    DATETIME = pipeline( PSIPacketReconstructor(),
#                         TimeAndDatePacketParser(),
#                         ConsoleEchoer(),
#                       ),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
#       ("DEMUX", "BBCONE"): ("BBCONE_LO", "inbox"),
#       ("DEMUX", "BBCONE_2"): ("BBCONE_HI", "inbox"),
       ("DEMUX", "BBCTWO_2"): ("BBCTWO_HI", "inbox"),
#       ("DEMUX", "CBEEBIES"): ("CBEEBIES", "inbox"),
#       ("DEMUX", "DATETIME"): ("DATETIME","inbox"),

    }
).run()



#
# mencoder -o current.200.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -
# mencoder -o current.512.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=512:abitrate=128 -vf scale=640:-2 -
#


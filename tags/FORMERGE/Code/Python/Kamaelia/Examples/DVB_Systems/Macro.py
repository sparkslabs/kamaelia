#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Demuxer,DVB_Multiplex
from Kamaelia.Device.DVB.SoftDemux import DVB_SoftDemuxer as DVB_Demuxer
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
print uid,"Starting transcoding into: "+encodingfile
        transcoder = Pipethrough("mencoder -o "+encodingfile+" "+self.mencoder_options)
        \
print uid,"Transcoder pipethough =",transcoder.name
        
        data_linkage = self.link( (self,"inbox"), (transcoder,"inbox"), passthrough=1 )
        ctrl_linkage = self.link( (self,"_stop"), (transcoder,"control"))
        done_linkage = self.link( (transcoder,"signal"), (self,"_transcodingcomplete") )
        
#        transcoder_logger = SimpleFileWriter(uid+".log").activate()
#        log_linkage = self.link( (transcoder,"outbox"), (transcoder_logger,"inbox"))
        
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
print uid,"shutdown received"
        while self.dataReady("control"):
            self.recv("control")                 # flush out shutdown messages
            
        # tell transcoder to stop
        \
print uid,"Transcoding must now stop..."
        self.send(producerFinished(), "_stop")
        
        \
print uid,"waiting for transcoder to finish"
        while not self.dataReady("_transcodingcomplete"):
            self.pause()
            yield 1
        \
print uid,"transcoder has finished"
        while self.dataReady("_transcodingcomplete"):
            self.recv("_transcodingcomplete")
        
        # move the transcoded file and eit data to final destination
        \
print uid,"Moving finished files"
        os.rename(encodingfile, finishedfile)
        os.rename(waitingEIT, finishedEIT)

        \
print uid,"Unlinking transcoder"
        self.unlink(data_linkage)
        self.unlink(ctrl_linkage)
        self.unlink(done_linkage)
#        self.unlink(log_linkage)

        \
print uid,"Sending done signal"
        self.send(producerFinished(), "signal")
        
#         # HACK HACK HACK
#         # force this program to terminate
#         # and clean up any extraneous EIT data
#         cruft = [file for file in os.listdir("/data/encoding"+self.dir_prefix+"/") if file[-4:]==".eit"]
#         for file in cruft:
#             os.remove("/data/encoding"+self.dir_prefix+"/"+file)
#         raise "STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP STOP!!!!"


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

location = "manchester"

if location == "london": # Crystal Palace
    freq = 505.833330 # 529.833330   # 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
elif location == "manchester": # WinterHill
    freq = 754.166670
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }

from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.File.Reading import RateControlledFileReader
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
         "CBBC"    : [620,621],
         "EIT"     : [18],
       }

service_ids = { "BBC ONE": 4164,
                "BBC TWO": 4228,
                "CBEEBIES":16960,
                "CBBC":4671,
              }

print "-----STARTING MACRO----- time =",time.time()

def repeatingFile():
    def rfa_factory(_):
        return RateControlledFileReader("junction.ts",readmode="bytes",rate=18000000/8,chunksize=2048)
    return Graphline(CAROUSEL=Carousel(rfa_factory, make1stRequest=True),
                     linkages = { ("CAROUSEL","requestNext") : ("CAROUSEL","next"),
                                  ("CAROUSEL","outbox") : ("self", "outbox"),
                                  ("CAROUSEL","signal") : ("self", "signal"),
                                },
                    )

Graphline(
    SOURCE=DVB_Multiplex(freq, pids["BBC TWO"]+pids["EIT"], feparams), # BBC Channels + EIT data
#    SOURCE=ReadFileAdaptor("junction.ts",readmode="bitrate",bitrate=6523000,chunkrate=6523000/8/2048),
#    SOURCE=repeatingFile(),
    DEMUX=DVB_Demuxer({
#        600: ["BBCONE","BBCONE_2"],
#        601: ["BBCONE","BBCONE_2"],
        610: ["BBCTWO","BBCTWO_2"],
        611: ["BBCTWO","BBCTWO_2"],
#        201 : ["CBEEBIES"],
#        401 : ["CBEEBIES"],
#        620 : ["CBBC"],
#        621 : ["CBBC"],
        18: ["BBCTWO","BBCTWO_2"],   # BBCONE","BBCONE_2","BBCTWO","BBCTWO_2", "CBEEBIES"
#        20: ["DATETIME"],
    }),
#    BBCONE_LO = ChannelTranscoder(4164, **params["LO"]),
#    BBCONE_HI = ChannelTranscoder(4164, **params["HI"]),
#    BBCTWO_LO = ChannelTranscoder(service_ids["BBC TWO"], **params["LO"]),
    BBCTWO_HI = ChannelTranscoder(service_ids["BBC TWO"], **params["HI"]),
#    CBBC_HI = ChannelTranscoder(service_ids["CBBC"], **params["HI"]),
#    CBEEBIES = ChannelTranscoder(service_ids["CBEEBIES"], **params["HI"]),

#    DATETIME = pipeline( PSIPacketReconstructor(),
#                         TimeAndDatePacketParser(),
#                         ConsoleEchoer(),
#                       ),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
#       ("DEMUX", "BBCONE"): ("BBCONE_LO", "inbox"),
#       ("DEMUX", "BBCONE_2"): ("BBCONE_HI", "inbox"),
#       ("DEMUX", "BBCTWO"): ("BBCTWO_LO", "inbox"),
       ("DEMUX", "BBCTWO_2"): ("BBCTWO_HI", "inbox"),
#       ("DEMUX", "CBBC"): ("CBBC_HI", "inbox"),
#       ("DEMUX", "CBEEBIES"): ("CBEEBIES", "inbox"),
#       ("DEMUX", "DATETIME"): ("DATETIME","inbox"),

    }
).run()

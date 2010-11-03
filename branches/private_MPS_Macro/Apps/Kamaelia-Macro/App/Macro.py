#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from Kamaelia.Device.DVB.Core import DVB_Demuxer,DVB_Multiplex
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.File.UnixProcess import UnixProcess
import Axon
import struct
import dvb3

from Axon.Ipc import shutdownMicroprocess, producerFinished
from Kamaelia.Device.DVB.EIT import PSIPacketReconstructor, EITPacketParser, NowNextServiceFilter, NowNextChanges, TimeAndDatePacketParser
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Chassis.Pipeline import Pipeline
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
        
        print uid,"Starting transcoding into: "+encodingfile
        transcoder = UnixProcess("mencoder -o "+encodingfile+" "+self.mencoder_options)
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
            
        print uid,"shutdown received"
        while self.dataReady("control"):
            self.recv("control")                 # flush out shutdown messages
            
        # tell transcoder to stop
        print uid,"Transcoding must now stop..."
        self.send(producerFinished(), "_stop")
        
        print uid,"waiting for transcoder to finish"
        while not self.dataReady("_transcodingcomplete"):
            self.pause()
            yield 1
        print uid,"transcoder has finished"
        while self.dataReady("_transcodingcomplete"):
            self.recv("_transcodingcomplete")
        
        # move the transcoded file and eit data to final destination
        print uid,"Moving finished files"
        os.rename(encodingfile, finishedfile)
        os.rename(waitingEIT, finishedEIT)

        print uid,"Unlinking transcoder"
        self.unlink(data_linkage)
        self.unlink(ctrl_linkage)
        self.unlink(done_linkage)
#        self.unlink(log_linkage)

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
    return Pipeline(
        PSIPacketReconstructor(),
        EITPacketParser(),
        NowNextServiceFilter(*service_ids),
        NowNextChanges(),
    )


def ChannelTranscoder(service_id, mencoder_options, dir_prefix): # BBC ONE
    def transcoder_factory(eit):
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
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
elif location == "manchester": # WinterHill
    freq = 754.166670
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
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

Graphline(
    SOURCE=DVB_Multiplex(freq, pids["BBC TWO"]+pids["EIT"], feparams), # BBC Channels + EIT data
    DEMUX=DVB_Demuxer({
        610: ["BBCTWO"],
        611: ["BBCTWO"],
        18: ["BBCTWO"],   # BBCONE","BBCONE_2","BBCTWO","BBCTWO_2", "CBEEBIES"
    }),
    BBCTWO_HI = ChannelTranscoder(service_ids["BBC TWO"], **params["HI"]),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
       ("DEMUX", "BBCTWO"): ("BBCTWO_HI", "inbox"),
    }
).run()

# RELEASE: MH, MPS

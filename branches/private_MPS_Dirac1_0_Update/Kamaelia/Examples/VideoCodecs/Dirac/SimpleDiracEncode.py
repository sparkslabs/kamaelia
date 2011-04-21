#!/usr/bin/python
# -*- coding: utf-8 -*-
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
# Download and build dirac first!
#
# Get the source raw video file (in rgb format) from here, and gunzip it:
# http://sourceforge.net/project/showfiles.php?group_id=102564&package_id=119507
#
# To convert RGB to YUV:
#   RGBtoYUV420 snowboard-jum-352x288x75.rgb snowboard-jum-352x288x75.yuv 352 288 75
#
# Alternatively, source your own AVI file and convert with:
#   ffmpeg -i file_from_digital_camera.avi rawvideo.yuv
#
# and alter the config below as required.

import sys
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Codec.RawYUVFramer import RawYUVFramer
# from Kamaelia.Codec.Dirac import DiracEncoder

# FILENAME  = "/data/dirac-video/snowboard-jum-352x288x75.yuv"

# encoder param sets it to iframe only (no motion based coding, faster)
# (overrides preset)

if len(sys.argv) != 2:
    sys.stderr.write("Usage:\n   "+sys.argv[0]+" <dirac-file>\n\n")
    sys.exit(1)

SIZE = (352,288)
DIRACPRESET = "CIF"         # dirac resolution and encoder settings preset
ENCPARAMS = {"num_L1":0}

FILENAME = sys.argv[1]

from Kamaelia.File.Writing import SimpleFileWriter
from Axon.Ipc import producerFinished, shutdownMicroprocess

import Axon
class Tracer(Axon.Component.component):
   def main(self):
       F = 0
       while not self.dataReady("control"):
           if self.dataReady("inbox"):
               for data in self.Inbox("inbox"):
                    F += 1
                    print self.tag,F
                    self.send(data, "outbox")
           elif not self.anyReady():
               self.pause()
           yield 1

       print self.tag,"exitted. Shutting down"
       for control_message in self.Inbox("control"):
           print self.tag, "control_message", control_message, repr(control_message)
           self.send(control_message,"signal")


from dirac_encoder import DiracEncoder as EncoderWrapper
from dirac_encoder import DiracEncodeException

class DiracEncoder(Axon.Component.component):

    def __init__(self, preset=None, verbose=False, encParams={}, seqParams={}, allParams={}):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DiracEncoder, self).__init__()
        self.encoder = EncoderWrapper(preset=preset, bufsize=1024*1024, verbose=verbose, allParams=allParams)
        
    def main(self):
        """Main loop"""
        done = False
        msg = None
        shutdown_message = None
        sourceDone = False
        framecount = 0
        while not done:
            for frame in self.Inbox("inbox"):
                data = "".join(frame['yuv'])
                framecount += 1
                print "GOT FRAME", framecount
                self.encoder.sendFrameForEncode(data)
                while 1:  # loop until 'needdata' event breaks out of this
                    try:
                        bytes = self.encoder.getCompressedData()
                        print "SENDING BYTES"
                        self.send(bytes,"outbox")
 
                    except DiracEncodeException, e:
                        reason = e.args[0]
                        if reason =="NEEDDATA":
                            if sourceDone:
                                done = True
                            break
                        elif reason =="ENCODERERROR":
                            print "Encoder Error"
                            raise RuntimeError("ENCODERERROR")
                        elif reason =="INTERNALFAULT":
                            print "Internal Fault"
                            raise RuntimeError("INTERNALFAULT")
                        else:
                            import sys
                            sys.stderr.write("BINGO\n\n")
                            sys.stderr.write(repr(reason) +"\n\n")
                            sys.stderr.write(repr(dir(reason)) +"\n\n")
                            sys.stderr.flush()
                            raise

            for control_message in self.Inbox("control"):
                if isinstance(msg, shutdownMicroprocess):
                    print "GOT shutdownMicroprocess"
                    shutdown_message = control_message
                    done = True
                elif isinstance(msg, producerFinished):
                    print "GOT producerFinished"
                    shutdown_message = control_message
                    sourceDone = True

            if not self.anyReady():
                self.pause()

            yield 1

        print "DIRAC ENCODER SHUTDOWN"
        self.send(shutdown_message, "signal")


Pipeline( ReadFileAdaptor(FILENAME, readmode="bitrate", bitrate= 10000000),
          RawYUVFramer( size=SIZE ),
          Tracer(tag="FRAME"),
          DiracEncoder(preset="CIF"),
          Tracer(tag="DIRAC FRAME"),
          SimpleFileWriter("result.drc"),
          Tracer(tag="DIRAC FRAME"),
        ).run()

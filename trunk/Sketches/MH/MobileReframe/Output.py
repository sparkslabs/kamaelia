#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# -------------------------------------------------------------------------
"""\
============================
Audio Playback using PyMedia
============================

This component plays raw audio sent to its "inbox" inbox using the pymedia
library.



Example Usage
-------------

Playing 8KHz 16 bit mono raw audio from a file::
    
    Pipeline( RateControlledFileReader("recording.raw", readmode="bytes", rate=8000*2/8,
              Output(sample_rate=8000, channels=1, format="S16_LE"),
            ).run()



How does it work?
-----------------

Output uses the PyMedia library to play back audio to the current audio playback
device.

Send raw binary audio data strings to its "inbox" inbox.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.
"""

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

import sys,os
from Axon.ThreadedComponent import threadedcomponent


import time
from math import log

import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

from Kamaelia.Support.PyMedia.AudioFormats import format2PyMediaFormat
from Kamaelia.Support.PyMedia.AudioFormats import pyMediaFormat2format
from Kamaelia.Support.PyMedia.AudioFormats import format2BytesPerSample


class _Output(threadedcomponent):
    """\
    Output([sample_rate][,channels][,format]) -> new Output component.
    
    Outputs (plays) raw audio data sent to its "inbox" inbox using the PyMedia
    library.
    
    Keyword arguments:
        
    - sample_rate  -- Sample rate in Hz (default = 44100)
    - channels     -- Number of channels (default = 2)
    - format       -- Sample format (default = "S16_LE")
    """
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(_Output,self).__init__(queuelengths=20)
        
        pformat = format2PyMediaFormat[format]
        self.snd = sound.Output(sample_rate, channels, pformat)
        

    def main(self):
        while 1:
            
            while self.dataReady("inbox"):
                self.snd.play(self.recv("inbox"))
                
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    self.snd.stop()
                    return
                self.send(msg,"signal")
        
            self.pause()
        
        

from Chassis import Pipeline
from RateChunker import RateChunker

def Output(sample_rate=44100, channels=2, format="S16_LE", maximumLag = 0.0):
    # no idea why, but it seems we need to pass to pymedia chunks of a
    # sufficiently short duration to prevent playback artefacts
    chunksize = sample_rate/40
    # round to nearest power of 2
    chunksize = 2**int(log(chunksize)/log(2))
    
    datarate = chunksize
    chunkrate = 1
    quantasize = 1
    
    return Pipeline(
        10, RateChunker(datarate, quantasize, chunkrate),
        10, _Output(sample_rate, channels, format)
    )

__kamaelia_prefabs__ = ( Output, )
#__kamaelia_components__ = ( Output, )

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
==============================
Resampling Audio using PyMedia
==============================

This component resamples raw audio data sent to its "inbox" inbox, changing it
to a different sample rate and/or number of channels, and outputting it from its
"outbox" outbox. It does this using the pymedia library.



Example Usage
-------------

Capturing CD quality audio and playing it at telephone quality (8KHz, mono)::
    
    Pipeline( Input(sample_rate=44100, channels=2, format="S16_LE"),
              Resample(44100, 2, 8000, 1),
              Output(sample_rate=8000, channels=1, format="S16_LE"),
            ).run()



How does it work?
-----------------

Resample uses the PyMedia library to change the sample rate and/or number of
channels of audio.

Send raw binary audio data strings to its "inbox" inbox. It will be resampled
and the resulting raw binary audio data strings are sent out of its "outbox"
outbox.

Note that resampling can change the sample rate or number of channels, but *not*
the sample format. The sample format output will be the same as the input.

Resampling is done by duplicating/dropping samples. No interpolation takes
place. This is therefore not a good quality resample, but it is reasonably fast.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.
"""
raise NotImplementedError("PyMedia doesn't seem to be available for python 3")

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

import pymedia.audio.sound as sound


class Resample(component):
    """\
    Resample(sample_rate,channels,to_sample_rate,to_channels) -> new Resample component.
    
    Resamples audio to a different sample rate and/or number of channels using
    the pymedia library.
    
    Keyword arguments:
        
    - sample_rate     -- Input sample rate in Hz
    - channels        -- Input number of channels
    - to_sample_rate  -- Desired sample rate in Hz
    - to_channels     -- Desired number of channels
    """
    def __init__(self, sample_rate, channels, to_sample_rate, to_channels):
        super(Resample,self).__init__()
        
        self.resampler = sound.Resampler( (sample_rate, channels), (to_sample_rate, to_channels) )
        
    def main(self):
        shutdown=False
        data=""
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                resampled = str(self.resampler.resample(data))
                self.send(resampled, "outbox")
        
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1


__kamaelia_components__ = ( Resample, )

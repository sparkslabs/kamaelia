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

from Axon.Component import component
from pymedia.audio import sound

from Axon.Ipc import shutdownMicroprocess, producerFinished

class SoundOutput(component):
    """pymedia sound output component

    Plays audio from received pymedia audio_frame objects.

    The sample_rate and channels parameters are taken from the audio_frame
    objects. The pymedia sound output object is therefore not created until
    the first audio_frame is received. If the parameters changed, then the
    sound output object is replaced.

    This component will shutdown in response to a producerFinished or
    shutdownMicroprocess message (received on 'control'). Immediately before
    shutting down, the message(s) are passed on (out of 'signal').
    """

    def __init__(self, audioformat = sound.AFMT_S16_LE):
        """Initialisation.

        afmt = raw audio data format. defaults to pymedia.audio.sound.AFMT_S16_LE
        """
        super(SoundOutput,self).__init__()

        self.audioformat = audioformat
        self.outputter = None
        self.channels = None
        self.sample_rate = None


    def main(self):
        done = False
        while not done:

            yield 1
            self.pause()

            while self.dataReady("inbox"):
                frame = self.recv("inbox")

                if not self.outputter or self.sample_rate != frame.sample_rate or self.channels != frame.channels:
                    self.sample_rate = frame.sample_rate
                    self.channels = frame.channels
                    self.outputter = sound.Output(self.sample_rate, self.channels, self.audioformat)

                self.outputter.play( frame.data )
                

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                    self.send(msg, "signal")
                    done = True

        
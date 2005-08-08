#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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

        
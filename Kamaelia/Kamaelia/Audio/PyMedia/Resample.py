#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

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
from pymedia.audio import acodec

from Axon.Ipc import shutdownMicroprocess, producerFinished

class AudioDecoder(component):
    """pymedia audio decoder component

       Send coded audio data to the inbox, and decoded audio data frames
       (pymedia audio_frame objects) will be sent out the outbox.

       This component will shutdown in response to a producerFinished or
       shutdownMicroprocess message (received on 'control'). Immediately before
       shutting down, the message(s) are passed on (out of 'signal').
    """

    def __init__(self, codec):
        """Initialisation. Create a decoder for the specified codec.
           Codec is specified by file extension. Available codecs are
           listed in pymedia.audio.acodec.extensions.
        """
        super(AudioDecoder, self).__init__()

        if float(acodec.version) > 2:
            self.codecid = acodec.getCodecId(codec)
            self.decoder = acodec.Decoder( {"id":self.codecid} )
        else:
            self.decoder = acodec.Decoder( codec )

        
    def main(self):
        done = False
        while not done:
            
            yield 1
            self.pause()

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                output = self.decoder.decode( data )
                if output:
                    self.send( output, "outbox" )

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                    self.send(msg, "signal")
                    done = True



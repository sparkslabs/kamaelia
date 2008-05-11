#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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



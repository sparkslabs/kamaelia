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
=======================================
Compressed audio decoding using PyMedia
=======================================

Decodes compressed audio data sent to its "inbox" inbox and outputs the raw
audio data from its "outbox" outbox. Decoding done using the PyMedia library.



Example Usage
-------------

Playing a MP3 file, known to be 128bkps, 44100Hz 16bit stereo::
    
    Pipeline( RateControlledFileReader("my.mp3", readmode="bytes", rate=128*1024/8),
              Decoder("mp3"),
              Output(44100, 2, "S16_LE"),
            ).run()



How does it work?
-----------------

Set up Decoder by specifying the filetype/codec to the initializer. What codecs
are supported depends on your PyMedia installation.

Send raw binary data strings containing the compressed audio data to the "inbox"
inbox, and raw binary data strings containing the uncompressed raw audio data
will be sent out of the "outbox" outbox.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.

"""

raise NotImplementedError("PyMedia doesn't seem to be available for python 3")

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

import sys,os
from Kamaelia.Support.PyMedia.AudioFormats import codec2fileExt
from Kamaelia.Support.PyMedia.AudioFormats import pyMediaFormat2format


class Decoder(component):
    """\
    Decoder(fileExtension) -> new pymedia Audio Decoder.
    
    Send raw data from a compressed audio file (which had the specified extension)
    to the "inbox" inbox, and decompressed blocks of raw audio data are emitted
    from the "outbox" outbox.
    
    Keyword  arguments:

    - codec  -- The codec (ones supported depend on your local installation)
    """
    Inboxes = { "inbox"  : "compressed audio data",
                "control": "Shutdown signalling",
              }
    Outboxes = { "outbox"   : "raw audio samples",
                 "format"   : "dictionary detailing sample_rate, sample_format and channels",
                 "needData" : "requests for more data (value is suggested minimum number of bytes",
                 "signal"   : "Shutdown signalling",
               }
               
    def __init__(self,codec):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Decoder,self).__init__()
        self.extension = codec2fileExt[codec]

    def main(self):
        
        dm = muxer.Demuxer(self.extension)
        
        shutdown=False
        decoder=None
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
        
                frames = dm.parse(data)
                
                for frame in frames:
                    
                    if not decoder:
                        # first time we get data from the demuxer
                        # we create the decoder
                        stream_index = frame[0]
                        decoder = acodec.Decoder(dm.streams[stream_index])

                        # decode our first frame
                        decoded = decoder.decode(frame[1])
                        # output the format of the audio
                        format = {
                            'channels'    : decoded.channels,
                            'sample_rate' : decoded.sample_rate,
                            'format'      : pyMediaFormat2format[sound.AFMT_S16_LE],
                        }
                        self.send(format, "format")
                    else:
                        # otherwise we just decode a frame
                        decoded = decoder.decode(frame[1])

                    self.send(str(decoded.data),"outbox")

            self.send(4096, "needData")
        
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1

__kamaelia_components__ = ( Decoder, )


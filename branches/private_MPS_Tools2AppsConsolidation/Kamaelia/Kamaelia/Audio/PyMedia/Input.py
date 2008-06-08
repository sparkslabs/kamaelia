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
===========================
Audio Capture using PyMedia
===========================

This component captures raw audio using the pymedia library, and outputs it
out of its "outbox" outbox.



Example Usage
-------------

Recording telephone quality audio to a file::
    
    Pipeline( Input(sample_rate=8000, channels=1, format="S16_LE"),
              SimpleFileWriter("recording.raw"),
            ).run()



How does it work?
-----------------

Input uses the PyMedia library to capture audio from the currently selected
audio capture device.

It outputs to its "outbox" outbox raw binary audio data in strings.

This component supports sending to a size limited inbox. If the size limited
inbox is full, this component will pause until it is able to send out the data.

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

import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

from Kamaelia.Support.PyMedia.AudioFormats import format2PyMediaFormat


class Input(threadedcomponent):
    """\
    Input([sample_rate][,channels][,format]) -> new Input component.
    
    Captures audio using the PyMedia library and sends the raw audio data out
    of its "outbox" outbox.
    
    Keyword arguments:
        
    - sample_rate  -- Sample rate in Hz (default = 44100)
    - channels     -- Number of channels (default = 2)
    - format       -- Sample format (default = "S16_LE")
    """
    Outboxes = { "outbox" : "raw audio samples",
                 "format" : "dictionary detailing sample_rate, sample_format and channels",
                 "signal" : "Shutdown signalling",
               }
    
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Input,self).__init__()
        
        pformat = format2PyMediaFormat[format]
        self.snd = sound.Input(sample_rate, channels, pformat)
        
        self.sample_rate = sample_rate
        self.channels = channels
        self.format = format
        
    def main(self):
        self.snd.start()
        
        format = {
            'channels'    : self.channels,
            'sample_rate' : self.sample_rate,
            'format'      : self.format,
        }
        self.send(format, "format")
        
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            raw = self.snd.getData()
            if raw and len(raw):
                data = str(raw)
                while data:
                    try:
                        self.send(data,"outbox")
                        data=None
                    except noSpaceInBox:
                        self.pause()
            else:
                self.pause(0.01)
                    
        self.snd.stop()


__kamaelia_components__ = ( Input, )

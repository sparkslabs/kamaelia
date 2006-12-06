#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
from Axon.Ipc import shutdownMicroprocess, producerFinished

import sys,os
sys.path.append(__file__[:1+__file__.rfind(os.sep)] + (".."+os.sep)*3 + "Timer")
#from Axon.ThreadedComponent import threadedcomponent
from ThreadedComponent import threadedcomponent


import time
from math import log

import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

from Support.PyMedia.AudioFormats import format2PyMediaFormat


class Input(threadedcomponent):
    Outboxes = { "outbox" : "raw audio samples",
                 "format" : "dictionary detailing sample_rate, sample_format and channels",
                 "signal" : "Shutdown signalling",
               }
    
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
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
            raw = str(self.snd.getData())
            self.send(raw,"outbox")
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
        self.snd.stop()

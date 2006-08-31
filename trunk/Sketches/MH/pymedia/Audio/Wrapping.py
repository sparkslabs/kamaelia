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
"""\
Components to:
* wrap raw audio samples into an audio 'frame' data structure
* unwrap audio 'frame' data structures into raw samples

"""
from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

class Unwrap(component):

    Inboxes = { "inbox"   : "Frames of audio data",
                "control" : "Shutdown signalling",
              }

    Outboxes = { "outbox"      : "Raw audio data",
                 "format"      : "Rest of data from audio frame (whenever it changes)",
                 "signal" : "Shutdown signalling",
               }

    def main(self):
        snd = None
        prevformat = None
        
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")

                newformat = { 'sample_rate' : data['sample_rate'],
                              'channels'    : data['channels'],
                              'format'      : data['format'],
                            }
                if newformat != prevformat:
                    prevformat = newformat
                    self.send(newformat, "format")

                self.send(data['audio'],       "outbox")

            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1


class Wrap(component):
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
        super(Wrap,self).__init__()
            
        self.sample_rate = sample_rate
        self.channels = channels
        self.format = format

    def main(self):
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                audio = self.recv("inbox")
                data = {}
                data['type'] = 'audio'
                data['audio'] = audio
                data['channels'] = self.channels
                data['sample_rate'] = self.sample_rate
                data['format'] = self.format
                self.send(data,"outbox")
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1

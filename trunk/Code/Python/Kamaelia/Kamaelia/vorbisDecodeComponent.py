#!/usr/bin/env python2.3
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
"""
Simple Vorbis Decoder Component, and Audio Playback Adaptor

"""
import Axon
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished
import vorbissimple
#import Kamaelia.AOPlayer
import sys
import time

import ao

class AOAudioPlaybackAdaptor(component):
   def __init__(self, id=None):
      super(AOAudioPlaybackAdaptor, self).__init__()
      self.dev = ao.AudioDevice("oss")

   def main(self):
      playing = True
      while playing:
         if self.dataReady("inbox"):
            buff = self.recv("inbox")
            self.dev.play(buff)
         else:
            if self.dataReady("control"):
               self.recv("control")
               sig = producerFinished(self)
               self.send(sig, "signal")
               playing = False
         yield 1

class VorbisDecode(component):
   def __init__(self, *args):
      super(VorbisDecode, self).__init__(*args)
      self.decoder = vorbissimple.vorbissimple()
      
   def main(self):
      decoding = True
      producerDone = False
      while decoding:
         try:
            data = self.decoder._getAudio()
            self.send(data, "outbox")
         except "RETRY":
            pass
         except "NEEDDATA":
            while not (self.dataReady("inbox") > 0) and not (self.dataReady("control") >0):
               if not producerDone:
                  self.pause()
                  yield 1

            if self.dataReady("inbox"):
               dataToSend = self.recv("inbox")
               self.decoder.sendBytesForDecode(dataToSend)
            
            if self.dataReady("control"):
               shutdownMessage = self.recv("control")
               sig = producerFinished(self)
               self.send(sig, "signal")
               producerDone = True # Necessary given next?
               decoding = False
   

if __name__ =="__main__":
   #
   # Simple Testing Spike
   #
   from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
   class testHarness(component):
      def __init__(self):
         super(testHarness, self).__init__()
         source = ReadFileAdaptor("./Support/ogg/khangman-splash.ogg",
                               readmode="bitrate", bitrate=400000)
         decoder = VorbisDecode()
         sink = AOAudioPlaybackAdaptor()
         self.source = source
         self.decoder = decoder
         self.sink = sink
         
      def initialiseComponent(self):
         self.addChildren(self.source,self.decoder,self.sink)
         
         self.link((self.source,"outbox"), (self.decoder,"inbox") )
         self.link((self.source,"signal"), (self.decoder, "control") )
         self.link((self.decoder,"outbox"), (self.sink,"inbox") )
         self.link((self.decoder,"signal"), (self.sink, "control") )
         self.link((self.sink,"signal"), (self, "control") )
         self.running = True
         return Axon.Ipc.newComponent(*(self.children))
         
      def mainBody(self):
            if self.dataReady("control"): # We always shutdown this way
               return 0
            return 1


   testHarness().activate()
   scheduler.run.runThreads()

#!/usr/bin/env python2.3
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
      self.__super.__init__()
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
      self.__super.__init__(*args)
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
         self.__super.__init__()
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

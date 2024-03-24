# -*- coding: utf-8 -*-

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

# Components for using Spee Encoding
#
# Based on original code by Devendra (original in /Sketches/DL/modules/Speex.py)
# with modifications to improve shutdown, and a few other things

raise NotImplementedError("Due to drift/bit rot, Speex libraries are not currently available for python")

from sys import path
import Axon
import speex
import Axon.ThreadedComponent

# class speex:
#     def new(klass,quality,raw):
#         return speex()
#     new = classmethod(new)
#     
#     def decode(self,data):
#         return data
#     
#     def encode(self,data):
#         return data

class SpeexEncode(Axon.ThreadedComponent.threadedcomponent):

    def __init__(self, quality=8):

        super(SpeexEncode, self).__init__()
        self.quality = quality
    
    def main(self):

        speexobj = speex.new(self.quality, raw=True)

        shutdown=False
        while self.dataReady("inbox") or not shutdown:
            if not self.dataReady("inbox"):
                print (".",)
            while self.dataReady("inbox"):

                 data = self.recv("inbox")
                 #print data
                 ret = speexobj.encode(data)

                 if ret != "":           # Speex objects use internal buffering
                   self.send(ret, "outbox")
#                   yield 1
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, (Axon.Ipc.shutdownMicroprocess,Axon.Ipc.producerFinished)):
                    shutdown=True
                self.send(msg,"signal")
            
            if not shutdown:
                self.pause()
#            yield 1

class SpeexDecode(Axon.ThreadedComponent.threadedcomponent):


    def __init__(self, quality=8):

        super(SpeexDecode, self).__init__()
        self.quality = quality
            
    def main(self):

        speexobj = speex.new(self.quality, raw=True)

        shutdown=False
        while self.dataReady("inbox") or not shutdown:
            while self.dataReady("inbox"):

                data = self.recv("inbox")
                ret = speexobj.decode(data)
                
                if ret:
                    self.send(ret, "outbox")
#                    yield 1

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, (Axon.Ipc.shutdownMicroprocess,Axon.Ipc.producerFinished)):
                    shutdown=True
                self.send(msg,"signal")
            
            if not shutdown:
                self.pause()
#            yield 1

__kamaelia_components__ = ( SpeexEncode, SpeexDecode, )


# Components for using Spee Encoding
#
# Based on original code by Devendra (original in /Sketches/DL/modules/Speex.py)
# with modifications to improve shutdown, and a few other things


import speex
#from Axon import ThreadedComponent
from Axon.Component import component
import Axon
from sys import path
path.append("../../MH/Timer")
import ThreadedComponent

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

class SpeexEncode(ThreadedComponent.threadedcomponent):

    def __init__(self, quality=8):

        super(SpeexEncode, self).__init__()
        self.quality = quality
    
    def main(self):

        speexobj = speex.new(self.quality, raw=True)

        shutdown=False
        while self.dataReady("inbox") or not shutdown:
            if not self.dataReady("inbox"):
                print ".",
            while self.dataReady("inbox"):

                 data = self.recv("inbox")
                 #print data
                 ret = speexobj.encode(data)

                 if ret is not "":           # Speex objects use internal buffering
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

class SpeexDecode(ThreadedComponent.threadedcomponent):


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

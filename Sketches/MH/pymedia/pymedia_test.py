#!/usr/bin/env python

# test to understand how pymedia 1.3.5 works

import time

filename="/home/matteh/music/Philip Glass/Solo Piano/01 - Metamorphosis One.mp3"
#filename="/home/matteh/music/Rodeohead.mp3"

extension = filename.split(".")[-1]
extension = extension.lower()

import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

import time
        
READSIZE=1000
        
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.Chassis.Pipeline import pipeline

class PyMediaAudioPlayer(component):
    
    def __init__(self,extension):
        super(PyMediaAudioPlayer,self).__init__()
        self.extension = extension

    def main(self):
        
        dm = muxer.Demuxer(extension)
        
        
        frame0 = True
        rawout=[]
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
        
                yield 1
                
                frames = dm.parse(data)
                
                yield 1
                
                for frame in frames:
                    yield 1
                    if frame0:
                        stream_index = frame[0]
                        dec = acodec.Decoder(dm.streams[stream_index])
                        raw = dec.decode(frame[1])
                        snd =sound.Output(raw.sample_rate, raw.channels, sound.AFMT_S16_LE)
                        self.send(snd,"outbox")
                        print len(dm.streams),raw.channels, raw.sample_rate
                        print dm.streams
                        print dm.getHeaderInfo()
                        frame0 = False
                        self.send(str(raw.data), "outbox")
                        
                    else:
                        raw = dec.decode(frame[1])
                        self.send(str(raw.data), "outbox")
        
            yield 1
        
class SoundOutput(component):
    def main(self):
        while not self.dataReady("inbox"):
            self.pause()
            yield 1
            
        snd = self.recv("inbox")
        
        #allraw = "".join(rawout)
        CHUNKSIZE=2048
        while 1:
            while self.dataReady("inbox"):
                chunk = self.recv("inbox")
                for i in xrange(0,len(chunk),CHUNKSIZE):
#                    t=time.time()
                    snd.play(chunk[i:i+CHUNKSIZE])
#                    print time.time()-t, snd.getSpace()
            yield 1

if __name__ == "__main__":
    pipeline( RateControlledFileReader(filename,readmode="bytes",rate=999999,chunksize=1024),
              PyMediaAudioPlayer(extension),
              SoundOutput(),
            ).run()
    
#!/usr/bin/env python

# test to understand how pymedia 1.3.5 works

import time

filename="/home/matteh/music/Philip Glass/Solo Piano/01 - Metamorphosis One.mp3"
filename="/home/matteh/music/Muse/Absolution/01 - Intro.mp3"
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

mapping_format_to_pymedia = {
    'AC3'       : sound.AFMT_AC3,
    'A_LAW'     : sound.AFMT_A_LAW,
    'IMA_ADPCM' : sound.AFMT_IMA_ADPCM,
    'MPEG'      : sound.AFMT_MPEG,
    'MU_LAW'    : sound.AFMT_MU_LAW,
    'S16_BE'    : sound.AFMT_S16_BE,
    'S16_LE'    : sound.AFMT_S16_LE,
    'S16_NE'    : sound.AFMT_S16_NE,
    'S8'        : sound.AFMT_S8,
    'U16_BE'    : sound.AFMT_U16_BE,
    'U16_LE'    : sound.AFMT_U16_LE,
    'U8'        : sound.AFMT_U8,
}

mapping_format_from_pymedia = dict([(v,k) for (k,v) in mapping_format_to_pymedia.items() ])


class PyMediaAudioPlayer(component):
    
    Outboxes = { "outbox" : "audio samples in data structures",
                 "signal" : "",
               }
               
    def __init__(self,extension):
        super(PyMediaAudioPlayer,self).__init__()
        self.extension = extension

    def main(self):
        
        dm = muxer.Demuxer(extension)
        
        
        frame0 = True
        shutdown=False
        while self.anyReady() or not shutdown:
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
                        frame0 = False
                        
                    raw = dec.decode(frame[1])
                        
                    data = {}
                    data['type'] = 'audio'
                    data['data'] = str(raw.data)
                    data['channels'] = raw.channels
                    data['sample_rate'] = raw.sample_rate
                    data['format'] = mapping_format_from_pymedia[sound.AFMT_S16_LE]
                    self.send(data,"outbox")
        
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1
        
class SoundOutput(component):
    def main(self):
        snd = None
        
        CHUNKSIZE=2048
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                if data['type'] == "audio":
                    if not snd:
                        snd =sound.Output(data['sample_rate'], data['channels'], data['format'])
                
                    chunk = data['data']
                
                    for i in xrange(0,len(chunk),CHUNKSIZE):
#                        t=time.time()
                        snd.play(chunk[i:i+CHUNKSIZE])
#                        print time.time()-t, snd.getSpace()
                yield 1
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1

class ExtractData(component):
    def main(self):
        snd = None
        
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data['data'],"outbox")
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1

class RawSoundOutput(component):
    def __init__(self, sample_rate=44050, channels=2, format="S16_LE"):
        super(RawSoundOutput,self).__init__()
        
        pformat = mapping_format_to_pymedia[format]
        self.snd = sound.Output(sample_rate, channels, pformat)
        
    def main(self):
        CHUNKSIZE=2048
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                chunk = self.recv("inbox")
                
                for i in xrange(0,len(chunk),CHUNKSIZE):
                    self.snd.play(chunk[i:i+CHUNKSIZE])
                yield 1
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1


if __name__ == "__main__":
    pipeline( RateControlledFileReader(filename,readmode="bytes",rate=999999,chunksize=1024),
              PyMediaAudioPlayer(extension),
#              SoundOutput(),
              ExtractData(),
              RawSoundOutput(),
            ).run()
    
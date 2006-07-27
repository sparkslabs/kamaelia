#!/usr/bin/env python

# test to understand how pymedia 1.3.5 works

import time


import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished


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


class AudioDecoder(component):
    """\
    AudioDecoder(fileExtension) -> new pymedia Audio Decoder.
    
    Send raw data from a compressed audio file (which had the specified extension)
    to the "inbox" inbox, and decompressed blocks of audio data (wrapped in a
    data structure) are emitted from the "outbox" outbox.
    
    Keyword  arguments:
    -- fileExtension  - The file extension (eg. "mp3" or "ogg") of the source (to allow the right codec to be chosen)
    """
    
    Outboxes = { "outbox" : "audio samples in data structures",
                 "signal" : "",
               }
               
    def __init__(self,fileExtension):
        super(AudioDecoder,self).__init__()
        self.extension = fileExtension.lower()

    def main(self):
        
        dm = muxer.Demuxer(extension)
        
        shutdown=False
        decoder=None
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
        
                yield 1
                
                frames = dm.parse(data)
                
                yield 1
                
                for frame in frames:
#                    yield 1
                    if not decoder:
                        stream_index = frame[0]
                        decoder = acodec.Decoder(dm.streams[stream_index])
                        
                    raw = decoder.decode(frame[1])
                        
                    data = {}
                    data['type'] = 'audio'
                    data['audio'] = str(raw.data)
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
    Outboxes = { "outbox" : "",
                 "signal" : "",
                 "_data"  : "raw audio samples going to outputter",
                 "_ctrl"  : "for shutting down an outputter",
               }
                
    def main(self):
        outputter = None
        format = None
        shutdown = False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                if data['type'] == "audio":
                    newformat = (data['sample_rate'], data['channels'], data['format'])
                    if newformat != format:
                        format=newformat
                        # need new audio playback component
                        # first remove any old one
                        if outputter:
                            self.removeChild(outputter)
                            self.send(producerFinished(), "_ctrl")
                            for l in linkages:
                                self.unlink(thelinkage=l)
                        # now make and wire in a new one
                        outputter = RawSoundOutput(*format).activate()
                        self.addChildren(outputter)
                        linkages = [ self.link( (self,"_data"), (outputter, "inbox") ),
                                     self.link( (self,"_ctrl"), (outputter, "control") ),
                                   ]
                
                    self.send(data['audio'], "_data")
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1

        if outputter:
            self.send(producerFinished(), "_ctrl")
            self.unlink(thelinkage=datalinkage)
            self.unlink(thelinkage=ctrllinkage)

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
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
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

class SoundInput(component):
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
        super(SoundInput,self).__init__()
        
        pformat = mapping_format_to_pymedia[format]
        self.snd = sound.Input(sample_rate, channels, pformat)
        
        self.sample_rate = sample_rate
        self.channels = channels
        self.format = format
        
    def main(self):
        self.snd.start()
        
        shutdown=False
        while self.anyReady() or not shutdown:
            raw = self.snd.getData()
            
            data={}
            data['type']        = 'audio'
            data['audio']       = str(raw)
            data['channels']    = self.channels
            data['sample_rate'] = self.sample_rate
            data['format']      = self.format
            
            self.send(data,"outbox")
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            yield 1

if __name__ == "__main__":
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.Chassis.Pipeline import pipeline

    filename="/home/matteh/music/Philip Glass/Solo Piano/01 - Metamorphosis One.mp3"
    #filename="/home/matteh/music/Muse/Absolution/01 - Intro.mp3"
    #filename="/home/matteh/music/Rodeohead.mp3"
    
    extension = filename.split(".")[-1]
        
    test = 1
    
    if test == 1:
        pipeline( RateControlledFileReader(filename,readmode="bytes",rate=999999,chunksize=1024),
                  AudioDecoder(extension),
                  SoundOutput(),
                ).run()
                
    elif test == 2:
        pipeline( RateControlledFileReader(filename,readmode="bytes",rate=999999,chunksize=1024),
                  AudioDecoder(extension),
                  ExtractData(),
                  RawSoundOutput(),
                ).run()
                
    elif test == 3:
        pipeline( SoundInput(),
                  SoundOutput(),
                ).run()


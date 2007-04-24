#!/usr/bin/env python

# test to understand how pymedia 1.3.5 works

import time


import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import sys
sys.path.append("../Timer")
#from Axon.ThreadedComponent import threadedcomponent
from ThreadedComponent import threadedcomponent

import pymedia.audio.sound as sound


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
        
        dm = muxer.Demuxer(self.extension)
        
        shutdown=False
        decoder=None
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
        
                frames = dm.parse(data)
                
                for frame in frames:
                    
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
            for linkage in linkages:
                self.unlink(thelinkage=linkage)

class ExtractData(component):
    def main(self):
        snd = None
        
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data['audio'],"outbox")
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1

class PackageData(component):
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
        super(PackageData,self).__init__()
            
        pformat = mapping_format_to_pymedia[format]
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
    

class RawSoundOutput(threadedcomponent):
    def __init__(self, sample_rate=44100, channels=2, format="S16_LE"):
        super(RawSoundOutput,self).__init__()
        
        pformat = mapping_format_to_pymedia[format]
        self.snd = sound.Output(sample_rate, channels, pformat)
        
        self.chunksize = sample_rate/40    # no idea why, but it seems we need to pass to pymedia chunks of a sufficiently short duration to prevent playback artefacts
        mask = 4*channels-1
#        self.chunksize = self.chunksize - (self.chunksize & mask) # ensure whole number of samples
        from math import log
        # round to nearest power of 2
        self.chunksize = 2**int(log(self.chunksize)/log(2))
        
    def main(self):
        CHUNKSIZE=self.chunksize
        shutdown=False
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                print "RawSoundOutput:",self.dataReady("inbox")
                chunk = self.recv("inbox")
                
                for i in range(0,len(chunk),CHUNKSIZE):
                    self.snd.play(chunk[i:i+CHUNKSIZE])
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
#            if not shutdown:
#                self.pause()
            
        self.snd.stop()

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
            
        self.snd.stop()

class AudioEncoder(component):
    def __init__(self, codec, bitrate, sample_rate, channels, **otherparams):
        super(AudioEncoder,self).__init__()
        
        params = { 'id'          : acodec.getCodecID(codec),
                   'bitrate'     : bitrate,
                   'sample_rate' : sample_rate,
                   'channels'    : channels 
                 }
        params.update(otherparams)
                 
        self.params = params
        self.codec = codec
        
    def main(self):
        mux = muxer.Muxer( self.codec )
        streamId = mux.addStream( muxer.CODEC_TYPE_AUDIO, self.params )
        enc = acodec.Encoder(self.params)
        
        data = mux.start()
        if data:
            self.send(data,"outbox")
        
        shutdown=False
        data=""
        MINSIZE=4096
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                newdata= self.recv("inbox")
                data = data+newdata['audio']
                if len(data)>=MINSIZE:
                    frames = enc.encode( data )
                    
                    for frame in frames:
                        muxed = mux.write( streamId, frame )
                        if muxed:
                            self.send(muxed, "outbox")
                            
                    data=""
        
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1
        
        data = mux.end()
        if data:
            self.send(data,"outbox")
        

class ResampleTo(component):
    Inboxes  = { "inbox" : "",
                 "control" : "",
                 "_resampled" : "",
               }
    Outboxes = { "outbox" : "",
                 "signal" : "",
                 "_data"  : "raw audio samples going to resampler",
                 "_ctrl"  : "for shutting down an resampler",
               }
    def __init__(self, sample_rate, channels):
        super(ResampleTo,self).__init__()
        self.params = (sample_rate, channels)

                
    def main(self):
        resampler = None
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
                        if resampler:
                            self.removeChild(resampler)
                            self.send(producerFinished(), "_ctrl")
                            for l in linkages:
                                self.unlink(thelinkage=l)
                        # now make and wire in a new one
                        resampler = RawResampleTo(format[0],format[1], *self.params).activate()
                        self.addChildren(resampler)
                        linkages = [ self.link( (self,"_data"), (resampler, "inbox") ),
                                     self.link( (self,"_ctrl"), (resampler, "control") ),
                                     self.link( (resampler,"outbox"), (self, "_resampled") ),
                                   ]
                
                    self.send(data['audio'], "_data")
            
            while self.dataReady("_resampled"):
                audio = self.recv("_resampled")
                data = {}
                data['type'] = 'audio'
                data['sample_rate'] = self.params[0]
                data['channels'] = self.params[1]
                data['format'] =  format[2]
                data['audio'] = audio
                self.send(data,"outbox")
            
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1

        if resampler:
            self.send(producerFinished(), "_ctrl")
            for linkage in linkages:
                self.unlink(thelinkage=linkage)

class RawResampleTo(component):
    def __init__(self, from_sample_rate, from_channels, to_sample_rate, to_channels):
        super(RawResampleTo,self).__init__()
        
        self.resampler = sound.Resampler( (from_sample_rate, from_channels), (to_sample_rate, to_channels) )
        
    def main(self):
        shutdown=False
        data=""
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                resampled = str(self.resampler.resample(data))
                self.send(resampled, "outbox")
        
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1
        


class SimpleDelay(component):
    def main(self):
        buffer = []
        while len(buffer) < 5:
            while self.dataReady("inbox"):
                buffer.append(self.recv("inbox"))
            self.pause()
            yield 1
            
        while buffer:
            self.send(buffer[0],"outbox")
            buffer.pop(0)
            
        while 1:
            while self.dataReady("inbox"):
                self.send(self.recv("inbox"),"outbox")
            self.pause()
            yield 1

if __name__ == "__main__":
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.Chassis.Pipeline import pipeline

    filename="/home/matteh/music/Philip Glass/Solo Piano/01 - Metamorphosis One.mp3"
    #filename="/home/matteh/music/Muse/Absolution/01 - Intro.mp3"
    #filename="/home/matteh/music/Rodeohead.mp3"
    
    extension = filename.split(".")[-1]
        
    test = 3
    
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
                  AudioEncoder(codec="mp3", bitrate=128000, sample_rate=44100, channels=2),
                  AudioDecoder("mp3"),
#                  SimpleDelay(),
                  SoundOutput(),
                ).run()

    elif test == 4:
        pipeline( RateControlledFileReader(filename,readmode="bytes",rate=999999,chunksize=1024),
                  AudioDecoder("mp3"),
                  ResampleTo(sample_rate=8000,channels=1),
                  SoundOutput(),
                ).run()
    elif test == 5:
        pipeline( RateControlledFileReader(filename,readmode="bytes",rate=999999,chunksize=1024),
                  AudioDecoder("mp3"),
                  SoundOutput(),
                ).activate()
        pipeline( RateControlledFileReader("/home/matteh/music/Muse/Absolution/03 - Time Is Running Out.mp3",readmode="bytes",rate=999999,chunksize=1024),
                  AudioDecoder("mp3"),
                  SoundOutput(),
                ).run()


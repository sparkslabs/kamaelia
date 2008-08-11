#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
============================
Multi-source Raw Audio Mixer
============================

A component that mixes raw audio data from an unknown number of sources, that
can change at any time. Audio data from each source is buffered until a minimum
threshold amount, before it is included in the mix. The mixing operation is a
simple addition. Values are not scaled down.



Example Usage
-------------

Mixing up to 3 sources of audio (sometimes a source is active, sometimes it
isn't)::

    Graphline(
        MIXER = RawAudioMixer( sample_rate=8000,
                               channels=1,
                               format="S16_LE",
                               readThreshold=1.0,
                               bufferingLimit=2.0,
                               readInterval=0.1),
                             ),
        A = pipeline( SometimesOn_RawAudioSource(), Entuple(prefix="A") ),
        B = pipeline( SometimesOn_RawAudioSource(), Entuple(prefix="B") ),
        C = pipeline( SometimesOn_RawAudioSource(), Entuple(prefix="C") ),
            
        OUTPUT = RawSoundOutput( sample_rate=8000,
                                 channels=1
                                 format="S16_LE",
                               ),
               linkages = {
                   (A, "outbox") : (MIXER, "inbox"),
                   (B, "outbox") : (MIXER, "inbox"),
                   (C, "outbox") : (MIXER, "inbox"),
                   
                   (MIXER, "outbox") : (OUTPUT, "inbox"),
               },
             ).run()

Each source is buffered for 1 second before it is output. If more than 2 seconds
of audio are buffered, then samples are dropped.



How does it work?
-----------------

Send (id, raw-audio) tuples to RawAudioMixer's inbox. Where 'id' is any value
that uniquely distinguishes each source of audio.

RawAudioMixer buffers each source of audio, and mixes them together additively,
outputting the resulting stream of audio data.

Constructor arguments:
   
   * sample_rate, channels, format
     The format of audio to be mixed. The only format understood at the moment
     is "S16_LE"
    
   * readThreshold
     number of seconds of audio that will be buffered before RawAudioMixer
     starts mixing it into its output.
     
   * bufferingLimit
     maximum number of seconds of audio that will be buffered. If more piles up
     then some audio will be lost.

   * readInterval
     number of seconds between each time RawAudioMixer outputs a chunk of audio
     data.

RawAudioMixer buffers each source of audio separately. If the amount of audio in
any buffer exceeds the 'buffering limit' then the oldest samples buffered will
be lost.

When one or more buffered sources reaches the 'read threshold' then they are
mixed together and output. How often audio is output is determined by setting
the 'read Interval'.

Mixing is done additively and is *not* scaled down (ie. it is a sum() function,
not an average() ). Therefore, ensure that the sum of the sources being mixed
does not exceed the range of values that samples can take.

Why the buffering, thresholds, and read intervals? It is done this way so that
RawAudioMixer can mix without needing to know what sources of audio there are,
and whether they are running or stopped. It also enables RawAudioMixer to cope
with audio data arriving from different sources at different times.

You may introduce new audio sources at any time - simply send audio data tagged
with a new, unique identifier.

You may stop an audio source at any time too - simply stop sending audio data.
The existing buffered data will be output, until there is not left.

If there is not enough audio in any of the buffers (or perhaps there are no
sources of audio) then RawAudioMixer will not output anything, not even
'silence'.

If a shutdownMicroprocess or producerFinished message is received on this
component's "control" inbox this component will cease reading in data from any
audio sources. If it is currently outputting audio from any of its buffers, it
will continue to do so until these are empty. The component will then forward
on the shutdown message it was sent, out of its "signal" outbox and immediately
terminate.


TODO:

    * Needs a timeout mechanism to discard very old data (otherwise this is
      effectively a memory leak!)
      
      - If an audio source sends less than the readThreshold amount of audio
        data, then stops; then this data never gets flushed out.
"""

from Axon.Ipc import shutdownMicroprocess, producerFinished
import time as _time

# want pausing capability in threadedcomponent
import sys
from Axon.ThreadedComponent import threadedcomponent


class AudioBuffer(object):
    """\
    AudioBuffer(activationThreshold, sizeLimit) -> new AudioBuffer component.
    
    Doesn't 'activate' until threshold amount of data arrives. Until it does,
    attempts to read data will just return nothing.
    
    
    Keyword arguments:
        
    -- activationThreshold  - Point at which the buffer is deemed activated
    -- sizeLimit            - Filling the buffer beyond this causes samples to be dropped
    """
    def __init__(self, activationThreshold, sizeLimit, silence):
        super(AudioBuffer,self).__init__()
        self.size = 0
        self.sizeLimit = sizeLimit
        self.activationThreshold = activationThreshold
        self.buffer = []
        self.active = False
        self.silence = silence

    def __len__(self):
        # return how much data there is
        return self.size

    def append(self, newdata):
        # add new data to the buffer, if there is too much, drop the oldest data
        
        self.buffer.append(newdata)
        self.size += len(newdata)

        if self.size >= self.activationThreshold:
            self.active = True

        if self.size > self.sizeLimit:
            self.drop(self.size - self.sizeLimit)


    def drop(self,amount):
        self.size -= amount
        while amount > 0:
            fragment = self.buffer[0]
            if len(fragment) <= amount:
                amount -= len(fragment)
                del self.buffer[0]
            else:
                self.buffer[0] = fragment[amount:]
                amount = 0
        self.size -= amount

    def pop(self, amount):
        if not self.active:
            return ""
        
        data = []

        padding_silence = ""
        if amount > self.size:
            padding_silence = self.silence * ((amount-self.size)/len(self.silence))
            amount = self.size

        self.size -= amount
        
        while amount > 0:
            fragment = self.buffer[0]
            if len(fragment) <= amount:
                data.append(fragment)
                amount -= len(fragment)
                del self.buffer[0]
            else:
                data.append(fragment[:amount])
                self.buffer[0] = fragment[amount:]
                amount = 0

        data.append(padding_silence)
        
        if self.size==0:
            self.active = False
        
        return "".join(data)



class RawAudioMixer(threadedcomponent):
    """\
    RawAudioMixer([sample_rate][,channels][,format][,readThreshold][,bufferingLimit][,readInterval]) -> new RawAudioMixer component.
    
    Mixes raw audio data from an unknown number of sources, that
    can change at any time. Audio data from each source is buffered until a minimum
    threshold amount, before it is included in the mix. The mixing operation is a
    simple addition. Values are not scaled down.
    
    Send (uniqueSourceIdentifier, audioData) tuples to the "inbox" inbox and
    mixed audio data will be sent out of the "outbox" outbox.
    
    Keyword arguments:
    
    - sample_rate     -- The sample rate of the audio in Hz (default=8000)
    - channels        -- Number of channels in the audio (default=1)
    - format          -- Sample format of the audio (default="S16_LE")
    - readThreshold   -- Duration to buffer audio before it starts being used in seconds (default=1.0)
    - bufferingLimit  -- Maximum buffer size for each audio source in seconds (default=2.0)
    - readInterval    -- Time between each output chunk in seconds (default=0.1)
    """
    
    def __init__(self, sample_rate=8000, channels=1, format="S16_LE",
                       readThreshold=1.0, bufferingLimit=2.0, readInterval=0.1):
        super(RawAudioMixer,self).__init__()
        self.sample_rate = sample_rate
        self.bufferingLimit = bufferingLimit
        self.readThreshold = readThreshold
        self.readInterval = readInterval

        if format=="S16_LE":
            self.mix     = self.mix_S16_LE
            self.quanta  = channels*2 # bytes per sample
            self.silence = "\0\0"
        else:
            raise "Format '"+str(format)+"' not (yet) supported. Sorry!"
        

    def checkForShutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return msg
            else:
                self.send(msg,"signal")
        return False
        
    def main(self):
        buffers = {}
        
        self.MAXBUFSIZE = int(self.sample_rate*self.bufferingLimit*self.quanta)
        self.BUFTHRESHOLD = int(self.sample_rate*self.readThreshold*self.quanta)
        
        READCHUNKSIZE = int(self.sample_rate*self.readInterval)*self.quanta

        shutdown = False
        while not shutdown:
            
            # whilst none of the buffers are active (ie. full enough to start reading out data)
            anyActive=False
            while not anyActive and not shutdown:
            
                while self.dataReady("inbox") and not anyActive:
                    activated = self.fillBuffer(buffers, self.recv("inbox"))
                    anyActive = anyActive or activated

                shutdown = shutdown or self.checkForShutdown()
                if shutdown:
                    break
                
                if not anyActive:
                    self.pause()
                    
            # switch to reading from buffers (active) mode
            nextReadTime = _time.time()
            
            # dump out audio until all buffers are empty
            while len(buffers) and not shutdown:

                # if we're not shutting down, and its not yet time to output audio
                # then read in more data into the buffers
                while not shutdown and self.dataReady("inbox") and _time.time() < nextReadTime:
                    reading = self.fillBuffer(buffers, self.recv("inbox"))
                
                now = _time.time()
                if now >= nextReadTime:
                    
                    # read from all buffers (only active ones output samples)
                    audios = []
                    for buf in buffers.keys():
                        audio = buffers[buf].pop(READCHUNKSIZE)
                        if audio:
                            audios.append(audio)
                            
                        # delete any empty buffers
                        if not len(buffers[buf]):
                            del buffers[buf]
                            
                    # assuming we've got something, mix it and output it
                    if audios:
                        self.send(self.mix(audios, READCHUNKSIZE), "outbox")
                
                    nextReadTime += self.readInterval
                    
                shutdown = shutdown or self.checkForShutdown()
                if shutdown:
                    break
                
                if len(buffers) and not self.dataReady("inbox"):
                    self.pause( nextReadTime - _time.time() )
                
            # now there are no active buffers, go back to reading mode
            # (or terminate!)
            
        if shutdown:
            self.send(shutdown, "signal")
            
    def fillBuffer(self, buffers, data):
        srcId, audio = data
        
        try:
            buf = buffers[srcId]
        except KeyError:
            buf = AudioBuffer(self.BUFTHRESHOLD,self.MAXBUFSIZE, self.silence)
            buffers[srcId] = buf
            
        buf.append(audio)
        
        return buf.active
        
    
    def mix_S16_LE(self,sources, amount):
        output = []
        for i in xrange(0,amount,2):
            sum=0
            for src in sources:
                value = ord(src[i]) + (ord(src[i+1]) << 8)
#                sum += value - ((value&0x8000) and 65536)
                if value & 0x8000:
                    value -= 65536
                sum += value
            output.append( chr(sum & 255)+chr((sum>>8) & 255) )
        return "".join(output)


__kamaelia_components__ = ( RawAudioMixer, )

#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
==========================================
Reading and writing simple WAV audio files
==========================================

The WavParser and WavWriter components
"""

# WavWriter is based on ryan's PCMToWave component, modified to match WAVParser's formats for
# conveying samplerate, channels etc
#
# also takes binary sample data, instead of integer samples


from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
from Axon.AxonExceptions import noSpaceInBox

import struct
import string


class WavParser(component):

    Outboxes = { "outbox":"",
                 "signal":"",
                 "sample_format":"",
                 "channels":"",
                 "sample_rate":"",
                 "all_meta":"",
               }

    def __init__(self):
        super(WavParser,self).__init__()
        self.remainder = ""
        self.shutdownMsg = None
    
    def checkShutdown(self):
        while self.dataReady("control"):
            newMsg = self.recv("control")
            if isinstance(newMsg, shutdownMicroprocess):
                self.shutdownMsg = newMsg
            elif self.shutdownMsg is None and isinstance(newMsg, producerFinished):
                self.shutdownMsg = newMsg
        if isinstance(self.shutdownMsg, shutdownMicroprocess):
            return "NOW"
        elif self.shutdownMsg is not None:
            return "WHENEVER"
        else:
            return None
        
    def readline(self):
        bytes = []
        newdata = self.remainder
        index = newdata.find("\x0a")
        while index==-1:
            bytes.append(newdata)
            while not self.dataReady("inbox"):
                if self.checkShutdown():
                    self.bytesread=""
                    return
                self.pause()
                yield 1
            newdata = self.recv("inbox")
            index = newdata.find("\x0a")
            
        tail = newdata[:index+1]
        self.remainder = newdata[index+1:]
        bytes.append(tail)
        
        self.bytesread = "".join(bytes)
        return
    
    
    def readbytes(self,size):
        buf = [self.remainder]
        bufsize = len(self.remainder)
        while bufsize < size:
            if self.dataReady("inbox"):
                newdata = self.recv("inbox")
                buf.append(newdata)
                bufsize += len(newdata)
            shutdown = self.checkShutdown()
            if shutdown == "NOW" or (shutdown and not self.dataReady("inbox") and bufsize<size):
                self.bytesread=""
                return
            if bufsize<size and not self.anyReady():
                self.pause()
            yield 1
            
        excess = bufsize-size
        if excess:
            wanted = buf[:-1]
            tail, self.remainder = buf[-1][:-excess], buf[-1][-excess:]
            wanted.append(tail)
        else:
            wanted = buf
            self.remainder = ""
        
        self.bytesread = "".join(wanted)
        return
    
    def safesend(self, data, boxname):
        while 1:
            try:
                self.send(data, boxname)
                break
            except noSpaceInBox:
                if self.checkShutdown() == "NOW":
                    return
                self.pause()
                yield 1
    
    
    def readuptobytes(self,size):
        while self.remainder == "":
            if self.dataReady("inbox"):
                self.remainder = self.recv("inbox")
            else:
                shutdown = self.checkShutdown()
                if shutdown == "NOW" or (shutdown and not self.dataReady("inbox")):
                    break
            if self.remainder == "":
                self.pause()
            yield 1

        self.bytesread = self.remainder[:size]
        self.remainder = self.remainder[size:]


    
    def main(self):
        # parse header
        for _ in self.readbytes(16): yield _
        if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
            self.send(self.shutdownMsg,"signal")
            return
        riff,filesize,wavfmt = struct.unpack("<4sl8s",self.bytesread)
        assert(riff=="RIFF" and wavfmt=="WAVEfmt ")

        for _ in self.readbytes(20): yield _
        if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
            self.send(self.shutdownMsg,"signal")
            return
        filesize -= 24

        chunksize, format, channels, sample_rate, bytesPerSec, blockAlign, bitsPerSample = struct.unpack("<lhHLLHH", self.bytesread)

        headerBytesLeft = 16 - chunksize

        if format == 1: # uncompressed audio
            if bitsPerSample <= 8:
                audioformat = "S8"
                blocksize=1*channels
            elif bitsPerSample <= 16:
                audioformat = "S16_LE"
                blocksize=2*channels
            else:
                raise "Can't handle WAV file with "+str(bitsPerSample)+"bits per sample"

            if blocksize != blockAlign:
                raise "Can't handle WAV files with awkward block alignment padding between *every* sample!"

            self.send(channels,"channels")
            self.send(audioformat,"sample_format")
            self.send(sample_rate,"sample_rate")

            self.send( {"channels"      : channels,
                        "sample_format" : audioformat,
                        "sample_rate"   : sample_rate,
                       }, "all_meta")

        else:
            raise "Can't handle WAV file in anything other than uncompressed format. Format tag found = "+str(format)

        # skip any excess header bytes
        if headerBytesLeft > 0:
            for _ in self.readbytes(headerBytesLeft): yield _
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                self.send(self.shutdownMsg,"signal")
                return
            
        filesize-=headerBytesLeft

        # hunt for the DATA chunk
        while 1:
            for _ in self.readbytes(8): yield _
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                self.send(self.shutdownMsg,"signal")
                return
            chunk, size = struct.unpack("<4sl",self.bytesread)
            if chunk=="data":
                break
            
            # skip over this chunk; if the size is odd, then take into account a postfixed padding byte
            if (size % 1):
                size+=1
            for _ in self.readbytes(size): yield _
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                self.send(self.shutdownMsg,"signal")
                return
            filesize-=size+8

        # we're now in a data chunk
        # we can read to our hearts content, until we reach the end
        if size<=0:
            size=-1
        while size!=0:
            if size>0:
                for _ in self.readuptobytes(size): yield _
            else:
                for _ in self.readuptobytes(32768): yield _
            self.send(self.bytesread,"outbox")
            size-=len(self.bytesread)
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                self.send(self.shutdownMsg,"signal")
                return


        if self.shutdownMsg:
            self.send(self.shutdownMsg, "signal")
        else:
            self.send(producerFinished(), "signal")




class WavWriter(component):
    def __init__(self, channels, sample_format, sample_rate):
        super(WavWriter, self).__init__()
        if sample_format == "S8":
            self.bitsPerSample = 8
            self.bytespersample = 1
        elif sample_format == "S16_LE":
            self.bitsPerSample = 16
            self.bytespersample = 2
        else:
            raise "WavWriter can't handle sample format "+str(sample_format)+" at the moment"
        
        self.samplingfrequency = sample_rate
        self.channels = channels
        
    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
    
    def waitSend(self,data,boxname):
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                if self.mustStop():
                    raise "STOP"

    def main(self):
        self.shutdownMsg=None
        
        try:
            #we don't know the length yet, so we say the file lasts an arbitrary (long) time 
            riffchunk = "RIFF" + struct.pack("<L", 0x0) + "WAVE"
            
            bytespersecond = self.bytespersample * self.channels * self.samplingfrequency
            
            formatchunk = "fmt "
            formatchunk += struct.pack("<L", self.bitsPerSample)
            formatchunk += struct.pack("<H", 0x01) #PCM/Linear quantization
            formatchunk += struct.pack("<H", self.channels) 
            formatchunk += struct.pack("<L", self.samplingfrequency)
            formatchunk += struct.pack("<L", bytespersecond)
            formatchunk += struct.pack("<H", self.bytespersample * self.channels)
            formatchunk += struct.pack("<H", self.bitsPerSample)
        
            datachunkheader = "data" + struct.pack("<L", 0x0) #again, an arbitrary (large) value
            
            for _ in self.waitSend(riffchunk + formatchunk + datachunkheader, "outbox"):
                yield 1
            
            running = True
            while running:
                yield 1
                
                while self.dataReady("inbox"): # we accept binary sample data in strings
                    sampledata = self.recv("inbox")
                    for _ in self.waitSend(sampledata, "outbox"):
                        yield 1
                    
                if self.canStop():
                    raise "STOP"
                        
                self.pause()

        except "STOP":
            self.send(self.shutdownMsg,"signal")




if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    from Kamaelia.Audio.PyMedia.Output import Output
    from Kamaelia.Chassis.Carousel import Carousel
    from Kamaelia.Chassis.Graphline import Graphline
    
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.File.Writing import SimpleFileWriter

    print "Reading in WAV file, parsing it, then writing it out as test.wav ..."
    Graphline(
        READ  = RateControlledFileReader("/usr/share/sounds/alsa/Front_Center.wav",readmode="bytes",rate=1000000),
        PARSE = WavParser(),
        ENC   = Carousel(lambda meta : WavWriter(**meta)),
        WRITE = SimpleFileWriter("test.wav"),
        linkages = {
            ("READ", "outbox") : ("PARSE", "inbox"),
            ("PARSE", "outbox") : ("ENC", "inbox"),
            ("PARSE", "all_meta") : ("ENC", "next"),
            ("ENC", "outbox") : ("WRITE", "inbox"),
            
            ("READ", "signal") : ("PARSE", "control"),
            ("PARSE", "signal") : ("ENC", "control"),
            ("ENC", "signal") : ("WRITE", "control"),
        },
    ).run()

    print "Reading in test.wav and playing it back ..."
    Graphline(
        SRC = RateControlledFileReader("test.wav",readmode="bytes",rate=44100*4),
        WAV = WavParser(),
        DST = Carousel(lambda meta:     
            Output(sample_rate=meta['sample_rate'],format=meta['sample_format'],channels=meta['channels'])
            ),
        linkages = {
            ("SRC","outbox") : ("WAV","inbox"),
            ("SRC","signal") : ("WAV","control"),
            ("WAV","outbox") : ("DST","inbox"),
            ("WAV","signal") : ("DST","control"),
            ("WAV","all_meta") : ("DST","next"),
        }
        ).run()


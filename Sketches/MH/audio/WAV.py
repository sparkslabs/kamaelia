#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import WaitComplete
from Axon.Ipc import shutdownMicroprocess, producerFinished
import struct


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
            msg = self.recv("control")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return msg
        return False
        
    def readline(self):
        bytes = []
        newdata = self.remainder
        index = newdata.find("\x0a")
        while index==-1:
            bytes.append(newdata)
            while not self.dataReady("inbox"):
                shutdownmsg = self.checkShutdown()
                if shutdownmsg:
                    self.bytesread = ""
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
            else:
                shutdownmsg = self.checkShutdown()
                if shutdownmsg:
                    self.bytesread = ""
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
    
    
    def ignorebytes(self,size):
        buf = [self.remainder]
        bufsize = len(self.remainder)
        while bufsize < size:
            if self.dataReady("inbox"):
                newdata = self.recv("inbox")
                buf.append(newdata)
                bufsize += len(newdata)
            else:
                shutdownmsg = self.checkShutdown()
                if shutdownmsg:
                    self.bytesread = ""
                    return
            if bufsize<size and not self.anyReady():
                self.pause()
            yield 1
            
        excess = bufsize-size
        if excess:
            self.remainder = buf[-1][-excess:]
        else:
            self.remainder = ""
        
        self.bytesread = ""
        return
    
    def readuptobytes(self,size):
        while self.remainder == "":
            if self.dataReady("inbox"):
                self.remainder = self.recv("inbox")
            else:
                shutdownmsg = self.checkShutdown()
                if shutdownmsg:
                    self.bytesread = ""
                    return
            if self.remainder == "":
                self.pause()
            yield 1

        self.bytesread = self.remainder[:size]
        self.remainder = self.remainder[size:]


    
    def main(self):
        # parse header
        yield WaitComplete(self.readbytes(16))
        riff,filesize,wavfmt = struct.unpack("<4sl8s",self.bytesread)
        assert(riff=="RIFF" and wavfmt=="WAVEfmt ")

        yield WaitComplete(self.readbytes(20))
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
            yield WaitComplete(self.readbytes(headerBytesLeft))
            
        filesize-=headerBytesLeft

        # hunt for the DATA chunk
        while 1:
            yield WaitComplete(self.readbytes(8))
            chunk, size = struct.unpack("<4sl",self.bytesread)
            if chunk=="data":
                break
            
            # skip over this chunk; if the size is odd, then take into account a postfixed padding byte
            if (size % 1):
                size+=1
            yield WaitComplete(self.readbytes(size))
            filesize-=size+8

        # we're now in a data chunk
        # we can read to our hearts content, until we reach the end
        if size<=0:
            size=-1
        while size!=0:
            yield WaitComplete(self.readuptobytes(size))
            self.send(self.bytesread,"outbox")
            size-=len(self.bytesread)


        if self.shutdownMsg:
            self.send(self.shutdownMsg, "signal")
        else:
            self.send(producerFinished(), "signal")





if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    from Kamaelia.Audio.PyMedia.Output import Output
    
    Pipeline( RateControlledFileReader("/usr/share/sounds/alsa/Front_Center.wav",readmode="bytes",rate=44100*4),
              WavParser(),
              Output(sample_rate=44100/2,format="S16_LE",channels=2),
            ).run()

#!/usr/bin/env python

from Axon.Component import component
#from Axon.Ipc import WaitComplete
from Axon.Ipc import shutdownMicroprocess, producerFinished
from Axon.AxonExceptions import noSpaceInBox
import re
from Kamaelia.Support.Data.Rationals import rational



class YUV4MPEGToFrame(component):
    def __init__(self):
        super(YUV4MPEGToFrame,self).__init__()
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
                return
            except noSpaceInBox:
                if self.checkShutdown() == "NOW":
                    return
                self.pause()
                yield 1
            
    
    def main(self):
        # parse header
        for _ in self.readline(): yield _
        if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
            self.send(self.shutdownMsg,"signal")
            return
        line = self.bytesread
        m = re.match("^YUV4MPEG2((?: .\S*)*)\n$", line)
        assert(m)
        fields = m.groups()[0]
        seq_params = parse_seq_tags(fields)
        
        yield 1
            
        while 1:
            for _ in self.readline(): yield _
            line = self.bytesread
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                break
            m = re.match("^FRAME((?: .\S*)*)\n$", line)
            assert(m)
            fields = m.groups()[0]
            frame_params = parse_frame_tags(fields)
            
            ysize = seq_params["size"][0] * seq_params["size"][1]
            csize = seq_params["chroma_size"][0] * seq_params["chroma_size"][1]
            
            for _ in self.readbytes(ysize): yield _
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                break
            y = self.bytesread
            
            for _ in self.readbytes(csize): yield _
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                break
            u = self.bytesread
            
            for _ in self.readbytes(csize): yield _
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and self.bytesread==""):
                break
            v = self.bytesread
            
            frame = { "yuv" : (y,u,v) }
            frame.update(seq_params)
            frame.update(frame_params)
            for _ in self.safesend(frame,"outbox"): yield _
            if self.checkShutdown() == "NOW" or (self.checkShutdown() and not self.dataReady("inbox")):
                break
            yield 1

        if self.shutdownMsg:
            self.send(self.shutdownMsg, "signal")
        else:
            self.send(producerFinished(), "signal")



def parse_seq_tags(fields):
    params = {}
    tags = {}
    while fields:
        m = re.match("^ (.)(\S*)(.*)$", fields)
        (tag,value,fields) = m.groups()
        tags[tag] = value
        
    if "W" in tags and "H" in tags:
        params['size'] = (int(tags["W"]), int(tags["H"]))
    else:
        raise
    
    if "C" in tags:
        C = tags["C"]
        if   C == "420jpeg":  # 4:2:0 with JPEG/MPEG-1 siting (default) 
            params['pixformat'] = "YUV420_planar"
            params['chroma_size'] = (params['size'][0]/2, params['size'][1]/2)
        elif C == "420mpeg2": # 4:2:0 with MPEG-2 siting 
            params['pixformat'] = "YUV420_planar"
            params['chroma_size'] = (params['size'][0]/2, params['size'][1]/2)
        elif C == "420paldv": # 4:2:0 with PAL-DV siting 
            params['pixformat'] = "YUV420_planar"
            params['chroma_size'] = (params['size'][0]/2, params['size'][1]/2)
        elif C == "411":      # 4:1:1, cosited 
            params['pixformat'] = "YUV411_planar"
            params['chroma_size'] = (params['size'][0]/4, params['size'][1])
        elif C == "422":      # 4:2:2, cosited 
            params['pixformat'] = "YUV422_planar"
            params['chroma_size'] = (params['size'][0]/2, params['size'][1])
        elif C == "444":      # 4:4:4 (no subsampling) 
            params['pixformat'] = "YUV444_planar"
            params['chroma_size'] = (params['size'][0], params['size'][1])
        elif C == "444alpha": # 4:4:4 with an alpha channel 
            params['pixformat'] = "YUV4444_planar"
            params['chroma_size'] = (params['size'][0], params['size'][1])
        elif C == "mono":     # luma (Y') plane only
            params['pixformat'] = "Y_planar"
            params['chroma_size'] = (0,0)
    else:
        params['pixformat'] = "YUV420_planar"
        params['chroma_size'] = (params['size'][0]/2, params['size'][1]/2)
        
    if "I" in tags:
        I = tags["I"]
        if   I == "?":        # unknown (default) 
            pass
        elif I == "p":        # progressive/none 
            params["interlaced"] = False
        elif I == "t":        # top-field-first 
            params["interlaced"] = True
            params["topfieldfirst"] = True
        elif I == "b":        # bottom-field-first 
            params["interlaced"] = True
            params["topfieldfirst"] = False
        elif I == "m":        # mixed-mode: refer to 'I' tag in frame header
            pass
        
    if "F" in tags:
        m = re.match("^(\d+):(\d+)$",tags["F"])
        num, denom = float(m.groups()[0]), float(m.groups()[1])
        if denom > 0:
            params["frame_rate"] = num/denom
    
    if "A" in tags:
        m = re.match("^(\d+):(\d+)$",tags["A"])
        num, denom = float(m.groups()[0]), float(m.groups()[1])
        if denom > 0:
            params["pixel_aspect"] = num/denom
    
    if "X" in tags:
        params["sequence_meta"] = tags["X"]
    
    return params



def parse_frame_tags(fields):
    params = {}
    tags = {}
    while fields:
        m = re.match("^ (.)(\S*)(.*)$", fields)
        (tag,value,fields) = m.groups()
        tags[tag] = value
        
    if "I" in tags:
        x,y,z = tags["I"][0], tags["I"][1], tags["I"][2]
        if   x == "t":        # top-field-first 
            params["interlaced"] = True
            params["topfieldfirst"] = True
        elif x == "T":        # top-field-first and repeat
            params["interlaced"] = True
            params["topfieldfirst"] = True
        elif x == "b":        # bottom-field-first 
            params["interlaced"] = True
            params["topfieldfirst"] = False
        elif x == "B":        # bottom-field-first and repeat
            params["interlaced"] = True
            params["topfieldfirst"] = False
        elif x == "1":        # single progressive frame
            params["interlaced"] = False
        elif x == "2":        # double progressive frame (repeat)
            params["interlaced"] = False
        elif x == "3":        # triple progressive frame (repeat)
            params["interlaced"] = False
        
        if   y == "p":        # fields sampled at same time
            params["interlaced"] = False
        elif y == "i":        # fields sampled at different times
            params["interlaced"] = True
    
        if   z == "p":        # progressive (subsampling over whole frame) 
            pass
        elif z == "i":        # interlaced (each field subsampled independently) 
            pass
        elif z == "?":        # unknown (allowed only for non-4:2:0 subsampling)
            pass
        
    if "X" in tags:
        params["meta"] = tags["X"]
    
    return params



class FrameToYUV4MPEG(component):
        
    def checkShutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg,shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg
    
    def canShutdown(self):
        return isinstance(self.shutdownMsg, (producerFinished, shutdownMicroprocess))
    
    def mustShutdown(self):
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
        
    def sendoutbox(self,data):
        while 1:
            try:
                self.send(data,"outbox")
                return
            except noSpaceInBox:
                self.checkShutdown()
                if self.mustShutdown():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                self.checkShutdown()
                if self.mustShutdown():
                    raise "STOP"
        
    def main(self):
        self.shutdownMsg = None
        
        try:
            while not self.dataReady("inbox"):
                self.checkShutdown()
                if self.canShutdown():
                    raise "STOP"
                self.pause()
                yield 1
            
            frame = self.recv("inbox")
            for _ in self.write_header(frame):
                yield _
            for _ in self.write_frame(frame):
                yield _
            
            while 1:
                while self.dataReady("inbox"):
                    frame = self.recv("inbox")
                    for _ in self.write_frame(frame):
                        yield _
                self.checkShutdown()
                if self.canShutdown():
                    raise "STOP"
                self.pause()
                yield 1
                
        except "STOP":
            self.send(self.shutdownMsg,"signal")

    def write_header(self, frame):
        format = "YUV4MPEG2 W%d H%d" % tuple(frame['size'])
        
        if   frame['pixformat']=="YUV420_planar":
            format += " C420mpeg2"
        elif frame['pixformat']=="YUV411_planar":
            format += " C411"
        elif frame['pixformat']=="YUV422_planar":
            format += " C422"
        elif frame['pixformat']=="YUV444_planar":
            format += " C444"
        elif frame['pixformat']=="YUV4444_planar":
            format += " C444alpha"
        elif frame['pixformat']=="Y_planar":
            format += " Cmono"

        interlace = frame.get("interlaced",False)
        topfieldfirst = frame.get("topfieldfirst",False)
        if   interlace and topfieldfirst:
            format += " It"
        elif interlace and not topfieldfirst:
            format += " Ib"
        elif not interlace:
            format += " Ip"

        rate = frame.get("frame_rate", 0)
        if rate > 0:
            num,denom = rational(rate)
            format += " F%d:%d" % (num,denom)
            
        rate = frame.get("pixel_aspect", 0)
        if rate > 0:
            num,denom = rational(rate)
            format += " A%d:%d" % (num,denom)
            
        if "sequence_meta" in frame:
            format += " X"+frame['sequence_meta']
            
        format += "\x0a"
        
        for _ in self.sendoutbox(format):
            yield _
    
    
    def write_frame(self, frame):
        for _ in self.sendoutbox("FRAME\x0a"):
            yield _
        for component in frame['yuv']:
            for _ in self.sendoutbox(component):
                yield _



if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    
    Pipeline( RateControlledFileReader("/data/stream.yuv",readmode="bytes",rate=25*(608256+128)),
              YUV4MPEGToFrame(),
              FrameToYUV4MPEG(),
              YUV4MPEGToFrame(),
              VideoOverlay(),
            ).run()

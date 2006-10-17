#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import WaitComplete
import re



class parseYUV4MPEG(component):
    def __init__(self):
        super(parseYUV4MPEG,self).__init__()
        self.file = open("/data/stream.yuv","rb")
    
    def readline(self):
        if 0:
            yield 1
        self.bytesread = self.file.readline()
        
    def readbytes(self,size):
        if 0:
            yield 1
        self.bytesread = self.file.read(size)
        
    
    def main(self):
        # parse header
        yield WaitComplete(self.readline())
        line = self.bytesread
        m = re.match("^YUV4MPEG2((?: .\S*)*)\n$", line)
        assert(m)
        fields = m.groups()[0]
        seq_params = parse_seq_tags(fields)
        
        yield 1
            
        while 1:
            yield WaitComplete(self.readline())
            line = self.bytesread
            if not line:
                break
            m = re.match("^FRAME((?: .\S*)*)\n$", line)
            assert(m)
            fields = m.groups()[0]
            frame_params = parse_frame_tags(fields)
            
            ysize = seq_params["size"][0] * seq_params["size"][1]
            csize = seq_params["chroma_size"][0] * seq_params["chroma_size"][1]
            
            yield WaitComplete(self.readbytes(ysize))
            y = self.bytesread
            yield WaitComplete(self.readbytes(csize))
            u = self.bytesread
            yield WaitComplete(self.readbytes(csize))
            v = self.bytesread
            
            frame = { "yuv" : (y,u,v) }
            frame.update(seq_params)
            frame.update(frame_params)
            self.send(frame, "outbox")
            yield 1



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


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    
    Pipeline( parseYUV4MPEG(),
              
              VideoOverlay(),
            ).run()

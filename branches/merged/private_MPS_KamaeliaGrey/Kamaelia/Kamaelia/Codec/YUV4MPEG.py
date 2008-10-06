#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#

"""\
=============================================
Parsing and Creation of YUV4MPEG format files
=============================================

YUV4MPEGToFrame parses YUV4MPEG format data sent to its "inbox" inbox and sends
video fram data structures to its "outbox" outbox.

FrameToYUV4MPEG does the reverse - taking frame data structures sent to its
"inbox" inbox and outputting YUV4MPEG format data to its "outbox" outbox."

The YUV4MPEG file format is supported by many tools, such as mjpegtools,
mplayer/mencoder, and ffmpeg.



Example Usage
-------------

Playback a YUV4MPEG format file::

    Pipeline( RateControlledFileReader("video.yuv4mpeg",readmode="bytes", ...),
              YUV4MPEGToFrame(),
              VideoOverlay()
            ).run()
            
Decode a dirac encoded video file to a YUV4MPEG format file::

    Pipeline( RateControlledFileReader("video.dirac",readmode="bytes", ...),
              DiracDecoder(),
              FrameToYUV4MPEG(),
              SimpleFileWriter("output.yuv4mpeg")
            ).run()



YUV4MPEGToFrame Behaviour
-------------------------

Send binary data as strings containing YUV4MPEG format data to the "inbox" inbox
and frame data structures will be sent out of the "outbox" outbox as soon as
they are parsed.

See below for a description of the uncompressed frame data structure format.

This component supports sending data out of its outbox to a size limited inbox.
If the size limited inbox is full, this component will pause until it is able
to send out the data. Data will not be consumed from the inbox if this component
is waiting to send to the outbox.

If a producerFinished message is received on the "control" inbox, this component
will complete parsing any data pending in its inbox, and finish sending any
resulting data to its outbox. It will then send the producerFinished message on
out of its "signal" outbox and terminate.

If a shutdownMicroprocess message is received on the "control" inbox, this
component will immediately send it on out of its "signal" outbox and immediately
terminate. It will not complete processing, or sending on any pending data.



FrameToYUV4MPEG Behaviour
-------------------------

Send frame data structures to the "inbox" inbox of this component. YUV4MPEG
format binary string data will be sent out of the "outbox" outbox.

See below for a description of the uncompressed frame data structure format.

The header data for the YUV4MPEG file is determined from the first frame.

All frames sent to this component must therefore be in the same pixel format and
size, otherwise the output data will not be valid YUV4MPEG.

This component supports sending data out of its outbox to a size limited inbox.
If the size limited inbox is full, this component will pause until it is able
to send out the data. Data will not be consumed from the inbox if this component
is waiting to send to the outbox.

If a producerFinished message is received on the "control" inbox, this component
will complete parsing any data pending in its inbox, and finish sending any
resulting data to its outbox. It will then send the producerFinished message on
out of its "signal" outbox and terminate.

If a shutdownMicroprocess message is received on the "control" inbox, this
component will immediately send it on out of its "signal" outbox and immediately
terminate. It will not complete processing, or sending on any pending data.



=========================
UNCOMPRESSED FRAME FORMAT
=========================

A frame is a dictionary data structure. It must, at minimum contain the first 3
("yuv", "size" and "pixformat")::
    
    {
      "yuv" : (y_data, u_data, v_data)  # a tuple of strings
      "size" : (width, height)          # in pixels
      "pixformat" :  pixelformat        # format of raw video data
      "frame_rate" : fps                # frames per second
      "interlaced" : 0 or not 0         # non-zero if the frame is two interlaced fields
      "topfieldfirst" : 0 or not 0      # non-zero the first field comes first in the data
      "pixel_aspect" : fraction         # aspect ratio of pixels
      "sequence_meta" : metadata        # string containing extended metadata
                                        # (no whitespace or control characters)
    }

All other fields are optional when providing frames to FrameToYUV4MPEG.

YUV4MPEGToFrame only guarantees to fill inthe YUV data itself. All other fields
will be filled in if the relevant header data is detected in the file.

The pixel formats recognised (and therefore supported) are::
    
        "YUV420_planar"
        "YUV411_planar"
        "YUV422_planar"
        "YUV444_planar"
        "YUV4444_planar"
        "Y_planar"

"""

from Axon.Component import component
#from Axon.Ipc import WaitComplete
from Axon.Ipc import shutdownMicroprocess, producerFinished
from Axon.AxonExceptions import noSpaceInBox
import re
from Kamaelia.Support.Data.Rationals import rational


class YUV4MPEGToFrame(component):
    """\
    YUV4MPEGToFrame() -> new YUV4MPEGToFrame component.
    
    Parses YUV4MPEG format binarydata, sent as strings to its "inbox" inbox
    and outputs uncompressed video frame data structures to its "outbox" outbox.
    """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(YUV4MPEGToFrame,self).__init__()
        self.remainder = ""
        self.shutdownMsg = None
    
    def checkShutdown(self):
        """\
        Collects any new shutdown messages arriving at the "control" inbox, and
        returns "NOW" if immediate shutdown is required, or "WHENEVER" if the
        component can shutdown when it has finished processing pending data.
        """
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
        """\
        Generator.
        
        Read up to the next newline char from the stream of chunks of binary
        string data arriving at the "inbox" inbox.
        
        Any excess data is placed into self.remainder ready for the next call
        to self.readline or self.readbytes.
        
        Data is only read from the inbox when required. It is not preemptively
        fetched.
        
        The read data is placed into self.bytesread
        
        If a shutdown is detected, self.bytesread is set to "" and this
        generator immediately returns.
        """
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
        """\
        Generator.
        
        Read the specified number of bytes from the stream of chunks of binary
        string data arriving at the "inbox" inbox.
        
        Any excess data is placed into self.remainder ready for the next call
        to self.readline or self.readbytes.
        
        Data is only read from the inbox when required. It is not preemptively
        fetched.
        
        The read data is placed into self.bytesread
        
        If a shutdown is detected, self.bytesread is set to "" and this
        generator immediately returns.
        """
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
        """\
        Generator.
        
        Sends data out of the named outbox. If the destination is full
        (noSpaceInBox exception) then it waits until there is space and retries
        until it succeeds.
        
        If a shutdownMicroprocess message is received, returns early.
        """
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
        """Main loop"""
        
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
    """Parses YUV4MPEG header tags"""
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
    """\
    Parses YUV4MPEG frame tags.
    """
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
    """\
    FrameToYUV4MPEG() -> new FrameToYUV4MPEG component.
    
    Parses uncompressed video frame data structures sent to its "inbox" inbox
    and writes YUV4MPEG format binary data as strings to its "outbox" outbox.
    """
        
    def checkShutdown(self):
        """\
        Collects any new shutdown messages arriving at the "control" inbox, and
        ensures self.shutdownMsg contains the highest priority one encountered
        so far.
        """
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg,shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg
    
    def canShutdown(self):
        """\
        Returns true if the component should terminate when it has finished
        processing any pending data.
        """
        return isinstance(self.shutdownMsg, (producerFinished, shutdownMicroprocess))
    
    def mustShutdown(self):
        """Returns true if the component should terminate immediately."""
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
        
    def sendoutbox(self,data):
        """\
        Generator.
        
        Sends data out of the "outbox" outbox. If the destination is full
        (noSpaceInBox exception) then it waits until there is space. It keeps
        retrying until it succeeds.
        
        If the component is ordered to immediately terminate then "STOP" is
        raised as an exception.
        """
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
        """Main loop"""
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
        """\
        Generator.
        
        Sends the YUV4MPEG format header to the "outbox" outbox, based on
        attributes of the supplied frame data structure.
        """
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
        """\
        Generator.
        
        Writes out YUV4MPEG format frame marker and data.
        """
        for _ in self.sendoutbox("FRAME\x0a"):
            yield _
        for component in frame['yuv']:
            for _ in self.sendoutbox(component):
                yield _


__kamaelia_components__  = ( YUV4MPEGToFrame, FrameToYUV4MPEG, )


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

#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===================
Dirac video decoder
===================

This component decodes a stream of video, coded using the Dirac codec, into
frames of YUV video data.

This component is a thin wrapper around the Dirac Python bindings.



Example Usage
-------------
A simple video player::

    pipeline(ReadFileAdapter("diracvideofile.drc", ...other args...),
             DiracDecoder(),
             RateLimit(framerate),
             VideoOverlay()
            ).activate()



More detail
-----------
Reads a raw dirac data stream, as strings, from the "inbox" inbox.

Sends out frames of decoded video to the "outbox" outbox.

The frames may not be emitted at a constant rate. You may therefore need to
buffer and rate limit them if displaying them.

The decoder will terminate if it receives a shutdownMicroprocess message on
its "control" inbox. The message is passed on out of the "signal" outbox.
 
It will ignore producerFinished messages.

The decoder is able to work out from the data stream when it has reached the
end of the stream. It then sends a producerFinished message out of the "signal"
outbox and terminates.

For more information see the Dirac Python bindings documentation.



===================
Dirac video encoder
===================

This component encodes frames of YUV video data with the Dirac codec.

This component is a thin wrapper around the Dirac Python bindings.



Example Usage
-------------
Raw video file encoder::

    imagesize = (352, 288)      # "CIF" size video
    
    pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
             RawYUVFramer(imagesize),
             DiracEncoder(preset="CIF"),
             WriteFileAdapter("diracvideo.drc")
            ).activate()

RawYUVFramer is needed to frame raw YUV data into individual video frames.



More detail
-----------

Reads video frames from the "inbox" inbox.

Sends out encoded video data (as strings) in chunks to the "outbox" outbox.

The encoder can be configured with simple presets and/or more detailed encoder
and sequence parameters. Encoder and sequence parameters override those set with
a preset.

For more information see the Dirac Python bindings documentation.

The encoder will terminate if it receives a shutdownMicroprocess or
producerFinished message on its "control" inbox. The message is passed on out of
the "signal" outbox. If the message is producerFinished, then it will also send
any data still waiting to be sent out of the "outbox" outbox, otherwise any
pending data is lost.

The component does not yet support output of instrumentation or locally decoded
frames (the "verbose" option).
 

=========================
UNCOMPRESSED FRAME FORMAT
=========================

Uncompresed video frames are output by the decoder, as dictionaries. Each
contains the following entries::
    {
      "yuv" : (y_data, u_data, v_data)  # a tuple of strings
      "size" : (width, height)          # in pixels
      "frame_rate" : fps                # frames per second
      "interlaced" : 0 or not 0         # non-zero if the frame is two interlaced fields
      "topfieldfirst" : 0 or not 0      # non-zero the first field comes first in the data
      "pixformat" :  "YUV420_planar"    # format of raw video data
      "chroma_size" : (width, height)   # in pixels, for the u and v data
    }

The encoder expects data in the same format, but only requires "yuv", "size",
and "pixformat".


"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

from dirac_parser import DiracParser
from dirac_encoder import DiracEncoder as EncoderWrapper

from Kamaelia.Support.Data.Rationals import rational

def map_chroma_type(chromatype):
    """Maps string names for chrominance data formats to those understood by the Dirac Python bindings."""
    if chromatype == "420":
        return "YUV420_planar"
    else:
        raise "Dont know how to deal with this chroma type yet, sorry! - " + chromtype


class DiracDecoder(component):
    """
    DiracDecoder() -> new Dirac decoder component

    Creates a component that decodes Dirac video.
    """

    Inboxes  = { "inbox"   : "Strings containing an encoded dirac video stream",
                 "control" : "for shutdown signalling",
               }
    Outboxes = { "outbox" : "YUV decoded video frames",
                 "signal" : "for shutdown/completion signalling",
               }
       
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DiracDecoder, self).__init__()
        self.decoder = DiracParser()
        self.inputbuffer = ""

    def main(self):
        """Main loop"""
        done = False
        while not done:
            dataShortage = False
        
            while self.dataReady("inbox"):
                self.inputbuffer += self.recv("inbox")

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    done=True
        
            try:
                frame = self.decoder.getFrame()
                frame['pixformat'] = map_chroma_type(frame['chroma_type'])
                self.send(frame,"outbox")
            
            except "NEEDDATA":
                if self.inputbuffer:
                    self.decoder.sendBytesForDecode(self.inputbuffer)
                    self.inputbuffer = ""
                else:
                    datashortage = True
        
            except "SEQINFO":
                # sequence info dict in self.decoder.getSeqData()
                pass
            
            except "END":
                done = True
                self.send(producerFinished(self), "signal")
        
            except "STREAMERROR":
                print "Stream error"
                raise "STREAMERROR"
        
            except "INTERNALFAULT":
                print "Internal fault"
                raise "INTERNALFAULT"

            if dataShortage and not done:
                self.pause()

            yield 1

            

class DiracEncoder(component):
    """
    DiracEncoder([preset][,verbose][,encParams][,seqParams]) -> new Dirac encoder component

    Creates a component to encode video using the Dirac codec. Configuration based on
    optional preset, optionally overriden by individual encoder and sequence parameters.

    Keyword arguments:
    preset     -- "CIF" or "SD576" or "HD720" or "HD1080" (presets for common video formats)
    verbose    -- NOT YET IMPLEMENTED (IGNORED)
    encParams  -- dict of encoder setup parameters
    seqParams  -- dict of video sequence info parameters
    """

    def __init__(self, preset=None, verbose=False, encParams={}, seqParams={}):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DiracEncoder, self).__init__()

        if 'frame_rate' in seqParams:
            seqParams['frame_rate'] = rational(seqParams['frame_rate'])
            
        self.encoder = EncoderWrapper(preset=preset, bufsize=1024*1024, verbose=verbose, encParams=encParams, seqParams=seqParams)

        
    def main(self):
        """Main loop"""
        done = False
        msg = None
        while not done:

            while self.dataReady("inbox"):
                frame = self.recv("inbox")
                data = "".join(frame['yuv'])
                self.encoder.sendFrameForEncode(data)

                while 1:  # loop until 'needdata' event breaks out of this
                    try:
                        bytes = self.encoder.getCompressedData()
                        self.send(bytes,"outbox")

                    except "NEEDDATA":
                        break

                    except "ENCODERERROR":
                        print "Encoder Error"
                        raise "ENCODERERROR"

                    except "INTERNALFAULT":
                        print "Internal Fault"
                        raise "INTERNALFAULT"


            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, shutdownMicroprocess):
                    self.send(msg,"signal")
                    done=True
                    
                elif isinstance(msg, producerFinished):
                    # write 'end of sequence' data
                    data = self.encoder.getEndSequence()
                    self.send(data, "outbox")
                    yield 1
                    self.send(msg, "signal")
                    

            if not done:
                self.pause()

            yield 1

__kamaelia_components__ = ( DiracDecoder, DiracEncoder )

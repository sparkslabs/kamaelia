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
#

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

from dirac_parser import DiracParser
from dirac_encoder import DiracEncoder as EncoderWrapper

from Kamaelia.Data.Rationals import rational

def map_chroma_type(chromatype):
    if chromatype == "420":
        return "YUV420_planar"
    else:
        raise "Dont know how to deal with this chroma type yet, sorry! - " + chromtype


class DiracDecoder(component):
    """Dirac decoder component

       decodes dirac video!

       Receives dirac encoded video as strings on inbox

       Responds only to shutdownMicroprocess msgs (ignores producerFinished)
       as dirac encoder is perfectly capable of working out that the stream has
       finished, at which point it sends its own producerFinished msg.
    """
       
    def __init__(self):
        super(DiracDecoder, self).__init__()
        self.decoder = DiracParser()
        self.inputbuffer = ""

    def main(self):

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
    """Dirac encoder component

       Encodes dirac video!

       Receives frame dictionaries containing a 'yuv' key containing (y,u,v)
       tuple of strings

       Emits byte stream as strings

       Finishes the stream in response to a producerFinished msg.
       shutdownMicroprocess does not do this, but will still shut the component
       down.

       Does not yet support output of instrumentation or locally decoded frames
    """

    def __init__(self, preset=None, verbose=False, encParams={}, seqParams={}):
        """Initialisation.

        Either specify a preset and/or encoder and sequence parameters
        to set up the encoder. Any encoder or sequence params manually specified will
        override those specified through a preset.

        bufsize is recommended to be at least 1 MByte. It is the buffer into which the
        compressed stream is output. If the buffer size is too small, the encoder will
        generate errors.
        """

        super(DiracEncoder, self).__init__()

        if 'frame_rate' in seqParams:
            seqParams['frame_rate'] = rational(seqParams['frame_rate'])
            
        self.encoder = EncoderWrapper(preset=preset, bufsize=1024*1024, verbose=verbose, encParams=encParams, seqParams=seqParams)

        
    def main(self):

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

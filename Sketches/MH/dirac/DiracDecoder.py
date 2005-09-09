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
import pygame
from dirac_parser import DiracParser


def map_chroma_type(chromatype):
    if chromatype == "420":
        return pygame.IYUV_OVERLAY
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

            

if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
    from VideoOverlay import VideoOverlay
    
    pipeline( ReadFileAdaptor("/data/dirac-video/snowboard-jum-352x288x75.dirac.drc", readmode="bitrate", bitrate = 200000*8/5),
              DiracDecoder(),
              VideoOverlay(),
            ).run()
    
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

       At the moment, reads it direct from a file, but that'll change shortly
    """
       
    def __init__(self):
        super(DiracDecoder, self).__init__()
        self.decoder = DiracParser()

    def main(self):

        f=open("/data/dirac-video/snowboard-jum-352x288x75.dirac.drc", "rb")

        while self.doDecoding(f):
            yield 1

    def doDecoding(self, f):
        try:
            frame = self.decoder.getFrame()
            frame['pixformat'] = map_chroma_type(frame['chroma_type'])
            self.send(frame,"outbox")
            return True
        
        except "NEEDDATA":
            data = f.read(4096)
            self.decoder.sendBytesForDecode(data)
            return True
    
        except "SEQINFO":
            # sequence info dict in self.decoder.getSeqData()
            return True
        
        except "END":
            return False
    
        except "STREAMERROR":
            print "Stream error"
            return False
    
        except "INTERNALFAULT":
            print "Internal fault"
            return False


if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from VideoOverlay import VideoOverlay
    
    pipeline( DiracDecoder(),
              VideoOverlay(),
            ).run()
    
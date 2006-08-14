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
#

# plays music at a whiteboard!

import Axon

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists

#
# The following application specific components will probably be rolled
# back into the repository.
#

from Whiteboard.TagFiltering import TagAndFilterWrapper, FilterAndTagWrapper
from Whiteboard.Tokenisation import tokenlists_to_lines, lines_to_tokenlists

from Whiteboard.Canvas import Canvas
from Whiteboard.Painter import Painter
from Whiteboard.TwoWaySplitter import TwoWaySplitter
from Whiteboard.SingleShot import OneShot
from Whiteboard.CheckpointSequencer import CheckpointSequencer


# stuff for doing audio
import sys
sys.path.append("../pymedia/")
sys.path.append("../")
sys.path.append("../audio")
from pymedia_test import SoundOutput,SoundInput,ExtractData,PackageData
from Speex import SpeexEncode,SpeexDecode
from RawAudioMixer import RawAudioMixer as _RawAudioMixer

def RawAudioMixer():
    return _RawAudioMixer( sample_rate    = 8000,
                           readThreshold  = 0.5,
                           bufferingLimit = 2.0,
                           readInterval   = 0.1
                         ),

class Entuple(component):
    def __init__(self, prefix=[], postfix=[]):
        super(Entuple,self).__init__()
        self.prefix = prefix
        self.postfix = postfix
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                entupled = self.prefix + [data] + self.postfix
                self.send( entupled, "outbox" )
            self.pause()
            yield 1

if __name__=="__main__":
    
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.File.Reading import RateControlledFileReader
    from pymedia_test import AudioDecoder, ResampleTo

    import sys
    try:
        if "--help" in sys.argv:
            sys.stderr.write("Usage:\n    ./MusicPlayer host port\n\n")
            sys.exit(0)
        rhost = sys.argv[1]
        rport = int(sys.argv[2])
    except:
        sys.stderr.write("Usage:\n    ./MusicPlayer host port\n\n")
        sys.exit(1)

#    rhost = "127.0.0.1"
#    rport=1500

    pipeline(
        RateControlledFileReader("/home/matteh/music/Philip Glass/Solo Piano/01 - Metamorphosis One.mp3", readmode="bytes", rate=160*1024/8,chunksize=1024),
        AudioDecoder("mp3"),
        ResampleTo(sample_rate=8000, channels=1),
        ExtractData(),
        SpeexEncode(3),
        Entuple(prefix=["SOUND"],postfix=[]),
        tokenlists_to_lines(),
        TCPClient(host=rhost,port=rport),
    ).run()
    
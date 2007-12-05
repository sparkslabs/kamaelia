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
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists

#
# The following application specific components will probably be rolled
# back into the repository.
#

from Kamaelia.Apps.Whiteboard.TagFiltering import TagAndFilterWrapper, FilterAndTagWrapper
from Kamaelia.Apps.Whiteboard.Tokenisation import tokenlists_to_lines, lines_to_tokenlists

from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Apps.Whiteboard.Painter import Painter
from Kamaelia.Apps.Whiteboard.TwoWaySplitter import TwoWaySplitter
from Kamaelia.Apps.Whiteboard.SingleShot import OneShot
from Kamaelia.Apps.Whiteboard.CheckpointSequencer import CheckpointSequencer


# stuff for doing audio
import sys
from Kamaelia.Codec.Speex import SpeexEncode,SpeexDecode
from Kamaelia.Audio.RawAudioMixer import RawAudioMixer as _RawAudioMixer

def RawAudioMixer():
    return _RawAudioMixer( sample_rate    = 8000,
                           readThreshold  = 0.5,
                           bufferingLimit = 2.0,
                           readInterval   = 0.1
                         ),

from Kamaelia.Apps.Whiteboard.Entuple import Entuple
if __name__=="__main__":
    
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.Audio.Codec.PyMedia.Decoder import Decoder
    from Kamaelia.Audio.PyMedia.Resample import Resample

    import sys
    try:
        if "--help" in sys.argv:
            sys.stderr.write("Usage:\n    ./MP3Player filename host port\n\n")
            sys.exit(0)
        filename = sys.argv[1]
        rhost = sys.argv[2]
        rport = int(sys.argv[3])
    except:
        sys.stderr.write("Usage:\n    ./MP3Player filename host port\n\n")
        sys.exit(1)

#    rhost = "127.0.0.1"
#    rport=1500

    Pipeline(
        RateControlledFileReader(filename, readmode="bytes", rate=160*1024/8,chunksize=1024),
        Decoder("mp3"),
        Resample(sample_rate=44100, channels=2,
                 to_sample_rate=8000, to_channels=1),
        SpeexEncode(3),
        Entuple(prefix=["SOUND"],postfix=[]),
        tokenlists_to_lines(),
        TCPClient(host=rhost,port=rport),
    ).run()
    
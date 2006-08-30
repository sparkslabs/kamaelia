#!/usr/bin/env python
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

from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller

class Bunch:
    pass

class AudioFrameMarshalling:
    fmt="PymediaAudioFrame %(bitrate)s %(channels)s %(sample_rate)s %(sample_length)s X%(data)s"

    def marshall(frame):
        out = AudioFrameMarshalling.fmt % { "bitrate":frame.bitrate,
                           "channels":frame.channels,
                           "data":frame.data,
                           "sample_length":frame.sample_length,
                           "sample_rate":frame.sample_rate,
                         }
        return out
    marshall = staticmethod(marshall)



    def demarshall(frame):
        id, bitrate, channels, sample_rate, sample_length, data = frame.split(" ", 5)

        if id == AudioFrameMarshalling.fmt.split(" ",1)[0]:
            frame = Bunch()
            frame.bitrate = eval(bitrate)
            frame.channels = eval(channels)
            frame.sample_rate = eval(sample_rate)
            frame.sample_length = eval(sample_length)
            frame.data = data[1:]
            return frame

    demarshall = staticmethod(demarshall)



class AudioFrameMarshaller(Marshaller):
    def __init__(self):
        super(AudioFrameMarshaller,self).__init__( AudioFrameMarshalling )


class AudioFrameDeMarshaller(DeMarshaller):
    def __init__(self):
        super(AudioFrameDeMarshaller,self).__init__( AudioFrameMarshalling )


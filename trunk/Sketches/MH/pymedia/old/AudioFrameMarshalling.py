#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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


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
#
raise NotImplementedError("PyMedia doesn't seem to be available for python 3")

from Kamaelia.Audio.PyMedia.Input  import Input  as _SoundInput
from Kamaelia.Audio.PyMedia.Output import Output as _SoundOutput
from Kamaelia.Audio.RawAudioMixer import RawAudioMixer as _RawAudioMixer

def SoundInput():
    return _SoundInput( channels=1, sample_rate=8000, format="S16_LE" )

def SoundOutput():
    return _SoundOutput( channels=1, sample_rate=8000, format="S16_LE", maximumLag=0.25 )

def RawAudioMixer():
    return _RawAudioMixer( sample_rate    = 8000,
                           channels       = 1,
                           format         = "S16_LE",
                           readThreshold  = 0.2,
                           bufferingLimit = 0.4,
                           readInterval   = 0.05,
                         )


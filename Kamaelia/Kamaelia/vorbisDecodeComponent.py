#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
"""\
This is a deprecation stub, due for later removal.
"""

import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.Codec.Vorbis import VorbisDecode as __VorbisDecode
from Kamaelia.Codec.Vorbis import AOAudioPlaybackAdaptor as __AOAudioPlaybackAdaptor

Deprecate.deprecationWarning("Use Kamaelia.Codec.Vorbis instead of Kamaelia.vorbisDecodeComponent")

VorbisDecode = Deprecate.makeClassStub(
    __VorbisDecode,
    "Use Kamaelia.Codec.Vorbis:VorbisDecode instead of Kamaelia.vorbisDecodeComponent:VorbisDecode",
    "WARN"
    )

AOAudioPlaybackAdaptor = Deprecate.makeClassStub(
    __AOAudioPlaybackAdaptor,
    "Use Kamaelia.Codec.Vorbis:AOAudioPlaybackAdaptor instead of Kamaelia.vorbisDecodeComponent:AOAudioPlaybackAdaptor",
    "WARN"
    )
   
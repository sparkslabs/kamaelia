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
raise NotImplementedError("Needs Updating: pymedia library which was a python2-ism")

import pymedia.audio.sound as sound


format2PyMediaFormat = {
    'AC3'       : sound.AFMT_AC3,
    'A_LAW'     : sound.AFMT_A_LAW,
    'IMA_ADPCM' : sound.AFMT_IMA_ADPCM,
    'MPEG'      : sound.AFMT_MPEG,
    'MU_LAW'    : sound.AFMT_MU_LAW,
    'S16_BE'    : sound.AFMT_S16_BE,
    'S16_LE'    : sound.AFMT_S16_LE,
    'S16_NE'    : sound.AFMT_S16_NE,
    'S8'        : sound.AFMT_S8,
    'U16_BE'    : sound.AFMT_U16_BE,
    'U16_LE'    : sound.AFMT_U16_LE,
    'U8'        : sound.AFMT_U8,
}

pyMediaFormat2format = dict([(v,k) for (k,v) in format2PyMediaFormat.items() ])

format2BytesPerSample = {
    'AC3'       : None,    # not recognised by alsa, so I dunno!
    'A_LAW'     : 1,
    'IMA_ADPCM' : 0.5,
    'MPEG'      : None,    # not applicable
    'MU_LAW'    : 1,
    'S16_BE'    : 2,
    'S16_LE'    : 2,
    'S16_NE'    : 2,
    'S8'        : 1,
    'U16_BE'    : 2,
    'U16_LE'    : 2,
    'U8'        : 1,
}

# mapping of codec names to file extensions (thats what pymedia wants to know
# when decoding)
codec2fileExt = {
   'MP3' : 'mp3',
   'mp3' : 'mp3',
   'Mp3' : 'mp3',
}

# mappings of codec names to ones that pymedia recognises for encoders
codec2PyMediaCodec = {
   'MP3' : 'mp3',
   'mp3' : 'mp3',
   'Mp3' : 'mp3',
}

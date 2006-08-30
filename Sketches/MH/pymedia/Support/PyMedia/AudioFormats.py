#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import pymedia.audio.sound as sound

mapping_format_to_pymedia = {
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

mapping_format_from_pymedia = dict([(v,k) for (k,v) in mapping_format_to_pymedia.items() ])

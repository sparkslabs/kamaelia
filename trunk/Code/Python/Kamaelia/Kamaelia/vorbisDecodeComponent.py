#!/usr/bin/env python

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
   
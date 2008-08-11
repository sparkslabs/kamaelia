#!/usr/bin/env python

# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor as __ReadFileAdaptor

Deprecate.deprecationWarning("Use Kamaelia.File.ReadFileAdaptor instead of Kamaelia.ReadFileAdaptor")

ReadFileAdaptor = Deprecate.makeClassStub(
    __ReadFileAdaptor,
    "Use Kamaelia.File.ReadFileAdaptor:ReadFileAdaptor instead of Kamaelia.ReadFileAdaptor:ReadFileAdaptor",
    "WARN"
    )
   
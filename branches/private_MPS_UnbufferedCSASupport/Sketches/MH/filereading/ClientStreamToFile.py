#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# RETIRED
print """
/Sketches/filereading/ClientStreamToFile.py

 This file has been retired.
 It is retired because it is now part of the main code base.
 If you want to use this, you can now find it in:
     Kamaelia-Distribution/Examples/example12/ClientStreamToFile.py

 (Hopefully contains enough info to do what you wanted to do.)
"""

import sys
sys.exit(0)
#
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.PipelineComponent import pipeline
from WriteFileAdapter import WriteFileAdapter

outputfile = "/tmp/received.raw"
clientServerTestPort=1500

pipeline(TCPClient("127.0.0.1",clientServerTestPort),
         WriteFileAdapter(outputfile)
        ).run()


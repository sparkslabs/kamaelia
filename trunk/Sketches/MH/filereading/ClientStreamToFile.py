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


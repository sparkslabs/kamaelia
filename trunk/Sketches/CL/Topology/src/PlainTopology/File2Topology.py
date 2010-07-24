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

"""\
==========================================================
Draw Topology from a file which contains drawing commands
==========================================================

Example Usage
-------------
File2Topology.py yourFile
or python File2Topology.py yourFile

Commands that can be used in yourFile
---------------------------------------
1. Add one node
ADD NODE TCPClient TCPClient auto -
ADD NODE VorbisDecode VorbisDecode auto -
2. add one link
ADD LINK TCPClient VorbisDecode
3. Delete one node/ link/ all 
DEL NODE TCPClient
ADD LINK TCPClient VorbisDecode
DEL ALL
"""

import sys

from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

# To see if the file name is included in the arguments
if len(sys.argv)==1:
    print "Bingo! not enough inputs: please type the file name you want to draw as well"
else:
    # ReadFileAdaptor->lines_to_tokenlists->TopologyViewer
    Pipeline(
        ReadFileAdaptor(filename=sys.argv[1], readmode="line"),
        lines_to_tokenlists(),
        TopologyViewer(),
        ConsoleEchoer(),
    ).run()    
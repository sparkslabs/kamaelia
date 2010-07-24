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
==================================================================
Draw Color Topology for relation definition received from RelationParser
==================================================================
"""

import sys

from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline

from Util.RelationAttributeParsing import RelationAttributeParser
from Util.GenericTopologyViewer import GenericTopologyViewer

if len(sys.argv)==1:
    print "Please type the command you want to draw"
    # ConsoleReader->lines_to_tokenlists->TopologyViewer
    Pipeline(
        ConsoleReader(">>> "),
        lines_to_tokenlists(),
        GenericTopologyViewer(),
        ConsoleEchoer(),
    ).run()
else:
    # Data can be from DataSource and console inputs
    Graphline(
        CONSOLEREADER = ConsoleReader(),
        FILEREADER = ReadFileAdaptor(sys.argv[1]),
        PARSER = RelationAttributeParser(),
        TOKENS = lines_to_tokenlists(),
        VIEWER = GenericTopologyViewer(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("PARSER","inbox"),
        ("FILEREADER","outbox") : ("PARSER","inbox"),
        ("PARSER","outbox") : ("TOKENS","inbox"),
        ("TOKENS","outbox")   : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
        
    }
    ).run()

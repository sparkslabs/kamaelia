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
from Kamaelia.Util.Marshalling import Marshaller
from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists
from Kamaelia.Chassis.Pipeline import Pipeline

class CommandParser:
    def marshall(data):
        output = [data]
        if data[0].upper() == "LOAD":
            output.append(["GETIMG"])    # to propogate loaded image to other connected canvases
        return output
    marshall = staticmethod(marshall)

def parseCommands():
    return Marshaller(CommandParser)

def CommandConsole():
    return Pipeline(ConsoleReader(),
                 text_to_tokenlists(),
                 parseCommands())

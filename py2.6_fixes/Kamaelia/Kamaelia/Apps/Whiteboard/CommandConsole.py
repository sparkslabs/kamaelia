#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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

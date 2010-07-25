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
# -------------------------------------------------------------------------

import Kamaelia.Visualisation.PhysicsGraph
from Kamaelia.Visualisation.Axon.AxonVisualiserServer import AxonVisualiserServer

def parseArgs(args, extraShortArgs="", extraLongArgs=[]):
    shortargs = "n" + extraShortArgs
    longargs  = ["navelgaze","introspect="] + extraLongArgs

    dictArgs, optlist, remargs = Kamaelia.Visualisation.PhysicsGraph.parseArgs(args, shortargs, longargs)
    
    if "help" in dictArgs:
        dictArgs["help"] += "   -n, --navelgaze\n" + \
                            "      Directly wire in an introspector instead of listening on a port\n\n" + \
                            "   --introspect=server:port\n\n" + \
                            "      Plug in an introspector that sends data to 'server' on 'port'\n" + \
                            "      (have fun! - loop back: \"--port=1500 --introspect=127.0.0.1:1500\")\n\n"
        
    else:
        for o,a in optlist:

            if o in ("-n","--navelgaze"):
                dictArgs['navelgaze'] = True
            if o in ("--introspect="):
                import re
                match = re.match(r"^([^:]+):(\d+)$", a)
                server=match.group(1)
                port=int(match.group(2))
                dictArgs['introspect'] = (server,port)
    
    return dictArgs, optlist, remargs

    
if __name__=="__main__":
    from Axon.Scheduler import scheduler as _scheduler

    import sys
    dictArgs, optlist, remargs = parseArgs(sys.argv[1:])

    if "help" in dictArgs:
        print dictArgs["help"]
        
    else:
    
        i = None
        if "navelgaze" in dictArgs:
            del dictArgs["navelgaze"]
            dictArgs['noServer'] = True
            from Kamaelia.Util.Introspector import Introspector
            i = Introspector()

        if "introspect" in dictArgs:
            (server, port) = dictArgs["introspect"]
            del dictArgs["introspect"]
            
            from Kamaelia.Util.Introspector import Introspector
            from Kamaelia.Internet.TCPClient import TCPClient
            from Kamaelia.Util.PipelineComponent import pipeline
            
            pipeline( Introspector(), 
                      TCPClient(server, port) 
                    ).activate()

        app = AxonVisualiserServer(caption="Axon / Kamaelia Visualiser", **dictArgs)

        if i:
            i.link( (i,"outbox"), (app,"inbox") )
            i.activate()

        app.activate()

        _scheduler.run.runThreads(slowmo=0)

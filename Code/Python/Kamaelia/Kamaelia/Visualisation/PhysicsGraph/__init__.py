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

# Simple topography viewer server - takes textual commands from a single socket
# and renders the appropriate graph

import re
from Kamaelia.Support.Particles import Particle as BaseParticle

def parseArgs(argv, extraShortArgs="", extraLongArgs=[]):
    import getopt
    
    shortargs = "fh" + extraShortArgs
    longargs  = ["help","fullscreen","resolution=","port="] + extraLongArgs
            
    optlist, remargs = getopt.getopt(argv, shortargs, longargs)
    
    dictArgs = {}
    for o,a in optlist:
        if o in ("-h","--help"):
            dictArgs['help'] = "Arguments:\n" + \
                               "   -h, --help\n" + \
                               "      This help message\n\n" + \
                               "   -f, --fullscreen\n" + \
                               "      Full screen mode\n\n" + \
                               "   --resolution=WxH\n" + \
                               "      Set window size to W by H pixels\n\n" + \
                               "   --port=N\n" + \
                               "      Listen on port N (default is 1500)\n\n"
    
        elif o in ("-f","--fullscreen"):
            dictArgs['fullscreen'] = True
            
        elif o in ("--resolution"):
            match = re.match(r"^(\d+)[x,-](\d+)$", a)
            x=int(match.group(1))
            y=int(match.group(2))
            dictArgs['screensize'] = (x,y)
            
        elif o in ("--port"):
            dictArgs['serverPort'] = int(a)
            
    return dictArgs, optlist, remargs
                    
                    
if __name__=="__main__":
    import sys
    import Axon
    from Axon.Scheduler import scheduler as _scheduler
    from .TopologyViewerServer import TopologyViewerServer

    print ("X1", sys.argv)
    print ("X2", sys.argv[1:])
    print ("X3", parseArgs(sys.argv[1:]))
    dictArgs, remargs, junk = parseArgs(sys.argv[1:])
    
    if "help" in dictArgs:
        print (dictArgs["help"])
        
    else:
        app = TopologyViewerServer(**dictArgs)
        app.activate()
        _scheduler.run.runThreads(slowmo=0)



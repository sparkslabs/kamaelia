#!/usr/bin/env python

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

# Simple topography viewer server - takes textual commands from a single socket
# and renders the appropriate graph

import pygame
from pygame.locals import *

import random, time, re, sys

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

import Kamaelia.Physics
from Kamaelia.Physics.Simple import Particle as BaseParticle
from Kamaelia.UI.MH import PyGameApp, DragHandler

component = _Axon.Component.component

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Visualisation.PhysicsGraph.RenderingParticle import RenderingParticle
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer import TopologyViewerServer


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
    print "X1", sys.argv
    print "X2", sys.argv[1:]
    print "X3", parseArgs(sys.argv[1:])
    dictArgs, remargs, junk = parseArgs(sys.argv[1:])
    
    if "help" in dictArgs:
        print dictArgs["help"]
        
    else:
        app = TopologyViewerServer(**dictArgs)
        app.activate()
        _scheduler.run.runThreads(slowmo=0)



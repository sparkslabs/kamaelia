#!/usr/bin/env python
#
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

import sys
from Kamaelia.Visualisation.Axon.AxonVisualiserServer import AxonVisualiserServer
from Kamaelia.Visualisation.Axon.AxonVisualiserServer import AxonVisualiserServer, AxonVisualiser, text_to_token_lists
from Kamaelia.UI.GraphicDisplay import PygameDisplay
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Visualisation.PhysicsGraph import parseArgs as _parseArgs

def parseArgs(args, extraShortArgs="", extraLongArgs=[]):
    shortargs = "n" + extraShortArgs
    longargs  = ["navelgaze","introspect="] + extraLongArgs

    dictArgs, optlist, remargs = _parseArgs(args, shortargs, longargs)
    
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

    dictArgs, optlist, remargs = parseArgs(sys.argv[1:])

    if "help" in dictArgs:
        print dictArgs["help"]
        sys.exit(0)
   
    resolution = dictArgs.get("screensize",(800,600))
    doNavelgaze = dictArgs.pop("navelgaze", None)
    doIntrospect = dictArgs.pop("introspect", None)

    pgd = PygameDisplay(width=resolution[0],height=resolution[1]).activate()
    PygameDisplay.setDisplayService(pgd)

    if doIntrospect is not None:
        (server, port) = doIntrospect
        
        Pipeline( Introspector(), 
                  TCPClient(server, port) 
                ).activate()

    if doNavelgaze:
        if "serverPort" in dictArgs:
            raise "Makes no sense to navelgaze and use --port option - they're mutually exclusive"
        app = Pipeline(
                 Introspector(),
                 text_to_token_lists(),
                 AxonVisualiser(caption="Axon / Kamaelia Visualiser", **dictArgs)
              ) 
    else:
        app = AxonVisualiserServer(caption="Axon / Kamaelia Visualiser", **dictArgs)
    
    app.run()


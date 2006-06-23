#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

"""\
==============================
Generic Topology Viewer Server
==============================

A generic topology viewer that one client can connect to at a time over a
TCP socket and send topology change data for visualisation.



Example Usage
-------------
Visualiser that listens on port 1500 for a TCP connection through which
it receives topology change data to render::
    TopologyViewerServer( serverPort = 1500 ).run()
    
A simple client to drive the visualiser::
    pipeline( ConsoleReader(),
              TCPClient( server=<address>, port=1500 ),
            ).run()
    
Run the server, then run the client::
    >>> DEL ALL
    >>> ADD NODE 1 "1st node" randompos -
    >>> ADD NODE 2 "2nd node" randompos -
    >>> ADD NODE 3 "3rd node" randompos -
    >>> ADD LINK 1 2
    >>> ADD LINK 3 2
    >>> DEL LINK 1 2
    >>> DEL NODE 1

See also Kamaelia.Visualisation.Axon.AxonVisualiserServer - which is a
specialisation of this component.



How does it work?
-----------------

TopologyViewerServer is a pipeline of the following components:
- Kamaelia.SingleServer
- chunks_to_lines
- lines_to_tokenlists
- TopologyViewerComponent
- consoleEchoer

This pipeline serves to listen on the specified port (defaults to 1500) for
clients. One client is allowed to connect at a time.

That client can then send topology change commands formatted as lines of text.
The lines are parsed and tokenised for the TopologyViewerComponent.

Any output from the TopologyViewerComponent is sent to the console.

If the noServer option is used at initialisation, then the pipeline is built
without the SingleServer component. It then becomes a TopologyViewer
capable of processing non-tokenised input and with diagnostic console output.

See TopologyViewerComponent for more detail on topology change data and
its behaviour.
"""

from Kamaelia.Util.PipelineComponent import pipeline

from chunks_to_lines import chunks_to_lines
from lines_to_tokenlists import lines_to_tokenlists
from TopologyViewerComponent import TopologyViewerComponent
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Util.ConsoleEcho import consoleEchoer


class TopologyViewerServer(pipeline):
    """\
    TopologyViewerServer([noServer][,serverPort],**args) -> new TopologyViewerServer component.

    One-client-at-a-time TCP socket Topology viewer server. Connect on the
    specified port and send topology change data for display by a
    TopologyViewerComponent.
    
    Keywork arguments:
    - noServer    -- False, or True to not include the server component (default=False)
    - serverPort  -- None, or port number to listen on (default=1500)
    - args        -- all remaining keyword arguments passed onto TopologyViewerComponent
    """

    def __init__(self, noServer = False, serverPort = None, **dictArgs):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature."""
        
        pipe = [chunks_to_lines(),
                lines_to_tokenlists(),
                TopologyViewerComponent(**dictArgs),
                consoleEchoer() ]
                
        if not noServer:
            if serverPort == None:
                serverPort = 1500
            pipe.insert(0, SingleServer(port=serverPort))

        super(TopologyViewerServer, self).__init__(*pipe)
         
__kamaelia_prefab__ = ( TopologyViewerServer, )

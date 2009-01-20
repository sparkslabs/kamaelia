#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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


from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
from Kamaelia.Chassis.Graphline import Graphline

from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D import TopologyViewer3D


# Example usage of TopologyViewer3D
"""
TopologyViewer3D manifests as a pygame OpenGL display surface  plus hierarchy topology support. 
As it is sent topology information, nodes and links between them will appear.


It accepts commands from both precoded DataSource and real-time console inputs.

Commands recognised are:

    [ "ADD", "NODE", <id>, <name>, <posSpec>, <particle type> ]
        Add a node, using:
          
        - id            -- a unique ID used to refer to the particle in other topology commands. Cannot be None.
                           For hierarchy topology, the id is joined by its parent id with ":" to represent the 
                           hierarchy structure.
                           E.g., suppose the topology has 3 levels. The id of a particle in the 1st level is 1Node;
                           it has a child particle whose id is 2Node; 2Node also has a child particle whose id is 3Node;
                           then their ids are represented as
                           1Node
                           1Node:2Node
                           1Node:2Node:3Node 
        - name          -- string name label for the particle
        - posSpec       -- string describing initial (x,y,z) (see _generateXY); spaces are allowed
                           within the tuple, but quotation is needed in this case.
                           E.g., " ( 0 , 0 , -10 ) "
        - particleType  -- particle type (default provided is "-", unless custom types are provided - see below)
                           currently supported: "-" same as cuboid, cuboid, sphere and teapot
                           Note: it would be much slower than cuboid if either sphere or teapot is used.
      
    [ "DEL", "NODE", <id> ]
        Remove a node (also removes all links to and from it)
        
    [ "ADD", "LINK", <id from>, <id to> ]
        Add a link, directional from fromID to toID
           
    [ "DEL", "LINK", <id from>, <id to> ]
        Remove a link, directional from fromID to toID
               
    [ "DEL", "ALL" ]
        Clears all nodes and links

    [ "GET", "ALL" ]
        Outputs the current topology as a list of commands, just like
        those used to build it. The list begins with a 'DEL ALL'.

    [ "UPDATE_NAME", "NODE", <id>, <new name> ]
        If the node does not already exist, this does NOT cause it to be created.

    [ "GET_NAME", "NODE", <id> ]
        Returns UPDATE_NAME NODE message for the specified node

        
Operations supported:

    * esc --- quit
    
    * a --- viewer position moves left
    * d --- viewer position moves right
    * w --- viewer position moves up
    * s --- viewer position moves down
    * pgup --- viewer position moves forward (zoom in)
    * pgdn --- viewer position moves backward (zoom out)
    
    * left --- rotate selected particles to left around y axis  (all particles if none of them is selected)
    * right --- rotate selected particles to right around y axis  (all particles if none of them is selected)
    * up --- rotate selected  particles to up around x axis  (all particles if none of them is selected)
    * down --- rotate selected particles to down around x axis  (all particles if none of them is selected)
    * < --- rotate selected particles anticlock-wise around z axis  (all particles if none of them is selected)
    * > --- rotate selected particles clock-wise around z axis  (all particles if none of them is selected)
    * return --- show next level's topology of the selected particle when only one particle is selected
    * backspace --- show last level's topology
    
    * Mouse click --- click particle to select one, click empty area to deselect all
    * Mouse drag --- move particles
    * Mouse double-click --- show next level's topology of the particle clicked
    * Mouse right-click --- show last level's topology
    
    * shift --- multi Select Mode; shift+click for multiple selection/ deselection
    * ctrl ---  rotation Mode; when ctrl is pressed, mouse motion will rotate the selected particle 
                (all particles if none of them is selected)
"""
#
# This example needs more documentation really, but works. (The latter is the most important point)
#
# Data can be from both DataSource and console inputs, and print any output to the console 
# print "Please type the command you want to draw"
#

Graphline(
    CONSOLEREADER = ConsoleReader(">>> "),
    DATASOURCE = DataSource([# The first level
                             'ADD NODE 1Node 1Node randompos teapot',
                             'ADD NODE 2Node 2Node randompos -',
                             'ADD NODE 3Node 3Node randompos sphere', 'ADD NODE 4Node 4Node randompos -',
                             'ADD NODE 5Node 5Node randompos sphere', 'ADD NODE 6Node 6Node randompos -',
                             'ADD NODE 7Node 7Node randompos sphere',
                             'ADD LINK 1Node 2Node',
                             'ADD LINK 1Node 3Node', 'ADD LINK 1Node 4Node',
                             'ADD LINK 1Node 5Node','ADD LINK 1Node 6Node', 'ADD LINK 1Node 7Node',
                             # The second level, children of 1Node
                             'ADD NODE 1Node:1Node 1Node:1Node randompos -', 'ADD NODE 1Node:2Node 1Node:2Node randompos -',
                             'ADD NODE 1Node:3Node 1Node:3Node randompos -', 'ADD NODE 1Node:4Node 1Node:4Node randompos -',
                             'ADD LINK 1Node:1Node 1Node:2Node', 'ADD LINK 1Node:2Node 1Node:3Node',
                             'ADD LINK 1Node:3Node 1Node:4Node', 'ADD LINK 1Node:4Node 1Node:1Node',
                             # The third level, children of 1Node:1Node
                             'ADD NODE 1Node:1Node:1Node 1Node:1Node:1Node randompos -',
                             'ADD NODE 1Node:1Node:2Node 1Node:1Node:2Node randompos -',
                             'ADD LINK 1Node:1Node:1Node 1Node:1Node:2Node',
                             # The second level, children of 5Node
                             'ADD NODE 5Node:1Node 5Node:1Node randompos sphere',
                             'ADD NODE 5Node:2Node 5Node:2Node randompos sphere',
                             'ADD LINK 5Node:1Node 5Node:2Node'
                             ]),
    TOKENS = lines_to_tokenlists(),
    VIEWER = TopologyViewer3D(),
    CONSOLEECHOER = ConsoleEchoer(),
linkages = {
    ("CONSOLEREADER","outbox") : ("TOKENS","inbox"),
    ("DATASOURCE","outbox") : ("TOKENS","inbox"),
    ("TOKENS","outbox")   : ("VIEWER","inbox"),
    ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()

# Licensed to the BBC under a Contributor Agreement: CL
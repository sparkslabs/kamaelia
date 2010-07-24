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


# Example usage of TopologyViewer3DWithParams
"""
TopologyViewer3DWithParams extends TopologyViewer3D by supporting additional parameters 
of "ADD" and "UPDATE" commands.

The format of "ADD" commands:
[ "ADD", "NODE", <id>, <name>, <positionSpec>, <particle type>, <parameters> ]

The format of "UPDATE" commands:
[ "UPDATE", "NODE", <id>, <parameters> ] 

The format of parameters: pa=pa_value;pb=pb_value

Add quotation if there are spaces within parameters.

Available parameters: see the documentation of TopologyViewer3DWithParams.


It accepts commands from both precoded DataSource and real-time console inputs.  

Commands recognised are:

    [ "ADD", "NODE", <id>, <name>, <posSpec>, <particle type>, <parameters>  ]
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
        - <parameters>  -- the attributes of the particle, such as the texture, colour and size; the format of parameters is 
                           pa=pa_value;pb=pb_value.
    
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
    
    [ "UPDATE", "NODE", <id>, <parameters> ] 
        Update the attributes of the particle, such as the texture, colour and size.
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

from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Support.Particles.SimpleLaws import SimpleLaws

from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams import TopologyViewer3DWithParams

# Data can be from both DataSource and console inputs, and print any output to the console 
#print "Please type the command you want to draw"

laws = SimpleLaws(bondLength=2.8)
Graphline(
    CONSOLEREADER = ConsoleReader(">>> "),
    DATASOURCE = DataSource([# The first level
                             'ADD NODE 1Node 1Node randompos teapot image=../../../Docs/cat.gif',
                             'ADD NODE 2Node 2Node randompos - image=../../../Docs/cat.gif',
                             'ADD NODE 3Node 3Node randompos sphere image=../../../Docs/cat.gif',
                             'ADD NODE 4Node 4Node randompos - image=http://kamaelia.sourceforge.net/Kamaelia.gif',
                             'ADD NODE 5Node 5Node randompos sphere image=http://edit.kamaelia.org/Kamaelia.gif', 
                             'ADD NODE 6Node 6Node randompos -',
                             'ADD NODE 7Node 7Node randompos sphere',
                             'ADD LINK 1Node 2Node',
                             'ADD LINK 1Node 3Node', 'ADD LINK 1Node 4Node',
                             'ADD LINK 1Node 5Node','ADD LINK 1Node 6Node', 'ADD LINK 1Node 7Node',
                             # The second level, children of 1Node
                             'ADD NODE 1Node:1Node 1Node:1Node randompos - image=../../../Docs/cat.gif', 
                             'ADD NODE 1Node:2Node 1Node:2Node randompos -',
                             'ADD NODE 1Node:3Node 1Node:3Node randompos -', 
                             'ADD NODE 1Node:4Node 1Node:4Node randompos -',
                             'ADD LINK 1Node:1Node 1Node:2Node', 'ADD LINK 1Node:2Node 1Node:3Node',
                             'ADD LINK 1Node:3Node 1Node:4Node', 'ADD LINK 1Node:4Node 1Node:1Node',
                             'ADD NODE 1Node:1Node:1Node 1Node:1Node:1Node randompos - image=../../../Docs/cat.gif',
                             'ADD NODE 1Node:1Node:2Node 1Node:1Node:2Node randompos -',
                             'ADD LINK 1Node:1Node:1Node 1Node:1Node:2Node',
                             # The second level, children of 5Node
                             'ADD NODE 5Node:1Node 5Node:1Node randompos sphere image=../../../Docs/cat.gif',
                             'ADD NODE 5Node:2Node 5Node:2Node randompos sphere',
                             'ADD LINK 5Node:1Node 5Node:2Node'
                             ]),
    TOKENS = lines_to_tokenlists(),
    VIEWER = TopologyViewer3DWithParams(laws=laws),
    CONSOLEECHOER = ConsoleEchoer(),
linkages = {
    ("CONSOLEREADER","outbox") : ("TOKENS","inbox"),
    ("DATASOURCE","outbox") : ("TOKENS","inbox"),
    ("TOKENS","outbox")   : ("VIEWER","inbox"),
    ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()

# Licensed to the BBC under a Contributor Agreement: CL
#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===========================================================
Generic 3D Topology Viewer With more Parameters supports
===========================================================

Extend TopologyViewer3D by supporting additional parameters of "ADD" and "UPDATE" commands.



Example Usage
-------------
A simple console driven topology viewer::

    Pipeline( ConsoleReader(),
              lines_to_tokenlists(),
              TopologyViewer3DWithParams(),
            ).run()

Then at runtime try typing these commands to change the topology in real time::

    >>> DEL ALL
    >>> ADD NODE 1 "1st node" (0,0,-10) teapot
    >>> ADD NODE 2 "2nd node" randompos sphere image=../../../Docs/cat.gif
    >>> ADD NODE 3 "3rd node" randompos - bgcolour=(255,255,0);bgcolour=(0,255,255)
    >>> UPDATE NODE 1 name=1st;bgcolour=(0,255,0)
    >>> UPDATE NODE 3 name=3rd;bgcolour=(255,0,0);fgcolour=(0,0,255);fontsize=100
    >>> ADD NODE 1:1 "1st child node of the 1st node" " ( 0 , 0 , -10 ) " -
    >>> ADD NODE 1:2 "2nd child node of the 1st node" randompos - "fontsize = 20"
    >>> ADD LINK 1 2
    >>> ADD LINK 3 2
    >>> DEL LINK 1 2
    >>> ADD LINK 1:1 1:2
    >>> DEL NODE 1
    
    
    
How does it work?
-----------------

Extend TopologyViewer3D by supporting additional parameters of "ADD" and "UPDATE" commands.

The format of "ADD" commands:
[ "ADD", "NODE", <id>, <name>, <positionSpec>, <particle type>, <parameters> ]

The format of "UPDATE" commands:
[ "UPDATE", "NODE", <id>, <parameters> ] 

The format of parameters: pa=pa_value;pb=pb_value

Add quotation if there are spaces within parameters.

Available parameters:
    
    - bgcolour  -- Colour of surfaces behind text label (default=(230,230,230)), only apply to label texture 
    - fgcolour  -- Colour of the text label (default=(0,0,0), only apply to label texture 
    - sidecolour -- Colour of side planes (default=(200,200,244)), only apply to CuboidParticle3D
    - bgcolourselected  -- Background colour when the particle is selected (default=(0,0,0)
    - bgcolourselected  -- Frontground colour when the particle is selected (default=(244,244,244))
    - sidecolourselected -- Side colour when the particle is selected (default=(0,0,100))
    - margin       -- Margin size in pixels (default=8)
    - fontsize     -- Font size for label text (default=50)
    - pixelscaling -- Factor to convert pixels to units in 3d, ignored if size is specified (default=100)
    - thickness    -- Thickness of button widget, ignored if size is specified (default=0.3)
    - image        -- The uri of image, image texture instead of label texture is used if specified
    
    
    
See Kamaelia.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D for more information.
"""

import re

def paramStr2paramDict(string):
    """Transform a parameters string to a parameters dictionary."""
    colourRegex = re.compile("^\( *(\d{1,3}) *, *(\d{1,3}) *, *(\d{1,3}) *\)$")
    decimalRegex = re.compile('^\d*\.?\d*$')
    dictionary = {}
    string = string.strip().strip(';')
    string_list = string.split(';')
    for item in string_list:
        result = item.split('=')
        param = result[0].strip()
        value = result[1].strip()
        mColour = colourRegex.match(value)
        if mColour: # If colour triple tuple
            value = map(int, mColour.groups())
        else:
            mDecimal = decimalRegex.match(value)
            if mDecimal: # If Decimal
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)

        dictionary.update({param : value})
    return dictionary


from TopologyViewer3D import TopologyViewer3D

class TopologyViewer3DWithParams(TopologyViewer3D):
    """\
    TopologyViewer3DWithParams(...) -> new TopologyViewer3DWithParams component.
    
    A component that takes incoming topology (change) data and displays it live
    using pygame OpenGL. A simple physics model assists with visual layout. Particle
    types, appearance and physics interactions can be customised.
    
    It extends TopologyViewer3D by supporting additional parameters of "ADD" commands.
    
    Keyword arguments (in order):
    
    - screensize          -- (width,height) of the display area (default = (800,600))
    - fullscreen          -- True to start up in fullscreen mode (default = False)
    - caption             -- Caption for the pygame window (default = "Topology Viewer")
    - particleTypes       -- dict("type" -> klass) mapping types of particle to classes used to render them (default = {"-":RenderingParticle})
    - initialTopology     -- (nodes,bonds) where bonds=list((src,dst)) starting state for the topology  (default=([],[]))
    - laws                -- Physics laws to apply between particles (default = SimpleLaws(bondlength=100))
    - simCyclesPerRedraw  -- number of physics sim cycles to run between each redraw (default=1)
    - border              -- Minimum distance from edge of display area that new particles appear (default=100)
    """
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(TopologyViewer3DWithParams, self).__init__(**argd)
    
    
    def updateParticle(self, node_id, **params):
        """\
        updateParticle(node_id, **params) -> updates the given node's parameters/attributes if it exists
        
        node_id - an id for an already existing node
        **params - the updated parameters/attributes dictionary of the particle, e.g. name, texture, colour and size
        """
        for p in self.physics.particles:
            if p.ID == node_id:
                p.updateAttrs(**params)
                p.needRedraw = True
                return
            
    
    def doCommand(self, msg):
        """\
        Proceses a topology command tuple:
            [ "ADD", "NODE", <id>, <name>, <positionSpec>, <particle type> ] 
            [ "DEL", "NODE", <id> ]
            [ "ADD", "LINK", <id from>, <id to> ]
            [ "DEL", "LINK", <id from>, <id to> ]
            [ "DEL", "ALL" ]
            [ "GET", "ALL" ]
        """
        #print 'doCommand'        

        if len(msg) >= 2:
            cmd = msg[0].upper(), msg[1].upper()
            
            # Add default arguments when they are not provided
            if cmd == ("ADD", "NODE"):
                if len(msg) == 4:
                    msg += ['randompos', '-']
                elif len(msg) == 5:
                    msg += ['-']

            if cmd == ("ADD", "NODE") and (len(msg) == 6 or len(msg) == 7):
                if len(msg) == 7 and msg[6].strip() != "":
                    params = paramStr2paramDict(msg[6])
                else:
                    params = {}
                if msg[2] in [p.ID for p in self.physics.particles]:
                    print "Node exists, please use a new node ID!"
                else:
                    if self.particleTypes.has_key(msg[5]):
                        #print 'ADD NODE begin'
                        ptype = self.particleTypes[msg[5]]
                        ident    = msg[2]
                        name  = msg[3]
                        
                        posSpec = msg[4]
                        pos     = self._generatePos(posSpec)

                        particle = ptype(position = pos, ID=ident, name=name, **params)
                        
                        particle.originaltype = msg[5]
                        #self.particles.append(particle)
                        #print self.particles[0]
                        self.addParticle(particle)
                        self.isNewNode = True
                        #print id(particle)
                        
                        #print 'ADD NODE end'
                
            elif cmd == ("DEL", "NODE") and len(msg) == 3:
                    ident = msg[2]
                    self.removeParticle(ident)        
            
            elif cmd == ("ADD", "LINK") and len(msg) == 4:
                src = msg[2]
                dst = msg[3]
                self.makeBond(src, dst)
                
            elif cmd == ("DEL", "LINK") and len(msg) == 4:
                src = msg[2]
                dst = msg[3]
                self.breakBond(src, dst)
                
            elif cmd == ("DEL", "ALL") and len(msg) == 2:
                self.removeParticle(*self.physics.particleDict.keys())
                self.currentLevel = 0
                self.currentParentParticleID = ''
                
            elif cmd == ("GET", "ALL") and len(msg) == 2:
                topology = [("DEL","ALL")]
                topology.extend(self.getTopology())
                self.send( ("TOPOLOGY", topology), "outbox" )
            
            elif cmd == ("UPDATE_NAME", "NODE") and len(msg) == 4:
                node_id = msg[2]
                new_name = msg[3]
                self.updateParticleLabel(node_id, new_name)
                self.send( ("UPDATE_NAME", "NODE", node_id, new_name), "outbox" )
            elif cmd == ("GET_NAME", "NODE") and len(msg) == 3:
                node_id = msg[2]
                name = self.getParticleLabel(node_id)
                self.send( ("GET_NAME", "NODE", node_id, name), "outbox" )
                
            elif cmd == ("UPDATE", "NODE") and len(msg) == 4:
                node_id = msg[2]
                params = paramStr2paramDict(msg[3])
                self.updateParticle(node_id, **params)
                self.send( ("UPDATE", "NODE", node_id, msg[3]), "outbox" )        
            else:
                print "Command Error: please check your command format!"
        else:
            print "Command Error: not enough parameters!"

__kamaelia_components__  = ( TopologyViewer3DWithParams, )



if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
    from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
    from Kamaelia.Chassis.Graphline import Graphline
    
    # Data can be from both DataSource and console inputs
    print "Please type the command you want to draw"
    Graphline(
        CONSOLEREADER = ConsoleReader(">>> "),
#        DATASOURCE = DataSource(['ADD NODE 1Node 1Node randompos -', 'ADD NODE 2Node 2Node randompos -',
#                                 'ADD NODE 3Node 3Node randompos -', 'ADD NODE 4Node 4Node randompos -',
#                                 'ADD LINK 1Node 2Node','ADD LINK 2Node 3Node', 'ADD LINK 3Node 4Node',
#                                 'ADD LINK 4Node 1Node']),
        DATASOURCE = DataSource(['ADD NODE 1Node 1Node randompos teapot image=../../../Docs/cat.gif',
                                 'ADD NODE 2Node 2Node randompos - image=../../../Docs/cat.gif',
                                 'ADD NODE 3Node 3Node randompos sphere image=../../../Docs/cat.gif',
                                 'ADD NODE 4Node 4Node randompos - image=http://kamaelia.sourceforge.net/Kamaelia.gif',
                                 'ADD NODE 5Node 5Node randompos sphere image=http://edit.kamaelia.org/Kamaelia.gif', 
                                 'ADD NODE 6Node 6Node randompos -',
                                 'ADD NODE 7Node 7Node randompos sphere',
                                 'ADD LINK 1Node 2Node',
                                 'ADD LINK 1Node 3Node', 'ADD LINK 1Node 4Node',
                                 'ADD LINK 1Node 5Node','ADD LINK 1Node 6Node', 'ADD LINK 1Node 7Node',
                                 'ADD NODE 1Node:1Node 1Node:1Node randompos - image=../../../Docs/cat.gif', 
                                 'ADD NODE 1Node:2Node 1Node:2Node randompos -',
                                 'ADD NODE 1Node:3Node 1Node:3Node randompos -', 
                                 'ADD NODE 1Node:4Node 1Node:4Node randompos -',
                                 'ADD LINK 1Node:1Node 1Node:2Node', 'ADD LINK 1Node:2Node 1Node:3Node',
                                 'ADD LINK 1Node:3Node 1Node:4Node', 'ADD LINK 1Node:4Node 1Node:1Node',
                                 'ADD NODE 1Node:1Node:1Node 1Node:1Node:1Node randompos - image=../../../Docs/cat.gif',
                                 'ADD NODE 1Node:1Node:2Node 1Node:1Node:2Node randompos -',
                                 'ADD LINK 1Node:1Node:1Node 1Node:1Node:2Node',
                                 'ADD NODE 5Node:1Node 5Node:1Node randompos sphere image=../../../Docs/cat.gif',
                                 'ADD NODE 5Node:2Node 5Node:2Node randompos sphere',
                                 'ADD LINK 5Node:1Node 5Node:2Node'
                                 ]),
        TOKENS = lines_to_tokenlists(),
        VIEWER = TopologyViewer3DWithParams(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("TOKENS","inbox"),
        ("DATASOURCE","outbox") : ("TOKENS","inbox"),
        ("TOKENS","outbox")   : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()
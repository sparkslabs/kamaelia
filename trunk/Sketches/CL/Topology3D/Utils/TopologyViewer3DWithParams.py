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
"""
Extend TopologyViewer3D by support additional parameters of commands.
[ "ADD", "NODE", <id>, <name>, <positionSpec>, <particle type>, <parameters> ] 
The format of parameters: pa=pa_value,pb=pb_value
"""
def str2dict(string):
    """Transform a string to a dictionary"""
    dictionary = {}
    string_list = string.split(',')
    for item in string_list:
        result = item.split('=')
        dictionary.update({result[0]: result[1]})
    return dictionary


from TopologyViewer3D import TopologyViewer3D

class TopologyViewer3DWithParams(TopologyViewer3D):
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(TopologyViewer3DWithParams, self).__init__(**argd)
    
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

            if cmd == ("ADD", "NODE") and (len(msg) == 6 or len(msg) == 7):
                if len(msg) == 7 and msg[6].strip() != "":
                    params = str2dict(msg[6])
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
                        #print pos

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
            else:
                print "Command Error: please check your command format!"
        else:
            print "Command Error: not enough parameters!"


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
        DATASOURCE = DataSource(['ADD NODE 1Node 1Node randompos teapot image=../Files/son.gif',
                                 'ADD NODE 2Node 2Node randompos - image=../Files/dad.gif',
                                 'ADD NODE 3Node 3Node randompos sphere image=../Files/mum.gif',
                                 'ADD NODE 4Node 4Node randompos - image=http://kamaelia.sourceforge.net/Kamaelia.gif',
                                 'ADD NODE 5Node 5Node randompos sphere image=../Files/dad.gif', 
                                 'ADD NODE 6Node 6Node randompos - image=../Files/son.gif',
                                 'ADD NODE 7Node 7Node randompos sphere image=../Files/son1.gif',
                                 'ADD LINK 1Node 2Node',
                                 'ADD LINK 1Node 3Node', 'ADD LINK 1Node 4Node',
                                 'ADD LINK 1Node 5Node','ADD LINK 1Node 6Node', 'ADD LINK 1Node 7Node',
                                 'ADD NODE 1Node:1Node 1Node:1Node randompos - image=../Files/son.gif', 
                                 'ADD NODE 1Node:2Node 1Node:2Node randompos - image=../Files/dad.gif',
                                 'ADD NODE 1Node:3Node 1Node:3Node randompos - image=../Files/mum.gif', 
                                 'ADD NODE 1Node:4Node 1Node:4Node randompos - image=../Files/son1.gif',
                                 'ADD LINK 1Node:1Node 1Node:2Node', 'ADD LINK 1Node:2Node 1Node:3Node',
                                 'ADD LINK 1Node:3Node 1Node:4Node', 'ADD LINK 1Node:4Node 1Node:1Node',
                                 'ADD NODE 1Node:1Node:1Node 1Node:1Node:1Node randompos -',
                                 'ADD NODE 1Node:1Node:2Node 1Node:1Node:2Node randompos -',
                                 'ADD LINK 1Node:1Node:1Node 1Node:1Node:2Node',
                                 'ADD NODE 5Node:1Node 5Node:1Node randompos sphere',
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
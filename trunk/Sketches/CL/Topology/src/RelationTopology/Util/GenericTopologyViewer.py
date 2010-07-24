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
import sys

from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Support.Particles import SimpleLaws

from Particles import GenericParticle   # To use dictionary map
import Particles     # To search particle class within it

def str2dict(string):
    """Transform a string to a dictionary"""
    dictionary = {}
    string_list = string.split(',')
    for item in string_list:
        result = item.split('=')
        dictionary.update({result[0]: result[1]})
    return dictionary
        
        
class GenericTopologyViewer(TopologyViewer):
    """
    =============================================================
    Extend TopologyViewer to accept more parameters
    =============================================================  
    """

    def __init__(self, **argd):
        if not argd.has_key('particleTypes'):
            argd.update({'particleTypes':{"-":GenericParticle}})
        if not argd.has_key('laws'):
            argd.update({'laws':SimpleLaws(bondLength=200)})
                       
        super(GenericTopologyViewer, self).__init__(**argd)
    
    def doCommand(self, msg):
        """\
        Proceses a topology command tuple:
            [ "ADD", "NODE", <id>, <name>, <positionSpec>, <particle type>, [attributes] ]
            [ "UPDATE", "NODE", <attributes> ]
            [ "DEL", "NODE", <id> ]
            [ "ADD", "LINK", <id from>, <id to> ]
            [ "DEL", "LINK", <id from>, <id to> ]
            [ "DEL", "ALL" ]
            [ "GET", "ALL" ]
        """
        
        try:            
            if len(msg) >= 2:
                cmd = msg[0].upper(), msg[1].upper()
    
                if cmd == ("ADD", "NODE") and (len(msg) == 6 or len(msg) == 7):
                    if self.particleTypes.has_key(msg[5]):
                        ptype = self.particleTypes[msg[5]]                        
                    else:
                        ptype = getattr(Particles, msg[5])
                    id    = msg[2]
                    name  = msg[3]
                    
                    posSpec = msg[4]
                    pos     = self._generateXY(posSpec)
                    
                    if len(msg) == 6:
                        particle = ptype(position = pos, ID=id, name=name)
                    else:
                        attrs = msg[6]
                        attrs_dict = str2dict(attrs)
                        particle = ptype(position = pos, ID=id, name=name, **attrs_dict)
                    particle.originaltype = msg[5]
                    self.addParticle(particle)
                    
                elif cmd == ("UPDATE", "NODE") and len(msg) == 4:
                    id    = msg[2]
                    attrs = msg[3]
                    attrs_dict = str2dict(attrs)
                    self.updateParticle(id,**attrs_dict)
                
                elif cmd == ("DEL", "NODE") and len(msg) == 3:
                    id = msg[2]
                    self.removeParticle(id)
                        
                elif cmd == ("ADD", "LINK") and len(msg) == 5:
                    src = msg[2]
                    dst = msg[3]
                    self.makeBond(src, dst)
                    relation = msg[4]
                    self.physics.particleDict[src].bondedRelations.update(
                    {self.physics.particleDict[dst]:relation})
                elif cmd == ("DEL", "LINK") and len(msg) == 4:
                    src = msg[2]
                    dst = msg[3]
                    self.breakBond(src, dst)
                    
                elif cmd == ("DEL", "ALL") and len(msg) == 2:
                    self.removeParticle(*self.physics.particleDict.keys())

                elif cmd == ("FREEZE", "ALL") and len(msg) == 2:
                    self.freezeAll()

                elif cmd == ("UNFREEZE", "ALL") and len(msg) == 2:
                    self.freezeAll()

                elif cmd == ("GET", "ALL") and len(msg) == 2:
                    topology = [("DEL","ALL")]
                    topology.extend(self.getTopology())
                    self.send( ("TOPOLOGY", topology), "outbox" )
                elif cmd == ("UPDATE_NAME", "NODE") and len(msg) == 4:
                    node_id = msg[2]
                    new_name = msg[3]
                    self.updateParticleLabel(node_id, new_name)
                elif cmd == ("GET_NAME", "NODE") and len(msg) == 3:
                    node_id = msg[2]
                    name = self.getParticleLabel(node_id)
                    self.send( ("UPDATE_NAME", "NODE", node_id, name), "outbox" )
                else:
                    raise "Command Error"
            else:
                raise "Command Error"
        except:     
            import traceback
            errmsg = reduce(lambda a,b: a+b, traceback.format_exception(*sys.exc_info()) )
            self.send( ("ERROR", "Error processing message : "+str(msg) + " resason:\n"+errmsg), "outbox")
            
    def updateParticle(self,id,**attrs_dict):
        """Update Particle attributes"""
        if self.physics.particleDict.has_key(id):
            self.physics.particleDict[id].updateAttrs(**attrs_dict)
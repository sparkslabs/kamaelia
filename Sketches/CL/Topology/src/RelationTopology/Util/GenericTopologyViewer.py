
import sys

from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer

from Particles import GenericParticle

class GenericTopologyViewer(TopologyViewer):
    """
    =============================================================
    Extend TopologyViewer to accept more parameters
    =============================================================
    
    TODO: be able to update the figure dynamically    
    """

    def __init__(self, **argd):
        if not argd.has_key('particleTypes'):
            argd.update({'particleTypes':{"-":GenericParticle}})            
        super(GenericTopologyViewer, self).__init__(**argd)
    
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
        
        try:            
            if len(msg) >= 2:
                cmd = msg[0].upper(), msg[1].upper()
    
                if cmd == ("ADD", "NODE") and (len(msg) == 6 or len(msg) == 7):
                    if self.particleTypes.has_key(msg[5]):
                        ptype = self.particleTypes[msg[5]]
                        
                    else:
                        ptype = eval(msg[5])
                    id    = msg[2]
                    name  = msg[3]
                    
                    posSpec = msg[4]
                    pos     = self._generateXY(posSpec)
                    
                    if len(msg) == 6:
                        particle = ptype(position = pos, ID=id, name=name)
                    else:
                        attributes = msg[6]
                        attributes_dict = eval('dict('+attributes+')')
                        particle = ptype(position = pos, ID=id, name=name, **attributes_dict)
                    particle.originaltype = msg[5]
                    self.addParticle(particle)
                
                elif cmd == ("DEL", "NODE") and len(msg) == 3:
                    id = msg[2]
                    self.removeParticle(id)
                        
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
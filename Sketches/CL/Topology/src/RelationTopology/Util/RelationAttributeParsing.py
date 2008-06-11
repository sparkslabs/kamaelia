#!/usr/bin/env python

"""\
===================================================
Parse entities and relations definition received
===================================================

Parse entities and relations definition received, one line one time.

1. Definition format
1.) Empty line (including any number of white spaces)
2.) Line starting with # to comment
3.) Entity definition
Example:
--------
person mum
person son gender="male",photo="../Files/son.gif"
4.) Relation definition
Example: 
--------
childof(mum, son)

2. NOTE:
1.) Any number of spaces can exist before, after and between the above line
Example:
--------
  person    mum  
     childof  (  mum  , son  )  
2.) Parse one line one time and then send out
3.) Entity definition needs to come before relation definition 
if the relations definition uses the entity      
"""

def parseEntity(entityLine):
    """ parse entity line """
    result = entityLine.split()
    #entity_ID = result[0]+'_'+result[1]
    entity_name = result[1]
    #particle = '-'
    particle = 'GenericParticle'
    if len(result) == 3:
        attributes = result[2]
        #attributes = attributes.lower()
        attributes = attributes.replace('gender','color')
        attributes = attributes.replace('female','pink')
        attributes = attributes.replace('male','blue')
        attributes = attributes.replace('photo','pic')
        attributes = attributes + ',type=' + result[0]
    else:
        attributes = 'type=' + result[0]               
    return "ADD NODE %s %s auto %s %s" % (entity_name,entity_name,particle,attributes)

def parseUpdatedEntity(entityLine):
    """ parse entity line """
    result = entityLine.split()
    #entity_ID = result[0]+'_'+result[1]
    entity_name = result[1]
    #particle = '-'
    #particle = 'GenericParticle'
    if len(result) == 3:
        attributes = result[2]
        #attributes = attributes.lower()
        attributes = attributes.replace('gender','color')
        attributes = attributes.replace('female','pink')
        attributes = attributes.replace('male','blue')
        attributes = attributes.replace('photo','pic')
        attributes = attributes.replace('name','label')
    else:
        #pass
        attributes = 'label=' + entity_name              
    return "UPDATE NODE %s %s" % (entity_name,attributes)

def parseRelation(relationLine):
    """ parse relation line """
    result = relationLine.split('(')
    relation = result[0].strip()
    #print relation
    entities_str = result[1].rstrip(')')
    entities_list = entities_str.split(',')
    src = entities_list[0].strip()
    dst = entities_list[1].strip()
    return "ADD LINK %s %s %s" % (src,dst,relation)


        
import re

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class RelationAttributeParser(Axon.Component.component):
    """\
=============================================================
A component to parse entities and relations definition
=============================================================
"""
    def shutdown(self):
        """ shutdown method: define when to shun down"""
        while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                self.shutdown_mess = data
                return True
        return False
      
    def main(self):
        #print 'aa'
        """ main method: do stuff """
        
        previousNodes = []  
        
        # Put all codes within the loop, so that others can be run even it doesn't shut down
        while not self.shutdown():
            #print previousNodes
            X = []
            links = []
            nodes = []
            updatedNodes = []
            while not self.anyReady():
                self.pause()
                yield 1
    
            while self.dataReady("inbox"):
                L = self.recv("inbox")
                #print L
                if L.strip() == "": continue # empty line
                if L.lstrip()[0] == "#": continue # comment
                X.append(L.strip())
                #print X
            #yield 1
            
            for item in X:            
                if re.match('(.+)\((.+),(.+)\)',item): # relation
                    command = parseRelation(item)
                    links.append(command)
                else:
                    isRepeated = False
                    print previousNodes
                    for node in previousNodes:
                        print item.split()[1],node.split()[2]
                        if item.split()[1] == node.split()[2]:
                            isRepeated = True
                    if not isRepeated: # entity
                        command = parseEntity(item)
                        nodes.append(command)        
                        previousNodes.append(command)
                    else:
                        print 'repeated'
                        command = parseUpdatedEntity(item)
                        updatedNodes.append(command)
            #print nodes
            for node in nodes:
                self.send(node, "outbox")
            for updatedNode in updatedNodes:
                self.send(updatedNode, "outbox")
            for link in links:
                self.send(link, "outbox")
            yield 1
            yield 1
        
        #print self.shutdown_mess
        #self.send(self.shutdown_mess,"signal")
        
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
    from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
    from GenericTopologyViewer import GenericTopologyViewer
    from Kamaelia.Chassis.Graphline import Graphline
    
    # Data can be from DataSource and console inputs
    Graphline(
        CONSOLEREADER = ConsoleReader(),
        DATASOURCE = DataSource(["  person  mum   gender=female,photo=../Files/mum.jpg,width=80,height=80 ", '  ', """   
                    """, 'person dad gender=male,shape=rect,width=80,height=80', 
                    '  person  son   gender=male,photo=../Files/son.gif,width=60,height=60',
                    'person son photo=../Files/son1.gif',
                     'person daughter radius=200', 'person daughter radius=100',
                     ' childof  (  mum  , son  ) ', 'childof(mum, daughter)',
                     'childof(dad, son)', 'childof(dad, daughter)']),
        PARSER = RelationAttributeParser(),
        TOKENS = lines_to_tokenlists(),
        VIEWER = GenericTopologyViewer(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("PARSER","inbox"),
        ("DATASOURCE","outbox") : ("PARSER","inbox"),
        ("PARSER","outbox") : ("TOKENS","inbox"),
        ("TOKENS","outbox")   : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
        
    }
).run()
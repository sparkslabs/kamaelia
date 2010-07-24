#!/usr/bin/env python
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
person son
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
    entity_name = result[1]
    return "ADD NODE %s %s auto -" % (entity_name,entity_name)

def parseRelation(relationLine):
    """ parse relation line """
    result = relationLine.split('(')
    entities_str = result[1].rstrip(')')
    entities_list = entities_str.split(',')
    src = entities_list[0].strip()
    dst = entities_list[1].strip()
    return "ADD LINK %s %s" % (src,dst)


        
import re

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class RelationParser(Axon.Component.component):
    """\
=============================================================
A component which can parse entities and relations definition
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
        """ main method: do stuff """
        X = []
        links = []
        nodes = []
        while not self.shutdown():
            while not self.anyReady():
                self.pause()
                yield 1

            while self.dataReady("inbox"):
                L = self.recv("inbox")
                if L.strip() == "": continue # empty line
                if L.lstrip()[0] == "#": continue # comment
                X.append(L.strip())
            yield 1

        for item in X:            
            if re.match('(.+)\((.+),(.+)\)',item): # relation
                command = parseRelation(item)
                links.append(command)
            else: # entity
                command = parseEntity(item)
                nodes.append(command)
        
        for node in nodes:
            self.send(node, "outbox")
        for link in links:
            self.send(link, "outbox")
        yield 1
        yield 1
        self.send(self.shutdown_mess,"signal")
        
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
    #from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
    from Kamaelia.Chassis.Pipeline import Pipeline
        
    Pipeline(
        DataSource(['  person  mum  ', '  ', """   
                          """, '  person  son ', ' childof  (  mum  , son  ) ']),
        RelationParser(),
        lines_to_tokenlists(),
        #ConsoleEchoer(),
        TopologyViewer(),
    ).run()        
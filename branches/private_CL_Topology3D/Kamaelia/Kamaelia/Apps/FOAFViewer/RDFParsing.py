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

"""\
=====================================
Parse RDF data received from a uri
=====================================
Fetch and parse RDF data, and then send out TopologyViewer commands



Example Usage
-------------
A simple console driven RDF parser and draw them with 3D topology viewer::

    Pipeline( ConsoleReader(),
              RDFParser(),
              TopologyViewer3DWithParams(),
              ConsoleEchoer(),
            ).run()

Then at runtime try typing these commands to change RDF data in real time::

    >>> http://fooshed.net/foaf.rdf 2 10
    >>> http://bigasterisk.com/foaf.rdf 
    >>> http://apassant.net/about/#alex 



How does it work?
-----------------
RDFParser is a Kamaeila component which fetch data from a uri which is a RDF data file 
or a web page which embeds RDF data.

The input format:
    "uri max_layer max_nodePerLayer": 
        - uri              -- is the uri of the data file. If the uri is a rdf data file, it will parse it directly;
                              if not, it will extract rdf data first before parsing. 
        - max_layer        -- the maximum layers of the rdf hierarchy structure (how deep) to parse
        - max_nodePerLayer -- the maximum nodes in one layer (how wide) to parse

The output is TopologyViewer commands.

Typically, it receives inputs from ConsoleReader or ConsoleReader 
and send output to TopologyViewer3D.

You may also need to install librdf, a rdf parsing lib from redland. 
See http://librdf.org/ for more information and 
http://librdf.org/bindings/INSTALL.html for installation information.
"""

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

import RDF

class RDFParser(Axon.Component.component):
    """\
    RDFParser(...) -> new RDFParser component.
    
    A component to parse RDF data received from a uri to TopologyViewer3D command.
    
    Arguments are got from inbox rather than the initialisation of the class.
    """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(RDFParser, self).__init__()
        self.rdf_prefix = """
                           PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                           PREFIX owl: <http://www.w3.org/2002/07/owl#>
                           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                          """
        self.num_allNodes = self.num_parentNodes = 0
        
    def shutdown(self):
        """Shutdown method: define when to shun down."""
        while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                self.shutdown_mess = data
                return True
        return False
      
    def main(self):
        """Main method: do stuff."""
        # Put all codes within the loop, so that others can be run even it doesn't shut down
        while not self.shutdown():
            while not self.anyReady():
                self.pause()
                yield 1
    
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if data.strip(): # Ignore empty data
                    # Clear the previous graph
                    self.send(["DEL", "ALL"], "outbox")
                    data_list = data.split()
                    if data_list[0].endswith('.rdf'): # If it's rdf file
                        self.rdf_uri = data_list[0]
                    else:
                        self.rdf_uri = "http://www.w3.org/2007/08/pyRdfa/extract?uri=" + data_list[0]
                    #print self.rdf_uri
                    
                    if len(data_list) == 2:
                        self.max_layer = int(data_list[1])
                    else:
                        self.max_layer = 2
                    
                    if len(data_list) == 3:
                        self.max_nodePerLayer = int(data_list[2])
                    else:
                        self.max_nodePerLayer = 0
                    self.parentNode_id = ""
                    self.fetch_data(self.rdf_uri)
                    print "num_parentNodes:", self.num_parentNodes, "num_allNodes:", self.num_allNodes
                
            yield 1
            
        self.send(self.shutdown_mess,"signal")
    
    def make_query(self, rdf, query):
        """Make sparql query."""
        model = RDF.Model()
        parser = RDF.Parser()
        parser.parse_into_model(model, rdf)
        sparql = """
        %s
        %s""" % (self.rdf_prefix, query)
        q = RDF.Query(sparql, query_language="sparql")
        return q.execute(model)

    def fetch_data(self, rdf_uri, current_layer=0):
        """Fetch data from an uri recursively."""
        if current_layer == self.max_layer:
            return
        else:
            self.num_parentNodes += 1
            query = """
            SELECT DISTINCT ?aname ?aimg ?name ?img ?seeAlso
            WHERE {
            ?a foaf:knows ?b . ?a foaf:name ?aname . ?b foaf:name ?name .
            OPTIONAL { ?a foaf:img ?aimg } .
            OPTIONAL { ?b foaf:img ?img } .
            OPTIONAL { ?b rdfs:seeAlso ?seeAlso }
            }
            """
            nodes = []
            results = self.make_query(rdf_uri, query)
            num_nodePerLayer = 1
            count = 0
            for result in results:
                if count == 0:
                    count += 1
                    linkedNode_name = str(result['aname'])
                    if self.parentNode_id == "":
                        linkedNode_id =  '_'.join(linkedNode_name.split())
                    else:
                        linkedNode_id =  self.parentNode_id + ':' + '_'.join(linkedNode_name.split())
                    if result['aimg']:
                        linkedNode_img = 'image=' + str(result['aimg']._get_uri())
                    else:
                        linkedNode_img = ""
                    cmd = [ "ADD", "NODE", linkedNode_id, linkedNode_name, "randompos", "-", linkedNode_img ]
                    self.send(cmd, "outbox")
                    
                if self.max_nodePerLayer > 0 and num_nodePerLayer > self.max_nodePerLayer:
                    break
                else:
                    num_nodePerLayer += 1
                    self.num_allNodes += 1
                    node_name = str(result['name'])
                    if self.parentNode_id == "":
                        node_id =  '_'.join(node_name.split())
                    else:
                        node_id =  self.parentNode_id + ':' + '_'.join(node_name.split())
                    if result['img']:
                        node_img = 'image=' + str(result['img']._get_uri())
                    else:
                        node_img = ""
                    cmd_node = [ "ADD", "NODE", node_id, node_name, "randompos", "-", node_img ]
                    self.send(cmd_node, "outbox")
                    cmd_link =  [ "ADD", "LINK", linkedNode_id, node_id ]
                    self.send(cmd_link, "outbox")
                    
                    uri = result['seeAlso']
                    if uri and str(uri).endswith('.rdf]'):
                        uri = uri._get_uri()
                        #print result['seeAlso'], uri
                        nodes.append((node_id, uri))
                    
            for node in nodes:
                self.parentNode_id = node[0]
                uri = node[1]
                try:
                    self.fetch_data(uri, current_layer+1)
                except:
                    pass          

__kamaelia_components__  = ( RDFParser, )                 

                    
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
    from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams import TopologyViewer3DWithParams
    from Kamaelia.Chassis.Graphline import Graphline
    
    # Data can be from both DataSource and console inputs
    Graphline(
        CONSOLEREADER = ConsoleReader('>>>'),
        DATASOURCE = DataSource(["http://fooshed.net/foaf.rdf 2 10"]),
        PARSER = RDFParser(),
        VIEWER = TopologyViewer3DWithParams(),
        CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("PARSER","inbox"),
        ("DATASOURCE","outbox") : ("PARSER","inbox"),   
        ("PARSER","outbox")   : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),     
        #("PARSER","outbox") : ("CONSOLEECHOER","inbox"),
        
    }
).run()
#!/usr/bin/env python

"""\
===============================================================
Parse RDF data received from a uri
===============================================================
1. If the uri is a rdf data file, it will parse it directly;
if not, it will extract rdf data first before parsing. 

2. The input format is "uri max_layer max_nodePerLayer": 
uri is the uri of the data file
max_layer is the maximum layers of the rdf hierarchy structure (how deep) to parse
max_nodePerLayer is the maximum nodes in one layer (how wide) to parse

3. The output is TopologyViewer commands

4. Typically, it receives inputs from ConsoleReader or ConsoleReader 
and send output to TopologyViewer3D.

5. You may also need to install librdf, a rdf parsing lib from redland. 
See http://librdf.org/ for more information and 
http://librdf.org/bindings/INSTALL.html for installation information.
"""

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

import RDF

class RDFParser(Axon.Component.component):
    """\
======================================================================
A component to parse RDF data received from a uri to TopologyViewer3D command
======================================================================
"""
    def __init__(self):
        super(RDFParser, self).__init__()
        self.rdf_prefix = """
                           PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                           PREFIX owl: <http://www.w3.org/2002/07/owl#>
                           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                          """
        self.num_allNodes = self.num_parentNodes = 0
        
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
        model = RDF.Model()
        parser = RDF.Parser()
        parser.parse_into_model(model, rdf)
        sparql = """
        %s
        %s""" % (self.rdf_prefix, query)
        q = RDF.Query(sparql, query_language="sparql")
        return q.execute(model)

    def fetch_data(self, rdf_uri, current_layer=0):
        if current_layer == self.max_layer:
            return
        else:
            self.num_parentNodes += 1
            #print "--- The ", layer, " layer ---"
            query1 = """
            SELECT DISTINCT ?name ?img
            WHERE { ?x foaf:name ?name .
            OPTIONAL { ?x foaf:img ?img }
            }
            """
            results = self.make_query(rdf_uri, query1)
            result = results.next()
            #print result['name'], ':', result['img']
            linkedNode_name = str(result['name'])
            if self.parentNode_id == "":
                linkedNode_id =  '_'.join(linkedNode_name.split())
            else:
                linkedNode_id =  self.parentNode_id + ':' + '_'.join(linkedNode_name.split())
            if result['img']:
                linkedNode_img = 'image=' + str(result['img']._get_uri())
            else:
                linkedNode_img = ""
            #print linkedNode_img
            cmd = [ "ADD", "NODE", linkedNode_id, linkedNode_name, "randompos", "-", linkedNode_img ]
            self.send(cmd, "outbox")
            #print "*Knows*"
            query2 = """
            SELECT DISTINCT ?name ?img ?seeAlso
            WHERE {
            ?a foaf:knows ?b . ?b foaf:name ?name .
            OPTIONAL { ?b foaf:img ?img } .
            OPTIONAL { ?b rdfs:seeAlso ?seeAlso }
            }
            """
            nodes = []
            results = self.make_query(rdf_uri, query2)
            num_nodePerLayer = 1
            for result in results:
                if self.max_nodePerLayer > 0 and num_nodePerLayer > self.max_nodePerLayer:
                    break
                else:
                    num_nodePerLayer += 1
                    self.num_allNodes += 1
                    #print result['name'], ':', result['img']
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
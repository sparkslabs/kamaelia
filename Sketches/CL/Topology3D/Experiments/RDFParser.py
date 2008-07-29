from rdflib.Graph import Graph, Namespace
from rdflib.URIRef import URIRef

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
ns = dict(foaf=FOAF, rdf=RDF, rdfs=RDF)

g = Graph()
g.parse("http://bigasterisk.com/foaf.rdf")

#g = Graph()
#g.parse("http://www.w3.org/2007/08/pyRdfa/extract?uri=http://apassant.net/about/#alex")

#g = Graph()
#g.parse("http://jibbering.com/foaf.rdf")

#g = Graph()
#g.parse("http://jibbering.com/rdfsvg/1025709113824.rdf")

#for item in g:
#    print g
#drew = URIRef('http://bigasterisk.com/foaf.rdf#drewp')

#for row in g.query('SELECT ?name WHERE { ?p foaf:name ?name }', initNs=ns, initBindings={'?p' : drew}):
#    print row

#for row in g.query('SELECT ?title ?name WHERE { ?x foaf:title ?title ; foaf:name ?name . }', initNs=ns):
#    #print 'Name: ', row[0]
#    print row[0], row[1]
#    #print "%s %s" %row

#! Space after { and before } is needed
sparql = """
SELECT DISTINCT ?name ?knows ?seeAlso ?img ?resource
WHERE {
  ?a foaf:knows ?knows .
  OPTIONAL { ?knows foaf:name ?name } .
  OPTIONAL { ?knows foaf:img ?img } .
  OPTIONAL { ?knows rdfs:seeAlso ?seeAlso . ?seeAlso rdf:resource ?resource }
}
"""


for row in g.query(sparql, initNs=ns):
    print row

## ?x is needed even it is not useful
#for row in g.query('SELECT ?bname WHERE { ?x foaf:knows ?b . ?b foaf:name ?bname . }', initNs=ns):
#    print 'seeAlso ', row
    
#for row in g.query('SELECT ?mbox_sha1sum WHERE { ?x foaf:mbox_sha1sum ?mbox_sha1sum . }', initNs=ns):
#    print 'mbox_sha1sum ', row
    
#for row in g.query('SELECT ?resource WHERE { ?x doap:homepage ?resource . }', initNs=ns):
#    print row
        
#for row in g.query('SELECT ?name ?mbox WHERE { ?x foaf:name ?name . ?x foaf:mbox ?mbox }', initNs=ns):
#    print row
        
#for row in g.query('SELECT ?aname ?bname WHERE { ?a foaf:knows ?b . ?a foaf:name ?aname . ?b foaf:name ?bname . }', 
#                   initNs=ns):
#    print "%s knows %s" % row
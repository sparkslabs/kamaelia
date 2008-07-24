from rdflib.Graph import Graph, Namespace
from rdflib.URIRef import URIRef

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
ns = dict(foaf=FOAF)

g = Graph()
g.parse("http://bigasterisk.com/foaf.rdf")

#for item in g:
#    print g
drew = URIRef('http://bigasterisk.com/foaf.rdf#drewp')

for row in g.query('SELECT ?name WHERE { ?x foaf:name ?name . }', initNs=ns):
    print row

for row in g.query('SELECT ?mbox_sha1sum WHERE { ?x foaf:mbox_sha1sum ?mbox_sha1sum . }', initNs=ns):
    print row
    
for row in g.query('SELECT ?name ?mbox WHERE { ?x foaf:name ?name . ?x foaf:mbox ?mbox }', initNs=ns):
    print row
        
for row in g.query('SELECT ?aname ?bname WHERE { ?a foaf:knows ?b . ?a foaf:name ?aname . ?b foaf:name ?bname . }', 
                   initNs=ns):
    print "%s knows %s" % row
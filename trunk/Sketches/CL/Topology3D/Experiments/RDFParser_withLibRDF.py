import RDF

model = RDF.Model()
parser = RDF.Parser()
#uri = "http://bigasterisk.com/foaf.rdf"
uri = "http://jibbering.com/foaf.rdf"
parser.parse_into_model(model, uri)

#query = """
#SELECT ?name
#WHERE {
#  ?x foaf:name ?name
#}
#""" 

query = """
SELECT DISTINCT ?name ?knows ?seeAlso ?img
WHERE {
  ?a foaf:knows ?knows .
  OPTIONAL { ?knows foaf:name ?name } .
  OPTIONAL { ?knows foaf:img ?img } .
  OPTIONAL { ?knows rdfs:seeAlso ?seeAlso }
}
"""

sparql = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
%s""" %query


q = RDF.Query(sparql, query_language="sparql")
results = q.execute(model)
#print results

for result in results:
    print result['name'], result['seeAlso']

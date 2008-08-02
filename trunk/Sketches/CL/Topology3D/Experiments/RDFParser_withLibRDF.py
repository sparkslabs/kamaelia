import RDF

#===============================================================================
# model = RDF.Model()
# parser = RDF.Parser()
# #uri = "http://bigasterisk.com/foaf.rdf"
# #uri = "http://jibbering.com/foaf.rdf"
# #uri = "http://www.perceive.net/xml/foaf.rdf"
# uri = "http://fooshed.net/foaf.rdf"
# parser.parse_into_model(model, uri)
# 
# #query = """
# #SELECT ?name
# #WHERE {
# #  ?x foaf:name ?name
# #}
# #""" 
# 
# 
# query = """
# SELECT DISTINCT ?aname ?aimg ?bname ?bimg ?seeAlso 
# WHERE {
#  ?a foaf:aname ?aname . ?a foaf:img ?aimg .
#  ?a foaf:knows ?b . 
#  OPTIONAL { ?b foaf:name ?name } .
#  OPTIONAL { ?b foaf:img ?bimg } .
#  OPTIONAL { ?b rdfs:seeAlso ?seeAlso }
# }
# """
# 
# sparql = """
# PREFIX foaf: <http://xmlns.com/foaf/0.1/>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# %s""" %query
# 
# 
# q = RDF.Query(sparql, query_language="sparql")
# results = q.execute(model)
# #print results
# 
# 
# for result in results:
#    print result['name'], ':', result['aimg'], result['seeAlso']
#===============================================================================

PREFIX = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

def make_query(rdf, query):
    model = RDF.Model()
    parser = RDF.Parser()
    parser.parse_into_model(model, rdf)
    sparql = """
    %s
    %s""" % (PREFIX, query)
    q = RDF.Query(sparql, query_language="sparql")
    return q.execute(model)

counter2 = counter = 0
def fetch_data(rdf_uri, layer=0, MAX_LAYER = 2):
    if layer == MAX_LAYER:
        return
    else:
        global counter, counter2
        counter += 1
        print "--- The ", layer, " layer ---"
        query1 = """
        SELECT DISTINCT ?name ?img
        WHERE { ?x foaf:name ?name .
        OPTIONAL { ?x foaf:img ?img }
        }
        """
        results = make_query(rdf_uri, query1)
        result = results.next()
        print result['name'], ':', result['img']
        
        print "*Knows*"
        query2 = """
        SELECT DISTINCT ?name ?img ?seeAlso
        WHERE {
        ?a foaf:knows ?b . ?b foaf:name ?name .
        OPTIONAL { ?b foaf:img ?img } .
        OPTIONAL { ?b rdfs:seeAlso ?seeAlso }
        }
        """
        results = make_query(rdf_uri, query2)
 #        import copy
 #        results2 = copy.deepcopy(results) 
        for result in results:
            counter2 += 1
            print result['name'], ':', result['img']
        results = make_query(rdf_uri, query2)
        for result in results:
            uri = result['seeAlso']
            if uri and str(uri).endswith('.rdf]'):
                uri = uri._get_uri()
                print result['seeAlso'], uri
                try:
                    fetch_data(uri, layer+1)
                except:
                        pass                    
    
fetch_data("http://www.w3.org/2007/08/pyRdfa/extract?uri=http://apassant.net/about/#alex")
print counter, counter2 

#MAX_LAYER = 2
#rdf_uris = ["http://fooshed.net/foaf.rdf"] 
#for x in xrange(MAX_LAYER):
#    print "--- The ", x, " layer ---"
#    print "--------------------------------"
#    for rdf_uri in rdf_uris:
#        counter += 1
#        query1 = """
#        SELECT DISTINCT ?name ?img
#        WHERE { ?x foaf:name ?name .
#        OPTIONAL { ?x foaf:img ?img }
#        }
#        """
#        results = make_query(rdf_uri, query1)
#        result = results.next()
#        print result['name'], ':', result['img']
#        rdf_uris = []
#        
#        print "*Knows*"
#        query2 = """
#        SELECT DISTINCT ?name ?img ?seeAlso
#        WHERE {
#        ?a foaf:knows ?b . ?b foaf:name ?name .
#        OPTIONAL { ?b foaf:img ?img } .
#        OPTIONAL { ?b rdfs:seeAlso ?seeAlso }
#        }
#        """
#        results = make_query(rdf_uri, query2)
#        for result in results:
#            counter2 += 1
#            uri = result['seeAlso']
#            if uri:
#                uri = uri._get_uri()
#                rdf_uris.append(uri)
#            print result['name'], ':', result['img']
#print counter, counter2 

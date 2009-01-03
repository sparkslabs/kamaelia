#!/usr/bin/python

#
# Usage: Modeller.py <filename>
#
# The parse expects a file that looks somewhat like this:
#
# entity missionagent
# entity person(missionagent)
# entity team(missionagent)
#
# entity missionitem:
#     simpleattributes visible
#
# entity activemission
#
# # Now the relationships
# #
# relation participatesin(activemission,missionagent)
# relation creates(missionagent,missionitem)
#
#
# The parser generates an intermediate model that look like this:
#
#    model = [
#        ["entity", { "name" : "missionagent" }],
#        ["entity", { "name" : "person",
#                     "subtype" : "missionagent",
#                   }],
#        ["entity", { "name" : "team",
#                     "subtype" : "missionagent",
#                   }],
#        ["entity", { "name" : "missionitem",
#                     "simpleattributes" : ["visible"],
#                   }
#        ],
#        ["entity", { "name" : "activemission" }],
#
#        ["relation", { "name" : "participatesin",
#                       "entities" : [ "activemission", "missionagent"],
#                     }],
#        ["relation", { "name" : "creates",
#                       "entities" : [ "missionagent", "missionitem"],
#                     }],
#     ]
#
# The next stage then emits data suitable for the ER Visualiser, which
# looks something like this:
#
# ADD NODE missionagent missionagent auto entity
# ADD NODE person person auto entity
# ADD NODE ISA1 isa auto isa
# ADD NODE team team auto entity
# ADD NODE missionitem missionitem auto entity
# ADD NODE visible visible auto attribute
# ADD NODE activemission activemission auto entity
# ADD NODE participatesin participatesin auto relation
# ADD NODE creates creates auto relation
# ADD LINK ISA1 missionagent
# ADD LINK person ISA1
# ADD LINK team ISA1
# ADD LINK missionitem visible
# ADD LINK activemission participatesin
# ADD LINK missionagent participatesin
# ADD LINK missionagent creates
# ADD LINK missionitem creates
#

import sys

F = open(sys.argv[1],"rb")
model_t = F.read()
F.close()

model_lines = model_t.split("\n")

def parser(model_lines):
    block = False
    for line in model_lines:
        if line == "": continue
        if line.lstrip()[0] == "#": continue
        if block and line[0] != " ":
            yield "ENDBLOCK"
            block = False
        if line[-1] == ":":
            yield "BLOCK"
            block = True
            line = line[:-1]
        yield line

def parseEntityLine(P):
    toks = P.split()
    entity = dict()
    namespec = toks[1]
    if ("(" in toks[1]) and toks[1][-1]==")":
        name, subtype = toks[1][:-1].split("(")
        namespec = name
        entity["subtype"] = subtype

    entity["name"] = namespec
    return ["entity", entity]

class ParseError(Exception): pass

def parseRelationLine(P):
    toks = P.split()
    entity = dict()
    namespec = toks[1]
    if ("(" in toks[1]) and toks[1][-1]==")":
        name, subtype = toks[1][:-1].split("(")
        namespec = name
        entity["entities"] = subtype.split(",")
    else:
        raise ParseError(P)

    entity["name"] = namespec
    return ["relation", entity]

def parseSimpleAttributes(P):
    toks = P.split()
    result = {"simpleattributes": toks[1:]}
    return result

def parseMultilineEntity(X):
    record = {}
    for P in X:
        if P[:6] == "entity":
            record.update(parseEntityLine(P)[1])
            continue
        if P[:16] == "simpleattributes":
            record.update(parseSimpleAttributes(P))

    return ["entity", record ]

def parse_model(model_lines):
    C = False
    for P in parser(model_lines):
        if P == "BLOCK":
            C = True
            X = []
            continue
        if P == "ENDBLOCK":
            X = [ x.strip() for x in X ]
            if X[0][:6] == "entity":
                record = parseMultilineEntity(X)
            yield record
            C = False
            continue
        if C:
            X.append(P)
        else:
            toks = P.split()
            record = []
            if toks[0] == "entity":
                record = parseEntityLine(P)
            if toks[0] == "relation":
                record = parseRelationLine(P)
            yield record

model3 = list(parse_model(model_lines))

entities = {}
supertypes = {}

NODES = []
LINKS = []
isamax = 0
for item in model3:
    if item[0] == "relation":
        relation = item[1]
        NODES.append("ADD NODE %s %s auto relation" % (relation["name"],relation["name"]))
        for entity in relation["entities"]:
            LINKS.append("ADD LINK %s %s" % (entity, relation["name"]))
    if item[0] == "entity":
        entity = item[1]
        name = entity["name"]
        entities[name] = entity
        supertype = entities[name].get("subtype")
        NODES.append("ADD NODE %s %s auto entity" % (name,name) )
        if supertype:
            if supertype not in supertypes:
                supertypes[supertype] = True
                isamax += 1
                NODES.append("ADD NODE ISA%d isa auto isa" % (isamax,) )
                LINKS.append("ADD LINK ISA%d %s" % (isamax,supertype) )
            LINKS.append("ADD LINK %s ISA%d" % (name,isamax) )
        attributes = entity.get("simpleattributes")
        if attributes:
            for attribute in attributes:
                NODES.append("ADD NODE %s %s auto attribute" % (attribute,attribute) )
                LINKS.append("ADD LINK %s %s" % (name,attribute) )

for node in NODES:
    print node

for link in LINKS:
    print link

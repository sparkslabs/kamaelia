#!/usr/bin/python

def parser(model_lines):
    block = False
    for line in model_lines:
        if line.lstrip() == "": continue
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

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess
import pprint

class ERParser(Axon.Component.component):
    def shutdown(self):
        while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                self.shutdown_mess = data
                return True
        return 0

    def main(self):
        X = []
        while not self.shutdown():
            while not self.anyReady():
                self.pause()
                yield 1
            while self.dataReady("inbox"):
                L = self.recv("inbox")
                L = L[:-1]
                X.append(L)
            yield 1

        Y= list(parse_model(X))
        self.send(Y,"outbox")

        yield 1
        yield 1
        self.send(self.shutdown_mess,"signal")

import pprint
class ERModel2Visualiser(Axon.Component.component):
    def shutdown(self):
        while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                self.shutdown_mess = data
                return True
        return 0
    def main(self):
        X = []
        while not self.shutdown():
            while not self.anyReady():
                self.pause()
                yield 1
            while self.dataReady("inbox"):
                L = self.recv("inbox")
                X+=(L)
            yield 1

        entities = {}
        supertypes = {}
        NODES = []
        LINKS = []
        isamax = 0
        for item in X:
            if len(item)==0: continue
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
            self.send(node, "outbox")

        for link in LINKS:
            self.send(link, "outbox")
        yield 1
        yield 1
        self.send(self.shutdown_mess,"signal")


if __name__ == "__main__":
    import sys
    import pprint
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Chassis.Pipeline import Pipeline
    Pipeline(
        ReadFileAdaptor(sys.argv[1]),
        ERParser(),
        ERModel2Visualiser(),
#        PureTransformer(lambda x: pprint.pformat(x)+"\n"),
#        ConsoleEchoer(),
    ).run()


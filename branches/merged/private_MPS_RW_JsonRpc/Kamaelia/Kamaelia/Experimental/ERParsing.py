#!/usr/bin/python
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
==============================================
Parser components for Entity-Relationship data
==============================================

ERParser parses and buffers lines of text containing entity-relationship data.
Once a shutdown message is received, it emits the parsed data as a list of
entities and relationships.

ERModel2Visualiser transforms parsed entity-relationship data into textual
commands for the TopologyViewer component to produce a visualisation. The
TopologyViewer must be configured with suitable particle types - such as
Kamaelia.Visualisation.ER.ERVisualiserServer.ERVisualiser

See: Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer



Example Usage:
--------------

A simple pipeline that reads in entity-relationship data from a file and writes
out commands, suitable for a topology visualiser, to the console::

    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Util.Console import ConsoleEchoer

    Pipeline(
        ReadFileAdaptor(entity_relationship_data_file),
        ERParser(),
        ERModel2Visualiser(),
        PureTransformer(lambda x: pprint.pformat(x)+"\\n"),
        ConsoleEchoer(),
    ).run()

Provide the following file of entity relationship data::

    #
    # entity relationship data in this file!
    #
    
    entity Artist:
        simpleattributes artisticname genre

    entity Manager:
        simpleattributes ID name1 telephone

    entity ContractInfo:
        simpleattributes contractID data_from data_to duration1

    entity MasterTrack:
        simpleattributes trackID working_title duration2

    entity SoundEngineer:
        simpleattributes sound_eng_ID name2

    entity FinishedTrack:
        simpleattributes version final_duration released_title

    entity Album:
        simpleattributes album_ID title

    relation ManagedBy(Artist,Manager)
    relation HasContract(Artist,ContractInfo)
    relation RecordedBy(MasterTrack,Artist)
    relation EditedBy(SoundEngineer,MasterTrack)
    relation OriginatesFrom(FinishedTrack,MasterTrack)
    relation GroupedOn(FinishedTrack,Album)
    relation CreatedBy(Album,Artist)

Once the ReadFileAdaptor component has finished reading and terminates, the
ERParser component sends a message, containing the following, out of its
"outbox" outbox::

    [['entity', {'name': 'Artist', 'simpleattributes': ['artisticname', 'genre']}],
     ['entity',
      {'name': 'Manager', 'simpleattributes': ['ID', 'name1', 'telephone']}],
     ['entity',
      {'name': 'ContractInfo',
       'simpleattributes': ['contractID', 'data_from', 'data_to', 'duration1']}],
     ['entity',
      {'name': 'MasterTrack',
       'simpleattributes': ['trackID', 'working_title', 'duration2']}],
     ['entity',
      {'name': 'SoundEngineer', 'simpleattributes': ['sound_eng_ID', 'name2']}],
     ['entity',
      {'name': 'FinishedTrack',
       'simpleattributes': ['version', 'final_duration', 'released_title']}],
     ['entity', {'name': 'Album', 'simpleattributes': ['album_ID', 'title']}],
     ['relation', {'entities': ['Artist', 'Manager'], 'name': 'ManagedBy'}],
     ['relation', {'entities': ['Artist', 'ContractInfo'], 'name': 'HasContract'}],
     ['relation', {'entities': ['MasterTrack', 'Artist'], 'name': 'RecordedBy'}],
     ['relation',
      {'entities': ['SoundEngineer', 'MasterTrack'], 'name': 'EditedBy'}],
     ['relation',
      {'entities': ['FinishedTrack', 'MasterTrack'], 'name': 'OriginatesFrom'}],
     ['relation', {'entities': ['FinishedTrack', 'Album'], 'name': 'GroupedOn'}],
     ['relation', {'entities': ['Album', 'Artist'], 'name': 'CreatedBy'}]]

And the following is output from the console::

    'ADD NODE Artist Artist auto entity'
    'ADD NODE artisticname artisticname auto attribute'
    'ADD NODE genre genre auto attribute'
    'ADD NODE Manager Manager auto entity'
    'ADD NODE ID ID auto attribute'
    'ADD NODE name1 name1 auto attribute'
    'ADD NODE telephone telephone auto attribute'
    'ADD NODE ContractInfo ContractInfo auto entity'
    'ADD NODE contractID contractID auto attribute'
    'ADD NODE data_from data_from auto attribute'
    'ADD NODE data_to data_to auto attribute'
    'ADD NODE duration1 duration1 auto attribute'
    'ADD NODE MasterTrack MasterTrack auto entity'
    'ADD NODE trackID trackID auto attribute'
    'ADD NODE working_title working_title auto attribute'
    'ADD NODE duration2 duration2 auto attribute'
    'ADD NODE SoundEngineer SoundEngineer auto entity'
    'ADD NODE sound_eng_ID sound_eng_ID auto attribute'
    'ADD NODE name2 name2 auto attribute'
    'ADD NODE FinishedTrack FinishedTrack auto entity'
    'ADD NODE version version auto attribute'
    'ADD NODE final_duration final_duration auto attribute'
    'ADD NODE released_title released_title auto attribute'
    'ADD NODE Album Album auto entity'
    'ADD NODE album_ID album_ID auto attribute'
    'ADD NODE title title auto attribute'
    'ADD NODE ManagedBy ManagedBy auto relation'
    'ADD NODE HasContract HasContract auto relation'
    'ADD NODE RecordedBy RecordedBy auto relation'
    'ADD NODE EditedBy EditedBy auto relation'
    'ADD NODE OriginatesFrom OriginatesFrom auto relation'
    'ADD NODE GroupedOn GroupedOn auto relation'
    'ADD NODE CreatedBy CreatedBy auto relation'
    'ADD LINK Artist artisticname'
    'ADD LINK Artist genre'
    'ADD LINK Manager ID'
    'ADD LINK Manager name1'
    'ADD LINK Manager telephone'
    'ADD LINK ContractInfo contractID'
    'ADD LINK ContractInfo data_from'
    'ADD LINK ContractInfo data_to'
    'ADD LINK ContractInfo duration1'
    'ADD LINK MasterTrack trackID'
    'ADD LINK MasterTrack working_title'
    'ADD LINK MasterTrack duration2'
    'ADD LINK SoundEngineer sound_eng_ID'
    'ADD LINK SoundEngineer name2'
    'ADD LINK FinishedTrack version'
    'ADD LINK FinishedTrack final_duration'
    'ADD LINK FinishedTrack released_title'
    'ADD LINK Album album_ID'
    'ADD LINK Album title'
    'ADD LINK Artist ManagedBy'
    'ADD LINK Manager ManagedBy'
    'ADD LINK Artist HasContract'
    'ADD LINK ContractInfo HasContract'
    'ADD LINK MasterTrack RecordedBy'
    'ADD LINK Artist RecordedBy'
    'ADD LINK SoundEngineer EditedBy'
    'ADD LINK MasterTrack EditedBy'
    'ADD LINK FinishedTrack OriginatesFrom'
    'ADD LINK MasterTrack OriginatesFrom'
    'ADD LINK FinishedTrack GroupedOn'
    'ADD LINK Album GroupedOn'
    'ADD LINK Album CreatedBy'
    'ADD LINK Artist CreatedBy'



ERParser Behaviour
------------------

Send entity-relationship textual description data to the "inbox" inbox as
individual strings, one line per string.

When a producerFinished or shutdownMicroprocess is sent to the "control" inbox
this component sends out a single message containing, as a list, the entities
and relationships parsed from the data.

ERParser then immediately terminates and sends out the shudown message it
received out of its "signal" outbox.

See description of "Entity-Relationship textual description format" and
"Parsed Entity-Relationship data".



ERModel2Visualiser Behaviour
----------------------------

Send parsed entity-relationship data to the "inbox" inbox.

When a producerFinished or shutdownMicroprocess is sent to the "control" inbox
this component transforms it into a set of textual (string) commands suitable
for a TopologyViewer component and sends it out of its "outbox" outbox in two
messages. The first contains the commands to create the required nodes and the
second contains the commands to create the linkages between them.

ERModel2Visualiser then immediately terminates and sends out the shudown message
it received out of its "signal" outbox.

The TopologyViewer component that receives the commands must be configured to
know the following node types:

- entity     -- represents an entity
- relation   -- represents the mid-point and name label of a relation
- attribute  -- represents an attribute of an entity
- isa        -- represents the mid-point and label of a subtype-supertype relation

See description of "Parsed Entity-Relationship data".



Entity-Relationship textual description format
----------------------------------------------

Entity relationship data is expressed as a text file. Blank lines or lines
beginning with a '#' character are ignored.

Define entities by writing `entity NAME:` on its own line, without indentation.
To define attributes for an entity, write, indented, on the next line,
`simpleattributes` followed by a space separated list of attributes. 

To make an entity a subtype of another entity, begin the entity declaration
instead with `entity NAME(SUPERTYPE):`.

Example entities::

    entity person:
        simpleattributes female name=sarah

    # the following entities are subtypes of the 'person' entity
            
    entity mum(person):
    
    entity daughter(person):
    
    entity son(person):
    
To define relations, write `relation RELATION_NAME(ENTITY,ENTITY,...)` on its
own line without indentation. A relation must involve two or more entities. For
example::

    relation RelatedTo(mum,daughter,son)
    relation siblings(son,daughter)



Parsed Entity-Relationship data
-------------------------------

The parsed data takes the form of a list of entities and relations.

An entity is represented as a list beginning with the string "entity", followed
by a dictionary defining attributes. The key "name" maps to the name of the
entity:

    [ "entity", { "name": <name>, "simpleattributes": [ <attribute>, <attribute>, ... ], "subtype": <supertype-name> ]

The key "simpleattributes", if present, maps to a list containing, as strings
each attribute.

Some may also contain a "subtype" key which maps to the name of the
entity that this one is a subtype of.

For example::

    [ "entity",
      { "name"             : "person",
        "simpleattributes" : [ "female", "name=sarah" ]
      }
    ]
    
    [ "entity",
      { "name" : "mum",
        "subtype" : "person"
      }
    ]
    
A relation is represented as a list beginning with the string "relation",
followed by a dictionary defining attributes:

    [ "relation", { "name": <name>, "entities": [ <entity-name>, <entity-name>, ... ]

The key "name" maps to the name of the entity. The key "entities" maps to a list
containing, as strings, the names of the entities involved in the relation. For
example::

    [ "relation",
      { "name"     : "IsA",
        "entities" : [ "mum", "person" ]
      }
    ]

"""

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
    if block:
        yield "ENDBLOCK"
        block = False

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
    """\
    ERParser() -> new ERParser component.
    
    Parses lines of Entity-Relationship data, send to the "inbox" inbox as
    strings. Once shutdown, sends out a list of parsed entity and relationship
    data.
    """
    
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
    """\
    ERModel2Visualiser() -> new ERModel2Visualiser component.
    
    Send parsed entity-relationship data as lists of entities and relations to
    the "inbox" inbox. Once shutdown, sends out commands to drive a
    TopologyViewer component to produce a visualisation of the described
    entities and relations.
    """
    
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



__kamaelia_components__ = ( ERParser, ERModel2Visualiser, )



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


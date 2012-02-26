#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
# Needed to allow import
#
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

See http://www.w3.org/TR/rdf-sparql-query/ for more information about SPARQL query, 
http://www.w3.org/RDF/ about for more information about RDF.
"""
                    
from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams import TopologyViewer3DWithParams
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Apps.CL.FOAFViewer.RDFParsing import RDFParser


Graphline(
    CONSOLEREADER = ConsoleReader('>>>'),
    PARSER = RDFParser(),
    VIEWER = TopologyViewer3DWithParams(),
    CONSOLEECHOER = ConsoleEchoer(),
    linkages = {
        ("CONSOLEREADER","outbox") : ("PARSER","inbox"),
        ("PARSER","outbox")   : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),     
        #("PARSER","outbox") : ("CONSOLEECHOER","inbox"),
        
    }
).run()
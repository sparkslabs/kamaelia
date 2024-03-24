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
=====================================================================================
CollabParser: Parse collaboration data between organizations received as dictionary
=====================================================================================
Parse collaboration data between organizations received as dictionary, 
and then send out TopologyViewer commands



Example Usage
-------------
A simple file driven collaboration parser and draw them with 3D topology viewer::

    Pipeline( ReadFileAdaptor('Data/collab.json'),
              JSONDecoder(),
              CollabParser(),
              TopologyViewer3DWithParams(),
              ConsoleEchoer(),
            ).run()



How does it work?
-----------------

The input format:
    The input is a dictionary,
    {'orgData' : {'org1' : ['staff1',...],...},
    'collabData' : {'collab1' : ['staff1',...],...}}
    e.g.,
    {'orgData' : {'BBC' : ['Beckham', 'Bell', 'Betty', 
        'Bill', 'Brad', 'Britney'],
        'Google' : ['Geoff', 'Gerard', 'Gordon', 'George', 'Georgia', 'Grant'],
        'Manchester' : ['Michael', 'Matt', 'Madonna', 'Mark', 'Morgon', 'Mandela'],
        'Leeds' : ['Leo', 'Lorri', 'Louis', 'Lampard', 'Lily', 'Linda'],
        'Sheffield' : ['Sylvain', 'Sugar', 'Sophie', 'Susan', 'Scarlet', 'Scot']},
    'collabData' : {'Audio' : ['Beckham', 'Bell', 'Geoff', 'Gerard', 'Gordon', 'Leo'],
           'Video' : ['Michael', 'Matt', 'Sophie', 'Susan'],
           'Internet' : ['Sylvain', 'Sugar', 'Beckham', 'Mandela'],
           'XML' : ['Lampard', 'Lily', 'Linda', 'Geoff', 'Scot'],
           'Visualisation' : ['Leo', 'Lorri', 'Susan', 'Britney']}
    }

The output is TopologyViewer commands.

Typically, it receives inputs from JSONDecoder and send output to TopologyViewer3D. 
After the data are drawn by TopologyViewer3D, double-click nodes to show all people involved 
in the collaboration or belonging to the organization.




==============================================================================================================
CollabWithViewParser: Parse collaboration data between organizations received as dictionary with view support
==============================================================================================================
Parse collaboration data between organizations received as dictionary, 
and then send out a dictionary of TopologyViewer commands



Example Usage
-------------
A simple file driven collaboration parser, and then send output to DictChooser 
and at last draw them with 3D topology viewer::

    Graphline(
        READER = ReadFileAdaptor('Data/collab.json'),
        JSONDECODER = JSONDecoder(),
        CONSOLEECHOER = ConsoleEchoer(),
        COLLABPARSER = CollabWithViewParser(),
        BUTTONORG = Button(caption="orgView", msg="orgView", position=(-10,8,-20)),
        BUTTONSTAFF = Button(caption="staffView", msg="staffView", position=(-8,8,-20)),
        DICTCHOOSER = DictChooser(),
        VIEWER = TopologyViewer3DWithParams(laws=laws),
    linkages = {
        ("READER","outbox") : ("JSONDECODER","inbox"),
        ("JSONDECODER","outbox")  : ("COLLABPARSER","inbox"),     
        ("COLLABPARSER","outbox")  : ("DICTCHOOSER","option"),
        ("BUTTONORG","outbox")  : ("DICTCHOOSER","inbox"),
        ("BUTTONSTAFF","outbox")  : ("DICTCHOOSER","inbox"),
        ("DICTCHOOSER","outbox")  : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()



How does it work?
-----------------
The input format:
Same as CollabParser.

The output is a dictionary of TopologyViewer commands. The format is
{'orgView' : [...], 'staffView' : [...]}

Typically, it receives inputs from JSONDecoder and sends output to the option box of DictChooser first,
and then DictChooser sends data to TopologyViewer3D.

After the data are drawn by TopologyViewer3D, double-click nodes to show all people involved 
in the collaboration or belonging to the organization. Click button to swith between different views. 
"""


from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams import TopologyViewer3DWithParams
from Kamaelia.Support.Particles.SimpleLaws import SimpleLaws
from Kamaelia.UI.OpenGL.Button import Button
from Kamaelia.Apps.CL.DictChooser import DictChooser
from Kamaelia.Apps.CL.JSON import JSONDecoder
from Kamaelia.Apps.CL.CollabViewer.CollabParsing import CollabWithViewParser

laws = SimpleLaws(bondLength=2.2)

# Data can be from both DataSource and console inputs
Graphline(
    CONSOLEREADER = ConsoleReader('>>>'),
    READER = ReadFileAdaptor('Data/collab.json'),
    JSONDECODER = JSONDecoder(),
    CONSOLEECHOER = ConsoleEchoer(),
    COLLABPARSER = CollabWithViewParser(),
    BUTTONORG = Button(caption="orgView", msg="orgView", position=(-10,8,-20)),
    BUTTONSTAFF = Button(caption="staffView", msg="staffView", position=(-8,8,-20)),
    DICTCHOOSER = DictChooser(allowDefault = True),
    VIEWER = TopologyViewer3DWithParams(laws=laws),
    linkages = {
        ("CONSOLEREADER","outbox") : ("JSONDECODER","inbox"),
        ("READER","outbox") : ("JSONDECODER","inbox"),
        ("JSONDECODER","outbox")  : ("COLLABPARSER","inbox"),     
        #("COLLABPARSER","outbox")  : ("CONSOLEECHOER","inbox"),
        ("COLLABPARSER","outbox")  : ("DICTCHOOSER","option"),
        ("BUTTONORG","outbox")  : ("DICTCHOOSER","inbox"),
        ("BUTTONSTAFF","outbox")  : ("DICTCHOOSER","inbox"),
        #("DICTCHOOSER","outbox")  : ("CONSOLEECHOER","inbox"),
        ("DICTCHOOSER","outbox")  : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()
#!/usr/bin/python

import Axon
from Axon.Component import component
import Axon.Ipc as Ipc
#from Axon.Ipc import producerFinished, shutdownMicroprocess, newComponent

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists

from Kamaelia.Visualisation.Axon.PComponent import PComponent
from Kamaelia.Visualisation.Axon.PPostbox import PPostbox
from Kamaelia.Visualisation.Axon.AxonLaws import AxonLaws
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent

from Kamaelia.UI.Pygame.Button import Button

from Introspector import Introspector
from Sandbox import Sandbox
from NameRemapper import NameRemapper
from EditorLogic import EditorLogic
from ComponentEditor import ComponentEditor

import re

classes = [ { "module"   : "Axon.Component",
              "class"    : "component",
              "defaults" : "",
            },
            { "module"   : "Kamaelia.Util.Console",
              "class"    : "ConsoleEchoer",
              "defaults" : "forwarder = True",
            },
            { "module"   : "Kamaelia.File.Reading",
              "class"    : "RateControlledFileReader",
              "defaults" : 'filename="Sandbox.py", readmode="lines", rate=5, chunksize=1',
            },
          ]
             


class PComponent2(PComponent):
    def __init__(self, ID, position, name):
        textualname = self.parsename(name)
        super(PComponent2, self).__init__(ID=ID, position=position, name=textualname)
        self.name = name

    def parsename(self, name):
        match = re.match("^(?:[^:]*?:)??([^(]+)", name)
        return match.group(0)
        

    def set_label(self, newname):
        print "new label :",newname
        textualname = self.parsename(newname)
        super(PComponent2,self).set_label(textualname)
        self.name = newname
        print "set"

particleTypes = { "component" : PComponent2,
                    "inbox"     : PPostbox.Inbox,
                    "outbox"    : PPostbox.Outbox
                }
TVC = TopologyViewerComponent(position=(0,0), laws = AxonLaws(), particleTypes=particleTypes)

SANDBOX = Sandbox()

Graphline(
    CONSOLEINPUT = pipeline(
                     ConsoleReader(">>> "),
                     chunks_to_lines(),
                     lines_to_tokenlists(),
                   ),
    DEBUG = ConsoleEchoer(forwarder=True),
    TVC = TVC,
    INTROSPECTOR = pipeline(Introspector(SANDBOX), chunks_to_lines(), lines_to_tokenlists()),
    SANDBOX = SANDBOX,
#    REMAPPER = NameRemapper(),
    NEW = Button(caption="New Component", msg="NEXT", position=(72,32)),
    CHANGE = Button(caption="Change Component", msg="NEXT", position=(182,32)),
    DEL = Button(caption="Delete Component", msg="NEXT", position=(292,32)),
    LINK = Button(caption="Make Link", msg="NEXT", position=(402,32)),
    GO   = Button(caption="Activate!", msg="NEXT", position=(500,32)),
    EDITOR_LOGIC = EditorLogic(),
    CED = ComponentEditor(classes),
    linkages = {
        ("INTROSPECTOR", "outbox") :  ("TVC", "inbox"),
        ("CONSOLEINPUT", "outbox") : ("SANDBOX", "inbox"),
#        ("SANDBOX", "outbox") : ("REMAPPER", "mappings"),
        
        ("TVC", "outbox") : ("EDITOR_LOGIC", "inbox"),
        ("EDITOR_LOGIC", "commands") : ("SANDBOX", "inbox"),
        ("NEW", "outbox"): ("EDITOR_LOGIC", "newnode"),
        ("CHANGE", "outbox"): ("EDITOR_LOGIC", "changenode"),
        ("DEL", "outbox") : ("EDITOR_LOGIC", "delnode"),
        ("LINK", "outbox") : ("EDITOR_LOGIC", "linknode"),
        ("GO", "outbox") : ("EDITOR_LOGIC", "go"),
        
        ("EDITOR_LOGIC", "outbox") : ("CED", "inbox"),
        ("EDITOR_LOGIC", "componentedit") : ("CED", "inbox"),
        ("CED", "outbox") : ("SANDBOX", "inbox"),
        ("CED", "topocontrol") : ("TVC", "inbox"),
    }
).run()

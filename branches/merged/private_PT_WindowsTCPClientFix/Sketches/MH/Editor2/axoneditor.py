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
            { "module"   : "Kamaelia.Internet.SingleServer",
              "class"    : "SingleServer",
              "defaults" : "port=1601",
            },
            { "module"   : "Kamaelia.Internet.TCPClient",
              "class"    : "TCPClient",
              "defaults" : 'host="localhost", port=1601, delay=0',
            },
            { "module"   : "Kamaelia.Codec.Vorbis",
              "class"    : "AOAudioPlaybackAdaptor",
              "defaults" : "",
            },
            { "module"   : "Kamaelia.Codec.Vorbis",
              "class"    : "VorbisDecode",
              "defaults" : "",
            },
            { "module"   : "Kamaelia.Codec.Dirac",
              "class"    : "DiracDecoder",
              "defaults" : "",
            },
            { "module"   : "Kamaelia.Util.RateFilter",
              "class"    : "MessageRateLimit",
              "defaults" : "messages_per_second = 15, buffer = 30",
            },
            { "module"   : "Kamaelia.UI.Pygame.VideoOverlay",
              "class"    : "VideoOverlay",
              "defaults" : "",
            },
            { "module" : "Kamaelia.Chassis.Pipeline",
              "class"  : "Pipeline",
              "defaults" : "",
            },
          ]
             
import time, pygame

class PComponent2(PComponent):
    def __init__(self, ID, position, name):
        (textualname, self.isrunning, self.ispaused) = self.parsename(name)
        super(PComponent2, self).__init__(ID=ID, position=position, name=name)
        (textualname, self.isrunning, self.ispaused) = self.parsename(name)
        self.name = name
        self.cycle = 0.0
        self.prevtime = time.time()
        self.arcradius = int(self.radius*0.7)
        self.arcradius2 = int(self.radius*1.4)
        self.arcwidth = int(self.radius*0.1)

    def parsename(self, name):
        match = re.match(r"^([*+]?)(?:[^.:(]*[.:])*([^.:(]+)", name)
        return match.group(2), match.group(1) == "*", match.group(1) == "+"
        

    def set_label(self, newname):
        (textualname, self.isrunning, self.ispaused) = self.parsename(newname)
        super(PComponent2,self).set_label(textualname)
        self.name = newname

    def render(self, surface):
        oldrenderer = PComponent.render(self, surface)
        yield oldrenderer.next()  # returns 1
        yield oldrenderer.next()  # returns 2
        yield oldrenderer.next()  # returns 3
        if self.isrunning or self.ispaused:
            x = int(self.pos[0] - self.left)
            y = int(self.pos[1] - self.top )
            timenow = 4*time.time()
            if not self.ispaused:
                self.cycle -= (timenow-self.prevtime)
            self.prevtime = timenow
            startangle = self.cycle
            stopangle = startangle + 1.0
            for i in range(0,4):
                pygame.draw.arc(surface, (255,255,255), pygame.Rect(x-self.arcradius, y-self.arcradius, self.arcradius2, self.arcradius2), startangle, stopangle, self.arcwidth)
                startangle = startangle + 1.57
                stopangle  = stopangle  + 1.57
        yield 4
        yield oldrenderer.next()                                                    

particleTypes = { "component" : PComponent2,
                    "inbox"     : PPostbox.Inbox,
                    "outbox"    : PPostbox.Outbox
                }
                
from Kamaelia.UI.PygameDisplay import PygameDisplay

pgd = PygameDisplay(width=800,height=600).activate()
PygameDisplay.setDisplayService(pgd)

TVC = TopologyViewerComponent(position=(0,48), laws = AxonLaws(), particleTypes=particleTypes)

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
    NEW = Button(caption="New Component", msg="NEXT", position=(8,8)),
    CHANGE = Button(caption="Change Component", msg="NEXT", position=(128,8)),
    DEL = Button(caption="Delete Component", msg="NEXT", position=(256,8)),
    LINK = Button(caption="Make Link", msg="NEXT", position=(402,8)),
    UNLINK = Button(caption="Break Link", msg="NEXT", position=(480,8)),
    GO   = Button(caption="Activate!", msg="NEXT", position=(590,8)),
    EDITOR_LOGIC = EditorLogic(),
    CED = ComponentEditor(classes),
    linkages = {
       ("CONSOLEINPUT", "outbox") : ("SANDBOX", "inbox"),
       ("LINK", "outbox") : ("EDITOR_LOGIC", "linknode"),
       ("UNLINK", "outbox") : ("EDITOR_LOGIC", "unlinknode"),
       ("CHANGE", "outbox"): ("EDITOR_LOGIC", "changenode"),
       ("EDITOR_LOGIC", "componentedit") : ("CED", "inbox"),
       ("DEL", "outbox") : ("EDITOR_LOGIC", "delnode"),
       ("INTROSPECTOR", "outbox") :  ("TVC", "inbox"),
       ("EDITOR_LOGIC", "outbox") : ("CED", "inbox"),
       ("CED", "topocontrol") : ("TVC", "inbox"),
       ("TVC", "outbox") : ("EDITOR_LOGIC", "inbox"),
       ("CED", "outbox") : ("SANDBOX", "inbox"),
       ("EDITOR_LOGIC", "commands") : ("SANDBOX", "inbox"),
       ("GO", "outbox") : ("EDITOR_LOGIC", "go"),
       ("NEW", "outbox"): ("EDITOR_LOGIC", "newnode"),      
    }
).run()

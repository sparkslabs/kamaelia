---
pagename: Examples/TopologyAndSlidesPresentationTool
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 8: How to combine the two applications into 1 tool. [Components
used:
]{style="font-weight:600"}[Graphline](/Components/pydoc/Kamaelia.Util.Graphline.Graphline.html),
[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.Button.html),
[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.Chooser.html),
[Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.Image.html),
[lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.lines_to_tokenlists.html),
[chunks\_to\_lines](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.chunks_to_lines.html),
[TopologyViewerComponent](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent.TopologyViewerComponent.html)


```{.python}
#!/usr/bin/python

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent
from Kamaelia.Util.Chooser import Chooser
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.PipelineComponent import pipeline
import os

graph = ["\n","""DEL ALL
ADD NODE This This auto -
ADD NODE is is auto -
ADD NODE a a auto -
ADD NODE pipeline pipeline auto -
ADD LINK This is
ADD LINK is a
ADD LINK a pipeline
""","""DEL NODE pipeline
ADD NODE graphline graphline auto -
ADD NODE because because auto -
ADD NODE it it auto -
ADD NODE isn't isn't auto -
ADD NODE pipelike pipelike auto -
ADD LINK a graphline
ADD LINK This because
ADD LINK it isn't
ADD LINK it pipelike
ADD LINK it is
""",
"""DEL ALL
""", """ADD NODE FIND FIND auto -
ADD NODE EGREP EGREP auto -
ADD NODE READ* READ* auto -
ADD NODE CP CP auto -
ADD LINK FIND EGREP
ADD LINK EGREP READ*
ADD LINK READ* CP
""",
"""ADD NODE ENV ENV auto -
ADD LINK ENV FIND
ADD LINK ENV EGREP
ADD LINK ENV READ*
ADD LINK ENV CP
""","""DEL ALL
""", """ADD NODE ComponentOne ComponentOne auto -
ADD NODE ComponentTwo ComponentTwo auto -
ADD NODE ComponentThree ComponentThree auto -
ADD NODE ComponentFour ComponentFour auto -
ADD NODE ComponentFive ComponentFive auto -
""","""ADD LINK ComponentOne ComponentTwo
ADD LINK ComponentTwo ComponentFive
ADD LINK ComponentThree ComponentFour
ADD LINK ComponentThree ComponentFive
ADD LINK ComponentTwo ComponentFour
""",
"""ADD NODE CAT CAT auto -
ADD LINK CAT ComponentOne
ADD LINK CAT ComponentTwo
ADD LINK CAT ComponentThree
ADD LINK CAT ComponentFour
ADD LINK CAT ComponentFive
""","""DEL ALL
""","""ADD NODE TCPClient TCPClient auto -
ADD NODE VorbisDecode VorbisDecode auto -
ADD NODE AOPlayer AOPlayer auto -
ADD LINK TCPClient VorbisDecode
ADD LINK VorbisDecode AOPlayer
""", """ADD NODE ReadFileAdaptor ReadFileAdaptor auto -
ADD NODE SimpleServer SimpleServer auto -
ADD LINK ReadFileAdaptor SimpleServer
""","""DEL NODE SimpleServer
DEL NODE ReadFileAdaptor
ADD NODE Multicast_Transceiver Multicast_Transceiver auto -
ADD NODE detuple detuple auto -
ADD LINK Multicast_Transceiver detuple
""","""DEL NODE TCPClient
ADD LINK detuple VorbisDecode
""","""DEL ALL
""",
"""ADD NODE reciever reciever auto -
ADD NODE demodulation demodulation auto -
ADD NODE error_correction error_correction auto -
ADD NODE demultiplexing demultiplexing auto -
ADD NODE decode decode auto -
ADD NODE display display auto -
ADD LINK reciever demodulation
ADD LINK demodulation error_correction
ADD LINK error_correction demultiplexing
ADD LINK demultiplexing decode
ADD LINK decode display
""","""DEL ALL
""",
"""ADD NODE ProtocolHandler ProtocolHandler auto -
ADD NODE SimpleServer SimpleServer auto -
ADD NODE FileChooser FileChooser auto -
ADD NODE ImageGrabber ImageGrabber auto -
ADD NODE MyFileReader MyFileReader auto -
ADD LINK ProtocolHandler SimpleServer
ADD LINK FileChooser ImageGrabber
ADD LINK ImageGrabber MyFileReader
ADD LINK ImageGrabber ProtocolHandler
ADD LINK MyFileReader ProtocolHandler
""","""ADD NODE ClientProtocolHandler ClientProtocolHandler auto -
ADD NODE PacketCombiner PacketCombiner auto -
ADD NODE FileWriter FileWriter auto -
ADD NODE PCDisplay PCDisplay auto -
ADD LINK ClientProtocolHandler PacketCombiner
ADD LINK PacketCombiner FileWriter
ADD LINK FileWriter PCDisplay
""","""DEL NODE PCDisplay
ADD NODE NokiaDisplay NokiaDisplay auto -
ADD LINK FileWriter NokiaDisplay
""","""DEL ALL
"""
]

path = "Slides"
extn = ".gif"
allfiles = os.listdir(path)
files = list()
for fname in allfiles:
    if fname[-len(extn):]==extn:
        files.append(os.path.join(path,fname))
files.sort()

# Slideshow component
Graphline(
     CHOOSER = Chooser(items = files),
     IMAGE = Image(size=(800,600), position=(0,0)),
     NEXT = Button(caption="Next", msg="NEXT", position=(64,0), transparent=True),
     PREVIOUS = Button(caption="Previous", msg="PREV",position=(0,0), transparent=True),
     FIRST = Button(caption="First", msg="FIRST",position=(256,0), transparent=True),
     LAST = Button(caption="Last", msg="LAST",position=(320,0), transparent=True),
     linkages = {
        ("NEXT","outbox") : ("CHOOSER","inbox"),
        ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
        ("FIRST","outbox") : ("CHOOSER","inbox"),
        ("LAST","outbox") : ("CHOOSER","inbox"),
        ("CHOOSER","outbox") : ("IMAGE","inbox"),
     }
).activate()

# Topology slideshow component
pipeline(
     Button(caption="dink", msg="NEXT", position=(136,0), transparent=True),
     Chooser(items = graph),
     chunks_to_lines(),
     lines_to_tokenlists(),
     TopologyViewerComponent(transparency = (255,255,255), showGrid = False, position=(0,0)),
).run()
```

**Source:** Examples/example8/topology_slideshow.py


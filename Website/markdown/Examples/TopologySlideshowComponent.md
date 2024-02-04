---
pagename: Examples/TopologySlideshowComponent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 8: Simple topology slideshow tool. [Components used:
]{style="font-weight:600"}[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.Button.html),
[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.Chooser.html),
[lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.lines_to_tokenlists.html),
[TopologyViewerComponent](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent.TopologyViewerComponent.html)

```{.python}
#!/usr/bin/python

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Util.Chooser import Chooser
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent
from Kamaelia.Util.PipelineComponent import pipeline

graph = """\

ADD NODE TCPClient TCPClient auto -
ADD NODE VorbisDecode VorbisDecode auto -
ADD NODE AOPlayer AOPlayer auto -
ADD LINK TCPClient VorbisDecode
ADD LINK VorbisDecode AOPlayer
ADD NODE Multicast_Transceiver Multicast_Transceiver auto -
ADD NODE detuple detuple auto -
ADD LINK Multicast_Transceiver detuple
DEL NODE TCPClient
ADD LINK detuple VorbisDecode
DEL ALL
""".split("\n")

pipeline(
     Button(caption="Next", msg="NEXT", position=(72,8)),
     Chooser(items = graph),
     lines_to_tokenlists(),
     TopologyViewerComponent(transparency = (255,255,255), showGrid = False),
).run()
```

**Source:** Examples/example8/topology.py

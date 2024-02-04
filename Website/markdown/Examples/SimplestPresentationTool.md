---
pagename: Examples/SimplestPresentationTool
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 8: Simple pygame based presentation tool. [Components used:
]{style="font-weight:600"}[Graphline](/Components/pydoc/Kamaelia.Util.Graphline.Graphline.html),
[Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.Button.html),
[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.Chooser.html),
[Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.Image.html)

```{.python}
#!/usr/bin/python

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Util.Chooser import Chooser
from Kamaelia.Util.Graphline import Graphline
import os

path = "Slides"
extn = ".gif"
allfiles = os.listdir(path)
files = list()
for fname in allfiles:
    if fname[-len(extn):]==extn:
        files.append(os.path.join(path,fname))

files.sort()

Graphline(
     CHOOSER = Chooser(items = files),
     IMAGE = Image(size=(800,600), position=(8,48)),
     NEXT = Button(caption="Next", msg="NEXT", position=(72,8)),
     PREVIOUS = Button(caption="Previous", msg="PREV",position=(8,8)),
     FIRST = Button(caption="First", msg="FIRST",position=(256,8)),
     LAST = Button(caption="Last", msg="LAST",position=(320,8)),
     linkages = {
        ("NEXT","outbox") : ("CHOOSER","inbox"),
        ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
        ("FIRST","outbox") : ("CHOOSER","inbox"),
        ("LAST","outbox") : ("CHOOSER","inbox"),
        ("CHOOSER","outbox") : ("IMAGE","inbox"),
     }
).run()
```

**Source:** Examples/example8/slideshow.py

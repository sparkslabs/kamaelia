---
pagename: Examples/SimpleTextTickerDemonstration
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Examples 11 : Simple example showing how to use the ticker component.
The ticker component was first developed for displaying subtitles.
[Components used:]{style="font-weight:600"}
[Ticker](/Components/pydoc/Kamaelia.UI.Pygame.Ticker.Ticker.html),
[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.ReadFileAdaptor.html)

```{.python}
#!/usr/bin/python

from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor

pipeline( ReadFileAdaptor("Ulysses"),
          Ticker(background_colour=(128,48,128),
                 render_left = 1,
                 render_top = 1,
                 render_right = 600,
                 render_bottom = 200,
                 position = (100, 300),
          )
).run()
```

**Source:** Examples/example11/Ticker.py

---
pagename: Examples/SimpleClientForSavingContentsOfTCPStream
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Examples 12 : Simple TCP based client for the streamer above.
[Components used:
]{style="font-weight:600"}[pipeline](/Components/pydoc/Kamaelia.Util.PipelineComponent.pipeline.html),
[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html),
[SimpleFileWriter](/Components/pydoc/Kamaelia.File.Writing.SimpleFileWriter.html)

```{.python}
#!/usr/bin/python

from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.File.Writing import SimpleFileWriter

outputfile = "/tmp/received.raw"
clientServerTestPort=1500

pipeline(TCPClient("127.0.0.1",clientServerTestPort),
         SimpleFileWriter(outputfile)
        ).run()
```

**Source:** Examples/example12/ClientStreamToFile.py

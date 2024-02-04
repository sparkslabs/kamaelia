---
pagename: Examples/NetworkControllableGraphViewer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 6: How to build a network controllable graph viewer. [Components used: ]{style="font-weight:600"}[TopologyViewerServer]{style="font-style:italic;color:#ff0004"}

```{.python}
#!/usr/bin/python

from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer import TopologyViewerServer

def parseArgs(argv, extraShortArgs="", extraLongArgs=[]):
    import getopt

    shortargs = "fh" + extraShortArgs
    longargs  = list("help","fullscreen","resolution=","port=") + extraLongArgs

    optlist, remargs = getopt.getopt(argv, shortargs, longargs)

    dictArgs = {}
    for o,a in optlist:
        if o in ("-h","--help"):
            dictArgs['help'] = "Arguments:\n" + \
                               "   -h, --help\n" + \
                               "      This help message\n\n" + \
                               "   -f, --fullscreen\n" + \
                               "      Full screen mode\n\n" + \
                               "   --resolution=WxH\n" + \
                               "      Set window size to W by H pixels\n\n" + \
                               "   --port=N\n" + \
                               "      Listen on port N (default is 1500)\n\n"

        elif o in ("-f","--fullscreen"):
            dictArgs['fullscreen'] = True

        elif o in ("--resolution"):
            match = re.match(r"^(\d+)[x,-](\d+)$", a)
            x=int(match.group(1))
            y=int(match.group(2))
            dictArgs['screensize'] = (x,y)

        elif o in ("--port"):
            dictArgs['serverPort'] = int(a)

    return dictArgs, optlist, remargs

if __name__=="__main__":
    import sys
    dictArgs, remargs, junk = parseArgs(sys.argv[1:])

    if "help" in dictArgs:
        print dictArgs["help"]
    else:
        TopologyViewerServer(**dictArgs).run()
```

**Source:** Examples/example6/TopologyVisualiser.py

---
pagename: MulticoreExample
last-modified-date: 2008-10-19
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
A Simple Multicore Example
==========================

To transform a single core application like this:\
\

        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.Console import ConsoleEchoer
        from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

        Pipeline(
                 Textbox(size = (800, 300), position = (0,0)),
                 TextDisplayer(size = (800, 300), position = (0,340))
        ).run()

\
Into a multicore application, you do this:\
\

        from Axon.experimental.Process import ProcessPipeline
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.Console import ConsoleEchoer
        from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

        ProcessPipeline(
                 Textbox(size = (800, 300), position = (0,0)),
                 TextDisplayer(size = (800, 300), position = (0,340))
        ).run()

And that\'s pretty much it. A very visual difference between these two
examples is that the first of these will use just one Pygame window, and
the latter will use two.\
\

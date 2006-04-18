#!/usr/bin/python

import Axon
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent
from Kamaelia.UI.Pygame.Button import Button

class EditorLogic(Axon.Component.component):
    Inboxes = {
        "inbox" : "Not used yet",
        "control" : "Not listened to yet - BUG",
        "itemselect" : "Recieves messages saying which item is currently selected",
        "editnode" : "Inbox where we recieve messages telling us to switch to edit mode",
        "newnode" : "Inbox where we recieve messages telling us to add a node",
        "delnode" : "Inbox where we recieve messages telling us to delete a node",
        "linknode" : "Inbox where we recieve messages telling us to form links",
    }
    Outboxes = {
        "outbox" : "Passthrough of events from the TVC",
        "signal" : "We don't do anything here yet",
        "nodeevents" : "Where messages to control a TVC go",
    }
    def main(self):
        import time
        node = None
        linkstart = None
        linkmode = False
        n = 1
        while 1:
            yield 1
            #
            # This really looks like a bunch of composite components operating on shared state.
            # Leads to an interesting question - how can we use this to our advantage - we
            # "clearly" can, but the question is "how" ?
            # One thing that's very clear here is this - even if these are all operating on shared
            # state, there's one thing that *must* be true - these components must NOT operate
            # concurrently.
            #
            # (Hmm... Sequential code on shared state defaulting to preclude concurrency? Makes
            # sense thinking about it)
            #
            # Hmmm. Further thought - this is akin to the idea of multiple mains run sequentially
            # inside a component. What if those "mains" are sequential sub-component mixins?
            #
            # This aspect is //similar// to the exogenous connectors idea.
            #
            if self.dataReady("itemselect"):
                event,type,new_node = self.recv("itemselect")
                if event is "SELECT":
                    if new_node is not None:
                        node = new_node
                        if linkmode and linkstart is not None:
                            self.send(("ADD", "LINK", linkstart, node), "nodeevents")
                            linkmode = False
                            linkstart = None

                self.send((event,type,new_node), "outbox")

            if self.dataReady("editnode"):
                self.recv("editnode")
                if node is not None:
                    self.send( ("UPDATE_NAME", "NODE", node, time.asctime()), "nodeevents")

            if self.dataReady("newnode"):
                self.recv("newnode")
                self.send( ("ADD", "NODE", n, "Unconfigured Component "+str(n), "auto", "-"), "nodeevents")
                node = n
                n = n + 1

            if self.dataReady("delnode"):
                self.recv("delnode")
                if node is not None:
                    self.send(("DEL", "NODE", node), "nodeevents")

            if self.dataReady("linknode"):
                self.recv("linknode")
                if node is not None:
                    linkstart = node
                    linkmode = True

TVC = TopologyViewerComponent(position=(0,0))
Graphline(
    NEW = Button(caption="New Component", msg="NEXT", position=(72,8)),
    EDIT = Button(caption="Edit Component", msg="NEXT", position=(182,8)),
    DEL = Button(caption="Delete Component", msg="NEXT", position=(292,8)),
    LINK = Button(caption="Make Link", msg="NEXT", position=(402,8)),
    CONSOLEINPUT = pipeline(
                     ConsoleReader(">>> "),
                     chunks_to_lines(),
                     lines_to_tokenlists(),
                   ),
    EDITOR_LOGIC = EditorLogic(),
    DEBUG = ConsoleEchoer(),
    TVC = TVC, 
    linkages = {
        ("CONSOLEINPUT", "outbox"): ("TVC", "inbox"),
        ("NEW", "outbox"): ("EDITOR_LOGIC", "newnode"),
        ("EDIT", "outbox"): ("EDITOR_LOGIC", "editnode"),
        ("DEL", "outbox") : ("EDITOR_LOGIC", "delnode"),
        ("LINK", "outbox") : ("EDITOR_LOGIC", "linknode"),
        ("TVC", "outbox") : ("EDITOR_LOGIC", "itemselect"),
        ("EDITOR_LOGIC", "outbox") : ("DEBUG", "inbox"),
        ("EDITOR_LOGIC", "nodeevents") : ("TVC", "inbox"),
    }
).run()




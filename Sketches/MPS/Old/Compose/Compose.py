#!/usr/bin/env python

# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
# First proper iteration of this code:
#    * Sat Sep 16 11:24:50 BST 2006, passing through Coventry
#   
# Was able to create a simple video server completely graphically.
#
# Issues:
#    * Code needs tidying up
#    * Want to be able to re-edit components that have already been created
#    * Want to be able to delete already created components
#    * Want to be able to break already created linkages
#
# Good start though !
#
# Sunday 17:
#    * Can delete already created components
#    * Can break already created linkages
#
#


# simple kamaelia pipeline builder GUI
# run this program

from Kamaelia.UI.Pygame.Button import Button
import Kamaelia.Support.Data.Repository
import Axon
import pprint

C = Kamaelia.Support.Data.Repository.GetAllKamaeliaComponents()
COMPONENTS = {}
for key in C.keys():
    COMPONENTS[".".join(key)] = C[key]

import inspect
    
def getAllClasses( modules ):
    _modules = list(modules.keys())
    _modules.sort()
    for modname in _modules:
        try:
            for entry in getModuleConstructorArgs( modname, modules[modname] ):
                yield entry
        except ImportError:
            print "WARNING: Import Error: ", modname
            continue

def getModuleConstructorArgs( modulename, classnames):
    clist = []

    module = __import__(modulename, [], [], classnames)
    for classname in classnames:
        theclass = eval("module."+classname)
        entry = { "module"   : modulename,
                  "class"    : classname,
                  "classdoc" : theclass.__doc__,
                  "initdoc"  : theclass.__init__.__doc__,
                  "args"     : getConstructorArgs(theclass),
                  "theclass" : theclass,
                }

        clist.append(entry)

    return clist

    

def getConstructorArgs(component):
    initfunc = eval("component.__init__")
    try:
        (args, vargs, vargkw, defaults) = inspect.getargspec(initfunc)
    except TypeError, e:
        print "FAILURE", str(component), repr(component), component
        raise e

    arglist = [ [arg] for arg in args ]
    if defaults is not None:
        for i in range(0,len(defaults)):
            arglist[-1-i].append( repr(defaults[-1-i]) )

    del arglist[0]   # remove 'self'
    
    return {"std":arglist, "*":vargs, "**":vargkw}
    
class Magic(Axon.Component.component):
    "This is where the magic happens"
    """
        OK, basic actions needed:
        * ADD COMPONENT (DONE)
            * *This also needs to store what the arguments were* (DONE)
                * Beyond the immediate scope of the visualiser component (DONE)
                * Implies a filter of somekind (undecorate/decorate) (DONE)
            * ADD COMPONENT (DONE)
            * FOR EACH INBOX -- NEW (DONE)
                * ADD AND LINK (DONE)
            * FOR EACH OUTBOX -- NEW (DONE)
                * ADD AND LINK (DONE)
        * DELETE COMPONENT
            * DELETE OUTBOXES -- NEW
            * DELETE INBOXES -- NEW
            * DELETE COMPONENT
        * LINK -- NEW ( NO IMPLICIT LINK ANYMORE)  (DONE)
            * THIS BOX (DONE)
            * TO THIS BOX (DONE)
    """
    Inboxes = {
        "from_panel" : "User events from the panel",
        "from_topology" : "User events from the topology visualiser",
        "makelink" : "Simple event to create links",
        "inbox" : "unused, default",
        "control" : "unused, default",
    }
    Outboxes={
        "to_topology" : "Messages to control the topology",
        "to_serialiser" : "Messages about the system topology are sent here for turning into code",
        "signal" : "default, unused",
        "outbox" : "default, unused",
    }    

    def __init__(self):
        super(Magic,self).__init__()
        self.topologyDB = {}
        self.LINKMODE = False
        self.linksource = None
        self.linksink = None
        self.topology = []
    def main(self):
        print "Let the magic begin!"
        while 1:
            if self.dataReady("from_panel"):
                event = self.recv("from_panel")
                print "MESSAGE FROM PANEL"
                pprint.pprint(event)
                if event[0] == "ADD":
                    nodeinfo = self.addNodeToTopology(event)
                    self.addNodeLocalDB(event, nodeinfo)
                if event[0] == "DEL":
                    self.handleDeleteNode(event)

            if self.dataReady("from_topology"):
                event =  self.recv("from_topology")
                if event[0] == "SELECT":
                    self.currentSelectedNode = event[2]

                    print "HMM, the next should display the most recently selected node"
                    print "AHA! It does"
                    print "We need to tell the panel to update itself with these details then"
                    
                    self.debug_PrintCurrentNodeDetails()
            if self.dataReady("makelink"):
                self.recv("makelink")
                self.LINKMODE = True
                self.linksource = None
                self.linksink = None
            yield 1

    def handleDeleteNode(self, event):
        """
        Messages look like this:
           * ("DEL", "2.control")
           * ("DEL", "2")
        """
        print "DELETE NODE, identifying type", event
        nodeid = event[1]
        nodetype = self.topologyDB[nodeid][0]
        if nodetype == "COMPONENT":
            ( nodetype, label, inboxes, outboxes, event ) = self.topologyDB[nodeid]
            print "ASKED TO DELETE component"
            print "We need to do this:"
            print "   * delete the component node"
            self.send( [ "DEL", "NODE", nodeid ], "to_topology" )
            print "   * delete its inboxes"
            print inboxes
            for inbox in inboxes:
                boxid = inbox[0]
                self.send( [ "DEL", "NODE", boxid ], "to_topology" )
            
            print "   * delete its outboxes"
            print outboxes
            for outbox in outboxes:
                boxid = outbox[0]
                self.send( [ "DEL", "NODE", boxid ], "to_topology" )
            
            """
            We need to do this:
            * delete the component node
            * delete its inboxes
            [['1.control', 'control'], ['1.inbox', 'inbox']]
            * delete its outboxes
            [['1.outbox', 'outbox'], ['1.signal', 'signal']]
            * delete linkages to/from said linkages
            NEED TO REMOVE LINKAGE ['1.outbox', '3.inbox']
            
            This needs to be removed from:
                  self.topology
                  self.topologyDB
                  also needs to be removed from the axon visualiser
                  (del node requests)
            """
            # Remove links from self.topology
            self.topology = [ link for link in self.topology if not self.matchesNode(nodeid, link) ]
            
            # remove inboxes from topologyDB
            inboxids = [ x[0] for x in inboxes ]
            for boxid in inboxids:
                del self.topologyDB[boxid]
            
            # remove outboxes from topologyDB
            outboxids = [ x[0] for x in outboxes ]
            for boxid in outboxids:
                del self.topologyDB[boxid]
            
            # Deleted the component itself from the topologyDB
            del self.topologyDB[nodeid]

        else:
            boxid = nodeid
            ( boxtype, label, nodeid ) = self.topologyDB[boxid]
            print "ASKED TO DELETE box"
            print "   * Can't actually do that!"
            print "   * Deleting linkages to/from that box instead!"
            if boxtype == "INBOX":
                print "DELETING AN INBOX!", nodeid, boxid
                # Remove links from visualiser
                for link in self.topology:
                    if self.matchesNode(boxid, link):
                        source, sink = link
                        print [ "DEL", "LINK", source, sink ], "to_topology", boxid, link, nodeid
                        self.send( [ "DEL", "LINK", source, sink ], "to_topology" )
                # Remove links from self.topology
                self.topology = [ link for link in self.topology if not self.matchesNode(boxid, link) ]
            if boxtype == "OUTBOX":
                print "DELETING AN OUTBOX!"

        self.updateSerialiser()
            
    def updateSerialiser(self):
        self.send( { "nodes": self.topologyDB, "links": self.topology },
                   "to_serialiser")

    def makeLink(self):
        self.send( [ "ADD", "LINK",
                            self.linksource,
                            self.linksink,
                    ], "to_topology" )
        self.topology.append([self.linksource,self.linksink])
        self.updateSerialiser()
    
    def matchesNode(self, nodeid, link):
        print "nodeid, link", nodeid, link
        linksource,linksink = link
        if "." not in nodeid:
            print "HERE 1"
            source, sourcebox = linksource.split(".")
            sink, sinkbox = linksink.split(".")
            print "(source == nodeid)", (source == nodeid)
            print "(sink == nodeid)", (sink == nodeid)
            return (source == nodeid) or (sink == nodeid)
        else:
            print "HERE 2"
            print "(linksource == nodeid)", (linksource == nodeid)
            print "(linksink == nodeid)", (linksink == nodeid)
            return (linksource == nodeid) or (linksink == nodeid)

    def debug_PrintCurrentNodeDetails(self):
        print "CURRENT NODE", self.currentSelectedNode
        if self.currentSelectedNode is None:
            self.LINKMODE = False
            return
        if self.LINKMODE:
            if self.linksource == None:
                self.linksource = self.currentSelectedNode
            else:
                self.linksink = self.currentSelectedNode
                self.makeLink()
                self.LINKMODE = False
        print self.topologyDB[self.currentSelectedNode]
        
    def addNodeLocalDB(self, event, nodeinfo):
        ( nodeid, label, inboxes, outboxes ) = nodeinfo
        self.topologyDB[nodeid] = ( "COMPONENT", label, inboxes, outboxes, event )
        for inbox in inboxes:
            ( boxid, label ) = inbox
            self.topologyDB[boxid] = ( "INBOX", label, nodeid )
        for outbox in outboxes:
            ( boxid, label ) = outbox
            self.topologyDB[boxid] = ( "OUTBOX", label, nodeid )
        self.updateSerialiser()

    def addNodeToTopology(self,event):
        print "ADD NODE"
        nodeid = "ID"
        label = "LABEL"
        (label, nodeid) = event[1]
        self.send( ["ADD", "NODE", 
                           nodeid, 
                           label, 
                           "randompos", 
                           "component"
                   ], "to_topology" )

        inboxes = []
        for inbox in event[3]["configuration"]["theclass"].Inboxes:
            boxid = str(nodeid) + "." + inbox
            self.send( [ "ADD", "NODE",
                                boxid,
                                inbox,
                                "randompos",
                                "inbox"
                       ], "to_topology" )
            self.send( [ "ADD", "LINK",
                                nodeid,
                                boxid,
                       ], "to_topology" )
            inboxes.append(  [ boxid, inbox]  )

        outboxes = []
        for outbox in event[3]["configuration"]["theclass"].Outboxes:
            boxid = str(nodeid) + "." + outbox
            self.send( [ "ADD", "NODE",
                                boxid,
                                outbox,
                                "randompos",
                                "outbox"
                       ], "to_topology" )
            self.send( [ "ADD", "LINK",
                                nodeid,
                                boxid,
                       ], "to_topology" )
            outboxes.append(  [ boxid, outbox]  )

        return ( nodeid, label, inboxes, outboxes )

if __name__ == "__main__":
    import sys

    from Axon.Scheduler import scheduler

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer

    from Kamaelia.Util.Splitter import PlugSplitter as Splitter
    from Kamaelia.Util.Splitter import Plug

#    from Filters import FilterSelectMsgs, FilterTopologyMsgs

    from Compose.PipeBuild import PipeBuild
    from Compose.PipelineWriter import PipelineWriter
    from Compose.CodeGen import CodeGen
    from Compose.BuildViewer import BuildViewer
    from Compose.GUI.BuilderControlsGUI import BuilderControlsGUI
    from Compose.GUI.TextOutputGUI import TextOutputGUI
    from Kamaelia.Util.Backplane import *

    items = list(getAllClasses( COMPONENTS ))

    # Create the TK GUI for selecting which components to add remove
    # Pass that data through an intermediary tracking the topology caled PipeBuild
    
    # Take the result from this and make it the data source for a Pluggable Splitter
    #   "pipegen"


    Backplane("Display").activate()
    Pipeline(SubscribeTo("Display"),
             TextOutputGUI("Code")
    ).activate()
    
    Backplane("Panel_Feedback").activate()
    Backplane("Panel_Events").activate()
    Pipeline(SubscribeTo("Panel_Feedback"),
             BuilderControlsGUI(items),
             PublishTo("Panel_Events")
    ).activate()
    
    Pipeline( SubscribeTo("VisualiserEvents"),
              PublishTo("Panel_Feedback"),
    ).activate()

    Backplane("VisualiserControl").activate()
    Backplane("VisualiserEvents").activate()
    Pipeline(
        SubscribeTo("VisualiserControl"),
        BuildViewer(),
        PublishTo("VisualiserEvents"),
    ).activate()
    
    #
    # Debugging console
    #
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.Visualisation.Axon.AxonVisualiserServer import text_to_token_lists
    Pipeline(
        ConsoleReader(),
        text_to_token_lists(),
        PublishTo("VisualiserControl")
    ).activate()

    Graphline(
        SEMANTIC_EVENTS=SubscribeTo("Panel_Events"),
        SELECTION_EVENTS=SubscribeTo("VisualiserEvents"),
        TOPOLOGY_VISUALISER=PublishTo("VisualiserControl"),
        CODE_DISPLAY = PublishTo("Display"),
        MAKELINK = Button(caption="make link",
                          size=(63,32),
                          position=(800, 0),
                          msg="LINK"),
        CENTRAL_CONTROL=Magic(),
        CODE_GENERATOR = CodeGen(),
        linkages = {
            ("SEMANTIC_EVENTS","outbox"):("CENTRAL_CONTROL","from_panel"),
            ("SELECTION_EVENTS","outbox"):("CENTRAL_CONTROL","from_topology"),
            ("MAKELINK", "outbox") : ("CENTRAL_CONTROL", "makelink"),
            ("CENTRAL_CONTROL","to_topology"):("TOPOLOGY_VISUALISER","inbox"),
            ("CENTRAL_CONTROL","to_serialiser"):("CODE_GENERATOR","inbox"),
            ("CODE_GENERATOR","outbox"): ("CODE_DISPLAY","inbox"),
        }
    ).run()


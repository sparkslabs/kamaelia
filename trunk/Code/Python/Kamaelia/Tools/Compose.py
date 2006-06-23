#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

# simple kamaelia pipeline builder GUI
# run this program

import Kamaelia.Data.Repository

C = Kamaelia.Data.Repository.GetAllKamaeliaComponents()
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
                  "args"     : getConstructorArgs(theclass)
                }

        clist.append(entry)
        
    return clist

    

def getConstructorArgs(component):
    initfunc = eval("component.__init__")
    (args, vargs, vargkw, defaults) = inspect.getargspec(initfunc)

    arglist = [ [arg] for arg in args ]
    if defaults is not None:
        for i in range(0,len(defaults)):
            arglist[-1-i].append( repr(defaults[-1-i]) )

    del arglist[0]   # remove 'self'
    
    return {"std":arglist, "*":vargs, "**":vargkw}
    


if __name__ == "__main__":
    import sys
    sys.path.append("PipeBuilder")

    from Axon.Scheduler import scheduler

    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent

    from Kamaelia.Util.Splitter import PlugSplitter as Splitter
    from Kamaelia.Util.Splitter import Plug

#    from Filters import FilterSelectMsgs, FilterTopologyMsgs

    from PipeBuild import PipeBuild
    from PipelineWriter import PipelineWriter
    from BuildViewer import BuildViewer
    from GUI import BuilderControlsGUI, TextOutputGUI


    items = list(getAllClasses( COMPONENTS ))

    
    pipegen = Splitter(pipeline( BuilderControlsGUI(items),
                                 PipeBuild()
                               )
                      )
                      
    viewer = Splitter(BuildViewer())
    
    Plug(viewer, pipegen).activate()   # feedback loop for 'selected' msgs
    
    Plug(pipegen, viewer).activate()
    Plug(pipegen, pipeline(PipelineWriter(),
                           TextOutputGUI("Pipeline code")
                          )
        ).activate()
    
    try:
        scheduler.run.runThreads()
    except:
        pass



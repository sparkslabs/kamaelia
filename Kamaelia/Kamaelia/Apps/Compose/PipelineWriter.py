#!/usr/bin/env python

# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class PipelineWriter(component):
    """Writes a Kamaelia pipeline based on instructions received.

    Accepts:
        ("PIPELINE", [pipelineelements])
            pipelineelements = dictionary containing:
                name : name of class/factory function
                module : module containing it
                instantiation : string of the arguments to be passed
                    (the bit that goes inside the brackets)

    Emits:
        Strings of python source code
        followed by 'None' to terminate
    """
    
    def main(self):
        done = False
        while not done:

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if data[0].upper() == "PIPELINE":
                    for output in PipelineWriter.generatePipeline(data[1]):
                        self.send(output,"outbox")
                    self.send(None, "outbox")
                            

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    done = True
                self.send(shutdownMicroprocess(self), "signal")

            if not done:
                self.pause()

            yield 1


    def generatePipeline(pipeline):
        yield "#!/usr/bin/env python\n\n"

        if len(pipeline):
            imports = { "Kamaelia.Chassis.Pipeline":["Pipeline"] }

            # go through all module/classname stuff to build the imports list
            for component in pipeline:
                classname = component['name']
                modulename = component['module']
                imports.setdefault( modulename, [] )
                if classname not in imports[modulename]:
                    imports[modulename].append(classname)
                
            # now output the imports
            for module in imports:
                yield "from "+module+" import "
                prefix=""
                for classname in imports[module]:
                    yield prefix+classname
                    prefix=", "
                yield "\n"
                        
            yield "\n"
            indent = "Pipeline( "
            for component in pipeline:
                yield indent + component['name']+"( "+component['instantiation'] + " ),\n"
                indent = " " * len(indent)
            yield "        ).run()\n"

        else:
            yield "# no pipeline!\n"

    generatePipeline = staticmethod(generatePipeline)
            

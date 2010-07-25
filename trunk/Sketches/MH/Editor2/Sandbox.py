#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import Axon
import Axon.Ipc as Ipc

import re


class Sandbox(Axon.Component.component):
    """\
    Component Sandbox
    
    Rather likea kind of graphline where components can be added and removed at runtime
    by sending commands to the inbox.
    
    ("ADD", "importpath:factorycmd", ...)
    ("DEL", id)
    ("LINK", introspector-outbox-id, introspector-inbox-id)
    ("UNLINK", introspector-outbox-id, introspector-inbox-id)
    
    Eventually need to add UNLINK and a way to replace components, eg. by specifying the id
    """
    Inboxes = { "inbox" : "Commands to drive the sandbox",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "NOT USED",
               }
               
    def __init__(self):
        super(Sandbox,self).__init__()
        self.linkages = {}
        
    def main(self):
        yield 1
        while 1:
            yield 1
            self.childrenDone()   # clean up any children we've lost!
            
            while self.dataReady("inbox"):
                cmd = self.recv("inbox")

                if cmd[0] == "ADD":
                    self.makeComponent(spec=cmd[2],uid=cmd[1])

                elif cmd[0] == "DEL":
                    self.destroyComponent(uid=cmd[1])
                
                elif cmd[0] == "UPDATE_NAME":
                    if cmd[1] == "NODE":
                        if self.destroyComponent(uid=cmd[2]):
                            self.makeComponent(spec=cmd[3],uid=cmd[2])
                
                elif cmd[0] == "LINK":
                    self.makeLink( cmd[1], cmd[2] )
                
                elif cmd[0] == "UNLINK":
                    self.unmakeLink( cmd[1], cmd[2] )
                
                elif cmd[0] == "GO":
                    yield self.go()
                    
            self.pause()
    
    def makeComponent(self, spec, uid=None):
        """\
        Takes spec of the form:
           "importname:classname(arguments)"
        and constructs it, eg
           "Kamaelia.Util.Console:consoleEchoer()"
        """
        match = re.match("^([^:]*):([^(]*)(.*)$", spec)
        (modulename, classname, arguments) = match.groups()
        module = __import__(modulename, [], [], [classname])

        try:
            thecomponent = eval("module."+classname+arguments)   ### XXX Probably a gaping security hole!!!
        except e:
            print "Couldn't instantiate component: ",str(e)
            
        if not uid is None:
            thecomponent.id = eval(uid)
        thecomponent.name = spec + "_" + str(thecomponent.id)
        self.addChildren(thecomponent)
        return thecomponent
        
    def destroyComponent(self, uid):
        for c in self.childComponents():
            if str(c.id) == uid:
                c.stop()
                self.removeChild(c)
                return True
        return False
        
        
    def makeLink(self, src, dst):
        # get right way around if back to front
        src, dst = eval(src), eval(dst)            # XXX SECURITY RISK
        print src
        if src[1] == "i" and dst[1] == "o":
            src, dst = dst, src
            
        sid, sboxtype, sbox = src
        did, dboxtype, dbox = dst
        if sboxtype == "o" and dboxtype == "i":
            passthrough = 0
        elif sboxtype == "i" and dboxtype == "i":
            passthrough = 1
        elif sboxtype == "o" and dboxtype == "o":
            passthrough = 2
        else:
            raise "Unrecognised box types!"
        
        components = self.childComponents()[:]
        components.append(self)
        source = [c for c in components if c.id == sid]
        dest   = [c for c in components if c.id == did]
        linkage = self.link( (source[0], sbox), (dest[0], dbox), passthrough=passthrough )
        self.linkages[ (src,dst) ] = linkage


    def unmakeLink(self, src, dst):
        # get right way around if back to front
        src, dst = eval(src), eval(dst)            # XXX SECURITY RISK
        print src
        if src[1] == "i" and dst[1] == "o":
            src, dst = dst, src
        
        linkage = self.linkages.get((src,dst),None)
        if linkage:
            self.unlink(thelinkage=linkage)
            del self.linkages[(src,dst)]
        
    def go(self):
        return Ipc.newComponent(*[c for c in self.childComponents()])

    def childrenDone(self):
        """\
        Unplugs any children that have terminated, and returns true if there are no
        running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())

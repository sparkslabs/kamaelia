#!/usr/bin/python

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
                    raise "Can't handle destroying links yet!"
                
                elif cmd[0] == "GO":
                    yield self.go()
                    
    
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

        thecomponent = eval("module."+classname+arguments)   ### XXX Probably a gaping security hole!!!
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
        self.link( (source[0], sbox), (dest[0], dbox), passthrough=passthrough )

        
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

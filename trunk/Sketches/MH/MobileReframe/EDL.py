#!/usr/bin/python

from Axon.Component import component
from Axon.Ipc import WaitComplete
from Axon.Ipc import producerFinished, shutdownMicroprocess

def contains(items,container):
    for item in items:
        if not container.has_key(item):
            return False
    return True



class EDLParser(component):
    """\
    Parse output from SAX parser into EDL items
    """

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                self.send(msg,"signal")
                return True
        return False
    
    def main(self):
        self.token = ["",]
        parser = self.parse()
        
        try:
            while 1:
                while self.dataReady("inbox"):
                    self.token = self.recv("inbox")
                    output = parser.next()
                    if output != None:
                        self.send(output,"outbox")
                        yield 1
                        
                if self.shutdown():
                    return
                
                self.pause()
                yield 1
            
        except StopIteration:
            self.send(producerFinished(), "signal")
            
    
    
    def parse(self):
        
        while not self.ifIs("element","EDL"):
            yield None
        
        while 1:
            yield None
            if self.ifIs("chars"):
                pass
            elif self.ifIs("element","FileID"):
                fileID = ""
                while not self.ifIs("/element","FileID"):
                    yield None
                    if self.ifIs("chars"):
                        fileID += self.token[1]
                fileID = fileID.replace("\n","").strip()
                yield None
                        
            elif self.ifIs("element","Edit"):
                edit = {"fileID":fileID}
                while not self.ifIs("/element","Edit"):
                    yield None
                    if self.ifIs("element","Start"):
                        attrs = self.token[2]
                        edit["start"] = int(attrs["frame"])
                    elif self.ifIs("element","End"):
                        attrs = self.token[2]
                        edit["end"] = int(attrs["frame"])
                    elif self.ifIs("element","Crop"):
                        attrs = self.token[2]
                        #assert( contains(("x1","y1","x2","y2"), attrs) )
                        edit["left"]   = int(attrs["x1"])
                        edit["top"]    = int(attrs["y1"])
                        edit["right"]  = int(attrs["x2"])
                        edit["bottom"] = int(attrs["y2"])
                        
                    elif self.ifIs("chars"):
                        pass
                #assert( contains["start","end","left","top","right","bottom"], edit)
                yield edit
                
            elif self.ifIs("/element","EDL"):
                return
                
    def ifIs(self,*args):
        return self.token[:len(args)] == args


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
    from SAX import XMLParser
    
    from Kamaelia.File.Reading import RateControlledFileReader
    
    Pipeline(
        RateControlledFileReader("TestEDL.xml",readmode="lines",rate=1000000),
        XMLParser(),
        EDLParser(),
        ConsoleEchoer(),
    ).run()


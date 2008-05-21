import Axon
import time
from htmltmpl import TemplateManager, TemplateProcessor

from Axon.Ipc import producerFinished

# Abstract class
class KamTemplateProcessor(Axon.Component.component):
    Inboxes = {
            'control'        : 'From component', 
            'inbox'          : 'Not used', 
            'feeds-inbox'    : 'Not used', 
            'config-inbox'   : 'Not used', 
            'channels-inbox' : 'Not used', 
        }
    def __init__(self, **argd):
        super(KamTemplateProcessor, self).__init__(**argd)
        self.feeds     = []
        self.channels  = []
        self.config    = None
        
    def fillTemplate(self, templateProcessor):
        raise NotImplementedError("fillTemplate method not implemented!")
        
    def getTemplateFileName(self):
        raise NotImplementedError("getTemplateFileName method not implemented!")

    def main(self):
        while True:
            while self.dataReady("control"):
                # TODO
                data = self.recv("control")
                for i in range(100):
                    print "%s: %s" % (type(self), data)
                self.send(data, "signal")
                return

            while self.dataReady("channels-inbox"):
                data = self.recv("channels-inbox")
                self.channels.append(data)
                yield 1

            while self.dataReady("feeds-inbox"):
                data = self.recv("feeds-inbox")
                self.feeds.append(data)
                yield 1

            while self.dataReady("config-inbox"):
                data = self.recv("config-inbox")
                self.config = data

            if self.config is not None and len(self.feeds) == 10: #TODO: 10
            
                tproc = TemplateProcessor()
                tmanager = TemplateManager()
                template = tmanager.prepare(self.getTemplateFileName())
                yield 1
                
                self.fillTemplate(tproc)
                result = tproc.process(template)
                yield 1
                
                print "File written" * 100#TODO
                self.send(result, "outbox")
                self.send(producerFinished(self), "signal")
                return

            if not self.anyReady():
                self.pause()

            yield 1


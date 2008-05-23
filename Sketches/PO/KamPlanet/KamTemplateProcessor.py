#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

import time
from htmltmpl import TemplateManager, TemplateProcessor

# Abstract class
class KamTemplateProcessor(Axon.Component.component):
    Inboxes = {
            'control'        : 'From component', 
            'inbox'          : 'Not used', 
            'feeds-inbox'    : 'Not used', 
            'config-inbox'   : 'Not used', 
            'channels-inbox' : 'Not used', 
        }
    Outboxes = {
            'outbox'         : 'From component', 
            'signal'         : 'From component', 
            'create-output'  : 'From component', 
        }
    def __init__(self, **argd):
        super(KamTemplateProcessor, self).__init__(**argd)
        self.feeds            = []
        self.channels         = []
        self.providerFinished = None
        self.mustStop         = None
        self.config           = None
        
    def fillTemplate(self, templateProcessor):
        raise NotImplementedError("fillTemplate method not implemented!")
        
    def getTemplateFileName(self):
        raise NotImplementedError("getTemplateFileName method not implemented!")
        
    def getOutputFileName(self):
        raise NotImplementedError("getOutputFileName method not implemented!")

    def checkControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,producerFinished):
                self.providerFinished = msg
            elif isinstance(msg,shutdownMicroprocess):
                self.mustStop = msg
        return self.mustStop, self.providerFinished
        
    def main(self):
        while True:                
            while self.dataReady("channels-inbox"):
                data = self.recv("channels-inbox")
                self.channels.append(data)
                
            while self.dataReady("feeds-inbox"):
                data = self.recv("feeds-inbox")
                self.feeds.append(data)
                
            while self.dataReady("config-inbox"):
                data = self.recv("config-inbox")
                self.config = data
            
            mustStop, providerFinished = self.checkControl()
            if mustStop:
                self.send(mustStop,"signal")
                return
            
            if providerFinished is not None and self.config is not None:
                tproc = TemplateProcessor()
                tmanager = TemplateManager()
                template = tmanager.prepare(self.getTemplateFileName())
                yield 1
                
                self.fillTemplate(tproc)
                result = tproc.process(template)
                yield 1
                
                self.send(self.getOutputFileName(), 'create-output')
                yield 1
                
                self.send(result, "outbox")
                yield 1
                
                self.send(producerFinished(self), "signal")
                print "File written %s" % self.getOutputFileName() # TODO
                return
                
            if not self.anyReady():
                self.pause()
                
            yield 1

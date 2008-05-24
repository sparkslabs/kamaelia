#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: PO

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

import time
from htmltmpl import TemplateManager, TemplateProcessor

# Abstract class
class KamTemplateProcessor(Axon.Component.component):
    Inboxes = {
            'control'        : 'From component', 
            'inbox'          : 'Not used', 
            'posts-inbox'    : 'Not used', 
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
        self.posts            = []
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
                
            while self.dataReady("posts-inbox"):
                data = self.recv("posts-inbox")
                self.posts.append(data)
                
            while self.dataReady("config-inbox"):
                data = self.recv("config-inbox")
                self.config = data
            
            mustStop, providerFinished = self.checkControl()
            if mustStop:
                self.send(mustStop,"signal")
                return
            
            if providerFinished is not None and self.config is not None:
                tproc = TemplateProcessor(html_escape=0)
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

#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished

class GeneralConfig(object):
    def __init__(self,  name, link):
        self.name = name
        self.link = link

class ConfigFileParser(Axon.Component.component):
    Outboxes = {
        "outbox"           : "Not used",
        "signal"           : "From component...",
        "feeds-outbox"     : "It will send one by one the parsed feeds. Instances of str by the moment",
        "config-outbox"    : "It will send an instance of GeneralConfig when parsed",
        "counter-outbox"   : "It will announce how many feeds were found through this channel"
    }
    def __init__(self, **argd):
        super(ConfigFileParser, self).__init__(**argd)
        self.feeds = []
        self.counter      = -1
        self.config       = None
        self.finished     = False

        # Temporal variables, for xml parsing
        self.temp_counter          = 0
        self.temp_config           = GeneralConfig(u'', u'')
        self.temp_feed             = None
        self.parsing_general       = False
        self.parsing_feed          = False
        self.parsing_feeds         = False
        self.parsing_general_field = None

    def parsingXml(self, data):
        # Main XML skeleton
        if data[0] == '/document':
            self.finished = True
        elif data[0] == 'element' and data[1] == 'general':
            self.parsing_general = True
        elif data[0] == '/element' and data[1] == 'general':
            self.parsing_general = False
            self.config = self.temp_config
        elif data[0] == 'element' and data[1] == 'feeds':
            self.parsing_feeds = True
        elif data[0] == '/element' and data[1] == 'feeds':
            self.parsing_feeds = False
            self.counter = self.temp_counter
        
        # Parsing general head
        if self.parsing_general:
            if data[0] == 'element' and data[1] == 'name':
                self.parsing_general_field = 'name'
            elif data[0] == 'element' and data[1] == 'link':
                self.parsing_general_field = 'link'
            elif data[0] == '/element' and data[1] in ('name', 'link'):
                prev = getattr(self.temp_config,  self.parsing_general_field)
                setattr(self.temp_config,  self.parsing_general_field,  str(prev))
                self.parsing_general_field = None
            
            if data[0] == 'chars' and self.parsing_general_field is not None:
                prev = getattr(self.temp_config,  self.parsing_general_field)
                setattr(self.temp_config,  self.parsing_general_field,  prev + data[1])
        
        # Parsing feeds
        if self.parsing_feeds:
            if data[0] == 'element' and data[1] == 'feed':
                self.parsing_feed = True
                url = data[2].get('url')
                self.temp_feed = str(url) # By the moment
            elif data[0] == '/element' and data[1] == 'feed':
                self.parsing_feed = False
                self.feeds.append(self.temp_feed)
                self.temp_counter += 1
                

    def main(self):
        while True:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                self.parsingXml(data)

            # If the counter has been parsed, send it
            if self.counter != -1:
                self.send(self.counter,  "counter-outbox")
                self.counter = -1

            # If the general config has been parsed, send it
            if self.config is not None:
                self.send(self.config,  'config-outbox')
                self.config = None
            
            # Send the parsed feeds
            while len(self.feeds) > 0:
                for feed in self.feeds:
                    self.send(feed,"feeds-outbox")
                self.feeds = []
            
            # If we're done, finish
            if self.finished:
                self.send(producerFinished(), "signal")
                yield 0
                
            if not self.anyReady():
                self.pause()
                
            yield 1


#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished

# TODO: maybe ConfigFileParser shouldn't handle GeneralConfig
# There could be a FeedConfigFileParser which would parse a file full of feeds
# And a GeneralConfigFileParser which would parse a file with general configuration 
# (and would use Backplanes)

class GeneralConfig(object):
    def __init__(self,  name, link):
        self.name = name
        self.link = link

class ConfigFileParser(Axon.Component.component):
    Outboxes = {
        "outbox"           : "Not used",
        "signal"           : "From component...",
        "feeds-outbox"     : "Feeds",
        "config-outbox"    : "General configuration",
        "counter-outbox"   : "Will announce how many feeds were found through this channel"
    }
    def __init__(self, **argd):
        super(ConfigFileParser, self).__init__(**argd)
        # TODO: First version, I should parse a configuration file or sth :-)
        # Right now all the config has been hardcoded
        self.ptr = 0
        self.feeds = [
            'http://pablo.ordunya.com/weblog/feed/',
            'http://pablo.ordunya.com/weblog/feed/',
            'http://pablo.ordunya.com/weblog/feed/',
            'http://pablo.ordunya.com/weblog/feed/',
        ]
        self.counter      = 0
        self.counter_sent = False
        self.config       = GeneralConfig("Kamaelia Planet", "http://somewhere/")
        self.config_sent  = False

    def mainBody(self):
        if len(self.feeds) <= self.counter:
            if not self.counter_sent:
                self.send(len(self.feeds), 'counter-outbox')
                self.counter_sent = True
                return 1
            if not self.config_sent:
                self.send(self.config,  'config-outbox')
                self.config_sent = True
                return 1
            self.send(producerFinished(), "signal")
            return 0

        if len(self.feeds) > self.ptr:
            feed = self.feeds[self.ptr]
            self.ptr = self.ptr + 1
            self.send(feed,"feeds-outbox")
            self.counter = self.counter + 1
            return 1
        
        if not self.anyReady():
            self.pause()

        return 1


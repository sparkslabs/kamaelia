#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

def _check_l10n(x,y):
    for param in x,y:
        if param.updated_parsed is None:
            raise Exception("feedparser could not parse date format: %s; l10n problems? \
                Take a look at feedparser._parse_date_hungarian and feedparser.\
                registerDateHandler" % param.updated
            ) # TODO: Exception is just too generic

def _cmp_entries(x,y):
    """ Given two FeedParserDicts, compare them taking into account their updated_parsed fields """
    _check_l10n(x['entry'],y['entry'])
    for pos, val in enumerate(x['entry'].updated_parsed):
        result = cmp(val, y['entry'].updated_parsed[pos])
        if result != 0:
            return result * -1
    return 0

class FeedSorter(Axon.Component.component):
    Inboxes = {
        "inbox"         : "Information coming from the socket",
        "control"       : "From component...",
        "config-inbox"  : "Configuration information"
    }
    def __init__(self, **argd):
        super(FeedSorter, self).__init__(**argd)
        self.ordered_entries  = []
        self.config           = None
        self.pleaseSleep      = False
        self.providerFinished = None
        self.mustStop         = None

    def checkControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,producerFinished):
                self.providerFinished = msg
            elif isinstance(msg,shutdownMicroprocess):
                self.mustStop = msg
        return self.mustStop, self.providerFinished
        
    def checkConfig(self):
        while self.dataReady("config-inbox"):
            data = self.recv("config-inbox")
            self.config = data
        
    def main(self):
        while True:            
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.ordered_entries.extend([
                                        {
                                            'feed'     : data.feed,
                                            'entry'    : x,
                                            'encoding' : data.encoding
                                        } for x in data.entries
                        ])
                self.ordered_entries.sort(_cmp_entries)
                
                self.checkConfig()
                if self.config is not None:
                    self.ordered_entries = self.ordered_entries[:self.config.maxPostNumber]
                
            mustStop, providerFinished = self.checkControl()
            if mustStop:
                self.send(mustStop,"signal")
                return
                
            if providerFinished is not None:
                    for entry in self.ordered_entries:
                        self.send(entry, 'outbox')
                    yield 1
                    self.send(producerFinished(self), 'signal')
                    return
                
            if not self.anyReady():
                self.pause()
                
            yield 1


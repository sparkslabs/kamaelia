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
        "counter-inbox" : "Will receive the number of feeds through this channel"
    }
    def __init__(self, **argd):
        super(FeedSorter, self).__init__(**argd)
        self.ordered_entries = []
        self.max_posts       = 10 #TODO: configure me
        self.pleaseSleep     = False

    def main(self):
        while True:
            while self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data, shutdownMicroprocess):
                    self.send(data, "signal")
                    return
                elif isinstance(data,  producerFinished):
                    for entry in self.ordered_entries:
                        self.send(entry, 'outbox')
                    yield 1
                    # TODO 
                    for _ in range(100):
                        yield 1
                    print "KILLING " * 100
                    self.send(producerFinished(self), 'signal')
                    return

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
                self.ordered_entries = self.ordered_entries[:self.max_posts]
                yield 1

            if not self.anyReady():
                self.pause()
                
            yield 1


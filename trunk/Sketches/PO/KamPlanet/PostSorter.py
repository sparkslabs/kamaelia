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

class PostSorter(Axon.Component.component):
    Inboxes = {
        "inbox"         : "Information coming from the socket",
        "control"       : "From component...",
        "config-inbox"  : "Configuration information"
    }
    def __init__(self, **argd):
        super(PostSorter, self).__init__(**argd)
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


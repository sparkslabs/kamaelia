#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
# 
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: PO

import sys

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

def _check_l10n(param):
    if not hasattr(param, 'updated_parsed') or param.updated_parsed is None:
        # updated_parsed_value = getattr(param,'updated_parsed',param)
        # print >> sys.stderr, "feedparser could not parse date format: %s; l10n problems? \
        #    Take a look at feedparser._parse_date_hungarian and feedparser.\
        #    registerDateHandler" % updated_parsed_value
        return False
    return True

def _cmp_entries(x,y):
    """ Given two FeedParserDicts, compare them taking into account their updated_parsed fields """
    # We know the dates:
    if _check_l10n(x['entry']) and _check_l10n(y['entry']):
        for pos, val in enumerate(x['entry'].updated_parsed):
            result = cmp(y['entry'].updated_parsed[pos], val)
            if result != 0:
                return result
        return 0
    
    # We do not know the dates of any of the two entries:
    if not _check_l10n(x['entry']) and not _check_l10n(x['entry']):
        return 0
    
    # We know the dates of one and only one of the entries
    if _check_l10n(x['entry']):
        return -1
    else:
        return 1


class PostSorter(Axon.Component.component):
    """
    PostSorter() -> PostSorter object
    
    Retrieves all the feeds, takes all their posts, it sorts them by date and 
    finally sends only the last "maxPostNumber" ones.
    
    It takes all these already parsed feeds from the "inbox" inbox, and the 
    configuration from the "config-inbox" inbox, and returns only the selected
    feeds through the "outbox" outbox. The maxPostNumber number is retrieved from
    the configuration object.
    """
    Inboxes = {
        "inbox"         : "Feeds in feedparser.FeedParserDict format",
        "control"       : "From component...",
        "config-inbox"  : "Configuration information in GeneralObjectParser format"
    }
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
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

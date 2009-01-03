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

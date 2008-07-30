#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: JMB

from Kamaelia.Protocol.HTTP import PopWsgiURI

from headstock.api.jid import JID

_uri_lookup_table = {
    u'amnorvend@jabber.org' : 'amnorvend'
}

_uris_active = {}

def GetURI(user):
    JIDText = user.nodeid()
    return _uri_lookup_table[JIDText]
    

def ExtractJID(request):
    #print request
    raw = request['REQUEST_URI']
    split_raw = raw.split('/')
    split_raw = [x for x in split_raw if x]  #remove empty strings
    #print split_raw
    PopWsgiURI(request)
    if split_raw:
        return _uris_active.get(split_raw[0])
    else:
        return ''

def AddUser(user):
    assert(isinstance(user, JID))
    #Add the JID without the resource as the key to the JID instance
    _uris_active[GetURI(user)] = user
    #print _uris_active    
    
def RmUser(user):
    assert(isinstance(user, JID))
    del _uris_active[GetURI(user)]

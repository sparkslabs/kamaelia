#!/usr/bin/env python
#
# JMB_PUBLISH_GATEWAY
#
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

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, Boolean, Unicode

class BaseUser(object):
    def __init__(self, jid, url_prefix, active=False):
        print "BaseUser.__init__"
        self.jid = jid
        self.url_prefix = url_prefix
        self.active = active
        
    def __repr__(self):
        print "BaseUser.__repr__"
        return '<User jid=%s, url_prefix=%s>' % (self.jid, self.url_prefix)
    
class User(BaseUser):
    pass

class ActiveUser(BaseUser):
    pass

def getUserTable(meta, tablename='users'):
    print "getUserTable"
    X = Table(tablename, meta,
                Column('id', Integer, primary_key=True),
                Column('jid', Unicode(50)),
                Column('url_prefix', Unicode(10)),
                Column('active', Boolean())
    )
    print "getUserTable", X
    return X

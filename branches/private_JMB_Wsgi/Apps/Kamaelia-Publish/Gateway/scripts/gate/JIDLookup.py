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

from Axon.STM import Store
from Kamaelia.Protocol.HTTP import PopWsgiURI
from Kamaelia.Apps.Wsgi.db import getUserTable, User
from headstock.api.jid import JID

import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.exceptions import InvalidRequestError

from atexit import register

UserSession = sessionmaker(autoflush=True, transactional=True)

_uris_active = {}
_connected = False

def GetURI(jid_, session):
    """A convenience function for GetUser in case we just want the uri."""
    return GetUser(jid_, session).url_prefix
    
def ExtractJID(request):
    #print request
    raw = request['REQUEST_URI']
    split_raw = raw.split('/')
    split_raw = [x for x in split_raw if x]  #remove empty strings
    #print split_raw
    PopWsgiURI(request)
    if split_raw:
        session = UserSession()
        user = GetUserByURI(split_raw[0], session)
        if user:    
            return user.jid
        else:
            return ''
    else:
        return ''

def setUserStatus(jid_, active):
    """This is used to mark a user as active or inactive."""
    if isinstance(jid_, JID):
        jid_ = jid_.nodeid()
    session = UserSession()
    user = GetUser(jid_, session)
    user.active=bool(active)
    session.update(user)
    session.commit()
    
def GetUser(jid_, session):
    """Gets a user out of the database by JID."""
    return session.query(User).filter_by(jid=jid_).one()

def GetUserByURI(uri, session):
    try:
        return session.query(User).filter_by(url_prefix=uri, active=True).one()
    except InvalidRequestError:
        return None
    
def connectToDB(Config, **argd):
    global _connected, _user_engine, _meta, _users
    if not _connected:
        _connected = True
        register(cleanup)
        
        _user_engine = sqlalchemy.create_engine(Config.server.db, **argd)
        UserSession.configure(bind=_user_engine)
        
        _meta = MetaData(bind=_user_engine)
        _users = getUserTable(_meta)
        _meta.create_all()
        
        mapper(User, _users)
        
        cleanup()   #make sure all users are inactive in the database
        
def cleanup():
    """This function will make sure that all users are inactive in the database."""
    session = UserSession()
    
    for user in session.query(User).filter_by(active=True):
        user.active=False
    
    session.commit()

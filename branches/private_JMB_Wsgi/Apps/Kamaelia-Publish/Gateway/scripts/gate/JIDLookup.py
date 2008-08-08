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
"""
This module will track users in a database.  You must first call connectToDB to
connect to the database.  This will bind the class UserSession to an engine.

Once this is done, you can call setUserStatus to control whether a user is online
or not.  You may also call ExtractJID to tetermine a user's JID based on the URI
that was passed to the server.
"""
from Kamaelia.Protocol.HTTP import PopWsgiURI
from Kamaelia.Apps.Wsgi.db import getUserTable, User
from Kamaelia.Apps.Wsgi.Console import debug
from headstock.api.jid import JID

import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.exceptions import InvalidRequestError

_logger_suffix = '.publish.gateway.JIDLookup'

#Generate a class type for sessions.
UserSession = sessionmaker(autoflush=True, transactional=True)

#A boolean value just to check and see if we've already connected to the db.
_connected = False

def _getURI(jid_text, session):
    """A convenience function for GetUser in case we just want the uri."""
    return GetUser(jid_text, session).url_prefix
    
def ExtractJID(request):
    """
    This function will take a request that has been generated by the HTTPServer
    (using the WSGILikeTranslator) and extract a JID from it.  If the JID wasn't
    found, this function will return an empty string.
    
    FIXME:  Sometimes, the user will show as inactive in the database even if they
    are active.  We really should check to see if the user is active before throwing
    a 404.
    """
    raw = request['REQUEST_URI']
    split_raw = raw.split('/')
    split_raw = [x for x in split_raw if x]  #remove empty strings
    PopWsgiURI(request)
    if split_raw:
        session = UserSession()
        user = _getUserByURI(split_raw[0], session)
        if user:    
            debug('%s located.' % (user.jid), _logger_suffix)    
            return user.jid
        else:
            debug('JID not found for %s' % (request['REQUEST_URI']), _logger_suffix)
            return ''
    else:
        debug('JID not found for %s' % (request['REQUEST_URI']), _logger_suffix)    
        return ''

def setUserStatus(jid_text, active):
    """This is used to mark a user as active or inactive.  If active is True, the
    JID specified will be marked as active.  If active is False, the JID will be
    marked inactive."""
    if isinstance(jid_text, JID):
        jid_text = jid_text.nodeid()
    session = UserSession()
    user = _getUser(jid_text, session)
    user.active=bool(active)
    session.update(user)
    session.commit()
    
def _getUser(jid_text, session):
    """Gets a user out of the database by JID."""
    return session.query(User).filter_by(jid=jid_text).one()

def _getUserByURI(uri, session):
    """Gets a user out of the database by URI."""
    try:
        return session.query(User).filter_by(url_prefix=uri, active=True).one()
    except InvalidRequestError:
        return ''
    
def connectToDB(Config, **argd):
    """
    This function will connect to the database.  The important part of Config is
    the db member of the server section.  This will specify the database to connect
    to.
    
    **argd represents keyword arguments that will be passed to sqlalchemy.create_engine.
    
    FIXME:  Currently, this will only connect to a sqlite database.
    """
    #Note:  this module is to be treated as an "object".  Thus, while these variables
    #may be marked global, they aren't necessarily intended to be used globally
    #throughout the application.
    global _connected, _user_engine, _meta, _users
    if not _connected:
        _connected = True
        
        _user_engine = sqlalchemy.create_engine(Config.server.db, **argd)
        UserSession.configure(bind=_user_engine)
        
        _meta = MetaData(bind=_user_engine)
        _users = getUserTable(_meta)
        _meta.create_all()
        
        mapper(User, _users)
        
        from atexit import register
        register(_cleanup)
        _cleanup()
        
def _cleanup():
    """This function will make sure that all users are inactive in the database."""
    session = UserSession()
    
    for user in session.query(User).filter_by(active=True):
        user.active=False
    
    session.commit()

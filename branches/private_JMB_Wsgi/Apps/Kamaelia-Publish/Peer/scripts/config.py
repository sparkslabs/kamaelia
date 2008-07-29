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
"""This is a collection of configuration objects that will allow for object-oriented
access of configuration data rather than having to use a dictionary."""

class XMPPConfigObject(object):
    def __init__(self, dictionary):
        self.username = u''
        self.domain = u''
        self.address = u''
        self.usetls = u''
        self.password = u''
        self.resource = u'headstock-client1'
        #for key in dictionary:
        #    self.__dict__[key] = unicode(dictionary[key], 'utf-8')
        self.__dict__.update(dictionary)
        self.username = unicode(self.username)
        self.domain = unicode(self.domain)
        self.resource = unicode(self.resource)
        self.server, self.port = self.address.split(':')
        self.port = int(self.port)
        if self.usetls:
            self.usetls = True
        else:
            self.usetls = False
            
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return repr(self.__dict__)
    
class StaticConfigObject(object):
    def __init__(self, dictionary):
        self.url = dictionary['url']
        self.homedirectory = dictionary['homedirectory']
        self.index = dictionary['index']
        
class ConfigObject(object):
    def __init__(self, dictionary):
        self.static = StaticConfigObject(dictionary['STATIC'])
        self.xmpp = XMPPConfigObject(dictionary['XMPP'])
        self.wsgi = dictionary['WSGI']  #FIXME:  Adapt the WSGI configuration dictionary
                                        #to be an object

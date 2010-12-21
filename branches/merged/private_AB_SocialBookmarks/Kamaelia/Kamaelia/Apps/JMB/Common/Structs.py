#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Licensed to the BBC under a Contributor Agreement: JMB
"""This is a collection of configuration objects that will allow for object-oriented
access of configuration data rather than having to use a dictionary.  This data is
intended to come from an ini file, but may come from anywhere.
"""

import os

class XMPPConfigObject(object):
    def __init__(self, dictionary):
        self.username = u''
        self.domain = u''
        self.address = u''
        self.usetls = u''
        self.password = u''
        self.resource = u'headstock-client1'
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
        
class ServerConfigObject(object):
    def __init__(self, dictionary):
        self.db = dictionary.get('db', None)
        self.log = os.path.expanduser(dictionary['log'])
        self.port = dictionary['port']
        
class ConfigObject(object):
    def __init__(self, dictionary, options):
        self.static = StaticConfigObject(dictionary['STATIC'])
        self.xmpp = XMPPConfigObject(dictionary['XMPP'])
        self.wsgi = dictionary['WSGI']  #FIXME:  Adapt the WSGI configuration dictionary
                                        #to be an object
        self.server = ServerConfigObject(dictionary['SERVER'])
        
        self.options = options

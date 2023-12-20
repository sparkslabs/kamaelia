# -*- coding: utf-8 -*-
# Needed to allow import
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
"""
WSGI Handler
=============

NOTE:  This is experimental software.  It has not been fully tested and will
probably break or behave in unexpected ways.

This is the WSGI handler for ServerCore.  It will wait on the HTTPParser to 
transmit the body in full before proceeding.  Thus, it is probably not a good 
idea to use any WSGI apps requiring a lot of large file uploads (although it 
could theoretically function fairly well for that purpose as long as the concurrency
level is relatively low).

For more information on WSGI, what it is, and to get a general overview of what
this component is intended to adapt the ServerCore to do, see one of the following
links:

* http://www.python.org/dev/peps/pep-0333/ (PEP 333)
* http://www.wsgi.org/wsgi/ (WsgiStart wiki)
* http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface (Wikipedia article on WSGI)

-------------
Dependencies
-------------

This component depends on the wsgiref module, which is included with python 2.5.
Thus if you're using an older version, you will need to install it before using
this component.  

The easiest way to install wsgiref is to use easy_install, which may be downloaded
from http://peak.telecommunity.com/DevCenter/EasyInstall .  You may then install
wsgiref using the command "sudo easy_install wsgiref" (without the quotes of course).

------------------
Factory Functions
------------------

The WSGI Handler may currently be instantiated in two ways:  using SimpleWSGIFactory
and using WSGIFactory.  Use SimpleWSGIFactory if you would like to create a WSGI
Handler but know that you will only use one WSGI Application for that handler.
WSGIFactory is a more advanced factory function that will use built in URL handling
to look up WSGI Applications.

SimpleWSGIFactory
~~~~~~~~~~~~~~~~~~
Creates a WSGI Handler that can handle only one WSGI Application.

  WSGIConfig - see the WsgiConfig section below
  app_object - The WSGI application object to run
  error_log - The file to store errors in
  logger_name - The name of the python logger to log errors to
  
WSGIFactory
~~~~~~~~~~~~
Creates a WSGI Handler using url routing.

  WSGIConfig - see the WSGIConfig section below
  url_list - A URL list to look up App objects.  It must contain three keys:
      kp.regex - the regex to match the uri against (will only match the first
        section)
      kp.import_path - The path to import the WSGI application object from
      kp.app_object - the attribute of the module named in kp.import_path that
        names the WSGI application object
  error_log - The file to store errors in
  logger_name - The name of the python logger to log errors to

--------------------------------
How do I use SimpleWSGIFactory
--------------------------------
To make a WSGI system using SimpleWSGIFactory, use the following:

import socket

import Axon
from Kamaelia.Protocol.HTTP.Handlers.WSGI import SimpleWSGIFactory
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP import ErrorPages
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol
from Kamaelia.Apps.WSGI.Simple import simple_app

port = 8080

#This is just a configuration dictionary for general WSGI stuff.  This needs to be passed to the handler
#to run
WsgiConfig ={
'server_software' : "Simple Example WSGI Web Server",
'server_admin' : "Jason Baker",
'wsgi_ver' : (1,0),
}

def main():
    #This line is so that the HTTPRequestHandler knows what component to route requests to.
    routing = [ ['/simple', SimpleWSGIFactory(WsgiConfig, simple_app)] ]
    server = ServerCore(protocol=HTTPProtocol(routing),
                        port=port,
                        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

    print 'Serving on port %s' % (port)
    server.run()

if __name__ == '__main__':
    main()

-----------------------------
How do I use WSGIFactory?
-----------------------------

Here is an example of how to create a simple WSGI server using WSGIFactory:

from Kamaelia.Support.Protocol.HTTP import HTTPProtocol
from Kamaelia.Protocol.HTTP.Handlers.WSGI import WSGIFactory

WsgiConfig = {
    'wsgi_ver' : (1, 0),
    'server_admin' : 'Jason Baker',
    'server_software' : 'Kamaelia Publish'
}

url_list = [ #Note that this is a list of dictionaries.  Order is important.
    {
        'kp.regex' : 'simple',
        'kp.import_path' : 'Kamaelia.Apps.WSGI.Simple',
        'kp.app_obj' : 'simple_app',
    }
    {
        'kp.regex' : '.*',  #The .* means that this is a 404 handler
        'kp.import_path' : 'Kamaelia.Apps.WSGI.ErrorHandler',
        'kp.app_obj' : 'application',
    }
]

routing = [['/', WsgiFactory(WsgiConfig, url_list)]]

ServerCore(
    protocol=HTTPProtocol(routing),
    port=8080,
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)).run()

------------------
Internal overview
------------------

request object
~~~~~~~~~~~~~~~

Note that certain WSGI applications will require configuration
data from the urls file.  If you use the WSGIFactory to run this
handler, all options specified in the urls list will be put into
the environment variable with a kp. in front of them.  

For example, the 'regex' entry in a urls file would go into the
environ dictionary like this if it was set to 'simple':

{
    ...
    'kp.regex' : 'simple',
    ...
}

wsgi.input
~~~~~~~~~~~

PEP 333 requires that the WSGI environ dictionary also contain a file-like object
that holds the body of the request.  Currently, the WsgiHandler will wait for the
full request before starting the application (which is not optimal behavior).  If
the method is not PUT or POST, the handler will use a pre-made null-file object that
will always return empty data.  This is an optimization to lower peak memory usage
and to speed things up.

WSGIConfig
~~~~~~~~~~~

The WSGI Handler requires a WSGIConfig dictonary for general configuration info. The
following items are required to be defined:

* wsgi_ver: the WSGI version as a Tuple.  You want to use (1, 0)
* server_admin: the name and/or email address of the server's administrator
* server_software: The software and/or software version that runs the server

FIXME:  It would be nice if the WsgiConfig were made into an object rather than a
dictionary.
"""
from ._factory import WSGIFactory, SimpleWSGIFactory

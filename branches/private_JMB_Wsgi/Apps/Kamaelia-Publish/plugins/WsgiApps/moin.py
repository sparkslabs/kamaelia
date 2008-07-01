# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - mod_wsgi driver script

    To use this, add those statements to your Apache's VirtualHost definition:
    
    # this is for icons, css, js (and must match url_prefix from wiki config):
    Alias       /moin_static162/ /usr/share/moin/htdocs/

    # this is the URL http://servername/moin/ you will use later to invoke moin:
    WSGIScriptAlias /moin/ /some/path/moin.wsgi

    # create some wsgi daemons - use someuser.somegroup same as your data_dir:
    WSGIDaemonProcess daemonname user=someuser group=somegroup processes=5 threads=10 maximum-requests=1000
    # umask=0007 does not work for mod_wsgi 1.0rc1, but will work later

    # use the daemons we defined above to process requests!
    WSGIProcessGroup daemonname

    @copyright: 2007 by MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""

import sys


import logging

from MoinMoin.server.server_wsgi import WsgiConfig, moinmoinApp

class Config(WsgiConfig):
    logPath = 'moin.log' # adapt this to your needs!
    #loglevel_file = logging.INFO # adapt if you don't like the default

config = Config() # MUST create an instance to init logging!

application = moinmoinApp


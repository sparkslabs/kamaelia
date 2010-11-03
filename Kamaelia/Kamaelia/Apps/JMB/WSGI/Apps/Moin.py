# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - wsgi driver script

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


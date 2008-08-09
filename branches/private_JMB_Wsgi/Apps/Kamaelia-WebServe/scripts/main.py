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
import sys, socket, os, zipfile, logging
import cProfile as profile
from pprint import pprint

from autoinstall import autoinstall

from Kamaelia.Apps.Wsgi.Factory import WsgiFactory
from Kamaelia.Apps.Wsgi.Console import info
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.File.ConfigFile import DictFormatter, ParseConfigFile
from Kamaelia.Protocol.HTTP import HTTPProtocol
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory
from Kamaelia.Apps.Wsgi.Config import ParseUrlFile
from Kamaelia.Apps.Wsgi.kpsetup import processPyPath, normalizeUrlList, normalizeWsgiVars, initializeLoggers
from Kamaelia.Support.Protocol.HTTP import WSGILikeTranslator

sys.path.insert(0, sys.argv[0] + '/data')

_profile_ = False
_logger_suffix = '.WebServe.main'

def run_program():
    """The main entry point for the application."""
    try:
        zip = zipfile.ZipFile(sys.argv[0], 'r')
        
        corrupt = zip.testzip()
        if corrupt:
            Console.prompt_corrupt(corrupt)
                    
        home_path = os.environ['HOME']
        
        if not os.path.exists(home_path + '/kp.ini'):
            autoinstall(zip, home_path)
            
        zip.close()
        
        configs = ParseConfigFile('~/kp.ini', DictFormatter())
        ServerConfig = configs['SERVER']
        WsgiConfig = configs['WSGI']
        StaticConfig = configs['STATIC']
        
        processPyPath(ServerConfig)
        normalizeWsgiVars(WsgiConfig)
    
        url_list = ParseUrlFile(WsgiConfig['url_list'])
        normalizeUrlList(url_list)
        
        StaticConfig['homedirectory'] = os.path.expanduser(StaticConfig['homedirectory'])
        routing = [
                      [StaticConfig['url'], MinimalFactory(
                                                           StaticConfig['index'], 
                                                           StaticConfig['homedirectory']
                                                           )],
                      ["/", WsgiFactory(WsgiConfig, url_list)],
                  ]
    
        initializeLoggers(ServerConfig.get('log', home_path + '/kpuser/ks.log'))
        
        kp = ServerCore(
            protocol=HTTPProtocol(routing),
            port=int(ServerConfig['port']),
            socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))
    
        info('Serving on port %s' % (ServerConfig['port']), _logger_suffix)
    except:
        import traceback
        print 'There was an error!  Info is in error.log'
        file = open('error.log', 'a')
        traceback.print_exc(file=file)
        file.close()
        sys.exit(1)
    try:
        kp.run()
    except KeyboardInterrupt:
        print "Halting server!"
    except:
        #Something's gone horribly wrong and the program doesn't know what to do
        #about it.
        import traceback
        traceback.print_exc()
        print "===========FATAL ERROR==========="
    finally:
        kp.stop()
        logging.shutdown()

def profile_main():
    """This is what you want to use if you intend on profiling the application."""
    pr = profile.Profile()  #Note that we've imported cProfile as profile.
    pr.run('main.run_program()')

if _profile_:
    main = profile_main
else:
    main = run_program
    
if __name__ == '__main__':
    main()

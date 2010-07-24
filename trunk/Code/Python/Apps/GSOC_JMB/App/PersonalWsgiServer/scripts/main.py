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
import sys, socket, os, zipfile, logging
import cProfile as profile
from pprint import pprint

from Kamaelia.Apps.JMB.WSGI import WSGIFactory
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory

#Stuff that's shared between some of the webservers
from Kamaelia.Apps.JMB.Common.Console import info
from Kamaelia.Apps.JMB.Common.ConfigFile import DictFormatter, ParseConfigFile
from Kamaelia.Apps.JMB.Common.autoinstall import autoinstall
from Kamaelia.Apps.JMB.Common.UrlConfig import ParseUrlFile
from Kamaelia.Apps.JMB.Common.ServerSetup import processPyPath, normalizeUrlList, \
    normalizeWsgiVars, initializeLogger

_profile_ = False
_logger_suffix = '.WebServe.main'

def run_program():
    """The main entry point for the application."""
    try:
        zip = zipfile.ZipFile(sys.argv[0], 'r')
        
        #prompt the user if this executable is corrupt
        corrupt = zip.testzip()
        if corrupt:
            Console.prompt_corrupt(corrupt)
                   
        
        initializeLogger()
        home_path = os.environ['HOME']
        
        #prompt the user to install the necessary software if this is the first
        #time to run Kamaelia WebServe
        if not os.path.exists(home_path + '/kp.ini'):
            autoinstall(zip, home_path, 'Kamaelia WebServe')
            
        zip.close()
        
        #Extract data from Config Files and organize it into dictionaries
        configs = ParseConfigFile('~/kp.ini', DictFormatter())
        ServerConfig = configs['SERVER']
        WsgiConfig = configs['WSGI']
        StaticConfig = configs['STATIC']
        
        processPyPath(ServerConfig)
        normalizeWsgiVars(WsgiConfig)
    
        url_list = ParseUrlFile(WsgiConfig['url_list'])
        normalizeUrlList(url_list)
        
        StaticConfig['homedirectory'] = os.path.expanduser(StaticConfig['homedirectory'])
        log = os.path.expanduser(ServerConfig['log'])
        routing = [
                      [StaticConfig['url'], MinimalFactory(
                                                           StaticConfig['index'], 
                                                           StaticConfig['homedirectory']
                                                           )],
                      ["/", WSGIFactory(WsgiConfig, url_list, log)],
                  ]

        kp = ServerCore(
            protocol=HTTPProtocol(routing),
            port=int(ServerConfig['port']),
            socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))
    
        info('Serving on port %s' % (ServerConfig['port']), _logger_suffix)
    except:
        import traceback
        print 'There was an error!  Info is in %s/error.log' % (os.getcwd())
        file = open('error.log', 'a')
        traceback.print_exc(file=file)
        file.write('\n')
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

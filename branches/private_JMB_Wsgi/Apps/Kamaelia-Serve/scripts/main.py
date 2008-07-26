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
import sys, socket, os, zipfile
import cProfile as profile
from pprint import pprint

from autoinstall import autoinstall
import console_io

from Kamaelia.Apps.Wsgi.Factory import WsgiFactory
import Kamaelia.Apps.Wsgi.LogWritable as LogWritable
from Kamaelia.Chassis.ConnectedServer import ServerCore
import Kamaelia.Apps.Wsgi.Log as Log
from Kamaelia.File.ConfigFile import DictFormatter, ParseConfigFile
from Kamaelia.Protocol.HTTP import HTTPProtocol
from Kamaelia.Apps.Wsgi.Config import ParseUrlFile
from Kamaelia.Protocol.HTTP.Translators.WSGILike import WSGILikeTranslator

sys.path.insert(0, sys.argv[0] + '/data')

_profile_ = False

def normalizeWsgiVars(WsgiConfig):
    """Put WSGI config data in a state that the server expects."""
    WsgiConfig['wsgi_ver'] = tuple(WsgiConfig['wsgi_ver'].split('.'))
    
def normalizeUrlList(url_list):
    """Add necessary default entries that the user did not enter."""
    for dict in url_list:
        if not dict.get('kp.app_object'):
            dict['kp.app_object'] = 'application'
            
def processServerConfig(ServerConfig):
    """Use the Server configuration data to actually configure the server."""
    print ServerConfig
    if ServerConfig.get('pypath_append'):
        path_append = ServerConfig['pypath_append'].split(':')
        sys.path.extend(path_append)
    
    if ServerConfig.get('pypath_prepend'):
        path_prepend = ServerConfig['pypath_prepend'].split(':')
        path_prepend.reverse()
        for path in path_prepend:
            sys.path.insert(0, path)
    
    #uncomment this if you want to debug what this code is doing to sys.path.
    #print 'sys.path-'
    #print sys.path

def run_program():
    """The main entry point for the application."""
    #console_out = sys.stdout
    #log_out = open('out.log', 'w')
    #sys.stdout = log_out
    try:
        zip = zipfile.ZipFile(sys.argv[0], 'r')
        
        corrupt = zip.testzip()
        if corrupt:
            console_io.prompt_corrupt(corrupt)
                    
        home_path = os.environ['HOME']
        
        if not os.path.exists(home_path + '/kp.ini'):
            autoinstall(zip, home_path)
            
        zip.close()
        
        configs = ParseConfigFile('~/kp.ini', DictFormatter())
        ServerConfig = configs['SERVER']
        WsgiConfig = configs['WSGI']
        
        processServerConfig(ServerConfig)
        
        #uncomment this if you wish to debug what is happening to WsgiConfig
        #from pprint import pprint
        #pprint(WsgiConfig)
        normalizeWsgiVars(WsgiConfig)
    
        sys.path.append(WsgiConfig['log'])
    
        url_list = ParseUrlFile(WsgiConfig['url_list'])
        normalizeUrlList(url_list)
    
        log = Log.LogWriter(WsgiConfig['log'], wrapper=Log.nullWrapper)
    
        log_writable = LogWritable.WsgiLogWritable(WsgiConfig['log'])
        log_writable.activate()
    
        routing = [
                      ["/", WsgiFactory(log_writable, WsgiConfig, url_list)],
                  ]
        
        if ServerConfig.get('use_hrouting'):
            #this assumes of course that hrouting.py is on the python path
            from hrouting import custom_routing
            custom_routing.reverse()
            for item in custom_routing:
                routing.insert(0, item)
            
            
        #print routing
    
        log.activate()
    
        kp = ServerCore(
            protocol=HTTPProtocol(routing, WSGILikeTranslator),
            port=int(ServerConfig['port']),
            socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))
    
        print "Serving on port %s" % (ServerConfig['port'])
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
        kp.stop()
    except:
        #Something's gone horribly wrong and the program doesn't know what to do
        #about it.
        import traceback
        traceback.print_exc()
        print "===========FATAL ERROR==========="
        kp.stop()

def profile_main():
    """This is what you want to use if you intend on profiling the application."""
    #uncomment this if you're using profile and want to calibrate.  If you're still
    #using cProfile, leave it commented out.
    #print "==CALIBRATING=="
    #pr = profile.Profile()
    #for i in range(5):
    #    print pr.calibrate(10000)

    pr = profile.Profile()  #Note that we've imported cProfile as profile.
    pr.run('main.run_program()')
    
    #Put the data into a format that KCacheGrind can understand.
    import lsprofcalltree
    k = lsprofcalltree.KCacheGrind(pr)
    data = open('prof.kgrind', 'w+')
    k.output(data)
    data.close()

if _profile_:
    main = profile_main
else:
    main = run_program
    
if __name__ == '__main__':
    main()

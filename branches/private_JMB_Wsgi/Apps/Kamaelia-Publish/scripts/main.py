#!/usr/bin/env
import sys, socket, os, zipfile
import cProfile as profile
from pprint import pprint

from autoinstall import autoinstall
import console_io

from Kamaelia.Experimental.Wsgi.WsgiHandler import HTML_WRAP,  WsgiHandler
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable
from Kamaelia.Chassis.ConnectedServer import ServerCore
import Kamaelia.Experimental.Wsgi.Log as Log
from Kamaelia.File.ConfigFile import DictFormatter, UrlListFormatter, ParseConfigFile
from Kamaelia.Protocol.HTTP import HTTPProtocol

sys.path.insert(0, sys.argv[0] + '/data')

_profile_ = False

def normalizeWsgiVars(WsgiConfig):
    WsgiConfig['wsgi_ver'] = tuple(WsgiConfig['wsgi_ver'].split('.'))
    
def normalizeUrlList(url_list):
    for dict in url_list:
        if not dict.get('kp.app_object'):
            dict['kp.app_object'] = 'application'
            
def processServerConfig(ServerConfig):
    if ServerConfig.get('pypath-append'):
        path_append = ServerConfig['pypath-append'].split(':')
        sys.path.extend(path_append)
    
    if ServerConfig.get('pypath-prepend'):
        path_prepend = ServerConfig['pypath-prepend'].split(':')
        path_prepend.reverse()
        for path in path_prepend:
            sys.path.insert(0, path)
    
    #print 'sys.path-'
    #print sys.path

def run_program():
    zip = zipfile.ZipFile(sys.argv[0], 'r')
    
    corrupt = zip.testzip()
    if corrupt:
        console_io.prompt_corrupt(corrupt)
                
    home_path = os.environ['HOME']
    
    if not os.path.exists(home_path + 'kp.ini'):
        autoinstall(zip, home_path)
        
    zip.close()
    
    configs = ParseConfigFile('~/kp.ini', DictFormatter())
    ServerConfig = configs['SERVER']
    WsgiConfig = configs['WSGI']
    
    processServerConfig(ServerConfig)
    
    #from pprint import pprint
    #pprint(WsgiConfig)
    normalizeWsgiVars(WsgiConfig)

    sys.path.append(WsgiConfig['log'])

    url_list = ParseConfigFile(WsgiConfig['url_list'], [DictFormatter(), UrlListFormatter()])
    normalizeUrlList(url_list)

    log = Log.LogWriter(WsgiConfig['log'], wrapper=Log.nullWrapper)

    log_writable = LogWritable.WsgiLogWritable(WsgiConfig['log'])
    log_writable.activate()

    routing = [
                  ["/", WsgiHandler(log_writable, WsgiConfig, url_list)],
              ]

    log.activate()

    kp = ServerCore(
        protocol=HTTPProtocol(routing),
        port=int(ServerConfig['port']),
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

    print "Serving on port %s" % (ServerConfig['port'])
    try:
        kp.run()
    except KeyboardInterrupt:
        print "Halting server!"
        kp.stop()
    except:
        import traceback
        traceback.print_exc()
        print "===========FATAL ERROR==========="
        kp.stop()

def profile_main():
    #print "==CALIBRATING=="
    #pr = profile.Profile()
    #for i in range(5):
    #    print pr.calibrate(10000)

    pr = profile.Profile()
    pr.run('main.run_program()')
    
    import lsprofcalltree
    k = lsprofcalltree.KCacheGrind(pr)
    data = open('prof.kgrind', 'w+')
    k.output(data)
    data.close()
    
    #import pstats
    #p = pstats.Stats('profile.log')
    #p.sort_stats('name')
    #p.print_stats()

if _profile_:
    main = profile_main
else:
    main = run_program
    
print "__name = ", __name__
print sys.argv
if __name__ == '__main__':
    run_program()

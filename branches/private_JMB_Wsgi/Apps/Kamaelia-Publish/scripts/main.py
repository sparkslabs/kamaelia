#!/usr/bin/env
import sys, socket
from pprint import pprint
from Kamaelia.Experimental.Wsgi.WsgiHandler import HTML_WRAP,  WsgiHandler
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable
from Kamaelia.Chassis.ConnectedServer import ServerCore
import Kamaelia.Experimental.Wsgi.Log as Log
from Kamaelia.File.ConfigFile import DictFormatter, UrlListFormatter, ParseConfigFile
from Kamaelia.Protocol.HTTP import HTTPProtocol

sys.path.insert(0, sys.argv[0] + '/data')

def normalizeWsgiVars(WsgiConfig):
    WsgiConfig['wsgi_ver'] = tuple(WsgiConfig['wsgi_ver'].split('.'))

def main():
    configs = ParseConfigFile('~/.kp', DictFormatter())
    ServerConfig = configs['SERVER']
    WsgiConfig = configs['WSGI']
    from pprint import pprint
    #pprint(WsgiConfig)
    normalizeWsgiVars(WsgiConfig)

    sys.path.append(WsgiConfig['log'])

    url_list = ParseConfigFile(WsgiConfig['url_list'], [DictFormatter(), UrlListFormatter()])

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

#!/usr/bin/env

import ServerConfig
import sys, socket
from pprint import pprint
from Kamaelia.Experimental.Wsgi.WsgiHandler import HTML_WRAP,  WsgiHandler
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable
from Kamaelia.Chassis.ConnectedServer import ServerCore
import Kamaelia.Experimental.Wsgi.Log as Log
from Kamaelia.File.ConfigFile import DictFormatter, UrlListFormatter, ParseConfigFile
from Kamaelia.Protocol.HTTP import HTTPProtocol

from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

sys.path.append(ServerConfig.WsgiAppLog)

def main():
    url_list = ParseConfigFile(ServerConfig.URL_LIST_LOCATION, [DictFormatter(), UrlListFormatter()])
#    pprint(url_list)


    log = Log.LogWriter(ServerConfig.WsgiAppLog, wrapper=Log.nullWrapper)

    log_writable = LogWritable.WsgiLogWritable(ServerConfig.WsgiAppLog)
    log_writable.activate()

    routing = [
                  ["/", WsgiHandler(log_writable, ServerConfig.WsgiConfig, url_list)],
              ]

    log.activate()

    des = ServerCore(
        protocol=HTTPProtocol(routing),
        port=8082,
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

    print "Serving on port %s" % (ServerConfig.PORT)
    des.run()

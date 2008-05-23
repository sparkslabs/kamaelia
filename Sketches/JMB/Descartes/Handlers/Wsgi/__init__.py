import Kamaelia.Util.Log as Log
import WsgiConfig

Logger = Log.Logger(WsgiConfig.WSGI_DIRECTORY + WsgiConfig.LOG_NAME,
                    Log.nullWrapper)

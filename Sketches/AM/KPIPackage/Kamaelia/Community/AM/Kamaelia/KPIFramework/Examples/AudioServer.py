from AudioLib import *
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.SimpleServerComponent import SimpleServer as _SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Graphline import *


def clientconnector():
    return subscribeTo("AudioServer")

Backplane("AudioServer").activate()
server=_SimpleServer(protocol=clientconnector, port=1256).activate()
pipeline(AudioSource(100000),
         AudioEncoder('mp3'),
         publishTo("AudioServer")
        ).run()

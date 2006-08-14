from AudioLib import *
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient

pipeline(_TCPClient("127.0.0.1",1256),
         AudioDecoder('mp3'),         
         SoundOutput()
        ).run()

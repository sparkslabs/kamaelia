#!/usr/bin/python


from Kamaelia.Util.PipelineComponent import pipeline
from Record import AlsaRecorder
from Play import AlsaPlayer
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient

pipeline(
    AlsaRecorder(),
    SingleServer(port=1601),
).activate()

pipeline(
    TCPClient("127.0.0.1", 1601),
    AlsaPlayer(),
).run()

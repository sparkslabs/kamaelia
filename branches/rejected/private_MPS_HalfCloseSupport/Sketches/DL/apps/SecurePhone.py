#!/usr/bin/python


from Kamaelia.Util.PipelineComponent import pipeline
from Record import AlsaRecorder
from Play import AlsaPlayer
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Integrity import IntegrityStamper, IntegrityChecker
#from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller
from DL_Util import Pickle, UnPickle

pipeline(
    AlsaRecorder(),
    IntegrityStamper(),
    Pickle(),
    SingleServer(port=1601),
).activate()

pipeline(
    TCPClient("127.0.0.1", 1601),
    UnPickle(),
    IntegrityChecker(),
    AlsaPlayer(),
).run()

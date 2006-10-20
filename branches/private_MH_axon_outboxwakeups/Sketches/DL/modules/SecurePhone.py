#!/usr/bin/python


from Kamaelia.Util.PipelineComponent import pipeline
from Alsa import AlsaRecorder, AlsaPlayer
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Integrity import IntegrityStamper, IntegrityChecker, DisruptiveComponent
#from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller
from DL_Util import Pickle, UnPickle
from Speex import SpeexEncode, SpeexDecode
#from DVB_Multicast import dataRateMeasure
from Axon.Component import component
from Encryption import Encryptor, Decryptor

import time
class dataRateMeasure(component):
    def main(self):
        size = 0
        c = 0
        t = time.time()
        while 1:
            while self.dataReady("inbox"):
                c += 1
                data = self.recv("inbox")
                size += len(data)
                self.send(data, "outbox")
            if (c % 20) == 0:
                t_dash = time.time()
                if t_dash - t > 1:
                    print int((size/(t_dash - t))*8)
                    t = t_dash
                    size = 0
            yield 1


pipeline(
    AlsaRecorder(),
    SpeexEncode(3),
#   Encryptor("1234567812345678", "AES"),
    dataRateMeasure(),
    SingleServer(port=1601),
).activate()

pipeline(
    TCPClient("127.0.0.1", 1601),
#    Decryptor("1234567812345678", "AES"),
    SpeexDecode(3),
    AlsaPlayer(),
).run()

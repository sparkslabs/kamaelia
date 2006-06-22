
import Kamaelia.ReadFileAdaptor
from Axon import Component
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Chargen import Chargen
from Kamaelia.Util.ConsoleEcho import consoleEchoer


class IntegrityStamper(Component.component):

    def __init__(self,  algorithm="SHA"):

        self.__super.__init__()
        self.algorithm = algorithm

    def setAlgorithm(self):

        if self.algorithm is "SHA":
            from Crypto.Hash import SHA
            self.hashobj = SHA.new()
        else:
            if self.algorithm is "MD5":
                from Crypto.Hash import MD5
                self.hashobj = SHA.new()

    def calcHash(self, data):

        self.hashobj.update(data)
        return self.hashobj.digest()
            
    def main(self):

        
        self.setAlgorithm()

        while 1:

            if self.dataReady("inbox"):
                data = self.recv("inbox")

                checksum = self.calcHash(data)

                self.send((data, checksum), "outbox")
            yield 1

class IntegrityChecker(Component.component):

    def __init__(self,  algorithm="SHA"):

        self.__super.__init__()
        self.algorithm = algorithm

    def setAlgorithm(self):

        if self.algorithm is "SHA":
            from Crypto.Hash import SHA
            self.hashobj = SHA.new()
        else:
            if self.algorithm is "MD5":
                from Crypto.Hash import MD5
                self.hashobj = SHA.new()

    def calcHash(self, data):

        self.hashobj.update(data)
        return self.hashobj.digest()
            
    def main(self):

        
        self.setAlgorithm()

        while 1:

            if self.dataReady("inbox"):
                (data, checksum) = self.recv("inbox")

                if checksum == self.calcHash(data):
                    self.send(data, "outbox")
            yield 1


        
pipeline(
    Chargen(),
    IntegrityStamper(),
    IntegrityChecker(),
    consoleEchoer()
    ).run()


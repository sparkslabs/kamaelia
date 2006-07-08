
import Kamaelia.ReadFileAdaptor
from Axon import Component
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Chargen import Chargen
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from DL_Util import SerialChargen
from Encryption import BasicEncryption

import random
"""
============================
Basic Data Integrity Checker
============================

This module contains a series of components which ensure the
integrity of data transferred between components.

It basically adds a hash code of the data to be transferred. Baisc Usage is

Data Producer -- (data) -- IntegrityStamper() -- (data, hash) -- <other components> ...

... <other components> -- (data, hash) -- IntegrityChecker() -- (data) -- Data Consumer

"""

class IntegrityError(Exception):

    def __str__(self):
        return "Checksum failed"
    
        
class BasicIntegrity(Component.component):

    def __init__(self,  algorithm="SHA"):

        self.__super.__init__()
        self.algorithm = algorithm
        self.setAlgorithm()
        
    def setAlgorithm(self):

        if self.algorithm is "SHA":
            from Crypto.Hash import SHA
            self.method = SHA
        elif self.algorithm is "MD5":
            from Crypto.Hash import MD5
            self.method = MD5
#        elif self.algorithm is "RIPEMD":
#            from Crypto.Hash import RIPEMD # Cannot do this for some reason
#            self.method = RIPEMD
            
        
    def calcHash(self, data):

        hashobj = self.method.new(data)
        return hashobj.digest()


class IntegrityStamper(BasicIntegrity):

    def __init__(self,  algorithm="SHA"):

        self.__super.__init__(algorithm)
            
    def main(self):

        while 1:

            if self.dataReady("inbox"):
                data = self.recv("inbox")

                checksum = self.calcHash(data)
                #print "Integrity stamper :", data, " ", checksum
                self.send((data, checksum), "outbox")
            yield 1

class IntegrityChecker(BasicIntegrity):

    def __init__(self,  algorithm="SHA"):

        self.__super.__init__(algorithm)

            
    def main(self):

        while 1:
            try:
                if self.dataReady("inbox"):

                    (data, checksum) = self.recv("inbox")
                    #print data , checksum , self.calcHash(data)                    
                    if checksum == self.calcHash(data):

                        self.send(data, "outbox")
                    else:                      # we have a hash failure
                        raise IntegrityError  # This mechanism needs improvement
            except IntegrityError:

                print "Integrity Error"
                
            yield 1

class DisruptiveComponent(Component.component):
    """ This component causes a minor change in the data
        so that data and its checksum will not match.
        Used for testing of integrity service.         """

    def __init__(self, probability=0.2):  # Probability of Disruption
        
        super(DisruptiveComponent, self).__init__()
        self.probability = probability

        
    def main(self):

        while 1:
            if self.dataReady("inbox"):
                (data, checksum) = self.recv("inbox")

                if random.random() < self.probability:  
                    #print "Corrupting Data"
                    data = data[:-1]           #Corrupt Data

                self.send((data, checksum), "outbox")
            yield 1

class MAC_Stamper(BasicIntegrity):
    """ Provides message authentication only, message is still sent in plain text
    """
       
    def __init__(self, key,  encryption="AES", mode="ECB", hash="SHA"):

        self.__super.__init__(hash)
        self.encryptobj = BasicEncryption(key, encryption, mode)
        
    def main(self):

        while 1:

            if self.dataReady("inbox"):
                data = self.recv("inbox")

                mac = self.encryptobj.encrypt(self.calcHash(data))
                self.send((data, mac), "outbox")
            yield 1


class MAC_Checker(BasicIntegrity):

    def __init__(self, key, encryption="AES", mode="ECB", hash="SHA"):

        self.__super.__init__(hash)
        self.decryptobj = BasicEncryption(key, encryption, mode)
        
    def main(self):

        while 1:
            try:
                if self.dataReady("inbox"):

                    (data, mac) = self.recv("inbox")
                    checksum = self.decryptobj.decrypt(mac)
                    if checksum == self.calcHash(data):

                        self.send(data, "outbox")
                    else:                      # we have a hash failure
                        raise IntegrityError  # This mechanism needs improvement
            except IntegrityError:

                print "Integrity Error"
                
            yield 1



if __name__ == "__main__":
    pipeline(
        SerialChargen(),
        MAC_Stamper("1234567812345678", mode="CBC"),
        DisruptiveComponent(),
        MAC_Checker("1234567812345678", mode="CBC"),
        consoleEchoer()
        ).run()


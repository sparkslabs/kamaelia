
import Kamaelia.ReadFileAdaptor
from Axon import Component
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Chargen import Chargen
from Kamaelia.Util.ConsoleEcho import consoleEchoer
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

class SerialChargen(Chargen):
    """ Generates Hello World0, Hello World1, Hello World2, ....."""

    def main(self):
        """Main loop."""
        count = 0
        while 1:
            self.send("Hello World" + str(count), "outbox")
            count += 1
            yield 1

                                  
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
        else:
            if self.algorithm is "MD5":
                from Crypto.Hash import MD5
                self.method = MD5

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

        
pipeline(
    SerialChargen(),
    IntegrityStamper(),
    DisruptiveComponent(),
    IntegrityChecker(),
    consoleEchoer()
    ).run()


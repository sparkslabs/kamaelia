
from Axon import Component
from Kamaelia.Util.Chargen import Chargen
from DL_Util import SerialChargen
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.Util.PipelineComponent import pipeline


class BasicEncryption(Component.component):
    
    def __init__(self, key, algorithm="AES", mode="ECB"):
        
        self.__super.__init__()
        self.blocksize = 8  # Most common 
        self.algorithm = algorithm
        self.mode = mode
        self.key = key  # needs to made private ?
        self.setAlgorithm()
        self.setMode()
        self.obj = self.method.new(key, self.operatingmode)
        
    def setAlgorithm(self):
        
        if self.algorithm is "AES":
            from Crypto.Cipher import AES
            self.method = AES
            self.blocksize = 16
        elif self.algorithm is "DES":
            from Crypto.Cipher import DES
            self.method = DES
            
    def setMode(self):
        
        if self.mode is "ECB":
            self.operatingmode = self.method.MODE_ECB
        elif self.mode is "CBC":
            self.operatingmode = self.method.MODE_CBC
            
    def createBlock(self, text):

        if len(text) % self.blocksize == 0:
            return text

        text = text + ( "\0" * (16 - len(text) % self.blocksize))
        # SMELL : Review padding procedure,  cryptographically unsecure, NULL at end of data stream will be gobbled up
        return text

    def destroyBlock(self, text):

        while text[-1:] is "\0":  #SMELL : Find an efficient way to do this ?
            text = text[:-1]
        return text
        
    def encrypt(self, plaintext):
        
        plaintext = self.createBlock(plaintext)
        return self.obj.encrypt(plaintext)

    def decrypt(self, ciphertext):

        ciphertext =  self.obj.decrypt(ciphertext)
        return self.destroyBlock(ciphertext)

class Encryptor(BasicEncryption):

    def __init__(self, key, algorithm="AES", mode="ECB"):

        self.__super.__init__(key, algorithm, mode)


    def main(self):

        while 1:

            if self.dataReady("inbox"):
                plaintext = self.recv("inbox")

                ciphertext = self.encrypt(plaintext)

                self.send(ciphertext, "outbox")
            yield 1

class Decryptor(BasicEncryption):

    def __init__(self, key, algorithm="AES", mode="ECB"):

        self.__super.__init__(key, algorithm, mode)


    def main(self):

        while 1:

            if self.dataReady("inbox"):
                ciphertext = self.recv("inbox")

                plaintext = self.decrypt(ciphertext)

                self.send(plaintext, "outbox")
            yield 1

if __name__ == "__main__":
    pipeline(
        SerialChargen(),
        Encryptor("1234567812345678"),
        Decryptor("1234567812345678"),
        consoleEchoer()
        ).run()

                
            

import unittest

import sys; sys.path.append("../")
from mini_http import LocalFileServer
from Axon.Component import component, scheduler, linkage
from Kamaelia.Util.PipelineComponent import pipeline
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.KamaeliaIPC import socketShutdown

#### Testy thingies follow #########################################################

class Tester(component):
    def __init__(self, tester):
        super(Tester, self).__init__()
        self.tester = tester

    def main(self):
        done = False
        while not done:
            self.pause()
            yield 1

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                self.tester.assertEqual(data, "line one\nline two \n")

            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    done = True
                    self.send(msg, "signal")

class GenericTester(component):
    """
    Goes in the end of a pipeline, and tests things for you.
    
    What it tests, is whatever you want it to test :)
    
    The constructor takes as many parameters as you want tests.
    Each param may be a function, or a list of functions. If the former, it's run on every 
    data item that this component recieves in it's inbox. If the latter, list[i] will be run 
    on the ith data element to be recieved. If you don't supply enough tests in your list, 
    they'll loop. 
    
    The functions you supply should take one parameter. That param will be the data that was 
    received, which you want to test.
    """
    def __init__(self, *tests):
        super(GenericTester, self).__init__()
        self.tests = tests
    
    def main(self):
        done = False
        testnum = 0
        while not done:
            yield 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                for test in self.tests:
                    if type(test) == type(list):
                        test = test[self.testnum%len(test)]
                    test(data)
                testnum+=1
            if self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    done = True
                    self.send(msg, "signal")

class filePointer(component):
    def __init__(self):
        super(filePointer, self).__init__()
            
    def main(self):
        self.send("input.txt","outbox")
        yield 1
        self.send( producerFinished(self), "signal" )
        yield 2

#############################################################################

class LocalFileServer_Tests(unittest.TestCase):
    def test_Simple(self):
        # initially manual wotsit
        pipeline(filePointer(),
            LocalFileServer(),
            Tester(self)
            ).activate()
        
        scheduler.run.runThreads()
        
    def test_Generic(self):
        pipeline(filePointer(),
            LocalFileServer(),
            GenericTester(lambda x : self.assertEqual(x, "line one\nline two \n"))
            ).activate()

if __name__=="__main__":
    unittest.main()
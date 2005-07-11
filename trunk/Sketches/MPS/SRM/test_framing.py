#!/usr/bin/python


import unittest
import Framing

from Axon.Ipc import producerFinished

class Framing_Tests(unittest.TestCase):

    def test_tuple2string_1(self):
        "SimpleFrame.__str__ - (1,'1') results in '1 1\\n1'"
        Frame = Framing.SimpleFrame(1,'1')
        result = str(Frame)
        self.assertEqual(result, '1 1\n1')

    def test_tuple2string_2(self):
        "SimpleFrame.__str__ - (1,'11') results in '1 2\\n11'"
        Frame = Framing.SimpleFrame(1,'11')
        result = str(Frame)
        self.assertEqual(result, '1 2\n11')

    def test_tuple2string_3(self):
        "SimpleFrame.__str__ - (1,'1111') results in '1 4\\n1111'"
        Frame = Framing.SimpleFrame(1,'1111')
        result = str(Frame)
        self.assertEqual(result, '1 4\n1111')

    def test_tuple2string_4(self):
        "SimpleFrame.__str__ - (50,'1111') results in '50 4\\n1111'"
        Frame = Framing.SimpleFrame(50,'1111')
        result = str(Frame)
        self.assertEqual(result, '50 4\n1111')

    def test_tuple2string_5(self):
        "SimpleFrame.__str__ - Random data as the data part of the tuple succeeds"
        import random
        length = 100
        r = []
        for x in xrange(length):
             r.append( chr(random.randrange(0,256)) )
        data = "".join(r)
      
        Frame = Framing.SimpleFrame(50,data)
        result = str(Frame)
        self.assertEqual(result, "50 100\n"+str(data))

    def test_tuple2string_6(self):
        "SimpleFrame.__str__ - Random data of random length as the data part of the tuple succeeds"
        import random
        length = random.randrange(100,200)
        r = []
        for x in xrange(length):
             r.append( chr(random.randrange(0,256)) )
        data = "".join(r)
      
        Frame = Framing.SimpleFrame(50,data)
        result = str(Frame)
        self.assertEqual(result, "50 "+str(length)+"\n"+str(data))

    def test_tuple2string_7(self):
        "SimpleFrame.__str__ - Completely random frame"
        import random
        length = random.randrange(100,200)
        r = []
        for x in xrange(length):
             r.append( chr(random.randrange(0,256)) )
        data = "".join(r)

        stamp = random.randrange(0,200)
      
        Frame = Framing.SimpleFrame(stamp,data)
        result = str(Frame)
        self.assertEqual(result, str(stamp)+ " "+str(length)+"\n"+str(data))

    def test_string2tuple(self):
        "SimpleFrame.fromString - '1 1\\n1' is parsed as (1,'1')"
        result = Framing.SimpleFrame.fromString('1 1\n1')
        self.assertEqual(result, (1,'1') )

    def test_string2tuple_1(self):
        "SimpleFrame.fromString - '1 2\\n11' is parsed as (1,'11')"
        result = Framing.SimpleFrame.fromString('1 2\n11')
        self.assertEqual(result, (1,'11') )

    def test_string2tuple_2(self):
        "SimpleFrame.fromString - '1 2\\n1111' is parsed as (1,'11') -- Corrupt frame!"
        result = Framing.SimpleFrame.fromString('1 2\n1111')
        self.assertEqual(result, (1,'11') )

    def test_string2tuple_4(self):
        "SimpleFrame.fromString - '1 2\\n' causes exception to be thrown - Corrupt frame!"
        try:
             result = Framing.SimpleFrame.fromString('1 2\n')
             self.fail("Should have died")
        except Framing.CorruptFrame:
           # Success
           pass

    def test_tuple2string_string2tuple_roundtrip_1(self):
        "SimpleFrame.__str__, Framing.SimpleFrame.fromString - roundtrip for (1,'1') succeeds"
        original = (1,'1')
        Frame = Framing.SimpleFrame(*original)
        FrameForWire = str(Frame)
        result = Framing.SimpleFrame.fromString(FrameForWire)
        self.assertEqual(original, result, "passed through unchanged")

    def test_tuple2string_string2tuple_roundtrip_2(self):
        "SimpleFrame.__str__, Framing.SimpleFrame.fromString - roundtrip for (50,'1111') succeeds"
        original = (50,'1111')
        Frame = Framing.SimpleFrame(*original)
        FrameForWire = str(Frame)
        result = Framing.SimpleFrame.fromString(FrameForWire)
        self.assertEqual(original, result, "passed through unchanged")

    def test_tuple2string_string2tuple_roundtrip_3(self):
        "SimpleFrame.__str__, Framing.SimpleFrame.fromString - roundtrip for random data, frame id 50 succeeds"
        import random
        length = random.randrange(100,200)
        r = []
        for x in xrange(length):
             r.append( chr(random.randrange(0,256)) )
        data = "".join(r)
        original = (50,data)
        Frame = Framing.SimpleFrame(*original)
        FrameForWire = str(Frame)
        result = Framing.SimpleFrame.fromString(FrameForWire)
        self.assertEqual(original, result, "passed through unchanged")

    def test_tuple2string_string2tuple_roundtrip_4(self):
        "SimpleFrame.__str__, Framing.SimpleFrame.fromString - roundtrip for random data, random frame id succeeds"
        import random
        length = random.randrange(100,200)
        r = []
        for x in xrange(length):
             r.append( chr(random.randrange(0,256)) )
        data = "".join(r)
        stamp = random.randrange(0,200)
      
        original = (stamp,data)

        Frame = Framing.SimpleFrame(*original)
        FrameForWire = str(Frame)
        result = Framing.SimpleFrame.fromString(FrameForWire)
        self.assertEqual(original, result, "passed through unchanged")

def makeTestCase(klass):
    class Component_ShutdownTests(unittest.TestCase):
        def test_smokeTest2(self):
            import random
            X = klass()
            X.activate()
            for i in xrange(random.randrange(0,2000)):
                try:
                    X.next()
                except StopIteration:
                    self.fail("Component should run until told to stop")

        def test_smokeTest3(self):
            # NOTE: This test is actually satisfied if no body to the component is put in place
            import random
            X = klass()
            X.activate()
            X._deliver(producerFinished(),"control")
            componentExit = False
            for i in xrange(random.randrange(0,2000)):
                try:
                    X.next()
                except StopIteration:
                    componentExit = True
                    break
            if not componentExit:
                self.fail("When sent a shutdown message, the component should shutdown")

        def test_smokeTest4(self):
            import random
            X = klass()
            X.activate()
            X._deliver("BINGLE","control")
            componentExit = False
            for i in xrange(random.randrange(0,2000)):
                try:
                    X.next()
                except StopIteration:
                    componentExit = True
                    break
            if componentExit:
                self.fail("Sending a random message to the control box should not cause a shutdown")

        def test_smokeTest5(self):
            import random
            X = klass()
            X.activate()
            shutdown_message = producerFinished()
            X._deliver(shutdown_message,"control")

            componentExit = False
            for i in xrange(random.randrange(0,2000)):
                try:
                    X.next()
                except StopIteration:
                    componentExit = True
                    break
            try:
                Y = X._collect("signal")
                self.assertEqual(shutdown_message, Y)
            except IndexError:
                self.fail("Shutdown Message should be passed on")
    return Component_ShutdownTests


class FramingComponent_Tests(unittest.TestCase):
    def test_smokeTest(self):
        X = Framing.Framer()
        X.activate()

    def test_marshalling(self):
        message = (1,'1')
        expect = str(Framing.SimpleFrame(*message))
        X = Framing.Framer()
        X.activate()
        X._deliver(message, "inbox")
        for i in xrange(20): # More than sufficient cycles (should be lots less!)
            X.next()
        result = X._collect("outbox")
        self.assertEqual(expect, result)

    def test_marshalling_sequence(self):
        X = Framing.Framer()
        X.activate()
        for i in xrange(100):
            message = (i,str(i))
            expect = str(Framing.SimpleFrame(*message))
            X._deliver(message, "inbox")
            for i in xrange(20): # More than sufficient cycles (should be lots less!)
                X.next()
            result = X._collect("outbox")
            self.assertEqual(expect, result)

class DeFramingComponent_Tests(unittest.TestCase):
    def test_smokeTest(self):
        X = Framing.DeFramer()
        X.activate()

    def test_demarshalling(self):
        original = (1,'1')
        message = str(Framing.SimpleFrame(*original))
        X = Framing.DeFramer()
        X.activate()
        X._deliver(message, "inbox")
        for i in xrange(20): # More than sufficient cycles (should be lots less!)
            X.next()
        result = X._collect("outbox")
        self.assertEqual(original, result)

    def test_demarshalling_sequence(self):
        X = Framing.DeFramer()
        X.activate()
        for i in xrange(100):
            original = (i,str(i))
            message = str(Framing.SimpleFrame(*original))
            X._deliver(message, "inbox")
            for i in xrange(20): # More than sufficient cycles (should be lots less!)
                X.next()
            result = X._collect("outbox")
            self.assertEqual(original, result)

def chunked_datasource():
    while 1:
        yield "XXXXXXXXXXXXXXXXXXXXXXXX"
        for i in xrange(1000):
            yield str(i)

FramerMarshall = makeTestCase(Framing.Framer)
FramerDeMarshall = makeTestCase(Framing.DeFramer)
DataChunkerBasics = makeTestCase(Framing.DataChunker)
DataDeChunkerBasics = makeTestCase(Framing.DataDeChunker)

class DataChunker_test(unittest.TestCase):
    def test_smokeTest(self):
        X = Framing.DataChunker()
        X.activate()
        
    def test_makeChunk(self):
        message = "1234567890qwertyuiopasdfghjklzxcvbnm\n"*20
	syncmessage = "XXXXXXXXXXXXXXXXXXXXXXX"
        X = Framing.DataChunker(syncmessage=syncmessage)
        X.activate()
        X._deliver(message, "inbox")
        for i in xrange(20): # More than sufficient cycles (should be lots less!)
            X.next()
        result = X._collect("outbox")
	result_start = result[:len(syncmessage)]
	result_message = result[len(syncmessage):]

	self.assertEqual(message, result_message)
	self.assertEqual(syncmessage, result_start)

    def test_makeChunk_oneSync(self):
	syncmessage = "XXXXXXXXXXXXXXXXXXXXXXX"
        message = "1234567890qwertyuiopasdfghjklzxcvbnm\n"*10
        message += syncmessage
        message += "1234567890qwertyuiopasdfghjklzxcvbnm\n"*10
        X = Framing.DataChunker(syncmessage=syncmessage)
        X.activate()
        X._deliver(message, "inbox")
        for i in xrange(20): # More than sufficient cycles (should be lots less!)
            X.next()
        result = X._collect("outbox")

	result_message = result[len(syncmessage):]
        index = result_message.find(syncmessage)
        self.assertEqual(-1, index, "Should not be able to find the syncmessage in the chunked version")


class DataDeChunker_test(unittest.TestCase):
    def makeBasicChunk(self, message, syncmessage):
        X = Framing.DataChunker(syncmessage=syncmessage)
        X.activate()
        X._deliver(message, "inbox")
        for i in xrange(20): # More than sufficient cycles (should be lots less!)
            X.next()
        result = X._collect("outbox")
        return result

    def test_DeChunkFullChunk(self):
        message = "1234567890qwertyuiopasdfghjklzxcvbnm\n"*20
	syncmessage = "XXXXXXXXXXXXXXXXXXXXXXX"
        chunk = self.makeBasicChunk(message, syncmessage)
        X = Framing.DataDeChunker(syncmessage=syncmessage)
	X.activate()
	X._deliver(message, "inbox")
	for i in xrange(20): # More than sufficient cycles (should be lots less...)
		X.next()
	result = X._collect("outbox")
 	self.assertEqual(result, message)

    def test_DeChunkFullChunk_1(self):
	syncmessage = "XXXXXXXXXXXXXXXXXXXXXXX"
        message = "1234567890qwertyuiopasdfghjklzxcvbnm\n"*10
        message += syncmessage
        message += "1234567890qwertyuiopasdfghjklzxcvbnm\n"*10
        chunk = self.makeBasicChunk(message, syncmessage)
        X = Framing.DataDeChunker(syncmessage=syncmessage)
	X.activate()
	X._deliver(message, "inbox")
	for i in xrange(20): # More than sufficient cycles (should be lots less...)
		X.next()
	result = X._collect("outbox")
 	self.assertEqual(result, message)


    def test_DeChunkFullChunk_2(self):
	syncmessage = "XXXXXXXXXXXXXXXXXXXXXXX"
        message = "123\\S\4567\\890qwer\\\tyuiopasdfg\\\\hjklzxcvbnm\n"*10
        message += syncmessage
        message += "1234567890q\\Swertyuiopasdfghjklzxcvbnm\n"*10
        chunk = self.makeBasicChunk(message, syncmessage)
        X = Framing.DataDeChunker(syncmessage=syncmessage)
	X.activate()
	X._deliver(message, "inbox")
	for i in xrange(20): # More than sufficient cycles (should be lots less...)
		X.next()
	result = X._collect("outbox")
 	self.assertEqual(result, message)

    def blocks(self, someData, blocksize=20):
        data = someData
        while len(data) > 20:
           yield data[:20]
           data = data[20:]
        yield data
        

    def test_DeChunk_SingleChunk_ManyBlocks(self):
        "The dechunker handles taking a chunk that's in many blocks and putting it back together"
	syncmessage = "XXXXXXXXXXXXXXXXXXXXXXX"
        message = "123\\S\4567\\890qwer\\\tyuiopasdfg\\\\hjklzxcvbnm\n"*10
        message += syncmessage
        message += "1234567890q\\Swertyuiopasdfghjklzxcvbnm\n"*10
        chunk = self.makeBasicChunk(message, syncmessage)
        X = Framing.DataDeChunker(syncmessage=syncmessage)
	X.activate()
	for block in self.blocks(chunk):
	    X._deliver(block, "inbox")
	for i in xrange(20): # More than sufficient cycles (should be lots less...)
		X.next()
	result = X._collect("outbox")
 	self.assertEqual(result, message)
 	self.fail("Test not implemented??")



if 0:
  class default_test(unittest.TestCase):
    def test_marshalling(self):
        X = Framing.Framer()
        self.fail("Test Not Implemented")

if __name__=="__main__":
    unittest.main()







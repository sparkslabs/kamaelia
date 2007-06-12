#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
# Full coverage testing of the NullPayloadRTP module.
#

# Test the module loads
import unittest
import sys ; sys.path.append("..")
import Kamaelia.NullPayloadRTP
NullPayloadRTP = Kamaelia.NullPayloadRTP

class NullPayloadRTP_Test(unittest.TestCase):
   def test_packLengthAsString(self):
      """Check that encoding a number as 4 ascii digits functions"""
      packLengthAsString=NullPayloadRTP.packLengthAsString
      ABCD = (ord("A")<<24) + (ord("B")<<16) +(ord("C")<<8) + ord("D")
      self.assertEqual(packLengthAsString(ABCD), "ABCD")

   def test_init_MinArgs(self):
      """Check that __init__ with minimal args works (smoke test)"""
      P = NullPayloadRTP.NullPayloadPreFramer("dummy")
      self.assertNotEqual(None,P, "Initialisation")
      self.assertEqual(P.sourcename,"dummy")
      self.assertEqual(P.sourcebitrate,65536)
      self.assertEqual(P.sourceoctetrate, 8192)
      self.assertEqual(P.chunksize, 1400)
      self.assertEqual(P.currentchunk, "")
      self.assertEqual(P.timestamp, 0)

   def test_init_AllArgs(self):
      """Smoke test with all user definable arguments"""
      P = NullPayloadRTP.NullPayloadPreFramer("dummy", sourcebitrate=32768,chunksize=700)
      self.assertNotEqual(None,P, "Initialisation")
      self.assertEqual(P.sourcename,"dummy")
      self.assertEqual(P.sourcebitrate,32768)
      self.assertEqual(P.sourceoctetrate, 4096.0)
      self.assertEqual(P.chunksize, 700)
      self.assertEqual(P.currentchunk, "")
      self.assertEqual(P.timestamp, 0)
      self.assertEqual(P._dataSent, 0)

   def test_initialiseComponent(self):
      """Check that created components initialise correctly"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      self.assert_(P.initialiseComponent())

   def test_updateTimestamp(self):
      """Check that updating the timestamp functions correctly, one off and cumulatively"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      bytesSent = 0
      self.assert_(P.timestamp==0)

      bytesToSend = "A"*(int(P.sourceoctetrate))
      P.updateTimestamp(bytesToSend)
      bytesSent += len(bytesToSend)
      self.assertEqual(P._dataSent, bytesSent)
      self.assertEqual(P.timestamp, bytesSent/P.sourceoctetrate)

      for i in [2,4,8,16,32,64]:
         bytesToSend = "A"*(int(P.sourceoctetrate/i))
         P.updateTimestamp(bytesToSend)
         bytesSent += len(bytesToSend)
         self.assertEqual(P._dataSent, bytesSent)
         self.assertEqual(P.timestamp, bytesSent/P.sourceoctetrate)

   def test_makeChunk_FullCase(self):
      """Check that creating a chunk works, including length marker"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      testString="A" * ((1<<24) + (2<<16) +(3<<8) + 4)
      self.assertEqual(len(testString), ((1<<24) + (2<<16) +(3<<8) + 4) )
      chunk = P.makeChunk(testString)
      self.assertNotEqual(chunk, None)
      self.assertEqual(len(chunk), len(testString)+4)
      self.assertEqual(chunk[0:4], chr(1)+chr(2)+chr(3)+chr(4))

   def test_makeChunk_EmptyCase(self):
      """Check that empty chunks are created correctly"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      testString="A" * ((0<<24) + (0<<16) +(0<<8) + 0)
      self.assertEqual(len(testString), ((0<<24) + (0<<16) +(0<<8) + 0) )
      chunk = P.makeChunk(testString)
      self.assertNotEqual(chunk, None)
      self.assertEqual(len(chunk), len(testString)+4)
      self.assertEqual(len(chunk), 4)
      self.assertEqual(chunk[0:4], chr(0)+chr(0)+chr(0)+chr(0))

   def test_makeChunk_PartialCase_Little(self):
      """Check that creating a chunk with small payload (smaller than 65536 octets) functions"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      testString="A" * ((0<<24) + (0<<16) +(3<<8) + 4)
      self.assertEqual(len(testString), ((0<<24) + (0<<16) +(3<<8) + 4) )
      chunk = P.makeChunk(testString)
      self.assertNotEqual(chunk, None)
      self.assertEqual(len(chunk), len(testString)+4)
      self.assertEqual(chunk[0:4], chr(0)+chr(0)+chr(3)+chr(4))

   def test_makeChunk_PartialCase_Large(self):
      """Check that a chunk with a size requiring only high end bits works"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      testString="A" * ((1<<24) + (2<<16) +(0<<8) + 0)
      self.assertEqual(len(testString), ((1<<24) + (2<<16) +(0<<8) + 0) )
      chunk = P.makeChunk(testString)
      self.assertNotEqual(chunk, None)
      self.assertEqual(len(chunk), len(testString)+4)
      self.assertEqual(chunk[0:4], chr(1)+chr(2)+chr(0)+chr(0))

   def test_sendCurrentChunk_EmptyNonPartial(self):
      """Check that sending an empty, non-partial chunk works"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      self.assertEqual(P.sendCurrentChunk(), 0,     "Sending empty, non-partial should result 0")

   def test_sendCurrentChunk_NonPartialSendOne(self):
      """Check that sending one non-partial chunk works"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P.currentchunk = "A"*(P.chunksize+1)

      self.assertNotEqual(P.sendCurrentChunk(),0,    "Sending valid chunk should result in non-zero")
      self.assertEqual(len(P.currentchunk), 1,       "Incorrectly Trimmed off 'chunksize' octets")
      self.assertEqual(len(P.outboxes['output']), 1, "Should have 1 result in output")

      theOutput = P.outboxes['output'][-1]   # Take the last thing to be .appended
      self.assertEqual(theOutput.__class__, tuple,    "The output should be a tuple")
      self.assertEqual(len(theOutput), 2,             "The output should be a 2-tuple")

      timestamp, dataSent = theOutput
      self.assertEqual(len(dataSent),P.chunksize+4,   "The chunk should be chunksize + 4")
      self.assertEqual(dataSent[4:],"A"*P.chunksize,  "The data should be a 'chunksize' num of A's")

      expectedLength = P.chunksize
      expectedLengthAsString = NullPayloadRTP.packLengthAsString(expectedLength)
      self.assertEqual(expectedLengthAsString, dataSent[0:4], "Length has been packed as 4 octets")

      self.assertEqual(timestamp, 0,                               "The timestamp should be _zero_")
      self.assertEqual(P.timestamp, P.chunksize/P.sourceoctetrate, "The next timestamp we get should be 1 chunk later")

   def test_sendCurrentChunk_NonPartialSendTwo(self):
      """Check that sending one non-partial chunks works"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P.currentchunk = "A"*(P.chunksize*2+1)

      self.assertNotEqual(P.sendCurrentChunk(),0,    "Sending valid chunk should result in non-zero")
      self.assertNotEqual(P.sendCurrentChunk(),0,    "Sending valid chunk should result in non-zero")
      self.assertEqual(len(P.currentchunk), 1,       "Incorrectly Trimmed off 'chunksize' octets")
      self.assertEqual(len(P.outboxes['output']), 2, "Should have 2 results in output")

      theOutput = P.outboxes['output'][-1]   # Take the last thing to be .appended
      self.assertEqual(theOutput.__class__, tuple,    "The output should be a tuple")
      self.assertEqual(len(theOutput), 2,             "The output should be a 2-tuple")

      timestamp, dataSent = theOutput
      self.assertEqual(len(dataSent),P.chunksize+4,   "The chunk should be chunksize + 4")
      self.assertEqual(dataSent[4:],"A"*P.chunksize,  "The data should be a 'chunksize' num of A's")

      expectedLength = P.chunksize
      expectedLengthAsString = NullPayloadRTP.packLengthAsString(expectedLength)
      self.assertEqual(expectedLengthAsString, dataSent[0:4], "Length has been packed as 4 octets")

      self.assertEqual(timestamp, P.chunksize/P.sourceoctetrate,     "The timestamp should be 1 chunk period")
      self.assertEqual(P.timestamp, P.chunksize*2/P.sourceoctetrate, "The next timestamp we get should be 1 chunk later")

   def test_sendCurrentChunk_Partial_NonEmpty(self):
      """Check that sending a partial chunks works"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      sentData = "A"*(P.chunksize/2)
      P.currentchunk = sentData

      self.assertNotEqual(P.sendCurrentChunk(sendpartial=True),0, "Sending valid chunk should result in non-zero")
      self.assertEqual(len(P.currentchunk), 0,       "Remainder of chunk should be empty")
      self.assertEqual(len(P.outboxes['output']), 1, "Should have 1 results in output")

      theOutput = P.outboxes['output'][-1]   # Take the last thing to be .appended
      self.assertEqual(theOutput.__class__, tuple,    "The output should be a tuple")
      self.assertEqual(len(theOutput), 2,             "The output should be a 2-tuple")

      timestamp, dataSent = theOutput
      self.assertEqual(len(dataSent),len(sentData)+4,   "The chunk should be sent data size + 4")
      self.assertEqual(dataSent[4:],sentData,           "The data should be the same as our original")

      expectedLength = len(sentData)
      expectedLengthAsString = NullPayloadRTP.packLengthAsString(expectedLength)
      self.assertEqual(expectedLengthAsString, dataSent[0:4], "Length has been packed as 4 octets")

      self.assertEqual(timestamp, 0,                                 "The timestamp should be 0")
      self.assertEqual(P.timestamp, len(sentData)/P.sourceoctetrate, "The next timestamp we get should be the time of the partial chunk later")

   def test_sendCurrentChunk_Partial_Empty(self):
      """Check that trying to send an empty chunk marked partial works"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      sentData = ""
      P.currentchunk = sentData

      self.assertNotEqual(P.sendCurrentChunk(sendpartial=True),0, "Sending valid chunk should result in non-zero")
      self.assertEqual(len(P.currentchunk), 0,       "Remainder of chunk should be empty")
      self.assertEqual(len(P.outboxes['output']), 1, "Should have 1 results in output")

      theOutput = P.outboxes['output'][-1]   # Take the last thing to be .appended
      self.assertEqual(theOutput.__class__, tuple,    "The output should be a tuple")
      self.assertEqual(len(theOutput), 2,             "The output should be a 2-tuple")

      timestamp, dataSent = theOutput
      self.assertEqual(len(dataSent),len(sentData)+4,   "The chunk should be sent data size + 4")
      self.assertEqual(dataSent[4:],sentData,           "The data should be the same as our original")

      expectedLength = len(sentData)
      expectedLengthAsString = NullPayloadRTP.packLengthAsString(expectedLength)
      self.assertEqual(expectedLengthAsString, dataSent[0:4], "Length has been packed as 4 octets")

      self.assertEqual(timestamp, 0,                                 "The timestamp should be 0")
      self.assertEqual(P.timestamp, len(sentData)/P.sourceoctetrate, "The next timestamp we get should be the time of the partial chunk later")

   def test_handleShutdown_NoData(self):
      """Check that chuntting down the component with no more data to send functions correctly"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P.currentchunk=""
      self.assertEqual(P.handleShutdown(), 0, "Result should be zero indicating no more data to send")

   def test_handleShutdown_OneChunk(self):
      """Check that chuntting down the component with one more chunk to send functions correctly"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P.currentchunk="A"*P.chunksize
      self.assertEqual(P.handleShutdown(), 2, "Result should be non-zero indicating more data to send")
      self.assertEqual(len(P.outboxes['output']), 1, "Should have 1 result in output")
      self.assertEqual(P.handleShutdown(), 0, "Result should be zero indicating no more data to send")
      self.assertEqual(len(P.outboxes['output']), 1, "Should have 1 result in output")

   def test_handleShutdown_TwoChunks(self):
      """Check that chuntting down the component with two more chunks to send functions correctly"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P.currentchunk="A"*(P.chunksize*2)
      self.assertEqual(P.handleShutdown(), 2, "Result should be non-zero indicating more data to send")
      self.assertEqual(len(P.outboxes['output']), 1, "Should have 1 result in output")
      self.assertEqual(P.handleShutdown(), 2, "Result should be zero indicating no more data to send")
      self.assertEqual(len(P.outboxes['output']), 2, "Should have 2 results in output")
      self.assertEqual(P.handleShutdown(), 0, "Result should be zero indicating no more data to send")
      self.assertEqual(len(P.outboxes['output']), 2, "Should have 2 results in output")

   def test_handleShutdown_N_whole_Chunks(self):
      """Check that chuntting down the component with several chunks to send functions correctly"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      chunkCount = 0
      chunksSent = 5
      P.currentchunk="A"*(P.chunksize*chunksSent)
      while P.handleShutdown():
         chunkCount += 1
         self.assertEqual(len(P.outboxes['output']), chunkCount , "Should have "+(str(chunkCount))+" result(s) in output")
      self.assertEqual(P.currentchunk, "")

   def test_handleShutdown_N_partial_Chunks(self):
      """Check that chuntting down the component with several partial chunks to send functions correctly"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      chunkCount = 0
      chunksSent = 5
      P.currentchunk="A"*(P.chunksize*chunksSent+1)
      while P.handleShutdown():
         chunkCount += 1
         self.assertEqual(len(P.outboxes['output']), chunkCount , "Should have "+(str(chunkCount))+" result(s) in output")
      self.assertEqual(P.currentchunk, "")
      lastChunk = P.outboxes['output'][-1]
      (ts,chunk) = lastChunk
      lastData = chunk[4:]
      self.assertEqual("A",lastData)

   def test_handleControl_noMessage(self):
      """Check that handling the control messages functions correctly with no messages"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      self.assertEqual(P.handleControl(), False, "With no messages, should return False (don't quit)")

   def test_handleControl_noShutdownMessage(self):
      """Check that handling the control messages functions correctly with a junk message (throws it away)"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P._deliver("ignore","control")
      lengthBefore = len(P.inboxes['control'])
      self.assertEqual(P.handleControl(), False, "With no shutdown messages, should return False (don't quit)")
      lengthAfter = len(P.inboxes['control'])
      self.assert_(lengthAfter == lengthBefore -1, "Ignored message has been consumed")

   def test_handleControl_ShutdownMessage(self):
      """Check that handling the control messages functions correctly with a shutdown message"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P._deliver("shutdown","control")
      lengthBefore = len(P.inboxes['control'])
      self.assertEqual(P.handleControl(), True, "With no shutdown messages, should return False (don't quit)")
      lengthAfter = len(P.inboxes['control'])
      self.assert_(lengthAfter == lengthBefore -1, "Processed message has been consumed")

   def test_CloseDownComponent(self):
      """Check that closing down the component doesn't raise an assert"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      P.closeDownComponent() # Does nothing at present. Here to handle asserts if valid later

   def test_mainBody(self):
      """Test the mainbody of the NullPayloadRTP preframer"""
      P=NullPayloadRTP.NullPayloadPreFramer("dummy")
      self.assert_(P.mainBody(), "In the just initialised, quiescent state this should return a true value")
      self.assertEqual(P.mainBody(), 5,"In fact should go all the way through the loop body")

      P.currentchunk = "A"*P.chunksize
      self.assertEqual(P.mainBody(), 1,"Should send the chunk and return")
      self.assertEqual(len(P.outboxes["output"]), 1, "There should be one result")

      P._deliver("A"*(P.chunksize+10),"recvsrc")
      self.assertEqual(len(P.inboxes["recvsrc"]), 1, "There should be one message to recieve")
      self.assertEqual(P.mainBody(), 3,"Should collect the chunk and return")
      self.assertEqual(len(P.inboxes["recvsrc"]), 0, "There should be no messages to recieve")
      self.assertEqual(P.mainBody(), 1,"Should send the chunk and return")
      self.assertEqual(len(P.outboxes["output"]), 2, "There should be two results")

      self.assertEqual(P.currentchunk, "A"*10, "There should be some data left, but not a whole chunk")
      self.assertEqual(P.mainBody(), 5,        "We are waiting for data")

      P._deliver("A"*(P.chunksize+10),"recvsrc")
      self.assertEqual(len(P.inboxes["recvsrc"]), 1, "There should be one message to recieve")
      self.assertEqual(P.mainBody(), 3,"Should collect the chunk and return")
      self.assertEqual(len(P.inboxes["recvsrc"]), 0, "There should be no messages to recieve")
      self.assertEqual(P.mainBody(), 1,"Should send the chunk and return")
      self.assertEqual(len(P.outboxes["output"]), 3, "There should be three results")

      self.assertEqual(P.currentchunk, "A"*20, "There should be some data left, but not a whole chunk - two fragments in fact")
      self.assertEqual(P.mainBody(), 5,        "We are waiting for data")

      P._deliver("garbage", "control")
      self.assertEqual(P.mainBody(), 4,    "Process the garbage control message")
      self.assert_(not P.quitFlag,         "It shouldn't make us quit")

      P._deliver("shutdown", "control")
      self.assertEqual(P.mainBody(), 4,    "Process the garbage control message")
      self.assert_(P.quitFlag,             "It should make us quit")

      self.assertEqual(P.mainBody(), 2,    "We should have just sent a message during a shutdown phase")
      self.assertEqual("",P.currentchunk,  "The last partial chunk should have been sent")
      self.assertEqual(P.mainBody(), 0,    "We are shutdown, and do no work")
      self.assertEqual(P.mainBody(), 0,    "We are shutdown, and do no work, however many times called")
      self.assertEqual(P.mainBody(), 0,    "We are shutdown, and do no work, however many times called")

#
# assert test_packLengthAsString(), "test_packLengthAsString FAILED"
# print "test_packLengthAsString OK"

if __name__=="__main__":
   unittest.main()


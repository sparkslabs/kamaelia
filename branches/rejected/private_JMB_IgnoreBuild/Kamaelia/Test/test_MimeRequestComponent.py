#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Actually based on glass/white box approach at present for logic checking.
#
# The exception here is the mainBody function.
#
# Can remove tests that check internal behaviour at a later point.
#

# Test the module loads
import unittest
import sys ; sys.path.append("..")
import Kamaelia.MimeRequestComponent as MimeRequestComponent


class mimeObject_Test(unittest.TestCase):
   def test_init_empty(self):
       """Test creating an empty mimeObject"""
       obj = MimeRequestComponent.mimeObject()
       self.assert_(obj is not None, "Smoke Test")
       self.assert_(obj.header=={}, "The header should be empty")
       self.assert_(obj.body=="", "The body should be empty")

   def test_init_emptyTwice(self):
       """Check that creating 2 empty mimeObjects does not create duplicate references"""
       obj1 = MimeRequestComponent.mimeObject()
       obj2 = MimeRequestComponent.mimeObject()
       self.assert_(obj1.header is not obj2.header, "Dictionaries, even empty, should not be shared")
       self.assert_(obj1.body is obj2.body, "Strings are immutable hence ''==''")

   def test_init_basicNormal(self):
       """Check creating a mimeObject with typical call values"""
       aHeader = {"a" : ["A", "1"] , "B": ["B", "1"] }
       theBody = "mime body"
       obj = MimeRequestComponent.mimeObject(header=aHeader, body=theBody)
       self.assert_(obj.header==aHeader, "Header have same value")
       self.assert_(obj.header is not aHeader, "Header should be copied, not a reference to the original")
       self.assert_(obj.body==theBody, "The body of should be the same as the original")
       self.assert_(obj.body is theBody, "Strings are immutable, so the body should *be* the same as our argument!")

   def test_init_basicNormalTwiceDifferentSources(self):
       """Check that creating 2 non-empty mimeObjects with differing source does not create duplicate references or overlapping objects"""
       aHeader = {"a" : ["A", "1"] , "B": ["B", "1"] }
       theBody = "mime body"
       bHeader = {"a" : ["A", "1"] , "B": ["B", "1"] }
       anotherBody = "mime body"

       self.assert_(theBody is anotherBody, "Due to immutable strings")
       self.assert_(aHeader is not bHeader, "Due to dicts being mutable")

       obj1 = MimeRequestComponent.mimeObject(header=aHeader, body=theBody)
       obj2 = MimeRequestComponent.mimeObject(header=bHeader, body=anotherBody)

       self.assert_(obj1.header==obj2.header, "Header have same value")
       self.assert_(obj1.header is not obj2.header, "Shouldn't be the same object...")
       self.assert_(obj1.body==obj2.body, "The body of both should be the same")
       self.assert_(obj1.body is obj2.body, "Strings are immutable, so the body should *be* the same as our argument!")

   def test_init_basicNormalTwiceSameSource(self):
       """Check that creating 2 non-empty mimeObjects with the same source does not create duplicate references or overlapping objects"""
       aHeader = {"a" : ["A", "1"] , "B": ["B", "1"] }
       theBody = "mime body"

       obj1 = MimeRequestComponent.mimeObject(header=aHeader, body=theBody)
       obj2 = MimeRequestComponent.mimeObject(header=aHeader, body=theBody)
       self.assert_(obj1 is not obj2, "The two objects should be different objects")

       self.assert_(obj1.header==obj2.header,       "Headers have same value")
       self.assert_(obj1.header is not obj2.header, "Shouldn't be the same object...")
       self.assert_(obj1.body==obj2.body)
       self.assert_(obj1.body is obj2.body, "Strings are immutable, so the body should *be* the same as our argument!")

   def test_str_Empty(self):
       """Check the str() of the empty object"""
       obj = MimeRequestComponent.mimeObject()
       self.assert_(str(obj) == '\n')

   def test_str_Basic(self):
       """Check the str() of a normal non-empty object"""
       aHeader = {"a" : ["A", "1"] , "B": ["B", "1"] }
       theBody = "mime body"
       obj = MimeRequestComponent.mimeObject(aHeader, theBody)
       self.assert_(str(obj) == 'A: 1\nB: 1\n\nmime body')

class MimeRequestComponent_Test(unittest.TestCase):
   def test_init(self):
      """Smoke Test for MimeRequestComponent"""
      C=MimeRequestComponent.MimeRequestComponent()
      self.assert_(C is not None, "Smoke test")
      self.assertEqual(C.header,{}, "Smoke header")
      self.assertEqual(C.requestLineRead, 0, "Smoke header")
      self.assertEqual(C.currentLineRead, 0, "Smoke header")
      self.assertEqual(C.seenEndHeader, 0, "Smoke header")
      self.assertEqual(C.currentLine, '', "Smoke header")
      self.assertEqual(C.currentBytes, '', "Smoke header")
      self.assertEqual(C.requestLine, '', "Smoke header")
      self.assertEqual(C.stillReading, 1, "Smoke header")
      self.assertEqual(C.needData, 0, "Smoke header")
      self.assertEqual(C.gotRequest, 0, "Smoke header")
      self.assertEqual(C.body, '', "Smoke header")
      self.assertEqual(C.step, 0, "Smoke header")

   def test_initialiseComponent(self):
      """Smoke test for initialise component - simply shouldn't raise an exception or return a value"""
      C=MimeRequestComponent.MimeRequestComponent()
      self.assert_(C.initialiseComponent() is None)

   def test_nextLine_noData(self):
      """Internal Diagnostic: Reading data from input (no data ready)"""
      C=MimeRequestComponent.MimeRequestComponent()
      self.assertEqual(C.nextLine(), (0,""), "Have no data ready, and no data")

   def test_nextLine_junkData(self):
      """Internal Diagnostic: Reading data from input (junk - non string - data ready)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver((None,), "inbox")
      self.assertEqual(C.nextLine(), (0,""), "Have no data ready, and no data")

   def test_nextLine_Data_emptyString(self):
      """Internal Diagnostic: Reading data from input (Empty string - data ready)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("", "inbox")
      self.assertEqual(C.nextLine(), (0,""), "Have no data ready, and no data")

   def test_nextLine_Data_nonEmptyStringNoEOL(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, no EOL)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data", "inbox")
      self.assertEqual(C.nextLine(), (0,""), "Have no data ready, and no data")

   def test_nextLine_Data_nonEmptyString_UnixFile_EOL(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, Unix EOL)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\n", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")

   def test_nextLine_Data_nonEmptyString_UnixFile_EOLMore(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, Unix EOL followed by data)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\nSome more data", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.currentBytes, "Some more data", "Still data in buffer")

   def test_nextLine_Data_nonEmptyString_UnixFile_TwoEOL(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, 2 Unix EOL)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\nMore Random Data\n", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.nextLine(), (1,"More Random Data"), "Have data ready, and data")

   def test_nextLine_Data_nonEmptyString_UnixFile_TwoEOLMore(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, 2 Unix EOL followed by data)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\nMore Random Data\nSome more data", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.nextLine(), (1,"More Random Data"), "Have data ready, and data")
      self.assertEqual(C.currentBytes, "Some more data", "Still data in buffer")

   def test_nextLine_Data_nonEmptyString_Network_EOL(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, Network EOL)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\r\n", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.currentBytes, "", "No data in buffer")

   def test_nextLine_Data_nonEmptyString_Network_EOLMore(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, Network EOL followed by data)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\r\nSome more data", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.currentBytes, "Some more data", "Still data in buffer")

   def test_nextLine_Data_nonEmptyString_Network_TwoEOL(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, 2 Network EOL)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\r\nMore Random Data\r\n", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.nextLine(), (1,"More Random Data"), "Have data ready, and data")
      self.assertEqual(C.currentBytes, "", "No data in buffer")

   def test_nextLine_Data_nonEmptyString_Network_TwoEOLMore(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, 2 Network EOL followed by data)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\r\nMore Random Data\r\nSome more data", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.nextLine(), (1,"More Random Data"), "Have data ready, and data")
      self.assertEqual(C.currentBytes, "Some more data", "Still data in buffer")

   def test_nextLine_Data_nonEmptyString_NetworkUnixMixed_TwoEOLMore(self):
      """Internal Diagnostic: Reading data from input (Useful data ready, 2 mixed EOLs followed by data)"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\r\nMore Random Data\nSome more data", "inbox")
      self.assertEqual(C.nextLine(), (1,"Some Random Data"), "Have data ready, and data")
      self.assertEqual(C.nextLine(), (1,"More Random Data"), "Have data ready, and data")
      self.assertEqual(C.currentBytes, "Some more data", "Still data in buffer")

   def test_getRequestLine(self):
      """Internal Diagnostic: Checking reading the first line in the inbox"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\n", "inbox")
      C.getRequestLine()
      self.assertEqual(C.requestLineRead,1)
      self.assertEqual(C.requestLine,"Some Random Data")

   def test_getALine(self):
      """Internal Diagnostic: Checking reading the first line in the inbox"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("Some Random Data\n", "inbox")
      C.getALine()
      self.assertEqual(C.currentLineRead,1)
      self.assertEqual(C.currentLine,"Some Random Data")

   def test_readHeader_validDataOnce(self):
      """Internal Diagnostic: Read header check - One valid field"""
      C=MimeRequestComponent.MimeRequestComponent()
      C.currentLine="From: random@hosts.com"
      C.readHeader()
      self.assertEqual(C.currentLineRead,0)
      self.assertEqual(C.header, {'from': ['From', 'random@hosts.com']}, "Correctly parsed correctly formatted line")
      self.assertEqual(C.currentLine,"", "C.currentLine has been used up")

   def test_readHeader_validDataTwiceSame(self):
      """Internal Diagnostic: Read header check - Test aggregation of repeated fields"""
      C=MimeRequestComponent.MimeRequestComponent()
      C.currentLine="From: random@hosts.com"
      C.readHeader()
      C.currentLine="From: Other@hosts.com"
      C.readHeader()
      self.assertEqual(C.currentLineRead,0)
      self.assertEqual(C.header, {'from': ['From', 'random@hosts.com, Other@hosts.com']}, "Correctly parsed correctly formatted lines")
      self.assertEqual(C.currentLine,"", "C.currentLine has been used up")

   def test_readHeader_validDataTwiceDiff(self):
      """Internal Diagnostic: Read header check - Test aggregation of repeated fields doesn't occur with different fields"""
      C=MimeRequestComponent.MimeRequestComponent()
      C.currentLine="From: random@hosts.com"
      C.readHeader()
      C.currentLine="Form: Other@hosts.com"  ## NB different field. (Whilst odd, consider Referrer and Referer - which one is in HTTP?)
      C.readHeader()
      self.assertEqual(C.currentLineRead,0)
      self.assertNotEqual(C.header, {'from': ['From', 'random@hosts.com, Other@hosts.com']}, "Correctly parsed correctly formatted lines")
      self.assertEqual(C.header, {'from': ['From', 'random@hosts.com'], 'form': ['Form', 'Other@hosts.com']}, "Correctly parsed correctly formatted lines")
      self.assertEqual(C.currentLine,"", "C.currentLine has been used up")

   def test_getData_noData(self):
      """Internal Diagnostic: getData check - check that it correctly accepts data when no data available"""
      C=MimeRequestComponent.MimeRequestComponent()
      before=(C.currentBytes,C.needData, C.inboxes, C.outboxes)
      C.getData()
      after=(C.currentBytes,C.needData, C.inboxes, C.outboxes)
      self.assertEqual(before,after, "No data results in no state change")

   def test_getData_DataAvailable(self):
      """Internal Diagnostic: getData check - check that it correctly accepts data when data available"""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("This is some test data", "inbox")
      C.getData()
      self.assertEqual(C.currentBytes, "This is some test data", "Take the data and store it correctly")
      self.assertEqual(C.needData, 0, "Flag that we've got the data")
      self.assertEqual(C.inboxes["inbox"], [], "Inbox is now empty")

   def test_checkEndOfHeader_noData(self):
      """Internal Diagnostic: End of Header check - with no data of any kind supplied"""
      C=MimeRequestComponent.MimeRequestComponent()
      C.needData=999
      C.checkEndOfHeader()
      self.assertEqual(C.seenEndHeader, 1, "Empty data means end of header")
      self.assertEqual(C.headerlength, 0, "The length of the body in the header is zero, since no content-length header")
      self.assertEqual(C.needData, 0, "Since no content-length header, we don't read any body part. (Value has been changed)")

   def test_checkEndOfHeader_minimalHeader_noData_noNeedData(self):
      """Internal Diagnostic: End of Header check - with Content Length header defined"""
      C=MimeRequestComponent.MimeRequestComponent()
      C.header={"content-length":["Content-Length",1024]}

      self.assert_(C.needData==0)
      C.needData=999
      C.checkEndOfHeader()
      self.assertEqual(C.seenEndHeader, 1, "Empty data means end of header")
      self.assertEqual(C.headerlength, 1024, "The header specifies a body length of 1024")
      self.assertEqual(C.needData, 999, "The value of needData is in fact unchanged")

   def test_checkEndOfHeader_minimalHeader_noData_noContentLength(self):
      """Internal Diagnostic: End of Header check - with no Content Length header"""
      C=MimeRequestComponent.MimeRequestComponent()
      C.header={"length":["Length",1024]}
      C.currentLine = 'Not: Done'
      self.assert_(C.needData==0)
      C.needData=999
      before= (C.needData)
      C.checkEndOfHeader()
      after=(C.needData)
      self.assertEqual(C.seenEndHeader, 0, "Non Empty line means still in header")
      self.assertEqual(before, after, "State is unchanged")
      r=None
      try:
         r =self.headerlength+2
      except AttributeError:
         r="HERE"
      self.assert_(r=="HERE", "r should be set to a non-numeric value due to headerlength not being set")

   def test_handleDataAquisition_noSetup(self):
      """Internal Diagnostic: Data aquisition - with no setup, shouldn't go bang!"""
      C=MimeRequestComponent.MimeRequestComponent()
      self.assertEqual(C.handleDataAquisition(), 1,"Should leave on first section")
      self.assertEqual(C.requestLineRead, 0,  "No request line read")
      self.assertEqual(C.requestLine, "", "No request line data read")
      self.assertEqual(C.handleDataAquisition(), 1, "Again, should leave on first section")
      self.assertEqual(C.requestLineRead, 0,  "No request line read")
      self.assertEqual(C.requestLine, "", "No request line data read")

   def test_handleDataAquisition_ValidRequestProvided_EmptyBody(self):
      """Internal Diagnostic: Data aquisition - full request, empty body."""
      C=MimeRequestComponent.MimeRequestComponent()
      C._deliver("GET http://user:password@127.0.0.1:1234/ HTTP/1.0\n", "inbox")

      self.assertEqual(C.handleDataAquisition(), 1,"Should leave on first section")
      self.assertEqual(1,  C.requestLineRead, "Request line read")
      self.assertEqual("GET http://user:password@127.0.0.1:1234/ HTTP/1.0", C.requestLine, "Request line data read")
      self.assertEqual(2,  C.handleDataAquisition(),"Since the request line has been read, should leave on second section")
      self.assertEqual(0,  C.currentLineRead, "No current line read")
      self.assertEqual("", C.currentLine, "No current line data read")

      C._deliver("A-Header-Field: value\n", "inbox")
      self.assertEqual(2,  C.handleDataAquisition(),"Since request line has been read, should leave on second section")
      self.assertEqual(1,  C.currentLineRead, "Current line read")
      self.assertEqual("A-Header-Field: value", C.currentLine, "Current line data read")

      self.assertEqual(3,  C.handleDataAquisition(),"Current line is valid, and we have data, and we've not seen end of header")
      self.assertEqual(0,  C.currentLineRead, "Current line has been used, means will need to get a line!")
      self.assertEqual("", C.currentLine, "Current line is now empty")
      self.assertEqual(C.header, {'a-header-field': ['A-Header-Field', 'value']}, "Field added, with value")
      self.assertEqual(C.currentBytes, "")

      self.assertEqual(2,  C.handleDataAquisition(),"Processed current data, need to get more")
      self.assertEqual(0,  C.currentLineRead, "No current line read (No data available)")
      self.assertEqual("", C.currentLine, "No current line data read")

      C._deliver("Another-Header-Field: value\n", "inbox")
      self.assertEqual(2,  C.handleDataAquisition(),"Since request line has been read, should leave on second section")
      self.assertEqual(1,  C.currentLineRead, "Current line read")
      self.assertEqual("Another-Header-Field: value", C.currentLine, "Current line data read")

      self.assertEqual(3,  C.handleDataAquisition(),"Current line is valid, and we have data, and we've not seen end of header")
      self.assertEqual(0,  C.currentLineRead, "Current line has been used, means will need to get a line!")
      self.assertEqual("", C.currentLine, "Current line is now empty")
      expectedHeaderDict = {'a-header-field': ['A-Header-Field', 'value'],
                            'another-header-field': ['Another-Header-Field', 'value']}
      self.assertEqual(C.header, expectedHeaderDict, "Field added, with value")
      self.assertEqual(C.currentBytes, "")

      self.assertEqual(2,  C.handleDataAquisition(),"Processed current data, need to get more")
      self.assertEqual(0,  C.currentLineRead, "No current line read (No data available)")
      self.assertEqual("", C.currentLine, "No current line data read")

      endOfHeader = '\n'
      C._deliver(endOfHeader, "inbox")
      self.assertEqual(2,  C.handleDataAquisition(),"Processed current data, got more")
      self.assertEqual(1,  C.currentLineRead, "Current line read")
      self.assertEqual("", C.currentLine, "Current line data read - empty")

      self.assertEqual(None, C.handleDataAquisition(), "Header has been read, with no content-length - and hence no body should be read, so return code is None to signify no more data to read")
      self.assertEqual(1,C.seenEndHeader, "Whether the header's been seen or not is correctly noted")


      #self.assertEqual(None,  C.handleDataAquisition(),"Current line is valid, and we have data, and we've not seen end of header")
      #self.assertEqual(4,  C.handleDataAquisition(),"Current line is valid, and we have data, and we've not seen end of header")
      #self.assertEqual(0,  C.currentLineRead, "Current line has been used")
      #self.assertEqual("", C.currentLine, "Current line is now empty")
      #self.assertEqual(C.header, {'a-header-field': ['A-Header-Field', 'value']}, "Field added, with value")

   def test_handleDataAquisition_ValidRequestProvided_NonEmptyBody_OneReadRequired(self):
      """Internal Diagnostic: Data aquisition - full request, medium body (bodysize >=chunksize"""
      C=MimeRequestComponent.MimeRequestComponent()
      # This setup is tested in test_handleDataAquisition_ValidRequestProvided_EmptyBody
      C._deliver("GET http://user:password@127.0.0.1:1234/ HTTP/1.0\n", "inbox")
      C.handleDataAquisition() # Read request line
      C._deliver("A-Header-Field: value\n", "inbox")
      C.handleDataAquisition() # Read header line
      C.handleDataAquisition() # Process header line
      C._deliver("Content-Length: 37\n", "inbox")
      C.handleDataAquisition() # Read header line
      C.handleDataAquisition() # Process header line
      endOfHeader = '\n'
      C._deliver(endOfHeader, "inbox")
      C.handleDataAquisition()

      C._deliver("....x....X....x....X....x....X....x..", "inbox")
      self.assertEqual(5, C.handleDataAquisition(), "Header has been read; We need to read data (needData) for the body section")
      self.assertEqual(4, C.handleDataAquisition(), "We read some data")
      self.assertEqual("....x....X....x....X....x....X....x..", C.currentBytes, "The data read is what was expected (entire body in this case)")
      self.assertEqual(None, C.handleDataAquisition(), "The system has detected we need no more data and returned None to indicate end of request")
      expectedBody="....x....X....x....X....x....X....x.."
      expectedHeader= {'a-header-field': ['A-Header-Field', 'value'],
                       'content-length': ['Content-Length', '37']}
      self.assertEqual(expectedBody, C.body, "Body has been correctly read")
      self.assertEqual(expectedHeader, C.header, "Header has expected value")

   def test_handleDataAquisition_ValidRequestProvided_NonEmptyBody_MultipleReadsRequired(self):
      """Internal Diagnostic: Data aquisition - full request, large body (body size >=2*chunksize"""
      C=MimeRequestComponent.MimeRequestComponent()
      # This setup is tested in test_handleDataAquisition_ValidRequestProvided_EmptyBody
      C._deliver("GET http://user:password@127.0.0.1:1234/ HTTP/1.0\n", "inbox")
      C.handleDataAquisition() # Read request line
      C._deliver("A-Header-Field: value\n", "inbox")
      C.handleDataAquisition() # Read header line
      C.handleDataAquisition() # Process header line
      C._deliver("Content-Length: 74\n", "inbox")
      C.handleDataAquisition() # Read header line
      C.handleDataAquisition() # Process header line
      endOfHeader = '\n'
      C._deliver(endOfHeader, "inbox")
      C.handleDataAquisition()

      C._deliver("....x....X....x....X....x....X....x..", "inbox")
      C._deliver("....v....Y....v....Y....v....Y....v..", "inbox")
      self.assertEqual(5, C.handleDataAquisition(), "Header has been read; We need to read data (needData) for the body section")
      self.assertEqual(4, C.handleDataAquisition(), "We read some data")
      self.assertEqual("....x....X....x....X....x....X....x..", C.currentBytes, "The data read is what was expected (part of body in this case)")
      self.assertEqual(5, C.handleDataAquisition(), "Data has been processed. Header has been read; We need to read data (needData) for the body section")
      self.assertEqual(4, C.handleDataAquisition(), "We read some data")
      self.assertEqual("....v....Y....v....Y....v....Y....v..", C.currentBytes, "The data read is what was expected (part of body in this case)")
      self.assertEqual(None, C.handleDataAquisition(), "The system has detected we need no more data and returned None to indicate end of request")
      expectedBody="....x....X....x....X....x....X....x.."+"....v....Y....v....Y....v....Y....v.."
      expectedHeader= {'a-header-field': ['A-Header-Field', 'value'],
                       'content-length': ['Content-Length', '74']}
      self.assertEqual(expectedBody, C.body, "Body has been correctly read")
      self.assertEqual(expectedHeader, C.header, "Header has expected value")

   def test_mainBody(self):
      """Black box test of mainBody"""
      C=MimeRequestComponent.MimeRequestComponent()
      self.assertEqual(len(C.outboxes["outbox"]), 0, "Outbox is empty")
      request = [ "GET http://user:password@127.0.0.1:1234/ HTTP/1.0\n",
                  "A-Header-Field: value\n",
                  "Content-Length: 74\n",
                  '\n',
                  "....x....X....x....X....x....X....x..",
                  "....v....Y....v....Y....v....Y....v.." ]
      for line in request:
         C._deliver(line, "inbox")
      expectedBody="....x....X....x....X....x....X....x.."+"....v....Y....v....Y....v....Y....v.."
      expectedHeader= {'a-header-field': ['A-Header-Field', 'value'],
                       'content-length': ['Content-Length', '74']}
      while C.mainBody():
         pass
      self.assertEqual(len(C.outboxes["outbox"]), 1, "Outbox contains a result")
      result=C.outboxes["outbox"][0]
      self.assert_(result.__class__ == MimeRequestComponent.mimeObject)
      self.assertEqual(result.header, expectedHeader, "Header correctly parsed")
      self.assertEqual(result.body, expectedBody, "Body correctly read")

   def test_closeDownComponent(self):
      """Closing down the component should not raise assertions"""
      "Closedown should not raise any assertions"
      C=MimeRequestComponent.MimeRequestComponent()
      C.closeDownComponent()

if __name__=="__main__":
   unittest.main()

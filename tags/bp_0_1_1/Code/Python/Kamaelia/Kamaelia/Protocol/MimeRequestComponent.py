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
"""
Mime Request Component.

Takes a request of the form:

XXXXX <url> PROTO/Ver
Key: value
Key: value
Content-Length: value
Key: value
>>blank line<<
>body
text<

And converts it into a python object that contains:
   requestMethod : string
   url : string
   Protocol : string
   Protocol Version : string (not parsed into a number)
   KeyValues : dict
   body : raw data

Has a default inbox, and a default outbox. Requests data comes in the
inbox. MimeRequest objects come out the outbox.
"""

from Axon.Component import component, scheduler,linkage,newComponent
from Axon.Ipc import errorInformation
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
import Kamaelia.requestLine

class mimeObject(object):
   """Accepts a Mime header represented as a dictionary object, and a body
   as a string. Provides a way of handling as a coherant unit.
   ATTRIBUTES:
      header : dictionary. (keys == fields, values = field values)
      body : body of MIME object
   """
   def __init__(self, header = {}, body = "",preambleLine=None):
      "Creates a mimeObect"
      self.header = dict(header)
      self.body = body
      if preambleLine:
         self.preambleLine = preambleLine
      else:
         self.preambleLine = None

   def __str__(self):
      """Dumps the Mime object in printable format - specifically as a formatted
      mime object"""
      result = ""
      for anItem in self.header.iteritems():
         (key,[origkey, value]) = anItem                   # For simplifying/checking testing
         result = result + origkey + ": "+value + "\n"
      result = result + "\n"
      result = result + self.body
      if self.preambleLine:
         result = str(self.preambleLine) + "\n"+result + self.body
      return result


class MimeRequestComponent(component):
   """Component that accepts raw data, parses it into consituent
   parts of a MIME request. Attempts no interpretation of the request
   however.
   """
   def __init__(self):
      self.__super.__init__()

      self.header = {}
      self.requestLineRead = 0
      self.currentLineRead = 0
      self.seenEndHeader = 0
      self.currentLine = ''
      self.currentBytes = ''
      self.requestLine = ''
      self.stillReading = 1
      self.needData = 0
      self.gotRequest = 0
      self.body = ''
      self.step = 0

   def initialiseComponent(self):
      pass

   def nextLine(self):
      if self.dataReady("inbox"):
         theData = self.recv("inbox")
         try:
            self.currentBytes = self.currentBytes + theData
         except TypeError: # theData isn't a string/stringable object, junk
            return (0,"")
      try:
         [newline,self.currentBytes] = self.currentBytes.split("\n",1) # This is independent, unless line is null!
         if newline !="" and newline[-1] == "\r":
            newline = newline[0:-1]
         got = 1
      except ValueError: # Still waiting for enough data
         return (0,"")

      return (got, newline)

   #
   # This code structure would be alot cleaner in a single threaded environment,
   # or if "yield" could be nested. Unfortunately "yield" can't be nested and we're
   # not single threaded. It's not _too_ bad though.
   #
   def getRequestLine(self):
      "Sets the *REQUEST* line arguments"
      (self.requestLineRead,self.requestLine) = self.nextLine()

   def getALine(self):
      "Sets the *CURRENT* line arguments"
      (self.currentLineRead, self.currentLine) = self.nextLine()

   def readHeader(self):
         [ origkey,value ] = self.currentLine.split(": ",1)
         key = origkey.lower()
         if not self.header.has_key(key):
            self.header[key] = [origkey, value]
         else:
            self.header[key][1] = self.header[key][1]+ ", " + value
         self.currentLineRead = 0 # We've processed the line, and therefore don't have a current line
         self.currentLine = ""    # So we also set the current line to ""

   def getData(self):
      if self.dataReady("inbox"):
         theData = self.recv("inbox")
         self.currentBytes = self.currentBytes + theData
         self.needData = 0

   def checkEndOfHeader(self):
      if self.currentLine == '' and not self.seenEndHeader:
         self.seenEndHeader = 1
         try:
            self.headerlength = int(self.header['content-length'][1])
         except KeyError:
            self.headerlength = 0
            self.needData = 0


   def handleDataAquisition(self):
      """This is currently clunky and effectively implements a state machine.
      Should consider rewriting as a generator"""
      if not self.requestLineRead:
         self.getRequestLine()
         return 1

      if not self.currentLineRead:
         self.getALine()      # Make sure we have a line(headers)
         return 2

      # This section collates the body if we've reached the end of the header
      # Exit condition is when we've read the content length specified in the header
      # The exit value is a None value.

      self.checkEndOfHeader()
      if not self.seenEndHeader: 	# !!!! We're in a loop, hence "if" rather than "while"
         self.readHeader()
         return 3

      self.body =self.body + self.currentBytes
      if not (len(self.body) >= self.headerlength):
         if self.needData:
            self.getData()       # Grab raw, unparsed data. (body)
            return 4
         else:
            self.currentBytes = ""
            self.needData = 1
            return 5


   def mainBody(self):
      # This is running inside a while() loop remember.
      # Optimisation would be reassignment of self.mainBody when we skip through
      # the different phases of execution.
      if not self.gotRequest:
         if self.handleDataAquisition():
            return 1
      self.gotRequest = 1
      try:
         self.request = requestLine.requestLine(self.requestLine)
      except requestLine.BadRequest, br:
         errinf = errorInformation(self, br)
         self.send(errinf, "signal")
         return 0

      assert self.debugger.note("MimeRequestComponent.mainBody",5, self.request,"\n")
      assert self.debugger.note("MimeRequestComponent.mainBody",10, "HEADER  \t:", self.header)
      assert self.debugger.note("MimeRequestComponent.mainBody",10, "BODY    \t:", self.body)

      self.mimeRequest = mimeObject(self.header, self.body, self.request)
      assert self.debugger.note("MimeRequestComponent.mainBody",5, self.mimeRequest)
      self.send(self.mimeRequest, "outbox")

   def closeDownComponent(self):
      pass

if __name__ =="__main__":
   class TestHarness(component):
#		def __init__(self):
#			component.__init__(self)
# If we leave out this, we get a default minimal component!

      def initialiseComponent(self):
         print "DEBUG: TestHarness::initialiseComponent"

         self.reader = ReadFileAdaptor(filename="SampleMIMERequest.txt")
         self.decoder = MimeRequestComponent()

         self.postoffice.name
         linkage(self.reader, self.decoder, "outbox", "inbox", self.postoffice)
         self.addChildren(self.reader,self.decoder)
         return newComponent(self.reader, self.decoder)

      def mainBody(self):
         "Don't really need to do much here..."
         #print "bleh: Now in the main loop"
         return 1

   TestHarness().activate()
   scheduler.run.runThreads()

# The following code reads from an input string (foo) a request.
# The request is split into the following 3 parts:
# Request line, Headers, Body
# Headers are stored in a dict, which multiple values concatenated using commas, as is normal for MIME.
# How the values are used is up to the client of the module

   #
   # It uses the following logic...
   # We use nextLine reads into our buffer enough to extract a line, and
   # extracts it returning the line & the buffer
   #
   # We store the header key/value fields here in 'header'
   # currentBytes forms an input buffer that we extract lines from.
   #
   # * We then grab the first line, which *SHOULD* be the request line.
   # * We then grab the next line after that - this will either be empty,
   #   ending the request header, or be a request header line.
   #
   # Assuming we're still processing the header, we then start looping, the
   # exit condition is we hit the end of the header.
   #
   # Then for each line, we split it into key & value fields, use these to populate
   # the 'header' dict. If we have a collision, values are comma separated.
   # (comma is considered a special char by RFC822/2822 in headers, which
   # HTTP/RTSP are at least partially based on and tend to follow by convention)
   #
   # Finally any remaining request data is mopped up into a body value.
   #

if 0: # The following is the original logic for sanity reasons.
   # It uses the following logic...
   # We use nextLine reads into our buffer enough to extract a line, and
   # extracts it returning the line & the buffer
   #
   # We store the header key/value fields here in 'header'
   # currentBytes forms an input buffer that we extract lines from.
   #
   # * We then grab the first line, which *SHOULD* be the request line.
   # * We then grab the next line after that - this will either be empty,
   #   ending the request header, or be a request header line.
   #
   # Assuming we're still processing the header, we then start looping, the
   # exit condition is we hit the end of the header.
   #
   # Then for each line, we split it into key & value fields, use these to populate
   # the 'header' dict. If we have a collision, values are comma separated.
   # (comma is considered a special char by RFC822/2822 in headers, which
   # HTTP/RTSP are at least partially based on and tend to follow by convention)
   #
   # Finally any remaining request data is mopped up into a body value.
   #
   def nextLine(line, wibble):
      newline = None
      got = 0
      while not got:
         try:
            [newline,line] = line.split("\n",1)
            got = 1
         except ValueError:
            line = line + wibble[0]
            del wibble[0]
      return (newline, line)

   stream = [ "BIBBLE foo://bar:baz@sd.sd.", "sd/bla?this&that=other PROTO/3.3\nKey",
               "1: Value1\nKey2: ","Value2\nKey3: Value3\nK","ey4: Bibble\n\nThis is th",
               "e body text\n" ]
   header = {}
   currentBytes = ""
   [requestLine,currentBytes] = nextLine(currentBytes,stream)
   [currentLine, currentBytes] = nextLine(currentBytes,stream)
   while(currentLine != ''):
      [ key,value ] = currentLine.split(": ",1)
      if not header.has_key(key):
         header[key] = value
      else:
         header[key] = header[key]+ ", " + value
      [currentLine, currentBytes] = nextLine(currentBytes,stream)
   body = currentBytes
   for i in stream: body = body + i
   print (requestLine,header,body)

#!/usr/bin/env python2.3
"""
Simple HTTP server

API Needs:

1) We don't/can't recieve notification from the ReadFileAdaptor that the
   file has been closed.
2) We can't actually tell the CSA to close itself down either...

EXTERNAL CONNECTORS
      * inboxes : inboxes=["datain","inbox"]
      * outboxes=["outbox"]

"""

import sys

from Axon.Component import component, scheduler, linkage, newComponent
from Axon.Ipc import producerFinished, errorInformation
from ReadFileAdaptor import ReadFileAdaptor
from SimpleServerComponent import SimpleServer
from MimeRequestComponent import mimeObject, MimeRequestComponent
from requestLine import BadRequest
from ToStringComponent import ToStringComponent

crashAndBurn = { "error404" : False }

class HTTPServer(component):
   Inboxes=["inbox","_frommime", "_errmon", "_fromfile", "_sigfromfile"]# List of inbox names if different
   Outboxes=["outbox","_pass","signal"]# List of outbox names if different
   def __init__(self, debug=0):
      self.__super.__init__()
      self.debug = debug

   def initialiseComponent(self):
      self.mimehandler = MimeRequestComponent()
      self.httphandler = HTTPReqestHandler()
#      toString = ToStringComponent()
#      myDataSource = ReadFileAdaptor(command="afortune.pl",
#                              readmode="bitrate",
#                              bitrate=95200, chunkrate=25)
      assert self.debugger.note("HTTPServer.initialiseComponent", 1, "Initialising HTTPServer protocol handler ", self.__class__)
#      self.link(        source=(self,"inbox"),
#               sink=(mimehandler,"inbox"),
#               passthrough=2)
      self.link(  source=(self,"_pass"),
                  sink=(self.mimehandler,"inbox"))
#      self.link(  source=(mimehandler,"outbox"),
#                  sink=(toString,"inbox"))
      self.link(  source=(self.mimehandler,"outbox"),
                  sink=(self.httphandler,"inbox"))
      self.link(  source=(self.httphandler,"outbox"),
                  sink=(self,"_frommime"))
      self.link(  source=(self.mimehandler,"signal"),
                  sink=(self,"_errmon"))
#      self.link(	source=(toString,"outbox"),
#              sink=(self,"outbox"),
#               passthrough=1)
      self.addChildren(self.mimehandler, self.httphandler)

      return newComponent( self.mimehandler, self.httphandler )#, toString ] )

   def mainBody(self):
      """All the interesting work has been done by linking the file reader's output
      to our output"""
      if self.dataReady("_fromfile"):
         temp = self.recv("_fromfile")
         self.send(temp)
         return 1
      if self.dataReady("_sigfromfile"):
         temp = self.recv("_sigfromfile")
         self.send(temp,"signal")
      if self.dataReady("inbox"):
         temp = self.recv("inbox")
         self.send(temp,"_pass")
      if self.dataReady("_frommime"):
         filename = self.recv("_frommime")
         try:
            file = open(filename, 'r')
            close(file)
         except Exception, e:
            msg = 'HTTP/1.0 404 "Not Found\n\n"'
            self.send(msg)
            self.send(producerFinished(self), "signal")
            if crashAndBurn["error404"]:
               raise e
            return 0
         msg ='HTTP/1.0 200 "OK\n\n"'
         self.send(msg)
         self.rfa = ReadFileAdapter(filename=filename, readmode="bitrate")
         self.link(source=(self.rfa, "outbox"),
                     sink=(self, "_fromfile"))
         self.link(source=(self.rfa, "signal"),
                     sink=(self, "_sigfromfile"))
         self.addChildren(self.rfa)
#         self.send(str(theData), "outbox")
#         sig = producerFinished(self)
#         self.send(sig, "signal")
         return [self.rfa]
      if self.dataReady("_errmon"):
         temp = self.recv("_errmon")
         if isinstance(temp, errorInformation):
            if isinstance(temp.exception, BadRequest):
               msg = 'HTTP/1.0 400 "Bad Request"\n'
               self.send(msg)
            sig = producerFinished(self)
            self.send(sig,"signal")
            return 0
      return 1

   def closeDownComponent(self):
      """Simple subcomponent killer."""
      for child in self.childComponents():
         self.removeChild(child)
      self.mimehandler=None
      self.httphandler=None
      self.rfa=None
#      self.toString=None

class HTTPReqestHandler(component):
   def __init__(self, debug=0):
      self.__super.__init__()
      self.debug = debug

   def mainBody(self):
      if self.dataReady("inbox"):
         reqdata = self.recv("inbox")
         filename = reqdata.preambleLine.url
         if filename[0] is '/':
            filename = filename[1:]
         self.send(filename)
      return 1

#   404str = 'HTTP/1.0 404 Not Found\nContent-type: text/html\nContent-length: 143\n\n<HTML>\n<TITLE> Not Found </TITLE>\n<BODY BGCOLOR="#FFFFFF">\n<FONT FACE="Arial,Helvetica,Geneva" SIZE=-1>\n<H2> Not Found </H2>\n</BODY>\n</HTML>\n\n'




if __name__ == '__main__':
   SimpleServer(protocol=HTTPServer, port=8082).activate()
   scheduler.run.runThreads(slowmo=0)

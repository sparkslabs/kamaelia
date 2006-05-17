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

from Axon.Component import component
from Kamaelia.SimpleServerComponent import SimpleServer
from Axon.Ipc import producerFinished, errorInformation
from Kamaelia.KamaeliaExceptions import BadRequest
import string
from Lagger import Lagger

def removeTrailingCr(line):
	if len(line) == 0: return line
	if line[-1] == "\r":
		return line[0:-1]
		
class HTTPParser(component):
	Inboxes =  { "inbox"         : "Raw HTTP requests",
	             "control"       : "UNUSED" }
	Outboxes = { "outbox"        : "HTTP request object",
	             "signal"        : "UNUSED" }
	
	def __init__(self):
		super(HTTPParser, self).__init__()
		readbuffer = ""
		self.requeststate = 1 # awaiting request line
		self.lines = []
		self.readbuffer = ""

	def linesFetch(self):
		if self.dataReady("inbox"):
			self.readbuffer += self.recv("inbox")
			self.lines += string.split(self.readbuffer, "\n")
			self.readbuffer = self.lines.pop() #the remainder after final \n
		else: self.pause()
		
	def main(self):

		while 1:
			requestobject = {}
			requestobject["bad"] = False
			requestobject["headers"] = {}

			#state 1 - awaiting initial line
			while len(self.lines) == 0:
				yield 1
				self.linesFetch()
			
			print "Initial line found"
			currentline = removeTrailingCr(self.lines.pop(0))
			splitline = string.split(currentline, " ")
			
			if len(splitline) < 2:
				requestobject["bad"] = True
				# bad request
			else:
				if len(splitline) < 3:
					# must be HTTP/0.9
					requestobject["method"] = splitline[0]
					requestobject["raw-uri"] = splitline[1]
					requestobject["protocol"] = "HTTP"
					requestobject["version"] = "0.9"
				else: #deal with normal HTTP including badly formed URIs
					requestobject["method"] = splitline[0]

					#next line supports all working clients but also 
					#some broken clients that don't encode spaces properly!
					requestobject["raw-uri"] = string.join(splitline[1:-1], "%20") 
					protvers = string.split(splitline[-1], "/")
					if len(protvers) != 2:
						requestobject["bad"] = True
						requestobject["version"] = "0.9"
					else:
						requestobject["protocol"] = protvers[0]
						requestobject["version"] = protvers[1]
		
				#foo://toor:letmein@server.bigcompany.com/bla?this&that=other could be handled better

				if requestobject["method"] == "PUT" or requestobject["method"] == "POST":
					bodiedrequest = True
				else:
					bodiedrequest = False

				if requestobject["version"] != "HTTP/0.9":
					#state 2 - as this is a valid request, we now accept headers	
					previousheader = ""
					while 1:
						yield 1
						if len(self.lines) == 0: self.linesFetch()
						if len(self.lines) > 0:
							currentline = removeTrailingCr(self.lines.pop(0))
							if currentline == "":
								print "End of headers found"
								break;
							else:
								if currentline[0] == " " or currentline[0] == "\t": #continued header
									requestobject["headers"][previousheader] += " " + string.lstrip(currentline)
								else:
									splitheader = string.split(currentline, ":")
									print "Found header: " + splitheader[0]
									requestobject["headers"][string.lower(splitheader[0])] = currentline[len(splitheader[0]) + 1:]
							#should parse headers header
				
				if bodiedrequest:
					#state 3 - the headers are complete - awaiting the message
					pass
				#state 4 - request complete, send it on
			print "Request sent on."
			print requestobject
			self.send(requestobject, "outbox")

class HTTPServer(component):
	"""\
	HTTPServer() -> new HTTPServer
	"""
	
	Inboxes =  { "inbox"         : "TCP data stream - receive",
	             "mime-outbox"   : "Data from MIME handler",
	             "mime-signal"   : "Error signals from MIME handler",
	             "http-outbox"   : "Data from HTTP resource retriever",
	             "control"       : "UNUSED" }


	Outboxes = { "outbox"        : "TCP data stream - send",
				 "mime-inbox"    : "To MIME handler",
				 "mime-control"  : "To MIME handler",
	             "http-inbox"    : "To HTTP resource retriever",
				 "signal"        : "UNUSED" }

	def __init__(self):
		super(HTTPServer, self).__init__()

	def initialiseComponent(self):
		self.mimehandler = HTTPParser()
		self.httphandler = HTTPRequestHandler()
		#self.httphandler.filereader = TriggeredFileReader()
		
		self.link( (self,"mime-inbox"), (self.mimehandler,"inbox") )
		self.link( (self,"mime-control"), (self.mimehandler,"control") )
		self.link( (self.mimehandler,"outbox"), (self, "mime-outbox") )
		self.link( (self.mimehandler,"signal"), (self, "mime-signal") )

		self.link( (self, "http-inbox"), (self.httphandler, "inbox") )
		self.link( (self.httphandler, "outbox"), (self, "http-outbox") )

		#elf.link( (self.httphandler, "filereader-inbox"), (self.httphandler.filereader, "inbox") )
		#self.link( (self.httphandler.filereader,"outbox"), (self.httphandler, "filereader-outbox") )
		
		self.addChildren(self.mimehandler, self.httphandler) #self.httphandler.filereader)
		self.httphandler.activate()
		self.mimehandler.activate()
		#self.httphandler.filereader.activate()

	def mainBody(self):
		if self.dataReady("inbox"):
			temp = self.recv("inbox")
			self.send(temp, "mime-inbox")

		if self.dataReady("http-outbox"):
			temp = self.recv("http-outbox")
			self.send(temp, "outbox")

		if self.dataReady("mime-outbox"):
			temp = self.recv("mime-outbox")
			self.send(temp, "http-inbox")

		if self.dataReady("mime-signal"):
			temp = self.recv("mime-signal")
			if isinstance(temp, errorInformation):
				if isinstance(temp.exception, BadRequest):
					msg = 'HTTP/1.0 400 "Bad Request"\n\n'
					self.send(msg, "outbox")
				sig = producerFinished(self)
				self.send(sig, "signal")
				print "close signal\n"
				return 0
		return 1

	def closeDownComponent(self):
		for child in self.childComponents():
			self.removeChild(child)
		self.mimehandler = None
		self.httphandler = None

class HTTPRequestHandler(threadedcomponent):
	Inboxes =  { "inbox"               : "Raw HTTP requests",
	             #"filereader-outbox"   : "File reader's outbox",
	             "control"             : "UNUSED" }
	Outboxes = { "outbox"              : "HTTP request object",
	             #"filereader-inbox"    : "File reader's inbox",
	             "signal"              : "UNUSED" }

	def __init__(self):
		super(HTTPRequestHandler, self).__init__()
		
	def getErrorPage(self, errorcode, msg = ""):
		if errorcode == 400:
			return { "statuscode" : "400",
			         "data"       : "<html>\n<title>400 Bad Request</title>\n<body style='background-color: black; color: white;'>\n<h2>400 Bad Request</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
			         "type"       : "text/html" }
		elif errorcode == 404:
			return { "statuscode" : "404",
			         "data"       : "<html>\n<title>404 Not Found</title>\n<body style='background-color: black; color: white;'>\n<h2>404 Not Found</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
			         "type"       : "text/html" }
		elif errorcode == 500:
			return { "statuscode" : "500",
			         "data"       : "<html>\n<title>500 Internal Server Error</title>\n<body style='background-color: black; color: white;'>\n<h2>500 Internal Server Error</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
			         "type"       : "text/html" }
		elif errorcode == 501:
			return { "statuscode" : "501",
			         "data"       : "<html>\n<title>501 Not Implemented</title>\n<body style='background-color: black; color: white;'>\n<h2>501 Not Implemented</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
			         "type"       : "text/html" }

	def fetchResource(self, host, uri):
		if uri == "/poweredbykamaelia.png":
			myfile = open("poweredbykamaelia.png", "rb", 0) # bad bad bad - blocking call!
			mydata = myfile.read()
			myfile.close()
			resource = { "type" : "image/png", "statuscode" : "200", "data": mydata }
		else:
			resource = { "type" : "text/html", "statuscode" : "200", "data": "<html>\n<body>\n<p>You requested " + uri + ". Isn't that nice?</p>\n<img src='/poweredbykamaelia.png' style='border: 1px solid #AAAAAA;' alt='Powered by Kamaelia' /></body>\n</html>\n" }
		return resource
		
	def formHeaderResponse(self, resource, protocolversion):
		if resource["statuscode"] == "200": statustext = "200 OK"
		if resource["statuscode"] == "400": statustext = "400 Bad Request"
		if resource["statuscode"] == "404": statustext = "404 Not Found"
		if resource["statuscode"] == "500": statustext = "500 Internal Server Error"
		if resource["statuscode"] == "501": statustext = "501 Not Implemented"

		header = "HTTP/" + protocolversion + " " + statustext + "\nContent-type: " + resource["type"] + "\nContent-length: " + str(len(resource["data"])) + "\n\n"
		return header

	def mainBody(self):
		if self.dataReady("inbox"):
			request = self.recv("inbox")
			if request["bad"]:
				pagedata = self.getErrorPage(400, "Non-HTTP")
				self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")

			if request["protocol"] != "HTTP":
				pagedata = self.getErrorPage(400, "Non-HTTP")
				self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
			else:
				if not request["headers"].has_key("host"):
					pagedata = self.getErrorPage(400, "could not find host header")
					self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
				elif request["method"] == "GET":
					pagedata = self.fetchResource(request["headers"]["host"], request["raw-uri"])
					self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
				else:
					pagedata = self.getErrorPage(501,"The request method is not implemented")
					self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
		return 1


if __name__ == '__main__':
	from Axon.Component import scheduler
	SimpleServer(protocol=HTTPServer, port=8082).activate()
	Lagger().activate()
	scheduler.run.runThreads(slowmo=0)

import string, time

def getErrorPage(errorcode, msg = ""):
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

def websiteHandlerForms(request):
	resource = {
		"type" : "text/html",
		"statuscode" : "200",
		"data" : "<html>\n<body>\n<p>You requested " + request["raw-uri"] + " with body data\n" + request["body"] + ". Isn't that just spiffing?</p>\n<img src='/poweredbykamaelia.png' style='border: 1px solid #AAAAAA;' alt='Powered by Kamaelia' /></body>\n</html>\n"
	}
	return resource
def websiteHandlerFish(request):
	resource = {
		"type" : "text/html",
		"statuscode" : "200",
		"data" : "<html>\n<body>\n<p>You requested " + request["raw-uri"] + ". Isn't that nice?</p>\n<img src='/poweredbykamaelia.png' style='border: 1px solid #AAAAAA;' alt='Powered by Kamaelia' /></body>\n</html>\n"
	}
	return resource
	
def sanitizePath(uri): #needs work
	outputpath = []
	while uri[0] == "/": #remove leading slashes
		uri = uri[1:]
		if len(uri) == 0: break
	
	splitpath = string.split(uri, "/")
	for directory in splitpath:
		if directory == ".":
			pass
		elif directory == "..":
			if len(outputpath) > 0: outputpath.pop()
		else:
			outputpath.append(directory)
	outputpath = string.join(outputpath, "/")
	return outputpath


def websiteHandlerIrcLogs(request):
	def formatIrcLogs(logs):
		outputtext = ""
		lines = string.split(logs, "\n")
		for line in lines:
			if line != "":
				splitline = string.split(line, " ")
				#print splitline
				eventtime = time.strftime("%H:%M", time.gmtime(float(splitline[0])))
				eventtype = splitline[1]
				eventuser = splitline[2]
				eventdata = line[len(splitline[0]+splitline[1]+splitline[2]+splitline[3]+"----"):]
				if eventtype == "LOGGINGOFF":
					outputtext += "[" + eventtime + "] Logging was disabled by " + eventuser + "\n"
				elif eventtype == "LOGGINGON":
					outputtext += "[" + eventtime + "] Logging was enabled by " + eventuser + "\n"		
				elif eventtype == "PRIVMSG":
					if eventdata[0:7] == "\x01ACTION":
						eventdata = "*" + string.lstrip(eventdata[7:-1]) + "*"
					if eventdata != "\x01VERSION\x01":
						outputtext += "[" + eventtime + "] " + eventuser + ": " + eventdata + "\n"
				elif eventtype == "PART":
					outputtext += "[" + eventtime + "] " + eventuser + " left the room\n"
				elif eventtype == "JOIN":
					outputtext += "[" + eventtime + "] " + eventuser + " joined the room\n"		
				elif eventtype == "QUIT":
					outputtext += "[" + eventtime + "] " + eventuser + " quit - " + eventdata + "\n"
				elif eventtype == "TOPIC":
					outputtext += "[" + eventtime + "] " + eventuser + " changed the topic to \"" + eventdata + "\"\n"
		return outputtext

	#try:
	filename = "kamaelia-logs.txt"
	sourcefile = open(filename, "rb", 0)
	data = sourcefile.read()
	sourcefile.close()
	resource = { "type" : "text/plain", "statuscode" : "200", "data" : formatIrcLogs(data) }	
	#except:
	#	resource = getErrorPage(500)
		
	return resource
	
def websiteHandlerDefault(request):
	try:
		filename = sanitizePath(request["raw-uri"])
		filetype = workoutMimeType(filename)
		sourcefile = open(homedirectory + filename, "rb", 0)
		data = sourcefile.read()
		sourcefile.close()
		resource = {
			"type" : filetype,
			"statuscode" : "200",
			"data" : data
		}
	except:
		resource = getErrorPage(404)
	
	return resource


def workoutMimeType(filename):
	fileextension = string.rsplit(filename,".",1)[-1]
	if extensionToMimeType.has_key(fileextension):
		return extensionToMimeType[fileextension]
	else:
		return "application/octet-stream"

extensionToMimeType = {
	"png" : "image/png",
	"gif" : "image/gif",
	"jpg" : "image/jpeg",
	"jpeg" : "image/jpeg",
	"txt" : "text/plain",
	"htm" : "text/html",
	"html" : "text/html"
}	


homedirectory = "/home/ryan/kamhttpsite/"
URLHandlers = [
	["/fish/"                  , websiteHandlerFish],
	["/formhandler"            , websiteHandlerForms],
	["/irc"                    , websiteHandlerIrcLogs],
	["/"                       , websiteHandlerDefault]
]

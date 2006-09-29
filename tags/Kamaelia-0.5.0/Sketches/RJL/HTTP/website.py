#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string, time, dircache
import websitetemplate
from cgi import escape

def getErrorPage(errorcode, msg = ""):
    if errorcode == 400:
        return { "statuscode" : "400",
                 "data"       : u"<html>\n<title>400 Bad Request</title>\n<body style='background-color: black; color: white;'>\n<h2>400 Bad Request</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
                 "type"       : "text/html" }
    elif errorcode == 404:
        return { "statuscode" : "404",
                 "data"       : u"<html>\n<title>404 Not Found</title>\n<body style='background-color: black; color: white;'>\n<h2>404 Not Found</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
                 "type"       : "text/html" }
    elif errorcode == 500:
        return { "statuscode" : "500",
                 "data"       : u"<html>\n<title>500 Internal Server Error</title>\n<body style='background-color: black; color: white;'>\n<h2>500 Internal Server Error</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
                 "type"       : "text/html" }
    elif errorcode == 501:
        return { "statuscode" : "501",
                 "data"       : u"<html>\n<title>501 Not Implemented</title>\n<body style='background-color: black; color: white;'>\n<h2>501 Not Implemented</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
                 "type"       : "text/html" }

def sanitizeFilename(filename):
    output = ""
    for char in filename:
        if char >= "0" and char <= "9": output += char
        elif char >= "a" and char <= "z": output += char
        elif char >= "A" and char <= "Z": output += char
        elif char == "-" or char == "_" or char == ".": output += char
    return output

def websiteKamaeliaIrcLogs(request):
    def currentDateString():
        curtime = time.gmtime()
        return time.strftime("%d-%m-%Y", curtime)
    
    arg = sanitizeFilename(string.rsplit(request["raw-uri"], "/", 1)[-1])
    meta = { "title" : ".kamaelia.irc" }
    if arg != "": meta["title"] += "." + arg
    
    dirname = string.rsplit("/" + request["raw-uri"], "/", 1)[0]
    #print "Dirname: " + dirname
    try:
        mymenu = websitetemplate.readMenu(homedirectory + "/kamaelia/menus.xml")
    except IOError:
        mymenu = []
    meta["extramenus"] = mymenu

    if arg == "":
        data = u"<h2>#kamaelia IRC channel logs</h2>\n<p>These logs are for the #kamaelia channel on irc.freenode.net</p>"
        datelist = dircache.listdir(homedirectory + "/kamaelia/irc/")
        datedict = {}
        for date in datelist:
            splitdata = date.split(".")[0].split("-")
            if len(splitdata) == 3:
                year = int(splitdata[2])
                month = int(splitdata[1])
                day = int(splitdata[0])
                if not datedict.has_key(year): datedict[year] = {}
                if not datedict[year].has_key(month): datedict[year][month] = {}
                datedict[int(splitdata[2])][int(splitdata[1])][int(splitdata[0])] = date
        monthnames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]
        for year, months in datedict.items():
            data += u"<h3>" + str(year) + u"</h3>\n"
            for month, days in months.items():
                data += u"<h4>" + monthnames[month-1] + u"</h4>\n"
                data += u"<ul style=\"font-size: 120%\">"
                for day, filename in days.items():
                    if filename == currentDateString() + ".txt":
                        data += u"<li><a href=\"/kamaelia/irc-view/" + unicode(filename, "utf-8") + u"\" style=\"color: #55AA22\">" + str(day) + u"</a> (today)</li>"
                    else:
                        data += u"<li><a href=\"/kamaelia/irc-view/" + unicode(filename, "utf-8") + u"\">" + str(day) + u"</a></li>"
                data += u"</ul>"
    
    	data = websitetemplate.formHeader(meta) + websitetemplate.formMainTableHeader(meta) + data + websitetemplate.formMainTableFooter(meta) + websitetemplate.formFooter(meta)
           
        resource = {
            "type" : "text/html",
            "statuscode" : "200",
            "data" : data
        }

    elif arg == "today":
       arg = currentDateString() + ".txt"
    
    if arg != "": #date given
        logsdata = websitetemplate.getIrcLogs(arg)
        if logsdata == 404:
            resource = getErrorPage(404, u"Specified log file not found.")
        else:
            data = u"<h2>#kamaelia IRC channel logs - " + arg + u"</h2><p>This page is also available in <a href=\"/kamaelia/irc/" + arg + u"\">plain text form</a>. All times given are in GMT.</p>\n<p style='font-family: Courier, monospace; font-size: 80%;'>"
            escapeddata = escape(logsdata)
            escapeddata = escapeddata.replace(u"\n", u"<br />\n")
            escapeddata = escapeddata.replace(u"@", u"<img src=\"/at.png\" /><!-->mail.<-->")
            data += escapeddata + u"</p>"
            data = websitetemplate.formHeader(meta) + websitetemplate.formMainTableHeader(meta) + data + websitetemplate.formMainTableFooter(meta) + websitetemplate.formFooter(meta)
            resource = {
                "type" : "text/html",
                "statuscode" : "200",
                "data" : data
            }
    return resource
    
def websiteHandlerForms(request):
    resource = {
        "type" : "text/html",
        "statuscode" : "200",
        "data" : u"<html>\n<body>\n<p>You requested " + request["raw-uri"] + u" with body data\n" + request["body"] + u". Isn't that just spiffing?</p>\n<img src='/poweredbykamaelia.png' style='border: 1px solid #AAAAAA;' alt='Powered by Kamaelia' /></body>\n</html>\n"
    }
    return resource
    
def websiteHandlerBuggy(request):
    x = 1 / 0
    return "hi"

def websiteHandlerFish(request):
    resource = {
        "type" : "text/html",
        "statuscode" : "200",
        "data" : u"<html>\n<body>\n<p>You requested " + request["raw-uri"] + u". Isn't that nice?</p>\n<img src='/poweredbykamaelia.png' style='border: 1px solid #AAAAAA;' alt='Powered by Kamaelia' /></body>\n</html>\n"
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
    
def websiteHandlerDefault(request):
    try:
        filename = sanitizePath(request["raw-uri"])
        if filename[-1:] == "/": filename += indexfilename
        
        if filename == "":
            filetype = "text/html"
            meta = {}
            data = websitetemplate.formHeader(meta) + websitetemplate.formMainPage(meta) + websitetemplate.formFooter(meta)
        else:
            filetype = workoutMimeType(filename)
            sourcefile = open(homedirectory + filename, "rb", 0)
            data = sourcefile.read()
            sourcefile.close()
            
            if filetype == "text/cool":
                filetype = "text/html"
                meta = { "title" : "." + filename[:-5], }
                dirname = string.rsplit("/" + filename, "/", 1)[0]
                #print "Dirname: " + dirname
                try:
                    mymenu = websitetemplate.readMenu(homedirectory + dirname[1:] + "/menus.xml")
                except IOError:
                    mymenu = []
                meta["extramenus"] = mymenu
                data = websitetemplate.formHeader(meta) + websitetemplate.formMainTableHeader(meta) + data + websitetemplate.formMainTableFooter(meta) + websitetemplate.formFooter(meta)
           
        resource = {
            "type" : filetype,
            "statuscode" : "200",
            "data" : data
        }
    except IOError:
        resource = getErrorPage(404)
    
    return resource


def workoutMimeType(filename):
    fileextension = string.rsplit(filename,".",1)[-1]
    if extensionToMimeType.has_key(fileextension):
        return extensionToMimeType[fileextension]
    else:
        return "application/octet-stream"

extensionToMimeType = {
    "png"  : "image/png",
    "gif"  : "image/gif",
    "jpg"  : "image/jpeg",
    "jpeg" : "image/jpeg",
    "txt"  : "text/plain",
    "htm"  : "text/html",
    "html" : "text/html",
    "css"  : "text/css",
    "cool" : "text/cool"
}	

indexfilename = "index.cool"
homedirectory = "/home/ryan/kamhttpsite/"
URLHandlers = [
    ["/fish/"                  , websiteHandlerFish],
    ["/formhandler"            , websiteHandlerForms],
    ["/kamaelia/irc-view/"     , websiteKamaeliaIrcLogs],
    ["/error"                  , websiteHandlerBuggy],    
    ["/"                       , websiteHandlerDefault] #should always be last as catches all
]

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

menus = [
    {
        "name"  : "projects",
        "links" : [ ("gdPlotGraph", "/gdplotgraph/", "/gdplotgraph.png"),
                    ("LORE",        "/mmorpg/",      "/mmorpg/longsword-sm-cropped.png"),
                    ("Kamaelia",    "/kamaelia/",    "kamaelialogo-sm.png")
                  ]
    },
    {
        "name"  : "",
        "links" : [ ("my blog",     "/blog.cool", ""),
                    ("links", "/links.cool", ""),
                    ("contact me",  "/contact", "")
                  ]
    }
]

import string, time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


def getIrcLogs(datestring):
    def formatIrcLogs(logs):
        logs = unicode(logs, "utf-8", "ignore")
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
                if eventtype == u"LOGGINGOFF":
                    outputtext += u"[" + eventtime + u"] Logging was disabled by " + eventuser + u"\n"
                elif eventtype == u"LOGGINGON":
                    outputtext += u"[" + eventtime + u"] Logging was enabled by " + eventuser + u"\n"		
                elif eventtype == u"PRIVMSG":
                    if eventdata[0:7] == u"\x01ACTION":
                        eventdata = u"*" + string.lstrip(eventdata[7:-1]) + u"*"
                    if eventdata != u"\x01VERSION\x01":
                        outputtext += u"[" + eventtime + u"] " + eventuser + u": " + eventdata + u"\n"
                elif eventtype == u"PART":
                    outputtext += u"[" + eventtime + u"] " + eventuser + u" left the room\n"
                elif eventtype == u"JOIN":
                    outputtext += u"[" + eventtime + u"] " + eventuser + u" joined the room\n"		
                elif eventtype == u"QUIT":
                    outputtext += u"[" + eventtime + u"] " + eventuser + u" quit - " + eventdata + "\n"
                elif eventtype == u"TOPIC":
                    outputtext += u"[" + eventtime + u"] " + eventuser + u" changed the topic to \"" + eventdata + "\"\n"
        return outputtext

    try:
        filename = "/home/ryan/kamhttpsite/kamaelia/irc/" + datestring
        sourcefile = open(filename, "rb", 0)
        data = sourcefile.read()
        sourcefile.close()
        return formatIrcLogs(data)
    except IOError:
    	return 404

def readMenu(filepath):
    mymenu = []
    class MenuHandler(ContentHandler):
        def startElement(self, name, attrs):
            if name == "group":
                self.currentGroupLinks = []
                self.currentGroupName = attrs.get("name","")
                self.currentGroupImage = attrs.get("img","")
            elif name == "link":
                self.currentLinkHref = attrs.get("href", "")
                self.currentLinkImage = attrs.get("img","")

        def characters (self, ch):
            self.characters = ch
            
        def endElement(self, name):
            if name == "link":
                self.currentGroupLinks.append( (self.characters, self.currentLinkHref, self.currentLinkImage) )
            elif name == "group":
                mymenu.append( {
                    "name" : self.currentGroupName,
                    "image" : self.currentGroupImage,
                    "links" : self.currentGroupLinks
                } )
        
    parser = make_parser()   
    myHandler = MenuHandler()
    parser.setContentHandler(myHandler)
    parser.parse(open(filepath))
    return mymenu
        
def formHeader(meta):
    if meta.has_key("title"):
        title = "Ryan's Site - " + meta["title"]
    else:
        title = "Ryan's Site"
    
    output = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>""" + title + u"""</title>
<link href="/style.css" rel="stylesheet" type="text/css" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />"""

    if meta.has_key("keywords"):
        output += u'<meta name="keywords" content="' +  meta["keywords"] + '" />\n'
    if meta.has_key("description"):
        output += u'<meta name="description" content="' +  meta["description"] + '" />\n'
    output += u"""</head>
<body style="padding: 0; margin: 0;">"""
    return output

def formMainTableHeader(meta):
    output = u"""<table style="width: 99.9%; border: 0; margin: 0; position: relative; min-height: 100%;" cellpadding="0" cellspacing="0">
<tr style="height: 100%;">
<td style="padding: 10px; vertical-align: top;">"""
    return output

def formMainPage(meta):
    additionalfooter = ""
    if meta.has_key("additionalfooter"): additionalfooter = meta["additionalfooter"]
    output = u"""<div style="text-align: center;">
<h1 style="padding: 0; margin: 0;">Ryan's Site - ronline.no-ip.info</h1>
<p class="i" style="margin: 0;">Mathematics, Computing, Technology</p>"""
    if meta.has_key("extramenus"):
        mymenus = meta["extramenus"]
    else:
        mymenus = []
    mymenus.extend(menus)   
    
    for menu in mymenus:
        if menu.has_key("name"):
            output += u"<h2>" + menu["name"] + "</h2>\n"
        else:
            print u"<br /><br />\n";

        output += """<table style="border: 0; padding: 5px; width: 100%; margin-left: auto; margin-right: auto;">\n<tr>"""
        firstlink = True
        for (label, url, img) in menu["links"]:
            if firstlink:
                firstlink = False
                output += "<td style=\"width: " + str(round(100 / len(menu["links"]), 3)) + "%; padding: 5px;\">" + "<a class=\"frontpagelink\" href=\"" + url + "\">\n<span class=\"frontpagelinkheader\">" + label + "</span>\n"
            else:
                output += "<td style=\"width: " + str(round(100 / len(menu["links"]), 3)) + "%; padding: 5px; " + "border-left: 1px solid #5079A0;\">" + "<a class=\"frontpagelink\" href=\"" + url + "\">\n<span class=\"frontpagelinkheader\">" + label + "</span>\n"

            if img != "":
                output += "<br /><img src=\"" + img + "\" alt=\"" + label + "\"></img>";
            output += "</a></td>\n";
        
        output += "</tr></table>"
    output += "</div>"
    output += "<p style=\"text-align: center; font-size: 70%;\">Copyright (C) 2006 ronline.no-ip.info. All rights reserved.</p>" + additionalfooter
    return output
    
def formMainTableFooter(meta):
    additionalfooter = ""
    if meta.has_key("additionalfooter"): additionalfooter = meta["additionalfooter"]
    output = "</td><td style='width: 200px; border-left: 1px dashed #D0E0FF; vertical-align: top; margin: 0; text-align: center;'>"
   
    if meta.has_key("extramenus"):
        mymenus = meta["extramenus"]
    else:
        mymenus = []
    mymenus.extend(menus)   
    
    for menu in mymenus:
        if menu.has_key("name"):
            output += "<h2 class=\"menuheader\">" + menu["name"] + "</h2>\n"
        else:
            output += "<br />\n";
        if menu.has_key("image"):
            output += "<img src=\"" + menu["image"] + "\" alt=\"" + menu["name"] + "\" />\n"

        output += "<p>"
        firstlink = True
        for (label, url, img) in menu["links"]:
            if firstlink:
                firstlink = False
            else:
                output += "<br />"
            
            output += "<a href=\"" + url + "\">" + label + "</a>"
        output += "</p>"
    output += """</td></tr>
<tr><td colspan="2" style="padding: 5px; border-top: 1px dotted #D0E0FF;"><p style="text-align: center; font-size: 70%;">Copyright (C) 2006 ronline.no-ip.info. All rights reserved.</p>""" + additionalfooter + "</td></tr>"
    return output
    
def formFooter(meta):
    return "</body>\n</html>"

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

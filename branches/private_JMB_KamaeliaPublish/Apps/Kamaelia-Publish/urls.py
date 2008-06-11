"""
This module contains the UrlList.  This is used to route requests to the proper
application by the WsgiHandler.  Please note that order DOES matter here.  The
URL matcher will use the first item in the list that it gets a match with.  In
particular, the .* element MUST be listed last.

You may use regular expressions here, but I'd reccommend not doing anything too
fancy unless you really know what you're doing.  I do reccommend placing ?/ in
front of and behind each item so that the items will match whether or not there
is a beginning or trailing slash
"""

UrlList = [
    ('/?simple/', 'WsgiApps.Apps.simple_app', 'simple_app', '/simple'),
    ('.*', 'WsgiApps.Apps.error_handler', 'application', '')
]

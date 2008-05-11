#!/usr/bin/env python
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
"""\
=============================
Parsing for URI request lines
=============================

This object parses a URI request line, such as those used in HTTP to request
data from a server.



Example
-------

::

    >>> r = requestLine("GET http://foo.bar.com/fwibble PROTO/3.3")
    >>> print parser.debug__str__()
    METHOD          :GET
    PROTOCOL        :PROTO
    VERSION         :3.3
    Req Type        :http
    USER            :
    PASSWORD        :
    DOMAIN          :foo.bar.com
    URL             :/fwibble
    >>> print r.domain
    foo.bar.com
"""
from Kamaelia.KamaeliaExceptions import BadRequest

class requestLine(object):
    """\
    requestLine(request) -> request object

    The URI request is processed. The components of the request are placed in
    these attributes:
    - method
    - protocol
    - reqprotocol
    - domain
    - url
    - user
    - passwd
    - version
    """
    def __init__(self,request):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        try:
            [self.method, rest] = request.split(" ",1)
            [self.reqprotocol, rest] = rest.split("://",1)
            [userdomain, rest] = rest.split("/",1)
            rest = "/" + rest # The leading / is significant
            try:
                [userpass,self.domain] = userdomain.split("@",1)
            except ValueError:
                [userpass,self.domain] = ["", userdomain]
            try:
                [self.user,self.passwd] = userpass.split(":",1)
            except ValueError:
                [self.user,self.passwd] = [userpass, ""]
            [self.url, protocolandver] = rest.split(" ", 1) # !!!! May well need changing due to Microsoft
            [self.protocol, self.version] = protocolandver.split("/",1)
        except Exception, e:
            raise BadRequest(request, e)

    def debug__str__(self):
        """Returns a multi line string listing all components of the request"""
        result =  "METHOD  \t:" + self.method + "\n" +\
            "PROTOCOL\t:" + self.protocol + "\n" +\
            "VERSION \t:" + self.version + "\n" +\
            "Req Type\t:" + self.reqprotocol + "\n" +\
            "USER    \t:" + self.user + "\n" +\
            "PASSWORD\t:" + self.passwd + "\n" +\
            "DOMAIN  \t:" + self.domain + "\n" +\
            "URL     \t:" + self.url
        return result

    def __str__(self):
        """Returns a reconstituted string representation of the original request"""
        result = ""
        result =  result + self.method + " "
        result =  result + self.reqprotocol + "://"
        if self.user:
            result =  result + self.user
            if self.passwd:
                result =  result + ":" + self.passwd
            result = result + "@"
        result =  result + self.domain
        result =  result + self.url +" "
        result =  result + self.protocol + "/"
        result =  result + self.version
        return result

if __name__ =="__main__":
    # These are the only format requests we accept. (Actually we only
    # accept the first 4, the 5th is not accepted.
    # All others are rejected
    requests = [
        "BIBBLE foo://toor:letmein@server.bigcompany.com/bla?this&that=other PROTO/3.3",
        "BIBBLE foo://toor@server.bigcompany.com/bla?this&that=other PROTO/3.3",
        "BIBBLE foo://server.bigcompany.com/bla?this&that=other PROTO/3.3",
        "BIBBLE foo://server.bigcompany.com/ PROTO/3.3",
        "foo://server.bigcompany.com/ PROTO/3.3"
        ]
    for REQ in requests:
        print "Parsing request:", REQ
        try:
            foo=requestLine(REQ)
        except BadRequest, e:
            foo= "Line is not parseable - does not match:\nMETHOD proto://(user(:passwd)?@)?domain/url proto/ver"
        print foo
        print

#!/usr/bin/env python2.3

from KamaeliaExceptions import BadRequest

class requestLine(object):
   def __init__(self,request):
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
      # These are the only format requests we accept.
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
         except "BadRequest":
            foo= "Line is not parseable - does not match:\nMETHOD proto://(user(:passwd)?@)?domain/url proto/ver"
         print foo
         print

class HTTPGetter(component):

    Inboxes = {
        "inbox" : "Receives a URL (and optional username and password) to get content from",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Sends out the retrieved raw data",
        "signal" : ""
    }

    def __init__(self, proxy = False, useragent = False):
        super(HTTPGetter, self).__init__()
        self.proxy = proxy
        self.useragent = useragent

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def getURLData(self, url, username = False, password = False):

        # Configure authentication
        if username and password:
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, username, password)
            authhandler = urllib2.HTTPBasicAuthHandler(passman)

        # Configure proxy and opener
        if username and password and self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            urlopener = urllib2.build_opener(authhandler, proxyhandler)
        elif username and password:
            urlopener = urllib2.build_opener(authhandler)
        elif self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            urlopener = urllib2.build_opener(proxyhandler)
        else:
            urlopener = urllib2.build_opener()

        # Get ready to grab data
        urllib2.install_opener(urlopener)
        if self.useragent:
            headers = {'User-Agent' : self.useragent}
        else:
            headers = ""

        # Grab data
        try:
            req = urllib2.Request(url,data,headers)
            conn1 = urllib2.urlopen(req)
        except httplib.BadStatusLine, e:
            return ["Error",str(e)]
            conn1 = False
        except urllib2.HTTPError, e:
            return ["HTTPError",str(e.code)]
            conn1= False
        except urllib2.URLError, e:
            return ['URLError',str(e.reason)]
            conn1 = False

        # Read and return programme data
        if conn1:
            content = conn1.read()
            conn1.close()
            return ["OK",content]

    def main(self):
        while not self.finished():
            if self.dataReady("inbox"):
                # Data format: [url,username(optional),password(optional)]
                request = self.recv("inbox")
                if len(request) == 3:
                    urldata = self.getURL(request[0],request[1],request[2])
                else:
                    urldata = self.getURL(request[0])
                # Data format: [OK/Error,message]
                self.send(urldata,"outbox")
            self.pause()
            yield 1
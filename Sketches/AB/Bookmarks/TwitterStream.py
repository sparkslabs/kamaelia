#! /usr/bin/python

# Interface to Twitter streaming API
# - Grabs JSON data based on chosen keywords
# - Currently also relays PIDs - this really needs moving elsewhere

import time
import urllib2
import urllib
import os
import cjson
import socket
from Axon.Ipc import producerFinished, shutdownMicroprocess

import oauth2 as oauth # TODO - Not fully implemented: Returns 401 unauthorised at the moment

from Axon.ThreadedComponent import threadedcomponent

class TwitterStream(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives lists containing keywords and PIDs - [[pid,pid],[keyword,keyword,keyword]]",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Sends out status messages from the streaming API connection",
        "signal" : "",
        "data" : "Sends out received tweets in the format [tweetjson,[pid,pid]]",
        "messages" : "Sends start and stop signals to ConnectionWatcher",
    }

    def __init__(self, username, password, proxy = False, reconnect = False):
        super(TwitterStream, self).__init__()
        self.proxy = proxy
        self.username = username
        self.password = password
        # Reconnect on failure?
        self.reconnect = reconnect
        timeout = 120
        socket.setdefaulttimeout(timeout) # Attempt to fix issues with streaming API connection hanging

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def kill(self):
        print ("running kill")
        self.g.throw(Exception)
        print ("ran kill")
        self.main()
        print ("ran main")
    # tried self.g.throw(Exception) but failed saying self.g was undefined

    def main_hack(self):
        twitterurl = "http://stream.twitter.com/1/statuses/filter.json"

        # Configure authentication for Twitter - temporary until OAuth implemented
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, twitterurl, self.username, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)

        # Configure proxy and opener
        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            twitopener = urllib2.build_opener(proxyhandler, authhandler)
        else:
            twitopener = urllib2.build_opener(authhandler)

        if 0: # 'Commented out' code for incomplete OAuth
            if self.keypair == False:
                while not self.dataReady("inbox"):
                    pass # Delay until sure the keypair will be saved

            try:
                homedir = os.path.expanduser("~")
                file = open(homedir + "/twitter-login.conf",'r')
                data = cjson.decode(file.read())
                self.keypair = [data['key'],data['secret']]
            except IOError, e:
                print ("Failed to load oauth keys for streaming API - exiting")
                sys.exit(0)

            params = {
                'oauth_version': "1.0",
                'oauth_nonce': oauth.generate_nonce(),
                'oauth_timestamp': int(time.time()),
                'user': self.username
            }

            consumer_key = '2kfk97VzNZQ36jOoZNvag'
            consumer_secret = 'Uye8ILqcBR3UpkbazSeezgIvlWKfRZcsU6YqPC1YYc'

            token = oauth.Token(key=self.keypair[0],secret=self.keypair[1])
            consumer = oauth.Consumer(key=consumer_key,secret=consumer_secret)

            params['oauth_token'] = token.key
            params['oauth_consumer_key'] = consumer.key

            req = oauth.Request(method="POST",url=twitterurl,parameters=params)

            signature_method = oauth.SignatureMethod_HMAC_SHA1()
            req.sign_request(signature_method, consumer, token)

            params['oauth_signature'] = req.get_parameter('oauth_signature')
            params['oauth_signature_method'] = req.get_parameter('oauth_signature_method')

        while not self.finished():
            if self.dataReady("inbox"):

                # Receive keywords and PIDs
                recvdata = self.recv("inbox")
                keywords = recvdata[0]

                # Abide by Twitter's keyword limit of 400
                if len(keywords) > 400:
                    keywords = keywords[0:400:1]
                    
                pids = recvdata[1]

                # Create POST data
                data = urllib.urlencode({"track": ",".join(keywords)})
                print ("Got keywords: " + data)

                # If using firehose, filtering based on keywords will be carried out AFTER grabbing data
                # This will be done here rather than by Twitter

                # Get ready to grab Twitter data
                urllib2.install_opener(twitopener)
                headers = {'User-Agent' : "BBC R&D Grabber"}

                # Connect to Twitter
                try:
                    req = urllib2.Request(twitterurl,data,headers)
                    conn1 = urllib2.urlopen(req)
                    print ("Connected to twitter stream. Awaiting data...")
                except urllib2.HTTPError, e:
                    self.send("Connect Error: " + str(e.code),"outbox") # TODO Errors get sent back to the requester
                    print(e.code)
                    conn1 = False
                except urllib2.URLError, e:
                    self.send("Connect Error: " + str(e.reason),"outbox") # TODO Errors get sent back to the requester
                    conn1 = False

                if conn1:
                    self.send("start","messages")
                    # While no new keywords have been passed in...
                    while not self.dataReady("inbox"):
                        # Collect data from the streaming API as it arrives - separated by carriage returns.
                        try:
                            content = ""
                            while not "\r\n" in content: # Twitter specified watch characters - readline doesn't catch this properly
                                content += conn1.read(1)
                            self.send([content,pids],"data") # Send to data collector / analyser rather than back to requester
                            failed = False
                        except IOError, e:
                            print str(e)
                            failed = True
                        except Axon.AxonExceptions.noSpaceInBox, e:
                            # Ignore data - no space to send out
                            failed = True
                            #self.send("Read Error: " + str(e),"outbox") # TODO: FIXME - Errors get sent back to the requester
                        if failed == True and self.reconnect == True:
                            # Reconnection procedure
                            print ("Streaming API connection failed.")
                            self.send("stop","messages")
                            conn1.close()
                            time.sleep(1)
                            try:
                                req = urllib2.Request(twitterurl,data,headers)
                                conn1 = urllib2.urlopen(req)
                                print ("Connected to twitter stream. Awaiting data...")
                                self.send("start","messages")
                            except urllib2.HTTPError, e:
                                self.send("Connect Error: " + str(e.code),"outbox") # Errors get sent back to the requester
                                print(e.code)
                                conn1 = False
                                break
                            except urllib2.URLError, e:
                                self.send("Connect Error: " + str(e.reason),"outbox") # Errors get sent back to the requester
                                conn1 = False
                                break
                    print ("Disconnecting from twitter stream.")
                    self.send("stop","messages")
                    if conn1:
                        conn1.close()
                    time.sleep(1) # TODO: Add in proper backoff algorithm and reconnection facility
                    # Reconnection util and backoff should really look at HTTP error codes

    def main(self):
        self.g = self.main_hack()
        for _ in self.g:
            pass
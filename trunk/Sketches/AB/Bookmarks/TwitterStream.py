#! /usr/bin/python

# Interface to Twitter streaming API
# - Grabs JSON data based on chosen keywords
# - Allows for reconnection on failure


import time
import urllib2
import urllib
import os
import cjson

import oauth2 as oauth # TODO - returns 401 unauthorised at the mo

from Axon.ThreadedComponent import threadedcomponent

class TwitterStream(threadedcomponent):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal", "data"]

    def __init__(self, username, password, proxy = False, reconnect = False):
        super(TwitterStream, self).__init__()
        self.proxy = proxy
        self.username = username
        #self.keypair = keypair
        self.password = password
        # Reconnect on failure?
        self.reconnect = reconnect # Not quite used yet

    def main(self):
        twitterurl = "http://stream.twitter.com/1/statuses/filter.json"

        # Configure authentication for Twitter
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # May not work any more using basic auth
        passman.add_password(None, twitterurl, self.username, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)

        # Configure proxy and opener
        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            twitopener = urllib2.build_opener(proxyhandler, authhandler)
        else:
            twitopener = urllib2.build_opener(authhandler)

        if 0:
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

        while 1:
            if self.dataReady("inbox"):
                recvdata = self.recv("inbox")
                keywords = recvdata[0]
                pids = recvdata[1]
                data = urllib.urlencode({"track": ",".join(keywords)})
                print ("Got keywords: " + data)
                # When using firehose, filtering based on keywords will be carried out AFTER grabbing data
                # This will be done here rather than by Twitter

                #test = req.get_normalized_parameters()
                #test = test + "&" + data


                #params['track'] = ",".join(keywords)

                #params = urllib.urlencode(params)
                # Get ready to grab Twitter data
                urllib2.install_opener(twitopener)
                headers = {'User-Agent' : "BBC R&D Grabber"}
                #print params
                # Grab twitter data
                try:
                    req = urllib2.Request(twitterurl,data,headers)
                    conn1 = urllib2.urlopen(req)
                    print ("Connected to twitter stream. Awaiting data...")
                except urllib2.HTTPError, e:
                    self.send("Connect Error: " + str(e.code),"outbox") # Errors get sent back to the requester
                    print(e.code)
                    conn1 = False
                except urllib2.URLError, e:
                    self.send("Connect Error: " + e.reason,"outbox") # Errors get sent back to the requester
                    conn1 = False

                if conn1:
                    while not self.dataReady("inbox"):
                        try:
                            content = ""
                            while not "\n" in content:
                                content += conn1.read(1)
                            #content = conn1.readline()
                            self.send([content,pids],"data") # Send to data collector / analyser rather than back to requester
                            # What is message size limit on inboxes - could be getting flooded in just one send
                        except IOError, e:
                            print str(e)
                            break # TODO: FIXME
                        except Axon.AxonExceptions.noSpaceInBox, e:
                            pass # Ignore data - no space
                            #self.send("Read Error: " + str(e),"outbox") # TODO: FIXME - Errors get sent back to the requester
                    print ("Disconnecting from twitter stream.")
                    conn1.close()
                    time.sleep(1) # TODO: Add in proper backoff algorithm and reconnection facility
                    # Reconnection util and backoff need to look at HTTP error codes
                    
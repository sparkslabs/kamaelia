#! /usr/bin/python

# Interface to Twitter streaming API
# - Grabs JSON data based on chosen keywords
# - Currently also relays PIDs - this really needs moving elsewhere
# TODO: Add watching for in-stream rate limiting / error messages
# - Doesn't currently honour tweet deletion messages (TODO)

import time
import urllib2
import urllib
import sys
import os
import cjson
import socket
from Axon.Ipc import producerFinished, shutdownMicroprocess
from threading import Timer
import Axon
import httplib

import oauth2 as oauth # TODO - Not fully implemented: Returns 401 unauthorised at the moment
# The 401 *may* be down to using the same stored received key and secret as the search component, but I would have thought this to be fine
import urlparse

from Axon.ThreadedComponent import threadedcomponent

class TwitterStream(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives lists containing keywords and PIDs - [[pid,pid],[keyword,keyword,keyword]]",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Sends out received tweets in the format [tweetjson,[pid,pid]]",
        "signal" : "",
    }

    def __init__(self, username, consumerkeypair, keypair, proxy = False, reconnect = False, timeout = 120):
        super(TwitterStream, self).__init__()
        self.proxy = proxy
        self.username = username
        #self.password = password
        self.consumerkeypair = consumerkeypair
        self.keypair = keypair
        # Reconnect on failure?
        self.reconnect = reconnect
        # In theory this won't matter, but add a timeout to be safe anyway
        self.timeout = timeout
        socket.setdefaulttimeout(self.timeout)
        self.backofftime = 1

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
        
    def getOAuth(self, consumer_key, consumer_secret):
        # Perform OAuth authentication
        request_token_url = 'http://api.twitter.com/oauth/request_token'
        access_token_url = 'http://api.twitter.com/oauth/access_token'
        authorize_url = 'http://api.twitter.com/oauth/authorize'

        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        resp, content = client.request(request_token_url, "POST")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))

        print "Request Token:"
        print "     - oauth_token        = %s" % request_token['oauth_token']
        print "     - oauth_token_secret = %s" % request_token['oauth_token_secret']
        print

        # The user must confirm authorisation so a URL is printed here
        print "Go to the following link in your browser:"
        print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
        print

        accepted = 'n'
        # Wait until the user has confirmed authorisation
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')
        oauth_verifier = raw_input('What is the PIN? ')

        token = oauth.Token(request_token['oauth_token'],
            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer,token)

        resp, content = client.request(access_token_url, "POST", body="oauth_verifier=%s" % oauth_verifier)
        access_token = dict(urlparse.parse_qsl(content))

        # Access tokens retrieved from Twitter
        print "Access Token:"
        print "     - oauth_token        = %s" % access_token['oauth_token']
        print "     - oauth_token_secret = %s" % access_token['oauth_token_secret']
        print
        print "You may now access protected resources using the access tokens above."
        print

        save = False
        # Load config to save OAuth keys
        try:
            homedir = os.path.expanduser("~")
            file = open(homedir + "/twitter-login.conf",'r')
            save = True
        except IOError, e:
            print ("Failed to load config file - not saving oauth keys: " + str(e))

        if save:
            raw_config = file.read()

            file.close()

            # Read config and add new values
            config = cjson.decode(raw_config)
            config['key'] = access_token['oauth_token']

            config['secret'] = access_token['oauth_token_secret']

            raw_config = cjson.encode(config)

            # Write out the new config file
            try:
                file = open(homedir + "/twitter-login.conf",'w')
                file.write(raw_config)
                file.close()
            except IOError, e:
                print ("Failed to save oauth keys: " + str(e))
        
        return [access_token['oauth_token'], access_token['oauth_token_secret']]

    def main(self):
        twitterurl = "http://stream.twitter.com/1/statuses/filter.json"

        # Check if OAuth has been done before - if so use the keys from the config file
        if self.keypair == False:
            self.keypair = self.getOAuth(self.consumerkeypair[0], self.consumerkeypair[1])

        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            twitopener = urllib2.build_opener(proxyhandler)
            urllib2.install_opener(twitopener)


        while not self.finished():
            if self.dataReady("inbox"):

                params = {
                    'oauth_version': "1.0",
                    'oauth_nonce': oauth.generate_nonce(),
                    'oauth_timestamp': int(time.time()),
                    'user': self.username
                }

                token = oauth.Token(key=self.keypair[0],secret=self.keypair[1])
                consumer = oauth.Consumer(key=self.consumerkeypair[0],secret=self.consumerkeypair[1])

                params['oauth_token'] = token.key
                params['oauth_consumer_key'] = consumer.key

                req = oauth.Request(method="POST",url=twitterurl,parameters=params)

                signature_method = oauth.SignatureMethod_HMAC_SHA1()
                req.sign_request(signature_method, consumer, token)

                params['oauth_signature'] = req.get_parameter('oauth_signature')
                params['oauth_signature_method'] = req.get_parameter('oauth_signature_method')

                # Receive keywords and PIDs
                recvdata = self.recv("inbox")
                keywords = recvdata[0]

                requesturl = req.to_url()

                # Abide by Twitter's keyword limit of 400
                if len(keywords) > 400:
                    sys.stderr.write('TwitterStream keyword list too long - sending shortened list')
                    keywords = keywords[0:400:1]
                    
                pids = recvdata[1]

                # Create POST data
                data = urllib.urlencode({"track": ",".join(keywords)})
                print ("Got keywords: " + data)

                # If using firehose, filtering based on keywords will be carried out AFTER grabbing data
                # This will be done here rather than by Twitter
                
                # Identify the client and add a keep alive message using the same timeout assigned to the socket
                headers = {'User-Agent' : "BBC R&D Grabber", "Keep-Alive" : self.timeout, "Connection" : "Keep-Alive"}

                # Add OAuth parameters to headers
                oauthlist = ""
                for key in params:
                    oauthlist += key + "=\"" + str(params[key]) + "\", "

                headers['OAuth'] = oauthlist.rstrip(", ")
                print headers
                print requesturl
                # Connect to Twitter
                try:
                    req = urllib2.Request(requesturl,data,headers)
                    conn1 = urllib2.urlopen(req,None,self.timeout)
                    self.backofftime = 1 # Reset the backoff time
                    print ("Connected to twitter stream. Awaiting data...")
                except httplib.BadStatusLine, e:
                    sys.stderr.write('TwitterStream BadStatusLine error: ' + str(e) + '\n')
                    # General network error assumed - short backoff
                    self.backofftime += 1
                    if self.backofftime > 16:
                        self.backofftime = 16
                    conn1 = False
                except urllib2.HTTPError, e:
                    sys.stderr.write('TwitterStream HTTP error: ' + str(e.code) + '\n')
                    sys.stderr.write('TwitterStream HTTP error: See http://dev.twitter.com/pages/streaming_api_response_codes \n')
                    if e.code == 401:
                        sys.stderr.write('TwitterStream HTTP error: Your access tokens may have expired. \n')
                    # Major error assumed - long backoff
                    if e.code > 200:
                        if self.backofftime == 1:
                            self.backofftime = 10
                        else:
                            self.backofftime *= 2
                        if self.backofftime > 240:
                            self.backofftime = 240
                    conn1 = False
                except urllib2.URLError, e:
                    sys.stderr.write('TwitterStream URL error: ' + str(e.reason) + '\n')
                    # General network error assumed - short backoff
                    self.backofftime += 1
                    if self.backofftime > 16:
                        self.backofftime = 16
                    conn1 = False
                except socket.timeout, e:
                    sys.stderr.write('TwitterStream socket timeout: ' + str(e) + '\n')
                    # General network error assumed - short backoff
                    self.backofftime += 1
                    if self.backofftime > 16:
                        self.backofftime = 16
                    conn1 = False

                if conn1:
                    # While no new keywords have been passed in...
                    while not self.dataReady("inbox"):
                        # Collect data from the streaming API as it arrives - separated by carriage returns.
                        try:
                            content = ""
                            # Timer attempt to fix connection hanging
                            # Could possibly force this to generate an exception otherwise - can't be sure if that will stop the read though
                            readtimer = Timer(self.timeout,conn1.close)
                            readtimer.start()
                            while not "\r\n" in content: # Twitter specified watch characters - readline doesn't catch this properly
                                content += conn1.read(1)
                                # Trying to work out what content is set to at the point it fails
                                filepath = "contentDebug.txt"
                                file = open(filepath, 'w')
                                file.write(content)
                                file.close()
                            readtimer.cancel()
                            self.send([content,pids],"outbox") # Send to data collector / analyser rather than back to requester
                            failed = False
                        except IOError, e:
                            sys.stderr.write('TwitterStream IO error: ' + str(e) + '\n')
                            failed = True
                        except Axon.AxonExceptions.noSpaceInBox, e:
                            # Ignore data - no space to send out
                            sys.stderr.write('TwitterStream no space in box error: ' + str(e) + '\n')
                            failed = True
                        except socket.timeout, e:
                            sys.stderr.write('TwitterStream socket timeout: ' + str(e) + '\n')
                            # General network error assumed - short backoff
                            self.backofftime += 1
                            if self.backofftime > 16:
                                self.backofftime = 16
                            failed = True
                        if failed == True and self.reconnect == True:
                            # Reconnection procedure
                            print ("Streaming API connection failed.")
                            conn1.close()
                            if self.backofftime > 1:
                                print ("Backing off for " + str(self.backofftime) + " seconds.")
                            time.sleep(self.backofftime)
                            print ("Attempting reconnection...")
                            try:
                                req = urllib2.Request(twitterurl,data,headers)
                                conn1 = urllib2.urlopen(req,None,self.timeout)
                                self.backofftime = 1
                                print ("Connected to twitter stream. Awaiting data...")
                            except httplib.BadStatusLine, e:
                                sys.stderr.write('TwitterStream BadStatusLine error: ' + str(e) + '\n')
                                # General network error assumed - short backoff
                                self.backofftime += 1
                                if self.backofftime > 16:
                                    self.backofftime = 16
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                            except urllib2.HTTPError, e:
                                sys.stderr.write('TwitterStream HTTP error: ' + str(e.code) + '\n')
                                sys.stderr.write('TwitterStream HTTP error: See http://dev.twitter.com/pages/streaming_api_response_codes \n')
                                if e.code == 401:
                                    sys.stderr.write('TwitterStream HTTP error: Your access tokens may have expired. \n')
                                # Major error assumed - long backoff
                                if e.code > 200:
                                    if self.backofftime == 1:
                                        self.backofftime = 10
                                    else:
                                        self.backofftime *= 2
                                    if self.backofftime > 240:
                                        self.backofftime = 240
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                            except urllib2.URLError, e:
                                sys.stderr.write('TwitterStream URL error: ' + str(e.reason) + '\n')
                                # General network error assumed - short backoff
                                self.backofftime += 1
                                if self.backofftime > 16:
                                    self.backofftime = 16
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                            except socket.timeout, e:
                                sys.stderr.write('TwitterStream socket timeout: ' + str(e) + '\n')
                                # General network error assumed - short backoff
                                self.backofftime += 1
                                if self.backofftime > 16:
                                    self.backofftime = 16
                                conn1 = False
                                # Reconnection failed - must break out and wait for new keywords
                                break
                    print ("Disconnecting from twitter stream.")
                    if conn1:
                        conn1.close()
                    if self.backofftime > 1:
                        print ("Backing off for " + str(self.backofftime) + " seconds.")
                    time.sleep(self.backofftime)
    
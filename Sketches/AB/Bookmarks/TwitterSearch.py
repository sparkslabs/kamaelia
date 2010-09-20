#! /usr/bin/python

# Interface to Twitter search API
# - Returns results of people searches as a dictionary
# TODO: If it's found that regularly different people have the same name, relate the twitter names found to particular PIDs / Brand PIDs too?

import urllib2
import urllib
import time
import os
import cjson
import string
from datetime import datetime,timedelta

import urlparse
import oauth2 as oauth

from Axon.Component import component

# TODO: Rate limit checking!

class PeopleSearch(component):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self, username, keypair, proxy = False):
        super(PeopleSearch, self).__init__()
        self.proxy = proxy
        self.keypair = keypair
        self.username = username
        self.ratelimited = datetime.today() - timedelta(minutes=15)

    def getOAuth(self, consumer_key, consumer_secret):
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

        print "Go to the following link in your browser:"
        print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
        print

        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')
        oauth_verifier = raw_input('What is the PIN? ')

        token = oauth.Token(request_token['oauth_token'],
            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer,token)

        resp, content = client.request(access_token_url, "POST", body="oauth_verifier=%s" % oauth_verifier)
        access_token = dict(urlparse.parse_qsl(content))

        print "Access Token:"
        print "     - oauth_token        = %s" % access_token['oauth_token']
        print "     - oauth_token_secret = %s" % access_token['oauth_token_secret']
        print
        print "You may now access protected resources using the access tokens above."
        print

        save = False
        # Load Config
        try:
            homedir = os.path.expanduser("~")
            file = open(homedir + "/twitter-login.conf",'r')
            save = True
        except IOError, e:
            print ("Failed to load config file - not saving oauth keys: " + str(e))

        if save:
            raw_config = file.read()

            file.close()

            # Read Config
            config = cjson.decode(raw_config)
            #if config.has_key('key'):
            #    config['key'].append(access_token['oauth_token'])
            #else:
            config['key'] = access_token['oauth_token']

            #if config.has_key('secret'):
            #    config['secret'].append(access_token['oauth_token_secret'])
            #else:
            config['secret'] = access_token['oauth_token_secret']

            raw_config = cjson.encode(config)

            try:
                file = open(homedir + "/twitter-login.conf",'w')
                file.write(raw_config)
                file.close()
            except IOError, e:
                print ("Failed to save oauth keys: " + str(e))
        
        return [access_token['oauth_token'], access_token['oauth_token_secret']]

    def main(self):
        twitterurl = "http://api.twitter.com/1/users/search.json"

        consumer_key = '2kfk97VzNZQ36jOoZNvag'
        consumer_secret = 'Uye8ILqcBR3UpkbazSeezgIvlWKfRZcsU6YqPC1YYc'

        if self.keypair == False:
            self.keypair = self.getOAuth(consumer_key, consumer_secret)

        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            twitopener = urllib2.build_opener(proxyhandler)
            urllib2.install_opener(twitopener)

        #headers = {'User-Agent' : "BBC R&D Grabber"}
        #data = ""
        

        while 1:
            # TODO: Watch rate limit of 60 per hour in search headers
            # TODO: Implement backoff algorithm in case of connection failures - watch out for the fact this could delay the requester component
            if self.dataReady("inbox"):
                if (datetime.today() - timedelta(minutes=15)) > self.ratelimited:
                    person = self.recv("inbox")

                    #print person
                    requesturl = twitterurl + "?q=" + urllib.quote(person) + "&per_page=5"
                    #print requesturl

                    params = {
                        'oauth_version': "1.0",
                        'oauth_nonce': oauth.generate_nonce(),
                        'oauth_timestamp': int(time.time()),
                        'user': self.username
                    }

                    token = oauth.Token(key=self.keypair[0],secret=self.keypair[1])
                    consumer = oauth.Consumer(key=consumer_key,secret=consumer_secret)

                    params['oauth_token'] = token.key
                    params['oauth_consumer_key'] = consumer.key

                    req = oauth.Request(method="GET",url=requesturl,parameters=params)

                    signature_method = oauth.SignatureMethod_HMAC_SHA1()
                    req.sign_request(signature_method, consumer, token)

                    requesturl = req.to_url()


                    if 1:
                        # Grab twitter data
                        try:
                            #req = urllib2.Request(requesturl,data,headers)
                            conn1 = urllib2.urlopen(requesturl)
                        except urllib2.HTTPError, e:
                            self.send("HTTP Error: " + str(e.code),"outbox") # Errors get sent back to the requester
                            conn1 = False
                        except urllib2.URLError, e:
                            self.send("Connect Error: " + e.reason,"outbox") # Errors get sent back to the requester
                            conn1 = False

                        if conn1:
                            headers = conn1.info() # Manual place to watch rate limit for now
                            headerlist = string.split(str(headers),"\n")
                            for line in headerlist:
                                splitheader = string.split(line," ")
                                if splitheader[0] == "X-FeatureRateLimit-Remaining:":
                                    print splitheader[0] + " " + str(splitheader[1])
                                    if splitheader[1] < 5:
                                        self.ratelimited = datetime.today()
                                    break
                            try:
                                data = conn1.read()
                                try:
                                    content = cjson.decode(data)
                                    self.send(content,"outbox")
                                except cjson.DecodeError, e:
                                    self.send(dict(),"outbox")
                            except IOError, e:
                                self.send("Read Error: " + str(e),"outbox") # TODO: FIXME - Errors get sent back to the requester
                            conn1.close()
                else:
                   print "Twitter search paused - rate limited"                
            self.pause()
            yield 1

'''
These are a set of test components aiming to translate retweets using 'RT @' into the proper form
and provide the option to strip user mentions, hashtags and links from tweet text.
Links can also be resolved to their real URL - particularly helpful for finding hidden PIDs
'''

raise NotImplementedError("Needs fixing due to MySQLdb  -- python 2.0 based -- MySQLdb")
import json as cjson
import os
import re
import MySQLdb
import urllib2

from Axon.Component import component
from Axon.Ipc import producerFinished
from Axon.Ipc import shutdownMicroprocess

from Kamaelia.Apps.SocialBookmarks.Print import Print
from Kamaelia.Apps.SocialBookmarks.DBWrapper import DBWrapper

class RetweetFixer(component):
    '''
    # Steps:
    # - Receives tweet dictionary via 'inbox'
    # - Checks to see if retweeted_status key is set
    # - If it isn't, looks for mentions of 'RT @PersonName:' (or 'via @PersonName' - at a later date)
    # - Adds a retweeted_status key including as much information that can be gleaned from the tweet text as possible
    # - Sends the tweet dictionary back via 'outbox'
    '''

    Inboxes = {
        "inbox" : "Receives tweet dict which may need its retweets fixing",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "Sends out fixed dict",
        "signal" : "",
    }

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):
        while not self.finished():
            while self.dataReady("inbox"):
                tweet = self.recv("inbox")
                if not ("retweeted_status" in tweet):
                    # Need to find the last match for an accurate retweet
                    rtresults = ""
                    usermention = ""
                    newtweettext = tweet['text']
                    while rtresults != None:
                        rtresults = re.match("((^|\s)(RT|rt|Rt|rT)(\s@\S{1,}))",newtweettext,re.I)
                        if rtresults != None:
                            newtweettext = newtweettext.replace(rtresults.group(),"").strip()
                            for entry in tweet['entities']['user_mentions']:
                                if entry['indices'][0] > rtresults.start() and entry['indices'][1] <= rtresults.end():
                                    usermention = entry['screen_name']
                                    name = entry['name']
                                    id = entry['id']

                    rtlength = len(tweet['text']) - len(newtweettext)
                    if usermention != "":
                        indices = [tweet['text'].find(newtweettext),tweet['text'].find(newtweettext)+len(newtweettext)]
                        entities = {"user_mentions":list(),"urls":list(),"hashtags":list()}
                        for item in tweet['entities']['user_mentions']:
                            if item['indices'][0] >= indices[0] and item['indices'][1] <= indices[1]:
                                tempitem = item.copy()
                                tempitem['indices'] = [item['indices'][0]-rtlength,item['indices'][1]-rtlength]
                                entities['user_mentions'].append(tempitem)
                        for item in tweet['entities']['urls']:
                            if item['indices'][0] >= indices[0] and item['indices'][1] <= indices[1]:
                                tempitem = item.copy()
                                tempitem['indices'] = [item['indices'][0]-rtlength,item['indices'][1]-rtlength]
                                entities['urls'].append(tempitem)
                        for item in tweet['entities']['hashtags']:
                            if item['indices'][0] >= indices[0] and item['indices'][1] <= indices[1]:
                                tempitem = item.copy()
                                tempitem['indices'] = [item['indices'][0]-rtlength,item['indices'][1]-rtlength]
                                entities['hashtags'].append(tempitem)
                        tweet['retweeted_status'] = {"user": {"id": id,"screen_name": usermention,"name": name}, "text": newtweettext, "entities": entities}

                self.send(tweet,"outbox")
                
            self.pause()
            yield 1

class RetweetCorrector(DBWrapper,component):
    '''
    This is a DB specific retweet fixer - the idea being to correct the retweet ID and text properly
    '''

    Inboxes = {
        "inbox" : "Receives tweet dict which may need elements removing",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "Sends out fixed dict",
        "signal" : "",
    }

    def __init__(self,dbuser,dbpass):
        super(RetweetCorrector, self).__init__(dbuser=dbuser,dbpass=dbpass)

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):

        self.dbConnect()

        while not self.finished():
            while self.dataReady("inbox"):
                tweetjson = self.recv("inbox")

                if ("retweeted_status" in tweetjson):
                    # Find this tweet's PIDs
                    self.db_select("""SELECT pid FROM rawdata WHERE tweet_id = %s""",(tweetjson['id']))
                    pids = self.db_fetchall()
                    breaker = False
                    for pid in pids:
                        tweettext = tweetjson['retweeted_status']['text']
                        if not ( "id" in tweetjson['retweeted_status'] ):
                            # This is a fixed retweet - let's try and fix it further by identifying the original
                            # Only worth doing for the same PID
                            self.db_select("""SELECT text,tweet_id FROM rawdata WHERE user = %s AND pid = %s""",(tweetjson['retweeted_status']['user']['screen_name'],pid[0]))
                            dataset = self.db_fetchall()
                            for row in dataset:
                                if row[0] == tweettext:
                                    # Tweet text is the same - add the ID
                                    tweetjson['retweeted_status']['id'] = row[1]
                                    breaker = True
                                    break
                                if len(row[0]) > len(tweettext) and len(tweettext) > 3:
                                    if tweettext[:-3] in row[0]:
                                        # Tweet text is the same but trimmed (allows for ... on the end too)
                                        tweetjson['retweeted_status']['id'] = row[1]
                                        tweetjson['retweeted_status']['text'] = row[0]
                                        tweetjson['text'] = tweetjson['text'].replace(tweettext,row[0])
                                        breaker = True
                                        break
                            if breaker:
                                # No need to check any further - found it
                                break

                self.send(tweetjson,"outbox")

            self.pause()
            yield 1


class TweetCleaner(component):
    '''
    # Steps:
    # - Receives tweet dictionary via 'inbox'
    # - Looks at 'self.filter' to determine what needs removing from the tweet text (selected from user_mentions,urls and/or hashtags)
    # - Uses the indices specified by Twitter to determine where these elements reside and to remove them
    # - Adds a new key to the tweet dictionary containing this 'filtered_text' (useful for NLTK analysis without Twitter specific content)
    # - Sends the tweet dictionary back via 'outbox'
    '''

    Inboxes = {
        "inbox" : "Receives tweet dict which may need elements removing",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "Sends out fixed dict",
        "signal" : "",
    }

    def __init__(self,filters):
        super(TweetCleaner, self).__init__()
        self.filters = filters

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def filterEntity(self,tweet):
        removallist = list()
        if "user_mentions" in self.filters:
           for item in tweet['entities']['user_mentions']:
               removallist.append(item['indices'])
        if "urls" in self.filters:
           for item in tweet['entities']['urls']:
               removallist.append(item['indices'])
        if "hashtags" in self.filters:
           for item in tweet['entities']['hashtags']:
               removallist.append(item['indices'])

        tweettext = tweet['text']
        newtweettext = ""
        index = 0
        for item in sorted(removallist):
            newtweettext += tweettext[index:item[0]]
            index = item[1]
        if len(tweettext) > index:
            newtweettext += tweettext[index:len(tweettext)]

        newtweettext = re.sub("\s{2,}"," ",newtweettext,re.I)

        return newtweettext.strip()

    def main(self):
        # possible filters: user_mentions, urls, hashtags
        while not self.finished():
            while self.dataReady("inbox"):
                tweet = self.recv("inbox")

                tweet['filtered_text'] = self.filterEntity(tweet)

                if ( "retweeted_status" in tweet ):
                    tweet['retweeted_status']['filtered_text'] = self.filterEntity(tweet['retweeted_status'])

                self.send(tweet,"outbox")

            self.pause()
            yield 1

class LinkResolver(component):
    '''
    # Steps:
    # - Receives tweet dictionary via 'inbox'
    # - Looks at the ['entities']['urls'] elements to identify if URLs have their 'expanded_url' elements set.
    # - If these elements aren't set, bit.ly's API is checked to itentify the real URL
    # - The 'expanded_url' key is modified for each URL given the bit.ly result
    # - Sends the tweet dictionary back via 'outbox'
    '''

    Inboxes = {
        "inbox" : "Receives tweet dict which may need links resolving",
        "responses" : "Received HTTP request responses",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "Sends out fixed dict",
        "urlrequests" : "Sends out URLs for HTTP requests",
        "signal" : "",
    }

    def __init__(self,username,apikey):
        super(LinkResolver, self).__init__()
        self.username = username
        self.apikey = apikey

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):
        while not self.finished():
            while self.dataReady("inbox"):
                tweet = self.recv("inbox")
                linkstoresolve = list()
                for url in tweet['entities']['urls']:
                    if url['expanded_url'] == None and "bbc.in" in url['url']:
                        linkstoresolve.append(url['url'])
                if ( "retweeted_status" in tweet ):
                    for url in tweet['retweeted_status']['entities']['urls']:
                        if url['expanded_url'] == None and "bbc.in" in url['url']:
                            linkstoresolve.append(url['url'])
                if len(linkstoresolve) > 0:
                    # Load the cache
                    homedir = os.path.expanduser("~")
                    linkcache = dict()
                    try:
                        homedir = os.path.expanduser("~")
                        file = open(homedir + "/linkcache.conf",'r')
                        raw_cache = file.read()
                        try:
                            linkcache = cjson.decode(raw_cache)
                        except cjson.DecodeError:
                            e =sys.exc_info()[1]
                            Print ("Failed to decode link cache - will attempt to create a new file: " , e)
                    except IOError:
                        e = sys.exc_info()[1]
                        Print ("Failed to load link cache - will attempt to create a new file: " , e)

                    linkstring = ""
                    for link in linkstoresolve:
                        if not ( link in linkcache) :
                            # Need to look this link up, add it to the list
                            linkstring += "&shortUrl=" + urllib2.quote(link.encode("utf8")) # Otherwise all sorts of things break badly...

                    if linkstring != "":
                        url = "http://api.bit.ly/v3/expand?login=" + self.username + "&apiKey=" + self.apikey + "&format=json"
                        url += linkstring
                        Print("Sending Request", url)
                        self.send([url],"urlrequests")
                        while not self.dataReady("responses"):
                            self.pause()
                            yield 1
                        response = self.recv("responses")
                        if response[0] == "OK":
                            try:
                                decodedresponse = cjson.decode(response[1])
                                if decodedresponse['status_txt'] == "OK":
                                    for resolvedlink in decodedresponse['data']['expand']:
                                        if ( "long_url" in resolvedlink) and ("short_url" in resolvedlink):
                                            # Resolution was successful for this link
                                            long_url = resolvedlink['long_url'].replace("\\/","/")
                                            short_url = resolvedlink['short_url'].replace("\\/","/")
                                            linkcache[short_url] = long_url
                            except cjson.DecodeError:
                                e = sys.exc_info()[1]
                                Print ("Decode error in result from bit.ly: " , e)

                    # Set the expanded URL fields in the tweet entity
                    for url in tweet['entities']['urls']:
                        if url['expanded_url'] == None and ( url['url'] in linkcache ):
                            url['expanded_url'] = linkcache[url['url']]

                    if ("retweeted_status" in tweet):
                        for url in tweet['retweeted_status']['entities']['urls']:
                            if url['expanded_url'] == None and ( url['url'] in linkcache):
                                url['expanded_url'] = linkcache[url['url']]

                    try:
                        file = open(homedir + "/linkcache.conf",'w')
                        raw_cache = cjson.encode(linkcache)
                        file.write(raw_cache)
                        file.close()
                    except IOError:
                        e = sys.exc_info()[1]
                        Print ("Failed to save name cache - could cause rate limit problems")
                        
                self.send(tweet,"outbox")

            self.pause()
            yield 1




if __name__ == "__main__":
    import sys

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    from Kamaelia.Apps.SocialBookmarks.URLGetter import HTTPGetter

    # This function won't live here - it's for testing only
    def spellingFixer(text):
        # Fix ahahahahahaha and hahahahaha
        text = re.sub("\S{0,}(ha){2,}\S{0,}","haha",text,re.I)
        # fix looooooool and haaaaaaaaaaa - fails for some words at the mo, for example welllll will be converted to wel, and hmmm to hm etc
        # Perhaps we could define both 'lol' and 'lool' as words, then avoid the above problem by reducing repeats to a max of 2
        x = re.findall(r'((\D)\2*)',text,re.I)
        for entry in sorted(x,reverse=True):
            if len(entry[0])>2:
                text = text.replace(entry[0],entry[1]).strip()
            if len(text) == 1:
                text += text
        return text

    # Load Config
    try:
        homedir = os.path.expanduser("~")
        file = open(homedir + "/twitter-login.conf")
    except IOError:
        e = sys.exc_info()[1]
        Print ("Failed to load login data - exiting")
        sys.exit(0)

    raw_config = file.read()
    file.close()

    # Read Config
    config = cjson.decode(raw_config)
    bitlyusername = config['bitlyusername']
    bitlyapikey = config['bitlyapikey']
    proxy = config['proxy']

    READER = ConsoleReader()
    DECODER = PureTransformer(lambda x: cjson.decode(x))
    CLEANER = TweetCleaner(['user_mentions','urls','hashtags'])
    WRITER = ConsoleEchoer()
    FIXER = RetweetFixer()
    SPELLING = PureTransformer(lambda x: spellingFixer(x))
    LINKER = LinkResolver(bitlyusername,bitlyapikey)
    REQUESTER = HTTPGetter(proxy, "BBC R&D Grabber")

    if 0:
        Pipeline(READER,DECODER,CLEANER,WRITER).run()

    if 0:
        Pipeline(READER,DECODER,FIXER,WRITER).run()

    if 0:
        Graphline(READER=READER,DECODER=DECODER,LINKER=LINKER,REQUESTER=REQUESTER,WRITER=WRITER,
                linkages = {("READER", "outbox") : ("DECODER", "inbox"),
                            ("DECODER", "outbox") : ("LINKER", "inbox"),
                            ("LINKER", "urlrequests") : ("REQUESTER", "inbox"),
                            ("REQUESTER", "outbox") : ("LINKER", "responses"),
                            ("LINKER", "outbox") : ("WRITER", "inbox"),}).run()

    if 1:
        Graphline(READER=READER,DECODER=DECODER,LINKER=LINKER,REQUESTER=REQUESTER,FIXER=FIXER,CLEANER=CLEANER,WRITER=WRITER,
                linkages = {("READER", "outbox") : ("DECODER", "inbox"),
                            ("DECODER", "outbox") : ("FIXER", "inbox"),
                            ("FIXER", "outbox") : ("LINKER", "inbox"),
                            ("LINKER", "urlrequests") : ("REQUESTER", "inbox"),
                            ("REQUESTER", "outbox") : ("LINKER", "responses"),
                            ("LINKER", "outbox") : ("CLEANER", "inbox"),
                            ("CLEANER", "outbox") : ("WRITER", "inbox"),}).run()

    if 0:
        Pipeline(READER,SPELLING,WRITER).run()
    

# EXAMPLE TWEETS:
#{"new_id_str":"610915840165945344","text":"RT @BBCBreaking: Dilma Rousseff is elected to succeed  Luiz Inacio Lula da Silva, becoming Brazil's first female president.\n\n http://www ...","id_str":"29385702704","truncated":true,"in_reply_to_status_id_str":null,"new_id":610915840165945344,"entities":{"user_mentions":[{"id_str":"5402612","indices":[3,15],"name":"BBC Breaking News","screen_name":"BBCBreaking","id":5402612}],"urls":[],"hashtags":[]},"place":null,"favorited":false,"in_reply_to_user_id_str":null,"coordinates":null,"source":"web","contributors":null,"geo":null,"in_reply_to_screen_name":null,"in_reply_to_status_id":null,"retweeted_status":{"text":"Dilma Rousseff is elected to succeed  Luiz Inacio Lula da Silva, becoming Brazil's first female president.\n\n http://www.bbc.co.uk/news","id_str":"29359216766","truncated":false,"in_reply_to_status_id_str":null,"entities":{"user_mentions":[],"urls":[{"indices":[109,134],"expanded_url":null,"url":"http://www.bbc.co.uk/news"}],"hashtags":[]},"place":null,"favorited":false,"in_reply_to_user_id_str":null,"coordinates":null,"source":"\u003Ca href=\"http://twitterfeed.com\" rel=\"nofollow\"\u003Etwitterfeed\u003C/a\u003E","contributors":null,"geo":null,"in_reply_to_screen_name":null,"in_reply_to_status_id":null,"retweet_count":null,"created_at":"Mon Nov 01 10:25:03 +0000 2010","user":{"lang":"en","id_str":"5402612","listed_count":25710,"following":null,"profile_background_tile":false,"profile_background_color":"ffffff","statuses_count":1163,"show_all_inline_media":false,"profile_use_background_image":true,"profile_text_color":"5a5a5a","description":"Breaking news alerts from the BBC. ","contributors_enabled":false,"geo_enabled":false,"profile_link_color":"1f527b","location":"London, UK","notifications":null,"friends_count":0,"verified":false,"favourites_count":0,"profile_sidebar_fill_color":"ffffff","protected":false,"profile_image_url":"http://a0.twimg.com/profile_images/1143158124/BBC_avatar_normal.jpg","follow_request_sent":null,"time_zone":"London","created_at":"Sun Apr 22 14:42:37 +0000 2007","name":"BBC Breaking News","profile_sidebar_border_color":"cccccc","url":"http://www.bbc.co.uk/news","screen_name":"BBCBreaking","id":5402612,"profile_background_image_url":"http://a3.twimg.com/profile_background_images/160789431/bbc_twitter_template1280b.jpg","utc_offset":0,"followers_count":664048},"retweeted":false,"in_reply_to_user_id":null,"id":29359216766},"retweet_count":null,"created_at":"Mon Nov 01 16:11:40 +0000 2010","user":{"lang":"en","id_str":"88119648","listed_count":0,"following":null,"profile_background_tile":true,"profile_background_color":"C6E2EE","statuses_count":38,"show_all_inline_media":false,"profile_use_background_image":true,"profile_text_color":"663B12","description":"Want To Work In Physcis Research Centre.Last Year Ph.d in Physics.A Ssimple Person With Modern Knowledge","contributors_enabled":false,"geo_enabled":false,"profile_link_color":"1F98C7","location":"Mumbai","notifications":null,"friends_count":190,"verified":false,"favourites_count":1,"profile_sidebar_fill_color":"bdc5c9","protected":false,"profile_image_url":"http://a0.twimg.com/profile_images/1098208212/n100000357732355_9867_normal.jpg","follow_request_sent":null,"time_zone":"Mumbai","created_at":"Sat Nov 07 05:19:49 +0000 2009","name":"Pratik Bhagwat","profile_sidebar_border_color":"4b6570","url":"http://twitter.com/Prince_Bhagwat","screen_name":"Prince_Bhagwat","id":88119648,"profile_background_image_url":"http://a3.twimg.com/profile_background_images/149157077/58591_151710018184255_100000357732355_315386_806516_n.jpg","utc_offset":19800,"followers_count":23},"retweeted":false,"in_reply_to_user_id":null,"id":29385702704}
#{"new_id_str":"610916544326664193","text":"RT @WhatsOnRadio2: Donna Summer \u2013 Hot Stuff http://bit.ly/bSG5XR #Radio2 #NowPlaying","id_str":"29385931449","truncated":false,"in_reply_to_status_id_str":null,"new_id":610916544326664193,"entities":{"user_mentions":[{"id_str":"174626103","indices":[3,17],"name":"Now Playing Radio 2","screen_name":"WhatsOnRadio2","id":174626103}],"urls":[{"indices":[44,64],"expanded_url":null,"url":"http://bit.ly/bSG5XR"}],"hashtags":[{"text":"Radio2","indices":[65,72]},{"text":"NowPlaying","indices":[73,84]}]},"place":null,"favorited":false,"in_reply_to_user_id_str":null,"coordinates":null,"source":"\u003Ca href=\"http://twidroid.com\" rel=\"nofollow\"\u003Etwidroid\u003C/a\u003E","contributors":null,"geo":null,"in_reply_to_screen_name":null,"in_reply_to_status_id":null,"retweeted_status":{"text":"Donna Summer \u2013 Hot Stuff http://bit.ly/bSG5XR #Radio2 #NowPlaying","id_str":"29385493777","truncated":false,"in_reply_to_status_id_str":null,"entities":{"user_mentions":[],"urls":[{"indices":[25,45],"expanded_url":null,"url":"http://bit.ly/bSG5XR"}],"hashtags":[{"text":"Radio2","indices":[46,53]},{"text":"NowPlaying","indices":[54,65]}]},"place":{"country":"United Kingdom","country_code":"","place_type":"neighborhood","bounding_box":{"type":"Polygon","coordinates":[[[-0.146397,51.515321],[-0.130336,51.515321],[-0.130336,51.524962],[-0.146397,51.524962]]]},"attributes":{},"full_name":"Fitzrovia, London","name":"Fitzrovia","id":"ed80cd5d41926d0e","url":"http://api.twitter.com/1/geo/id/ed80cd5d41926d0e.json"},"favorited":false,"in_reply_to_user_id_str":null,"coordinates":{"type":"Point","coordinates":[-0.142822,51.52074]},"source":"\u003Ca href=\"http://www.twitter.com/marklkelly\" rel=\"nofollow\"\u003ENow Playing BBC Radio 2\u003C/a\u003E","contributors":null,"geo":{"type":"Point","coordinates":[51.52074,-0.142822]},"in_reply_to_screen_name":null,"in_reply_to_status_id":null,"retweet_count":null,"created_at":"Mon Nov 01 16:09:10 +0000 2010","user":{"lang":"en","id_str":"174626103","listed_count":4,"following":null,"profile_background_tile":true,"profile_background_color":"ffa200","statuses_count":10495,"show_all_inline_media":false,"profile_use_background_image":true,"profile_text_color":"333333","description":"Follow me to see what's playing on BBC Radio 2. ","contributors_enabled":false,"geo_enabled":true,"profile_link_color":"0084B4","location":"On the airwaves.","notifications":null,"friends_count":15,"verified":false,"favourites_count":0,"profile_sidebar_fill_color":"ffd503","protected":false,"profile_image_url":"http://a3.twimg.com/profile_images/1101640979/2-iconv2_normal.png","follow_request_sent":null,"time_zone":"Monrovia","created_at":"Wed Aug 04 11:50:29 +0000 2010","name":"Now Playing Radio 2","profile_sidebar_border_color":"ffbf00","url":"http://twitter.com/marklkelly","screen_name":"WhatsOnRadio2","id":174626103,"profile_background_image_url":"http://a1.twimg.com/profile_background_images/130950316/bbc_radio_two_640_360.jpg","utc_offset":0,"followers_count":124},"retweeted":false,"in_reply_to_user_id":null,"id":29385493777},"retweet_count":null,"created_at":"Mon Nov 01 16:14:28 +0000 2010","user":{"lang":"es","id_str":"16545501","listed_count":23,"following":null,"profile_background_tile":false,"profile_background_color":"0099B9","statuses_count":3204,"show_all_inline_media":false,"profile_use_background_image":true,"profile_text_color":"3C3940","description":"Activista cultural, aficionado a la literatura, nuevas tecnolog\u00edas, m\u00fasica, conciertos... Quieres saber m\u00e1s? Preg\u00fantame ;-)","contributors_enabled":false,"geo_enabled":true,"profile_link_color":"0099B9","location":"Alicante, Spain","notifications":null,"friends_count":354,"verified":false,"favourites_count":10,"profile_sidebar_fill_color":"95E8EC","protected":false,"profile_image_url":"http://a3.twimg.com/profile_images/1117901803/keitaro_normal.jpg","follow_request_sent":null,"time_zone":"Madrid","created_at":"Wed Oct 01 15:50:18 +0000 2008","name":"Miguel \u00c1ngel R\u00edos","profile_sidebar_border_color":"5ED4DC","url":"http://miguel-musicaparamisoidos.blogspot.com","screen_name":"Miguel_Alicante","id":16545501,"profile_background_image_url":"http://a1.twimg.com/profile_background_images/73819044/bganimals1.jpg","utc_offset":3600,"followers_count":307},"retweeted":false,"in_reply_to_user_id":null,"id":29385931449}
#
#{"new_id_str":"610916612479909888",
#"text":"RT @bbccaribbean: BBC Caribbean News in Brief: The UN preparing Haitians for a possible hit from Tomas,  capital punishment rejected...  ...",
#"id_str":"29385953868",
#"truncated":true,
#"in_reply_to_status_id_str":null,
#"new_id":610916612479909888,
#"entities":
#       {"user_mentions":
#               [{"id_str":"18077108",
#               "indices":[3,16],
#               "name":"bbccaribbean",
#               "screen_name":"bbccaribbean",
#               "id":18077108}],
#       "urls":[],
#       "hashtags":[]
#       },
#"place":null,
#"favorited":false,
#"in_reply_to_user_id_str":null,
#"coordinates":null,
#"source":"web",
#"contributors":null,
#"geo":null,
#"in_reply_to_screen_name":null,
#"in_reply_to_status_id":null,
#"retweeted_status":
#       {"text":"BBC Caribbean News in Brief: The UN preparing Haitians for a possible hit from Tomas,  capital punishment rejected... http://bbc.in/amOAhV",
#       "id_str":"29385700752",
#       "truncated":false,
#       "in_reply_to_status_id_str":null,
#       "entities":
#               {"user_mentions":[],
#               "urls":
#                       [{"indices":[118,138],
#                       "expanded_url":null,
#                       "url":"http://bbc.in/amOAhV"}],
#               "hashtags":[]
#               },
#       "place":null,
#       "favorited":false,
#       "in_reply_to_user_id_str":null,
#       "coordinates":null,
#       "source":"\u003Ca href=\"http://twitterfeed.com\" rel=\"nofollow\"\u003Etwitterfeed\u003C/a\u003E",
#       "contributors":null,
#       "geo":null,
#       "in_reply_to_screen_name":null,
#       "in_reply_to_status_id":null,
#       "retweet_count":null,
#       "created_at":"Mon Nov 01 16:11:39 +0000 2010",
#       "user":
#               {"lang":"en",
#               "id_str":"18077108",
#               "listed_count":168,
#               "following":null,
#               "profile_background_tile":false,
#               "profile_background_color":"00006C",
#               "statuses_count":2747,
#               "show_all_inline_media":false,
#               "profile_use_background_image":true,
#               "profile_text_color":"333333",
#               "description":"BBC Caribbean - bringing the Caribbean to the world and the world to the Caribbean",
#               "contributors_enabled":false,
#               "geo_enabled":false,
#               "profile_link_color":"003399",
#               "location":"London",
#               "notifications":null,
#               "friends_count":0,
#               "verified":false,
#               "favourites_count":0,
#               "profile_sidebar_fill_color":"f5f5f5",
#               "protected":false,
#               "profile_image_url":"http://a2.twimg.com/profile_images/67211626/bbc_normal.png",
#               "follow_request_sent":null,
#               "time_zone":"London",
#               "created_at":"Fri Dec 12 14:38:48 +0000 2008",
#               "name":"bbccaribbean",
#               "profile_sidebar_border_color":"8f8f8f",
#               "url":"http://www.bbccaribbean.com",
#               "screen_name":"bbccaribbean",
#               "id":18077108,
#               "profile_background_image_url":"http://a1.twimg.com/profile_background_images/80378630/twitter_final_bg.jpg",
#               "utc_offset":0,
#               "followers_count":1912
#               },
#       "retweeted":false,
#       "in_reply_to_user_id":null,
#       "id":29385700752
#       },
#"retweet_count":null,
#"created_at":"Mon Nov 01 16:14:44 +0000 2010",
#"user":
#       {"lang":"en",
#       "id_str":"15604930",
#       "listed_count":42,
#       "following":null,
#       "profile_background_tile":false,
#       "profile_background_color":"9AE4E8",
#       "statuses_count":19150,
#       "show_all_inline_media":false,
#       "profile_use_background_image":true,
#       "profile_text_color":"333333",
#       "description":"#stl taxicab hack. I love helping stray pets & homeless people & anyone else. Got #Haiti on my mind & love the great orgs & ppl that help others. #compassion",
#       "contributors_enabled":false,
#       "geo_enabled":false,
#       "profile_link_color":"0084B4",
#       "location":"St. Louis, Missouri",
#       "notifications":null,
#       "friends_count":510,
#       "verified":false,
#       "favourites_count":2,
#       "profile_sidebar_fill_color":"DDFFCC",
#       "protected":false,
#       "profile_image_url":"http://a2.twimg.com/profile_images/1074072198/burn_candle_normal.jpg",
#       "follow_request_sent":null,
#       "time_zone":"Central Time (US & Canada)",
#       "created_at":"Fri Jul 25 22:47:55 +0000 2008",
#       "name":"Joe_Taxi",
#       "profile_sidebar_border_color":"BDDCAD",
#       "url":"http://myspace.com/k9s1bestfriend",
#       "screen_name":"Joe_Taxi",
#       "id":15604930,
#       "profile_background_image_url":"http://a3.twimg.com/profile_background_images/124954613/unshaken1.jpg",
#       "utc_offset":-21600,
#       "followers_count":687
#       },
#"retweeted":false,
#"in_reply_to_user_id":null,
#"id":29385953868
#}

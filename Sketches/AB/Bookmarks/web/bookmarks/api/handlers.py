from piston.handler import BaseHandler
from bookmarks.output.models import programmes, keywords, analyseddata, rawdata, rawtweets
from datetime import timedelta,datetime
from django.core.exceptions import ObjectDoesNotExist
import locale

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]

radiochannels = ["radio1","1xtra","radio2","radio3","radio4","5live","sportsextra","6music","radio7","asiannetwork","worldservice"]

allchannels = tvchannels + radiochannels

class ProgrammesHandler(BaseHandler):
    allowed_methods = ('GET',)
    # The below could be used if I wasn't adding keywords too - not sure how to imply some sort of JOIN operation
    #fields = ('pid', 'channel', 'title', 'expectedstart', 'timediff', 'duration', 'imported', 'analysed', 'totaltweets', 'meantweets', 'mediantweets', 'modetweets', 'stdevtweets')
    #model = programmes

    def read(self, request, pid):
        retdata = dict()
        data = programmes.objects.filter(pid=pid)
        if len(data) == 1:
            retdata['status'] = "OK"
            retdata['pid'] = data[0].pid
            retdata['title'] = data[0].title
            retdata['timestamp'] = data[0].timestamp
            retdata['utcoffset'] = data[0].utcoffset
            retdata['timediff'] = data[0].timediff
            retdata['duration'] = data[0].duration
            retdata['imported'] = data[0].imported
            retdata['analysed'] = data[0].analysed
            retdata['totaltweets'] = data[0].totaltweets
            retdata['meantweets'] = data[0].meantweets
            retdata['mediantweets'] = data[0].mediantweets
            retdata['modetweets'] = data[0].modetweets
            retdata['stdevtweets'] = data[0].stdevtweets
            kwdata = keywords.objects.filter(pid=pid).all()
            retdata['keywords'] = list()
            for row in kwdata:
                retdata['keywords'].append({'keyword' : row.keyword, 'type' : row.type})
            retdata['bookmarks'] = list()

            progdate = datetime.utcfromtimestamp(data[0].timestamp) + timedelta(seconds=data[0].utcoffset)
            actualstart = progdate - timedelta(seconds=data[0].timediff)
            minutedata = analyseddata.objects.filter(pid=pid).order_by('timestamp').all()
            tweetmins = dict()
            lastwasbookmark = False
            bookmarks = list()
            bookmarkcont = list()
            for minute in minutedata:
                # This isn't the most elegant BST solution, but it appears to work
                tweettime = datetime.utcfromtimestamp(minute.timestamp) + timedelta(seconds=data[0].utcoffset)
                proghour = tweettime.hour - actualstart.hour
                progmin = tweettime.minute - actualstart.minute
                progsec = tweettime.second - actualstart.second
                playertime = (((proghour * 60) + progmin) * 60) + progsec - 90 # needs between 60 and 120 secs removing to allow for tweeting time - using 90 for now
                if playertime > (data[0].duration - 60):
                    playertimemin = (data[0].duration/60) - 1
                    playertimesec = playertime%60
                elif playertime > 0:
                    playertimemin = playertime/60
                    playertimesec = playertime%60
                else:
                    playertimemin = 0
                    playertimesec = 0
                if minute.totaltweets > (1.5*data[0].stdevtweets+data[0].meantweets):
                    if lastwasbookmark == True:
                        bookmarkcont.append(playertimemin)
                    else:
                        if minute.totaltweets > (2.2*data[0].stdevtweets+data[0].meantweets) and minute.totaltweets > 9:
                            lastwasbookmark = True
                            bookmarks.append(playertimemin)
                        else:
                            lastwasbookmark = False
                else:
                    lastwasbookmark = False
                if not tweetmins.has_key(str(playertimemin)):
                    tweetmins[str(playertimemin)] = int(minute.totaltweets)
            if len(tweetmins) > 0:
                xlist = range(0,data[0].duration/60)
                for min in xlist:
                    if min in bookmarks:
                        retdata['bookmarks'].append({'iplayer' : "http://bbc.co.uk/i/" + pid + "/?t=" + str(min) + "m" + str(playertimesec) + "s", 'startseconds' : min*60+playertimesec, 'endseconds' : min*60+playertimesec+60})
                        lastindex = len(retdata['bookmarks']) - 1
                    elif min in bookmarkcont:
                        retdata['bookmarks'][lastindex]['endseconds'] = min*60+playertimesec+60

        else:
            retdata['status'] = "ERROR"
        return retdata

class SummaryHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        retdata = {"channels" : list()}

        # Prevent division by zero later on...
        largeststdev = 1

        for channel in allchannels:
            retdata['channels'].append({"channel" : channel})
            data = programmes.objects.filter(channel=channel).latest('timestamp')
            if isinstance(data,object):
                progdate = datetime.utcfromtimestamp(data.timestamp + data.utcoffset)
                progdate = progdate + timedelta(seconds=data.duration - data.timediff)
                datenow = datetime.now()
                if data.imported == 0:
                    retdata['channels'][len(retdata['channels']) - 1]['pid'] = data.pid
                    retdata['channels'][len(retdata['channels']) - 1]['stdev'] = data.stdevtweets
                    retdata['channels'][len(retdata['channels']) - 1]['interestingness'] = 0
                if data.stdevtweets > largeststdev and datenow <= progdate:
                    largeststdev = data.stdevtweets

        normaliser = 1/float(largeststdev)
        for channelgroup in retdata['channels']:
            if channelgroup.has_key('stdev'):
                channelgroup['interestingness'] = channelgroup['stdev'] * normaliser
                channelgroup.pop('stdev')
        retdata['status'] = "OK"

        return retdata

class TweetHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, pid):
        retdata = {"tweets" : list()}
        # Need to add full tweet dicts to this once the model has been added
        data = rawdata.objects.filter(pid=pid).order_by('timestamp').all()
        for tweet in data:
            tweetid = int(tweet.tweet_id)
            try:
                rawtweetquery = rawtweets.objects.get(tweet_id = tweetid)
                tweetjson = rawtweetquery.tweet_json
            except ObjectDoesNotExist, e:
                tweetjson = None
            retdata['tweets'].append({"id" : tweetid,"timestamp" : tweet.timestamp,"programme_position" : tweet.programme_position,"json" : tweetjson})
        return retdata

class TimestampHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, pid, timestamp):
        retdata = {"tweets" : list()}
        timestamp = int(timestamp)
        # Need to add full tweet dicts to this once the model has been added
        timestamp2 = timestamp + 60
        data = rawdata.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=timestamp2).order_by('timestamp').all()
        for tweet in data:
            tweetid = int(tweet.tweet_id)
            try:
                rawtweetquery = rawtweets.objects.get(tweet_id = tweetid)
                tweetjson = rawtweetquery.tweet_json
            except ObjectDoesNotExist, e:
                tweetjson = None
            retdata['tweets'].append({"id" : tweetid,"timestamp" : tweet.timestamp,"programme_position" : tweet.programme_position,"json" : tweetjson})
        return retdata
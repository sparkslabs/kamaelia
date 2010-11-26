from piston.handler import BaseHandler
from bookmarks.output.models import programmes, keywords, analyseddata, rawdata, rawtweets, programmes_unique, wordanalysis
from datetime import timedelta,datetime
from django.core.exceptions import ObjectDoesNotExist
import math

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]

radiochannels = ["radio1","1xtra","radio2","radio3","radio4","5live","sportsextra","6music","radio7","asiannetwork","worldservice"]

allchannels = tvchannels + radiochannels

class ProgrammesHandler(BaseHandler):
    allowed_methods = ('GET',)
    # The below could be used if I wasn't adding keywords too - not sure how to imply some sort of JOIN operation
    #fields = ('pid', 'channel', 'title', 'expectedstart', 'timediff', 'duration', 'imported', 'analysed', 'totaltweets', 'meantweets', 'mediantweets', 'modetweets', 'stdevtweets')
    #model = programmes

    def read(self, request, pid, timestamp=False):
        #TODO: Add redux support for bookmarks here
        retdata = dict()
        try:
            master = programmes_unique.objects.get(pid=pid)
        except ObjectDoesNotExist, e:
            pass # This is handled later
        if timestamp:
            data = programmes.objects.filter(pid=pid,timestamp=timestamp)
        else:
            data = programmes.objects.filter(pid=pid)
        if len(data) > 0:
            retdata['status'] = "OK"
            retdata['pid'] = master.pid
            retdata['title'] = master.title
            if len(data) == 1:
                retdata['timestamp'] = data[0].timestamp
                retdata['utcoffset'] = data[0].utcoffset
                retdata['timediff'] = data[0].timediff
                retdata['imported'] = data[0].imported
                retdata['analysed'] = data[0].analysed
            retdata['duration'] = master.duration
            retdata['keywords'] = list()
            kwdata = keywords.objects.filter(pid=pid).all()
            for row in kwdata:
                retdata['keywords'].append({'keyword' : row.keyword, 'type' : row.type})

            minutegroups = dict()
            totaltweets = 0
            minlimit = 0
            for row in data:
                # This may not return some results at extreme ends, but should get the vast majority
                # No point in looking for data outside this anyway as we can't link back into it
                minutedata = analyseddata.objects.filter(pid=pid,timestamp__gte=row.timestamp-row.timediff,timestamp__lt=row.timestamp+master.duration-row.timediff).order_by('timestamp').all()
                # Set up the counter if not done already
                if not minutegroups.has_key(0):
                    durcount = int(master.duration / 60)
                    while durcount > 0:
                        durcount -= 1
                        minutegroups[durcount] = 0
                for line in minutedata:
                    group = int((line.timestamp - (row.timestamp - row.timediff)) / 60)
                    if minlimit < group:
                        minlimit = group
                    if minutegroups.has_key(group):
                        minutegroups[group] += line.totaltweets
                        totaltweets += line.totaltweets

            minuteitems = minutegroups.items()
            minuteitems.sort()

            if len(data) == 1:
                meantweets = data[0].meantweets
                mediantweets = data[0].mediantweets
                modetweets = data[0].modetweets
                stdevtweets = data[0].stdevtweets
            else:
                meantweets = totaltweets / (master.duration / 60)
                stdevtotal = 0
                medianlist = list()
                modelist = dict()
                for minute in minuteitems:
                    # Calculate standard deviation
                    stdevtotal += (minute[1] - meantweets) * (minute[1] - meantweets)
                    medianlist.append(minute[1])
                    if modelist.has_key(minute[1]):
                        modelist[minute[1]] += 1
                    else:
                        modelist[minute[1]] = 1
                medianlist.sort()
                mediantweets = medianlist[int(len(medianlist)/2)]
                modeitems = [[v, k] for k, v in modelist.items()]
                modeitems.sort(reverse=True)
                modetweets = int(modeitems[0][1])
                stdevtweets = math.sqrt(stdevtotal / len(minuteitems))

            retdata['totaltweets'] = totaltweets
            retdata['meantweets'] = meantweets
            retdata['mediantweets'] = mediantweets
            retdata['modetweets'] = modetweets
            retdata['stdevtweets'] = stdevtweets


            if 0:
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

    def read(self, request, pid, timestamp=False):
        retdata = {"tweets" : list()}
        try:
            master = programmes_unique.objects.get(pid=pid)
        except ObjectDoesNotExist, e:
            pass # This is handled later
        if timestamp:
            timestamp = int(timestamp)
            data = programmes.objects.filter(pid=pid,timestamp=timestamp)
        else:
            data = programmes.objects.filter(pid=pid)
        if len(data) > 0:
            if timestamp:
                progstart = data[0].timestamp - data[0].timediff
                duration = master.duration
                data = rawdata.objects.filter(pid=pid,timestamp__gte=progstart,timestamp__lt=progstart+duration).order_by('timestamp').all()
            else:
                data = rawdata.objects.filter(pid=pid,programme_position__gte=0,programme_position__lt=master.duration).order_by('programme_position').all()
            for tweet in data:
                tweetid = int(tweet.tweet_id)
                try:
                    rawtweetquery = rawtweets.objects.get(tweet_id = tweetid)
                    tweetjson = rawtweetquery.tweet_json
                    legacy = False
                except ObjectDoesNotExist, e:
                    legacy = True
                if legacy:
                    retdata['tweets'].append({"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"screen_name" : tweet.user,"text" : tweet.text, "legacy" : legacy})
                else:
                    retdata['tweets'].append({"id" : tweetid,"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"json" : tweetjson, "legacy" : legacy})
        return retdata

class TimestampHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, pid, timestamp, aggregated=False):
        retdata = {"tweets" : list()}
        timestamp = int(timestamp)
        if aggregated == "aggregated":
            # Timestamp is actually programme_position here
            progpos = timestamp * 60
            data = rawdata.objects.filter(pid=pid,programme_position__gte=progpos,programme_position__lt=progpos+60).order_by('programme_position').all()
        elif timestamp:
            data = rawdata.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=timestamp+60).order_by('timestamp').all()

        for tweet in data:
            tweetid = int(tweet.tweet_id)
            try:
                rawtweetquery = rawtweets.objects.get(tweet_id = tweetid)
                tweetjson = rawtweetquery.tweet_json
                legacy = False
            except ObjectDoesNotExist, e:
                legacy = True
            if legacy:
                retdata['tweets'].append({"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"screen_name" : tweet.user,"text" : tweet.text, "legacy" : legacy})
            else:
                retdata['tweets'].append({"id" : tweetid,"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"json" : tweetjson, "legacy" : legacy})
        return retdata
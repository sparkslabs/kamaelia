'''
API output handlers
'''
from piston.handler import BaseHandler
from bookmarks.output.models import programmes, keywords, analyseddata, rawdata, rawtweets, programmes_unique, wordanalysis
from datetime import timedelta,datetime
from django.core.exceptions import ObjectDoesNotExist
import math
import string

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]

radiochannels = ["radio1","1xtra","radio2","radio3","radio4","5live","sportsextra","6music","radio7","asiannetwork","worldservice"]

reduxmapping = {"bbcnews" : "bbcnews24","bbcparliament" : "bbcparl", "radio1" : "bbcr1", "1xtra" : "bbc1x", "radio2" : "bbcr2", \
                "radio3" : "bbcr3", "radio4" : "bbcr4", "5live" : "bbcr5l", "sportsextra" : "r5lsx", "6music" : "bbc6m", "radio7" : "bbc7", \
                "asiannetwork" : "bbcan"}

allchannels = tvchannels + radiochannels

class ProgrammesHandler(BaseHandler):
    allowed_methods = ('GET',)
    '''
    API output from /api/pid/timestamp/stats.format or /api/pid/stats.format giving statistics available and bookmarks identified
    Including a timestamp restricts to a single broadcast
    '''
    def read(self, request, pid, timestamp=False, redux=False):
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
            # Found the PID, so return an 'OK' status with the data that's immediately available
            retdata['status'] = "OK"
            retdata['pid'] = master.pid
            retdata['title'] = master.title
            if len(data) == 1:
                # If we're looking at a single broadcast, we can return all of the below
                retdata['timestamp'] = data[0].timestamp
                retdata['utcoffset'] = data[0].utcoffset
                retdata['timediff'] = data[0].timediff
                retdata['imported'] = data[0].imported
                retdata['analysed'] = data[0].analysed
            retdata['duration'] = master.duration
            retdata['keywords'] = list()
            kwdata = keywords.objects.filter(pid=pid).all()
            for row in kwdata:
                # List the keywords and what they represent (Participant, Title, Twitter etc)
                retdata['keywords'].append({'keyword' : row.keyword, 'type' : row.type})

            minutegroups = dict()
            totaltweets = 0
            minlimit = 0
            maxtweets = 0
            progtimestamp = 0
            progchannel = None
            progtimediff = 0
            reduxchannel = None
            # Identify bookmarks and calculate stats if viewing aggregated broadcasts
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
                        minutegroups[group] += int(line.totaltweets)
                        totaltweets += line.totaltweets
                        if minutegroups[group] > maxtweets:
                            maxtweets = minutegroups[group]

                if row.timestamp > progtimestamp:
                    progtimestamp = row.timestamp
                    progtimediff = row.timediff
                    progchannel = row.channel
                    if reduxmapping.has_key(progchannel):
                        reduxchannel = reduxmapping[progchannel]
                    else:
                        reduxchannel = progchannel

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


            if 1:
                # Identify bookmarks
                retdata['bookmarks'] = list()

                if redux == "redux":
                    progdatetime = datetime.utcfromtimestamp(progtimestamp)
                    progdatestring = progdatetime.strftime("%Y-%m-%d")
                    progtimestring = progdatetime.strftime("%H-%M-%S")

                bookmarks = list()
                for minute in minuteitems:
                    # Work out where the bookmarks should be
                    if minute[1] > (2.2*stdevtweets+meantweets) and minute[1] > 9: # Arbitrary value chosen for now - needs experimentation - was 9

                        wfdata = wordanalysis.objects.filter(timestamp=progtimestamp-progtimediff+(minute[0]*60),pid=pid,is_keyword=0,is_common=0).order_by('-count').all()

                        if len(wfdata) > 0:
                            bookmarkstart = False
                            bookmarkend = False

                            # Find most popular keyword
                            is_word = True
                            if wfdata[0].word != "":
                                keyword = wfdata[0].word
                            else:
                                keyword = wfdata[0].phrase
                                is_word = False
                            # Now look at each previous minute until it's no longer the top keyword
                            currentstamp = progtimestamp-progtimediff+(minute[0]*60)
                            topkeyword = keyword
                            while topkeyword == keyword:
                                currentstamp -= 60
                                try:
                                    dataset = wordanalysis.objects.filter(timestamp=currentstamp,pid=pid,is_keyword=0,is_common=0).order_by('-count').all()
                                except ObjectDoesNotExist:
                                    break
                                for line in dataset:
                                    if is_word:
                                        topkeyword = line.word
                                    else:
                                        topkeyword = line.phrase
                                    break

                            startstamp = currentstamp
                            endstamp = currentstamp + 60

                            # Investigate the previous minute to see if the keyword from above is in the top 10
                            tweetset = False
                            rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=startstamp,timestamp__lt=endstamp).order_by('timestamp').all()
                            for tweet in rawtweets:
                                tweettext = string.lower(tweet.text)
                                for items in """!"#$%&(),:;?@~[]'`{|}""":
                                    tweettext = string.replace(tweettext,items,"")
                                try:
                                    if str(keyword).lower() in tweettext:
                                        bookmarkstart = int(tweet.timestamp)
                                        tweetset = True
                                        break
                                except UnicodeEncodeError:
                                    break

                            if not tweetset:
                                rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=currentstamp,timestamp__lt=(currentstamp + 60)).order_by('timestamp').all()
                                for tweet in rawtweets:
                                    tweettext = string.lower(tweet.text)
                                    for items in """!"#$%&(),:;?@~[]'`{|}""":
                                        tweettext = string.replace(tweettext,items,"")
                                    try:
                                        if str(keyword).lower() in tweettext:
                                            bookmarkstart = int(tweet.timestamp)
                                            break
                                    except UnicodeEncodeError:
                                        break

                            # Now look at each next minute until it's no longer the top keyword
                            currentstamp = progtimestamp-progtimediff+(minute[0]*60)
                            topkeyword = keyword
                            while topkeyword == keyword:
                                currentstamp += 60
                                try:
                                    dataset = wordanalysis.objects.filter(timestamp=currentstamp,pid=pid,is_keyword=0,is_common=0).order_by('-count').all()
                                except ObjectDoesNotExist:
                                    break
                                for line in dataset:
                                    if is_word:
                                        topkeyword = line.word
                                    else:
                                        topkeyword = line.phrase
                                    break

                            startstamp = currentstamp
                            endstamp = currentstamp + 60

                            # Investigate the previous minute to see if the keyword from above is in the top 10
                            tweetset = False
                            rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=startstamp,timestamp__lt=endstamp).order_by('-timestamp').all()
                            for tweet in rawtweets:
                                tweettext = string.lower(tweet.text)
                                for items in """!"#$%&(),:;?@~[]'`{|}""":
                                    tweettext = string.replace(tweettext,items,"")
                                try:
                                    if str(keyword).lower() in tweettext:
                                        bookmarkend = int(tweet.timestamp)
                                        tweetset = True
                                        break
                                except UnicodeEncodeError:
                                    break

                            if not tweetset:
                                rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=currentstamp,timestamp__lt=(currentstamp + 60)).order_by('-timestamp').all()
                                for tweet in rawtweets:
                                    tweettext = string.lower(tweet.text)
                                    for items in """!"#$%&(),:;?@~[]'`{|}""":
                                        tweettext = string.replace(tweettext,items,"")
                                    try:
                                        if str(keyword).lower() in tweettext:
                                            bookmarkend = int(tweet.timestamp)
                                            break
                                    except UnicodeEncodeError:
                                        break

                            if (bookmarkstart and bookmarkend) and (bookmarkstart != bookmarkend):
                                if bookmarkstart < (progtimestamp - progtimediff):
                                    bookmarkstart = progtimestamp - progtimediff
                                if bookmarkend > (progtimestamp - progtimediff + master.duration):
                                    bookmarkend = progtimestamp - progtimediff + master.duration
                                # Only bookmark worthy if it creates 'buzz' for 60 seconds or more
                                if (len(bookmarks) > 0):
                                    # Check if the bookmarks should be merged, allowing a slight overlap time of 20 seconds in case of a sudden lack of tweets
                                    checkkeyword = bookmarks[len(bookmarks)-1][3]
                                    originalkeyword = keyword
                                    #try:
                                    #    checkkeyword = string.lower(checkkeyword)
                                    #    originalkeyword = string.lower(originalkeyword)
                                    #except UnicodeEncodeError:
                                    #    pass
                                    if bookmarks[len(bookmarks)-1][1] >= (bookmarkstart - 20) and checkkeyword == originalkeyword:
                                        bookmarks[len(bookmarks)-1][1] = bookmarkend
                                        continue
                                if (bookmarkend - bookmarkstart) > 60:
                                    bookmarks.append([bookmarkstart,bookmarkend,bookmarkstart-80,keyword])

                # Add the bookmarks found to the API output in the format specified
                for bookmark in bookmarks:
                    bookmarkpos = int(bookmark[2]-progtimestamp-progtimediff)
                    bookmarkmins = int(bookmarkpos / 60)
                    bookmarksecs = int(bookmarkpos % 60)
                    if redux == "redux":
                        retdata['bookmarks'].append({'redux' : "http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(bookmarkpos), 'startseconds' : bookmark[2]-progtimestamp-progtimediff, 'endseconds' : bookmark[1]-progtimestamp-progtimediff})
                    else:
                        retdata['bookmarks'].append({'iplayer' : "http://bbc.co.uk/i/" + pid + "/?t=" + str(bookmarkmins) + "m" + str(bookmarksecs) + "s", 'startseconds' : bookmark[2]-progtimestamp-progtimediff, 'endseconds' : bookmark[1]-progtimestamp-progtimediff})

        else:
            retdata['status'] = "ERROR"
        return retdata

class SummaryHandler(BaseHandler):
    allowed_methods = ('GET',)
    '''
    API output from /api/summary.format
    Lists all channels, their current PID and a rough estimation of the programme's online activity compared to others airing at the same time
    '''
    def read(self, request):
        retdata = {"channels" : list()}
        
        # Prevent division by zero later on...
        largeststdev = 1

        for channel in allchannels:
            retdata['channels'].append({"channel" : channel})
            try:
                data = programmes.objects.filter(channel=channel).latest('timestamp')
                try:
                    master = programmes_unique.objects.get(pid=data.pid)
                except ObjectDoesNotExist, e:
                    pass # This is handled later
                progdate = datetime.utcfromtimestamp(data.timestamp + data.utcoffset)
                progdate = progdate + timedelta(seconds=master.duration - data.timediff)
                datenow = datetime.now()
                if data.imported == 0:
                    retdata['channels'][len(retdata['channels']) - 1]['pid'] = data.pid
                    retdata['channels'][len(retdata['channels']) - 1]['stdev'] = data.stdevtweets
                    retdata['channels'][len(retdata['channels']) - 1]['interestingness'] = 0
                if data.stdevtweets > largeststdev and datenow <= progdate:
                    largeststdev = data.stdevtweets
            except ObjectDoesNotExist, e:
                pass


        normaliser = 1/float(largeststdev)
        for channelgroup in retdata['channels']:
            if channelgroup.has_key('stdev'):
                channelgroup['interestingness'] = channelgroup['stdev'] * normaliser
                channelgroup.pop('stdev')
        retdata['status'] = "OK"

        return retdata

class TweetHandler(BaseHandler):
    allowed_methods = ('GET',)
    '''
    Output from /api/pid.format or /api/pid/timestamp.format showing raw tweets for entire programmes
    '''
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
            # Find raw tweets for the broadcast identified by the timestamp included, or for all together
            if timestamp:
                progstart = data[0].timestamp - data[0].timediff
                duration = master.duration
                data = rawdata.objects.filter(pid=pid,timestamp__gte=progstart,timestamp__lt=progstart+duration).order_by('timestamp').all()
            else:
                data = rawdata.objects.filter(pid=pid,programme_position__gte=0,programme_position__lt=master.duration).order_by('programme_position').all()
            for tweet in data:
                tweetid = int(tweet.tweet_id)
                # Look for the tweets found in the rawtweets table to grab original JSON
                try:
                    rawtweetquery = rawtweets.objects.get(tweet_id = tweetid)
                    tweetjson = rawtweetquery.tweet_json
                    legacy = False
                except ObjectDoesNotExist, e:
                    legacy = True
                if legacy:
                    # If no JSON found, return a legacy output giving all that's available
                    retdata['tweets'].append({"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"screen_name" : tweet.user,"text" : tweet.text, "legacy" : legacy})
                else:
                    retdata['tweets'].append({"id" : tweetid,"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"json" : tweetjson, "legacy" : legacy})
        return retdata

class TimestampHandler(BaseHandler):
    allowed_methods = ('GET',)
    '''
    Output from /api/pid/timestamp/tweets.format or /api/pid/timestamp/aggregated/tweets.format
    Provides raw tweet output for a specific minute period in a programme, either aggregated across broadcasts or not
    '''
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
            # Check for existence of the original JSON
            try:
                rawtweetquery = rawtweets.objects.get(tweet_id = tweetid)
                tweetjson = rawtweetquery.tweet_json
                legacy = False
            except ObjectDoesNotExist, e:
                legacy = True
            if legacy:
                # If no JSON found, return what's available
                retdata['tweets'].append({"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"screen_name" : tweet.user,"text" : tweet.text, "legacy" : legacy})
            else:
                retdata['tweets'].append({"id" : tweetid,"created_at" : tweet.timestamp,"programme_position" : tweet.programme_position,"json" : tweetjson, "legacy" : legacy})
        return retdata
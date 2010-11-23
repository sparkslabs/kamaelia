# Create your views here.
from django.http import HttpResponse
from bookmarks.output.models import programmes,analyseddata,rawdata,wordanalysis,programmes_unique
from datetime import date,timedelta,datetime
from pygooglechart import SimpleLineChart, Axis #lc
import time
import cjson
import string
#import re
from django.core.exceptions import ObjectDoesNotExist
#TODO: Replace ugly meta refresh tags with AJAX

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]
            
radiochannels = ["radio1","1xtra","radio2","radio3","radio4","5live","sportsextra","6music","radio7","asiannetwork","worldservice"]

reduxmapping = {"bbcnews" : "bbcnews24","bbcparliament" : "bbcparl", "radio1" : "bbcr1", "1xtra" : "bbc1x", "radio2" : "bbcr2", \
                "radio3" : "bbcr3", "radio4" : "bbcr4", "5live" : "bbcr5l", "sportsextra" : "r5lsx", "6music" : "bbc6m", "radio7" : "bbc7", \
                "asiannetwork" : "bbcan"}

allchannels = tvchannels + radiochannels

header = '<html><head><title>Social Bookmarks</title><script type="text/javascript" src="/media/jquery/jquery.min.js"></script>\
            <style type="text/css">h1 { margin-top: 20px; font-size: 20pt; } h2 { font-size: 14pt; }</style> \
            </head><body style="margin: 0px"><div style="background-color: #FFFFFF; position: absolute; width: 100%; height: 100%">\
            <div style="width: 100%; overflow: hidden; height: 80px; font-family: Arial, Helvetica, sans-serif; position: absolute; background-color: #A9D0F5">\
            <div style="padding-left: 10px"><h1>Social Bookmarks</h1></div></div><div style="position: absolute; top: 80px; font-family: Arial, Helvetica, sans-serif; padding: 10px">'

footer = '</div></div></body></html>'

def index(request):
    currentdate = date.today()
    output = header
    output += "<meta http-equiv='refresh' content='60'>"
    output += "<style type=\"text/css\">.box a:link, .box a:visited, .box a:active, .box a:hover { color: inherit; }</style>"
    # Prevent division by zero later on...
    largeststdev = 1

    # Identify the total tweets for each current programme (provided the grabber is still running)
    for channel in allchannels:
        data = programmes.objects.filter(channel=channel).latest('timestamp')
        if isinstance(data,object):
            progdate = datetime.utcfromtimestamp(data.timestamp + data.utcoffset)
            progdate = progdate + timedelta(seconds=data.duration - data.timediff)
            if data.stdevtweets > largeststdev and data.imported==0:
                largeststdev = data.stdevtweets

    normaliser = 1/float(largeststdev)

    #output += "<h2>Note:</h2><p>- Some programme durations are currently identified incorrectly. Despite this, all data for the period will have been collected.</p>
    output += "<div style=\"display: inline; position: relative\"><h2>TV</h2>"
    for channel in tvchannels:
        data = programmes.objects.filter(channel=channel).latest('timestamp')
        if isinstance(data,object):
            progdate = datetime.utcfromtimestamp(data.timestamp + data.utcoffset)
            if data.imported==0:
                opacity = normaliser * data.stdevtweets
                if opacity < 0.5:
                    fontcolour = "#000000"
                else:
                    fontcolour = "#FFFFFF"
                bgval = str(int(255 - (255 * opacity)))
                bgcolour = "rgb(" + bgval + "," + bgval + "," + bgval + ")"
                output += "<div style=\"float: left; margin-right: 5px;\"><a href=\"/channel-graph/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "<div id=\"" + channel + "\" class=\"box\" style=\"width: 77px; background-color: " + bgcolour + "; color: " + fontcolour + "; text-align: center;\"><a href=\"/programmes/" + data.pid + "/\" style=\"text-decoration: none; color: " + fontcolour + "\">" + str(data.totaltweets) + "</a></div></div>"
            else:
                output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channel-graph/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "Off Air</div>"
        else:
            output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channel-graph/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
            output += "No Data</div>"

    output += "<br /><br /></div><br /><br /><div style=\"display: inline; position: relative\"><h2>Radio</h2>"
    for channel in radiochannels:
        data = programmes.objects.filter(channel=channel).latest('timestamp')
        if isinstance(data,object):
            progdate = datetime.utcfromtimestamp(data.timestamp + data.utcoffset)
            if data.imported==0:
                opacity = normaliser * data.stdevtweets
                if opacity < 0.5:
                    fontcolour = "#000000"
                else:
                    fontcolour = "#FFFFFF"
                bgval = str(int(255 - (255 * opacity)))
                bgcolour = "rgb(" + bgval + "," + bgval + "," + bgval + ")"
                output += "<div style=\"float: left; margin-right: 5px;\"><a href=\"/channel-graph/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "<div id=\"" + channel + "\" class=\"box\" style=\"width: 77px; background-color: " + bgcolour + "; color: " + fontcolour + "; text-align: center;\"><a href=\"/programmes/" + data.pid + "/\" style=\"text-decoration: none; color: " + fontcolour + "\">" + str(data.totaltweets) + "</a></div></div>"
            else:
                output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channel-graph/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "Off Air</div>"
        else:
            output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channel-graph/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
            output += "No Data</div>"
        
    output += "<br /><br /></div><br /><br />API: <a href=\"/api/summary.json\" target=\"_blank\">JSON</a> - <a href=\"/api/summary.xml\" target=\"_blank\">XML</a>" + footer

    return HttpResponse(output)

def channel(request,channel,year=0,month=0,day=0):
    output = header
    data = programmes.objects.filter(channel=channel)
    if channel not in radiochannels and channel not in tvchannels:
        output += "<br />Invalid channel supplied."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    else:
        output += '<style type="text/css">@import "/media/jquery/jquery.datepick.css";</style>\n \
                    <script type="text/javascript" src="/media/jquery/jquery.datepick.js"></script>\n'
        output += "<script type=\"text/javascript\">\n \
                        $(function() {\n "
        if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
            output += "$('#inlineDatepicker').datepick({onSelect: showDate, defaultDate: '" + month + "/" + day + "/" + year + "', selectDefaultDate: true});\n"
        else:
            output += "$('#inlineDatepicker').datepick({onSelect: showDate});\n "
        output += "});\n \
                        \n \
                        function showDate(date) {\n \
                            pickerYear = date[0].getFullYear().toString();\n \
                            pickerMonth = (date[0].getMonth() + 1).toString();\n \
                            pickerDay = date[0].getDate().toString();\n \
                            if (pickerMonth.length < 2) {\n \
                                pickerMonth = '0' + pickerMonth;\n \
                            }\n \
                            if (pickerDay.length < 2) {\n \
                                pickerDay = '0' + pickerDay;\n \
                            }\n \
                            window.location = '/channels/" + channel + "/' + pickerYear + '/' + pickerMonth + '/' + pickerDay + '/';\n \
                        }\n \
                    </script>\n"
        
        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
        if len(data) < 1:
            output += "<br />Please note: No data has yet been captured for this channel."
        else:
            output += '<br /><div id="inlineDatepicker"></div>'
            if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
                output += "<br />Currently viewing shows for " + day + "/" + month + "/" + year + "<br />"
                starttimestamp = time.mktime(datetime(int(year),int(month),int(day),0,0,0,0).timetuple())
                if starttimestamp + (86400 * 8) < time.time():
                    redux = True
                else:
                    redux = False
                endtimestamp = starttimestamp + 86400
                data = programmes.objects.filter(channel__exact=channel,timestamp__gte=starttimestamp,timestamp__lt=endtimestamp).order_by('timestamp').all()
                for programme in data:
                    progdate = datetime.utcfromtimestamp(programme.timestamp) + timedelta(seconds=programme.utcoffset)
                    if redux:
                        output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "/redux\">" + programme.title + "</a>"
                    else:
                        output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "\">" + programme.title + "</a>"
                if len(data) < 1:
                    output += "<br />No data for this date - please select another from the picker above.<br />"
            else:
                output += "<br />Please select a date from the picker above.<br />"
        output += "<br /><br /><a href=\"/\">Back to index</a> - <a href=\"/channel-graph/" + channel + "/" + str(year) + "/" + str(month) + "/" + str(day) + "\">Graphical view</a>"

    output += footer
    return HttpResponse(output)

def channelgraph(request,channel,year=0,month=0,day=0):
    output = header
    data = programmes.objects.filter(channel=channel)
    if channel not in radiochannels and channel not in tvchannels:
        output += "<br />Invalid channel supplied."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    else:
        output += '<style type="text/css">@import "/media/jquery/jquery.datepick.css";</style>\n \
                    <script type="text/javascript" src="/media/jquery/jquery.datepick.js"></script>\n'
        output += "<script type=\"text/javascript\">\n \
                        $(function() {\n "
        if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
            output += "$('#inlineDatepicker').datepick({onSelect: showDate, defaultDate: '" + month + "/" + day + "/" + year + "', selectDefaultDate: true});\n"
        else:
            output += "$('#inlineDatepicker').datepick({onSelect: showDate});\n "
        output += "});\n \
                        \n \
                        function showDate(date) {\n \
                            pickerYear = date[0].getFullYear().toString();\n \
                            pickerMonth = (date[0].getMonth() + 1).toString();\n \
                            pickerDay = date[0].getDate().toString();\n \
                            if (pickerMonth.length < 2) {\n \
                                pickerMonth = '0' + pickerMonth;\n \
                            }\n \
                            if (pickerDay.length < 2) {\n \
                                pickerDay = '0' + pickerDay;\n \
                            }\n \
                            window.location = '/channel-graph/" + channel + "/' + pickerYear + '/' + pickerMonth + '/' + pickerDay + '/';\n \
                        }\n \
                    </script>\n"

        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
        if len(data) < 1:
            output += "<br />Please note: No data has yet been captured for this channel."
        else:
            output += '<br /><div id="inlineDatepicker"></div>'
            if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
                output += "<br />Currently viewing shows for " + day + "/" + month + "/" + year + "<br />"
                starttimestamp = time.mktime(datetime(int(year),int(month),int(day),0,0,0,0).timetuple())
                if starttimestamp + (86400 * 8) < time.time():
                    redux = True
                else:
                    redux = False
                endtimestamp = starttimestamp + 86400
                data = programmes.objects.filter(channel__exact=channel,timestamp__gte=starttimestamp,timestamp__lt=endtimestamp).order_by('timestamp').all()
                for programme in data:
                    progdate = datetime.utcfromtimestamp(programme.timestamp) + timedelta(seconds=programme.utcoffset)

                    if programme.totaltweets > 0:

                        if redux:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "/redux\">" + programme.title + "</a> (see below)"
                        else:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "\">" + programme.title + "</a> (see below)"

                        actualstart = progdate - timedelta(seconds=programme.timediff)
                        minutedata = analyseddata.objects.filter(pid=programme.pid).order_by('timestamp').all()

                        tweetmins = dict()
                        for minute in minutedata:
                            tweettime = datetime.utcfromtimestamp(minute.timestamp) + timedelta(seconds=data[0].utcoffset)
                            proghour = tweettime.hour - actualstart.hour
                            progmin = tweettime.minute - actualstart.minute
                            progsec = tweettime.second - actualstart.second
                            playertime = (((proghour * 60) + progmin) * 60) + progsec - 90 # needs between 60 and 120 secs removing to allow for tweeting time - using 90 for now
                            if playertime > (programme.duration - 60):
                                playertimemin = (programme.duration/60) - 1
                            elif playertime > 0:
                                playertimemin = playertime/60
                            else:
                                playertimemin = 0
                            if not tweetmins.has_key(str(playertimemin)):
                                tweetmins[str(playertimemin)] = int(minute.totaltweets)

                        xlist = range(0,programme.duration/60)
                        ylist = list()
                        for min in xlist:
                            if tweetmins.has_key(str(min)):
                                ylist.append(tweetmins[str(min)])
                            else:
                                ylist.append(0)

                        maxy = max(ylist)
                        maxx = max(xlist)

                        mainwidth = int(1000/(maxx+1)) * (maxx + 1)

                        graph = SimpleLineChart(mainwidth,300,y_range=[0,maxy])
                        graph.add_data(ylist)

                        #TODO: Fix the bad labelling! - perhaps see if flotr is any better
                        graph.set_title("Tweets per minute")
                        left_axis = ['',int(maxy/4),int(maxy/2),int(3*maxy/4),int(maxy)]
                        bottom_axis = [0,int(maxx/8),int(maxx/4),int(3*maxx/8),int(maxx/2),int(5*maxx/8),int(3*maxx/4),int(7*maxx/8),int(maxx)]
                        graph.set_axis_labels(Axis.LEFT,left_axis)
                        graph.set_axis_labels(Axis.BOTTOM,bottom_axis)
                        output += "<br /><img src=\"" + graph.get_url() + "\"><br />"

                    else:
                        if redux:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "/redux\">" + programme.title + "</a>"
                        else:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "\">" + programme.title + "</a>"
                        output += " - No data available<br />"

                if len(data) < 1:
                    output += "<br />No data for this date - please select another from the picker above.<br />"
            else:
                output += "<br />Please select a date from the picker above.<br />"
        output += "<br /><br /><a href=\"/\">Back to index</a> - <a href=\"/channels/" + channel + "/" + str(year) + "/" + str(month) + "/" + str(day) + "\">Textual view</a>"

    output += footer
    return HttpResponse(output)

def programme(request,pid,redux=False):
    # Now that this is live, would be clever to use AJAX to refresh graphs etc every minute whilst still unanalysed?

    output = header
    data = programmes.objects.filter(pid=pid).all()
    output += "<br />This output is due to be replaced. New views are currently under development at /programmesv2.<br />"
    if len(data) == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    elif len(data) == 1:
        if data[0].analysed == 0:
            output += "<meta http-equiv='refresh' content='30'>"
        channel = data[0].channel
        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
        progdatetime = datetime.utcfromtimestamp(data[0].timestamp)
        progdatestring = progdatetime.strftime("%Y-%m-%d")
        progtimestring = progdatetime.strftime("%H-%M-%S")
        progdate = progdatetime + timedelta(seconds=data[0].utcoffset)
        actualstart = progdate - timedelta(seconds=data[0].timediff)
        minutedata = analyseddata.objects.filter(pid=pid).order_by('timestamp').all()
        output += str(progdate.strftime("%d/%m/%Y")) + "<br />"
        output += "<strong>" + data[0].title + "</strong><br />"
        output += "Expected show times: " + str(progdate.strftime("%H:%M:%S")) + " to " + str((progdate + timedelta(seconds=data[0].duration)).strftime("%H:%M:%S")) + "<br />"
        output += "Actual show times (estimated): " + str(actualstart.strftime("%H:%M:%S")) + " to " + str((actualstart + timedelta(seconds=data[0].duration)).strftime("%H:%M:%S")) + "<br />"
        output += "<br />Total tweets: " + str(data[0].totaltweets)
        #rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=data[0].timestamp,timestamp__lt=data[0].timestamp+data[0].duration).order_by('timestamp').all()
        #tweetseccount = dict()
        #for tweet in rawtweets:
        #    if tweetseccount.has_key(tweet.timestamp):
        #        tweetseccount[tweet.timestamp] += 1
        #    else:
        #        tweetseccount[tweet.timestamp] = 1
        #if len(tweetseccount) > 0:
        #    tweetseccount = [(v,k) for k, v in tweetseccount.items()]
        #    tweetseccount.sort(reverse=True)
        #    output += "<br />Tweets per second: " + str(tweetseccount)
        tweetmins = dict()
        tweetstamps = dict()
        #appender = ""
        lastwasbookmark = False
        bookmarks = list()
        bookmarkcont = list()
        bookmarkstest = list()
        for minute in minutedata:
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
            #appender += "<br />" + str(tweettime.strftime("%H:%M")) + ": <a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(playertimemin) + "m" + str(playertimesec) + "s\" target=\"_blank\">" + str(minute.totaltweets) + "</a>"
            if minute.totaltweets > (1.5*data[0].stdevtweets+data[0].meantweets):
                if lastwasbookmark == True:
                    #appender += " cont'd..."
                    bookmarkcont.append(playertimemin)
                else:
                    if minute.totaltweets > (2.2*data[0].stdevtweets+data[0].meantweets) and minute.totaltweets > 9: # Arbitrary value chosen for now - needs experimentation - was 9
                        #appender += " BOOKMARK!"
                        lastwasbookmark = True
                        bookmarks.append(playertimemin)
                        # BOOKMARK TEST
                        wfdata = wordanalysis.objects.filter(timestamp=minute.timestamp,pid=pid,is_keyword=0).order_by('-count').all()

                        # Find most popular keyword
                        is_word = True
                        if wfdata[0].word != "":
                            keyword = wfdata[0].word
                        else:
                            keyword = wfdata[0].phrase
                            is_word = False
                        # Now look at each previous minute until it's no longer the top keyword
                        currentstamp = minute.timestamp
                        topkeyword = keyword
                        while topkeyword == keyword:
                            currentstamp -= 60
                            try:
                                dataset = wordanalysis.objects.filter(timestamp=currentstamp,pid=pid,is_keyword=0).order_by('-count').all()
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
                                    bookmarkstest.append(tweet.timestamp)
                                    tweetset = True
                                    break
                            except UnicodeEncodeError:
                                break

                        if not tweetset:
                            rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=minute.timestamp,timestamp__lt=(minute.timestamp + 60)).order_by('timestamp').all()
                            for tweet in rawtweets:
                                tweettext = string.lower(tweet.text)
                                for items in """!"#$%&(),:;?@~[]'`{|}""":
                                    tweettext = string.replace(tweettext,items,"")
                                try:
                                    if str(keyword).lower() in tweettext:
                                        bookmarkstest.append(tweet.timestamp)
                                        break
                                except UnicodeEncodeError:
                                    break

                    else:
                        lastwasbookmark = False
            else:
                lastwasbookmark = False
            if not tweetmins.has_key(str(playertimemin)):
                tweetmins[str(playertimemin)] = int(minute.totaltweets)
            if not tweetstamps.has_key(str(playertimemin)):
                tweetstamps[str(playertimemin)] = int(minute.timestamp)
        if len(tweetmins) > 0:
            output += " - Tweets per minute - Mean: " + str(round(data[0].meantweets,2)) + " - Median: " + str(data[0].mediantweets) + " - Mode: " + str(data[0].modetweets) + " - STDev: " + str(round(data[0].stdevtweets,2)) + "<br />"
            xlist = range(0,data[0].duration/60)
            ylist = list()
            for min in xlist:
                if tweetmins.has_key(str(min)):
                    ylist.append(tweetmins[str(min)])
                else:
                    ylist.append(0)

            maxy = max(ylist)
            maxx = max(xlist)

            mainwidth = int(1000/(maxx+1)) * (maxx + 1)
            # blockgraph = main gradient based output
            # blockgraph2 = iPlayer bookmarks selection
            # blockgraph3 = raw tweets selection
            blockgraph = "<div style=\"border-top: 1px #CCCCCC solid; border-left: 1px #CCCCCC solid; border-right: 1px #CCCCCC solid; height: 50px; width: " + str(mainwidth) + "px; overflow: hidden\">"
            blockgraph2 = "<div style=\"border-left: 1px #CCCCCC solid; border-right: 1px #CCCCCC solid; height: 20px; width: " + str(mainwidth) + "px; overflow: hidden\">"
            blockgraph3 = "<div style=\"border-bottom: 1px #CCCCCC solid; border-left: 1px #CCCCCC solid; border-right: 1px #CCCCCC solid; height: 20px; width: " + str(mainwidth) + "px; overflow: hidden\">"
            width = int(1000/(maxx+1))
            lastbookmark = None
            if redux == "redux":
                if reduxmapping.has_key(channel):
                    reduxchannel = reduxmapping[channel]
                else:
                    reduxchannel = channel
                for min in xlist:
                    if tweetmins.has_key(str(min)):
                        opacity = float(tweetmins[str(min)]) / maxy
                    else:
                        opacity = 0
                    blockgraph += "<a href=\"http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(60*min+playertimesec) + "\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 50px; cursor: pointer; float: left; background-color: #000000; opacity: " + str(opacity) + "; filter:alpha(opacity=" + str(int(opacity * 100)) + ")\"></div></a>"
                    if min in bookmarks:
                        blockgraph2 += "<a href=\"http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(60*min+playertimesec) + "\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #888888\"></div></a>"
                        lastbookmark = min
                    elif min in bookmarkcont and lastbookmark != None:
                        blockgraph2 += "<a href=\"http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(60*lastbookmark+playertimesec) + "\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #888888\"></div></a>"
                    else:
                        blockgraph2 += "<div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #FFFFFF\"></div>"
                    if tweetstamps.has_key(str(min)):
                        blockgraph3 += "<a href=\"/programmes/" + pid + "/" + str(tweetstamps[str(min)]) + "/\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #000000; opacity: " + str(opacity) + "\"></div></a>"
                    else:
                        blockgraph3 += "<div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #000000; opacity: " + str(opacity) + "\"></div>"
            else:
                for min in xlist:
                    if tweetmins.has_key(str(min)):
                        opacity = float(tweetmins[str(min)]) / maxy
                    else:
                        opacity = 0
                    blockgraph += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(min) + "m" + str(playertimesec) + "s\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 50px; cursor: pointer; float: left; background-color: #000000; opacity: " + str(opacity) + "; filter:alpha(opacity=" + str(int(opacity * 100)) + ")\"></div></a>"
                    if min in bookmarks:
                        blockgraph2 += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(min) + "m" + str(playertimesec) + "s\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #888888\"></div></a>"
                        lastbookmark = min
                    elif min in bookmarkcont and lastbookmark != None:
                        blockgraph2 += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(lastbookmark) + "m" + str(playertimesec) + "s\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #888888\"></div></a>"
                    else:
                        blockgraph2 += "<div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #FFFFFF\"></div>"
                    if tweetstamps.has_key(str(min)):
                        blockgraph3 += "<a href=\"/programmes/" + pid + "/" + str(tweetstamps[str(min)]) + "/\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #000000; opacity: " + str(opacity) + "\"></div></a>"
                    else:
                        blockgraph3 += "<div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #000000; opacity: " + str(opacity) + "\"></div>"
            blockgraph += "</div>"
            blockgraph2 += "</div>"
            blockgraph3 += "</div>"

            if mainwidth > 1000:
                mainwidth = 1000

            graph = SimpleLineChart(mainwidth,300,y_range=[0,maxy])
            graph.add_data(ylist)

            #TODO: Fix the bad labelling! - perhaps see if flotr is any better
            graph.set_title("Tweets per minute")
            left_axis = ['',int(maxy/4),int(maxy/2),int(3*maxy/4),int(maxy)]
            bottom_axis = [0,int(maxx/8),int(maxx/4),int(3*maxx/8),int(maxx/2),int(5*maxx/8),int(3*maxx/4),int(7*maxx/8),int(maxx)]
            graph.set_axis_labels(Axis.LEFT,left_axis)
            graph.set_axis_labels(Axis.BOTTOM,bottom_axis)
            output += "<br /><img src=\"" + graph.get_url() + "\"><br /><br /><!--[if lte IE 8]><strong>Note:</strong> It looks like you're using Internet Explorer - until a code bug is fixed, you won't be able to see the last minute(s) of programmes in the plot below.<br /><br /><![endif]-->"
            output += blockgraph
            output += blockgraph2
            output += blockgraph3
            #output += appender
            if len(bookmarkstest) > 0:
                output += "<br /><b>New Bookmark Testing</b>"
                for entry in bookmarkstest:
                    tweettime = datetime.utcfromtimestamp(entry) + timedelta(seconds=data[0].utcoffset)
                    proghour = tweettime.hour - actualstart.hour
                    progmin = tweettime.minute - actualstart.minute
                    progsec = tweettime.second - actualstart.second
                    playertime = (((proghour * 60) + progmin) * 60) + progsec - 80 # needs between 60 and 120 secs removing to allow for tweeting time - using 90 for now
                    if playertime > (data[0].duration - 60):
                        playertimemin = (data[0].duration/60) - 1
                        playertimesec = playertime%60
                    elif playertime > 0:
                        playertimemin = playertime/60
                        playertimesec = playertime%60
                    else:
                        playertimemin = 0
                        playertimesec = 0
                    if redux == "redux":
                        output += "<br /><a href=\"http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(60*playertimemin+playertimesec) + "\" target=\"_blank\">http://g.bbcredux.com/programme/" + channel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(60*playertimemin+playertimesec) + "</a>"
                    else:
                        output += "<br /><a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(playertimemin) + "m" + str(playertimesec) + "s\" target=\"_blank\">http://bbc.co.uk/i/" + pid + "/?t=" + str(playertimemin) + "m" + str(playertimesec) + "s</a>"
        else:
            output += "<br />Not enough data to generate statistics.<br />"

        output += "<br /><br />API: <a href=\"/api/" + data[0].pid + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + data[0].pid + ".xml\" target=\"_blank\">XML</a>"
        output += "<br />Tweets: <a href=\"/api/" + data[0].pid + "/tweets.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + data[0].pid + "/tweets.xml\" target=\"_blank\">XML</a>"
        # Reveal tweets is temporary - will allow selection and viewing of single minutes once the database has been redesigned.
        output += "<br /><br /><a href=\"/channel-graph/" + data[0].channel + "/" + str(progdate.strftime("%Y/%m/%d")) + "/\">Back to channel page</a> - <a href=\"http://www.bbc.co.uk/programmes/" + data[0].pid + "\" target=\"_blank\">View BBC /programmes page</a>"

    else:
        output += "<br />Database consistency error - somehow a primary key appears twice. The world may have ended."
        output += "<br /><br /><a href=\"/\">Back to index</a>"

    output += footer
    return HttpResponse(output)

def programmev2(request,pid,timestamp=False,redux=False):
    # Now that this is live, would be clever to use AJAX to refresh graphs etc every minute whilst still unanalysed?

    output = header

    if programmev2data(False,"status",pid,timestamp,redux,False) == "206":

        # Ajax refresh code for divs TODO: Each time, request to /data/status to see if we need to keep refreshing
        scripting = """<script>
                            $(document).ready(function() {
                                var refreshId = setInterval(function() {
                                    $('#statistics').load('/data/statistics/""" + pid
        if timestamp:
            scripting += "/" + str(timestamp)
        if redux == "redux":
            scripting += "/redux"

        scripting += """?randval='+Math.random());
                                    $('#graphs').load('/data/graphs/""" + pid
        if timestamp:
            scripting += "/" + str(timestamp)
        if redux == "redux":
            scripting += "/redux"

        scripting += """?randval='+Math.random());}, 5000);
                    });
                    </script>"""

        output += scripting

        # Allowance for non-JS browsers
        output += "<noscript><meta http-equiv='refresh' content='30'></noscript>"

    master = programmes_unique.objects.get(pid=pid)
    if timestamp:
        data = programmes.objects.filter(pid=pid,timestamp=timestamp).all()
        # Viewing a single instance
    else:
        data = programmes.objects.filter(pid=pid).all()
        # Viewing all instances (inc repeats etc) - shows the same as the timestamp case if only one row found
    rowcount = len(data)
    if rowcount == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    else:
        if rowcount == 1:
            channel = data[0].channel
            output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
            progdatetime = datetime.utcfromtimestamp(data[0].timestamp)
            progdate = progdatetime + timedelta(seconds=data[0].utcoffset)
            actualstart = progdate - timedelta(seconds=data[0].timediff)
            output += str(progdate.strftime("%d/%m/%Y"))
        output += "<br /><strong>" + master.title + "</strong><br />"
        if rowcount == 1:
            output += "Expected show times: " + str(progdate.strftime("%H:%M:%S")) + " to " + str((progdate + timedelta(seconds=master.duration)).strftime("%H:%M:%S")) + "<br />"
            output += "Actual show times (estimated): " + str(actualstart.strftime("%H:%M:%S")) + " to " + str((actualstart + timedelta(seconds=master.duration)).strftime("%H:%M:%S")) + "<br />"
        else:
            proghours = master.duration / 3600 - master.duration % 3600
            progmins = (master.duration % 3600) / 60
            if proghours >= 1:
                output += "Duration: " + str(proghours) + " hours, " + str(progmins) + " minutes<br />"
            else:
                output += "Duration: " + str(progmins) + " minutes<br />"
        
        output += "<br /><div id=\"statistics\">"
        output += programmev2data(False,"statistics",pid,timestamp,redux,False)
        output += "</div>"
        output += "<br /><div id=\"statistics\">"
        output += programmev2data(False,"graphs",pid,timestamp,redux,False)
        output += "</div>"

        if rowcount > 1:
            output += "<br /><br /><strong>Broadcasts</strong>"
            for row in data:
                output += "<br /><a href=\"/programmesv2/" + pid + "/" + str(int(row.timestamp))
                if redux == "redux":
                    output += "/redux"
                output += "\">"
                progdatetime = datetime.utcfromtimestamp(row.timestamp)
                progdate = progdatetime + timedelta(seconds=row.utcoffset)
                output += str(progdate.strftime("%d/%m/%Y %H:%M:%S"))
                output += "</a>"

    output += footer
    return HttpResponse(output)

def programmev2data(request,element,pid,timestamp=False,redux=False,wrapper=True):

    output = "" # Initialise output buffer
    master = programmes_unique.objects.get(pid=pid)
    if timestamp:
        data = programmes.objects.filter(pid=pid,timestamp=timestamp).all()
    else:
        data = programmes.objects.filter(pid=pid).all()
    rowcount = len(data)
    if element == "statistics":
        # Print a line like Total tweets: 7 - Tweets per minute - Mean: 0.27 - Median: 0 - Mode: 0 - STDev: 0.53
        # TODO: Recalculate median, mode and stdev if rowcount > 1
        totaltweets = 0
        meantweets = 0
        mediantweets = None
        modetweets = None
        stdevtweets = None
        for row in data:
            totaltweets += row.totaltweets
            meantweets += row.meantweets
            if rowcount == 1:
                mediantweets = row.mediantweets
                modetweets = row.modetweets
                stdevtweets = row.stdevtweets
        if rowcount > 0:
            meantweets = meantweets / rowcount

        output += "Total tweets: " + str(totaltweets) + " - Tweets per minute - Mean: " + str(round(meantweets,2))
        if mediantweets != None:
            output += " - Median: " + str(round(mediantweets,2))
        if modetweets != None:
            output += " - Mode: " + str(round(modetweets,2))
        if stdevtweets != None:
            output += " - STDev: " + str(round(stdevtweets,2))
    elif element == "graphs":
        for row in data:
            # This may not return some results at extreme ends, but should get the vast majority
            # No point in looking for data outside this anyway as we can't link back into it
            rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=row.timestamp-row.timediff,timestamp__lt=row.timestamp+master.duration-row.timediff).order_by('timestamp').all()
            minutegroups = dict()
            durcount = int(master.duration / 60)
            # Set up the counter
            while durcount > 0:
                durcount -= 1
                minutegroups[durcount] = 0
            for line in rawtweets:
                if line.programme_position >= 0:
                    group = int(line.programme_position / 60)
                    if minutegroups.has_key(group):
                        minutegroups[group] += 1
            output += str(minutegroups)

    elif element == "status":
        if len(data) == 0:
            output += "404" # Invalid PID
        else:
            some_analysed = False
            some_unanalysed = False
            for row in data:
                if row.analysed == 1:
                    some_analysed = True
                elif row.analysed ==0:
                    some_unanalysed = True
            if some_analysed and not some_unanalysed:
                output += "200" # Fully Analysed
            elif some_unanalysed:
                output += "206" # Part Analysed

    if wrapper:
        return HttpResponse(output)
    else:
        return output

def rawtweets(request,pid,timestamp):
    output = header
    progdata = programmes.objects.filter(pid=pid).all()
    timestamp = int(timestamp)
    if len(progdata) == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
    else:
        endstamp = timestamp + 60
        channel = progdata[0].channel
        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
        progdate = datetime.utcfromtimestamp(progdata[0].timestamp) + timedelta(seconds=progdata[0].utcoffset)
        starttime = datetime.utcfromtimestamp(timestamp) + timedelta(seconds=progdata[0].utcoffset)
        endtime = datetime.utcfromtimestamp(endstamp) + timedelta(seconds=progdata[0].utcoffset)
        output += str(progdate.strftime("%d/%m/%Y")) + "<br />"
        output += "<strong>" + progdata[0].title + "</strong><br />"
        output += "Raw tweet output between " + str(starttime.strftime("%H:%M:%S")) + " and " + str(endtime.strftime("%H:%M:%S")) + "<br />"
        rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=endstamp).order_by('timestamp').all()
        output += "<div id=\"rawtweets\" style=\"font-size: 9pt\">"
        #tweetseccount = dict()
        for tweet in rawtweets:
        #    if tweetseccount.has_key(tweet.timestamp):
        #        tweetseccount[tweet.timestamp] += 1
        #    else:
        #        tweetseccount[tweet.timestamp] = 1
            output += "<br /><strong>" + str(datetime.utcfromtimestamp(tweet.timestamp + progdata[0].utcoffset)) + ":</strong> " + "@" + tweet.user + ": " + tweet.text
        output += "</div><br /><br />"
        output += "Tweets: <a href=\"/api/" + pid + "/" + str(timestamp) + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(timestamp) + ".xml\" target=\"_blank\">XML</a><br />"
        #if len(tweetseccount) > 0:
        #    tweetseccount = [(v,k) for k, v in tweetseccount.items()]
        #    tweetseccount.sort(reverse=True)
        #    output += "<br />" + str(tweetseccount)
        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=endstamp,is_common=0).order_by('-count').all()
        for entry in newanalysis:
            output += "<br />" + entry.word + ": " + str(entry.count) + " " + str(entry.is_keyword) + " " + str(entry.is_entity) + " " + str(entry.is_common)
    output += footer
    return HttpResponse(output)
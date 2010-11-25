# Create your views here.
from django.http import HttpResponse
from bookmarks.output.models import programmes,analyseddata,rawdata,wordanalysis,programmes_unique
from datetime import date,timedelta,datetime
from pygooglechart import SimpleLineChart, Axis #lc
import time
import string
import math
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
    output += "<br />This output is due to be replaced. New views are currently under development at <a href=\"/programmesv2/" + pid + "\">/programmesv2</a>.<br />"
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
                        wfdata = wordanalysis.objects.filter(timestamp=minute.timestamp,pid=pid,is_keyword=0).order_by('-count').all()
                        if len(wfdata) > 0:
                            lastwasbookmark = True
                            bookmarks.append(playertimemin)
                            # BOOKMARK TEST


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
                            jQuery.noConflict();
                            jQuery(document).ready(function() {
                                var refreshId = setInterval(function() {
                                    jQuery('#statistics').load('/data/statistics/""" + pid
        if timestamp:
            scripting += "/" + str(timestamp)
        if redux == "redux":
            scripting += "/redux"

        scripting += """?randval='+Math.random());
                                    jQuery('#graphs').load('/data/graphs/""" + pid
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

    output += """<!--[if IE]><script type=\"text/javascript\" src=\"/media/prototypejs/excanvas.js\"></script><![endif]-->
                <script type=\"text/javascript\" src=\"/media/prototypejs/prototype.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/base64.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/canvas2image.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/canvastext.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/flotr.js\"></script>"""
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later

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
        output += "<br /><div id=\"graphs\">"
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
                output += str(progdate.strftime("%d/%m/%Y %H:%M:%S")) + " (" + str(row.channel) + ")"
                output += "</a>"

        # TODO The channel linked to here won't necessarily be the right one
        output += "<br /><br />"#<a href=\"/channel-graph/" + row.channel + "/" + str(progdate.strftime("%Y/%m/%d")) + "/\">Back to channel page</a> -
        output += "<a href=\"http://www.bbc.co.uk/programmes/" + pid + "\" target=\"_blank\">View BBC /programmes page</a>"

    output += footer
    return HttpResponse(output)

def programmev2data(request,element,pid,timestamp=False,redux=False,wrapper=True):

    output = "" # Initialise output buffer
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later
    if timestamp:
        data = programmes.objects.filter(pid=pid,timestamp=timestamp).all()
    else:
        data = programmes.objects.filter(pid=pid).all()
    if element == "statistics":
        # Print a line like Total tweets: 7 - Tweets per minute - Mean: 0.27 - Median: 0 - Mode: 0 - STDev: 0.53
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

        output += "Total tweets: " + str(totaltweets) + " - Tweets per minute - Mean: " + str(round(meantweets,2))
        output += " - Median: " + str(round(mediantweets,2)) + " - Mode: " + str(round(modetweets,2))
        output += " - STDev: " + str(round(stdevtweets,2))
    elif element == "graphs":
        output += """<style type=\"text/css\">
                        .bmgradient {
                            background: #FF6633;
                            filter: progid:DXImageTransform.Microsoft.gradient(startColorStr='#FF6633', endColorStr='#FFDDAA'); /* for IE */
                            background: -webkit-gradient(linear, left top, right top, from(#FF6633), to(#FFDDAA)); /* Webkit */
                            background: -moz-linear-gradient(left,#FF6633,#FFDDAA); /* Firefox 3.6+ */
                        }
                    </style>"""
        minutegroups = dict()
        totaltweets = 0
        maxtweets = 0
        progtimestamp = 0
        progchannel = None
        progtimediff = 0
        reduxchannel = None
        for row in data:
            if row.timestamp > progtimestamp:
                progtimestamp = row.timestamp
                progtimediff = row.timediff
                progchannel = row.channel
                if reduxmapping.has_key(progchannel):
                    reduxchannel = reduxmapping[progchannel]
                else:
                    reduxchannel = progchannel
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
                if minutegroups.has_key(group):
                    minutegroups[group] += int(line.totaltweets)
                    if minutegroups[group] > maxtweets:
                        maxtweets = minutegroups[group]
                    totaltweets += line.totaltweets

        if maxtweets > 0:
            minuteitems = minutegroups.items()
            minuteitems.sort()

            jsminlist = str(minuteitems).replace(")","]")
            jsminlist = jsminlist.replace("(","[")

            output += "<div style=\"width: 990px; text-align: center; margin-left: 20px\"><strong>Tweets Per Minute vs. Programme Position</strong></div><div id=\"container\" style=\"width: 990px; height: 300px\"></div>"

            output += "<script type=\"text/javascript\">var data = " + jsminlist + "; var f =  Flotr.draw($('container'),[data],{label: 'test label', lines: {lineWidth: 1}});</script>"

            if len(data) == 1:
                meantweets = data[0].meantweets
                stdevtweets = data[0].stdevtweets
            else:
                meantweets = totaltweets / (master.duration / 60)
                stdevtotal = 0
                for minute in minuteitems:
                    # Calculate standard deviation
                    stdevtotal += (minute[1] - meantweets) * (minute[1] - meantweets)
                stdevtweets = math.sqrt(stdevtotal / len(minuteitems))

            slicewidth = int(1000/len(minuteitems))
            if slicewidth < 1:
                slicewidth = 1

            if redux == "redux":
                progdatetime = datetime.utcfromtimestamp(progtimestamp)
                progdatestring = progdatetime.strftime("%Y-%m-%d")
                progtimestring = progdatetime.strftime("%H-%M-%S")

            progskipplot = ""
            bookmarkplot = ""
            rawtweetplot = ""
            bookmarks = list()
            for minute in minuteitems:
                opacity = float(minute[1]) / maxtweets
                if redux == "redux":
                    # Any channel will work fine for redux but iPlayer needs the most recent
                    progskipplot += "<a href=\"http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(60*minute[0]) + "\" target=\"_blank\">"
                else:
                    progskipplot += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(minute[0]) + "m0s\" target=\"_blank\">"
                progskipplot += "<div style=\"float: left; opacity: " + str(opacity) + ";cursor: pointer;background-color: #3333FF; height: 40px; width: " + str(slicewidth) + "px;filter:alpha(opacity=" + str(int(opacity * 100)) + ")\"></div></a>"
                if len(data) == 1:
                    rawtweetplot += "<a href=\"/raw/" + pid + "/" + str(int(progtimestamp-progtimediff+(minute[0]*60))) + "\" target=\"_blank\"><div style=\"float: left; opacity: " + str(opacity) + ";cursor: pointer;background-color: #009933; height: 40px; width: " + str(slicewidth) + "px;filter:alpha(opacity=" + str(int(opacity * 100)) + ")\"></div></a>"
                else:
                    rawtweetplot += "<a href=\"/raw/" + pid + "/" + str(minute[0]) + "/aggregated\" target=\"_blank\"><div style=\"float: left; opacity: " + str(opacity) + ";cursor: pointer;background-color: #009933; height: 40px; width: " + str(slicewidth) + "px;filter:alpha(opacity=" + str(int(opacity * 100)) + ")\"></div></a>"

                if 1:
                    # Work out where the bookmarks should be

                    if minute[1] > (2.2*stdevtweets+meantweets) and minute[1] > 9: # Arbitrary value chosen for now - needs experimentation - was 9

                        wfdata = wordanalysis.objects.filter(timestamp=progtimestamp-progtimediff+(minute[0]*60),pid=pid,is_keyword=0).order_by('-count').all()

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
                                        bookmarkstart = int(tweet.timestamp)
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
                                rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=minute.timestamp,timestamp__lt=(minute.timestamp + 60)).order_by('-timestamp').all()
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
                                if (bookmarkend - bookmarkstart) > 60:
                                    bookmarks.append([bookmarkstart,bookmarkend])

            # The +3 in the widths below gets around an IE CSS issue. All other browsers will ignore it
            output += "<div id=\"blockcontainer\" style=\"margin-left: 28px; border: 1px solid #444444; max-width: " + str(len(minuteitems)*slicewidth) + "\">"
            if redux == "redux":
                output += "<div style=\"font-size: 8pt; padding: 2px 0px 2px 4px; background-color: #3333FF; opacity: 0.8; color: #FFFFFF; filter:alpha(opacity=30)\">Redux Links</div>"
            else:
                output += "<div style=\"font-size: 8pt; padding: 2px 0px 2px 4px; background-color: #3333FF; opacity: 0.8; color: #FFFFFF; filter:alpha(opacity=30)\">iPlayer Links</div>"
            output += "<div style=\"width= " + str(len(minuteitems)*slicewidth+3) + "px;overflow: hidden;height: 40px;\">" + progskipplot + "</div>"
            output += "<div style=\"font-size: 8pt; padding: 2px 0px 2px 4px; background-color: #FF6633; opacity: 0.8; color: #FFFFFF; filter:alpha(opacity=30)\">Bookmarks</div>"
            bmtotal = len(bookmarks)
            bmcurrent = 0
            bmsecondwidth = float(len(minuteitems)*slicewidth) / master.duration
            progstart = progtimestamp - progtimediff
            progend = progtimestamp - progtimediff + master.duration
            bookmarks.sort()
            for bookmark in bookmarks:
                if bmcurrent == 0 and bookmark[0] != progstart:
                    bookmarkplot += "<div style=\"float: left; background-color: #FFFFFF; height: 40px; width: " + str(int((bookmark[0] - progstart)*bmsecondwidth)) + "px\"></div>"
                #TODO Ensure that bookmarks that overlap are clearly defined - need gradient?
                bookmarkpos = bookmark[0] - progstart
                if redux == "redux":
                    # Any channel will work fine for redux but iPlayer needs the most recent
                    bookmarkplot += "<a href=\"http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(int(bookmarkpos)) + "\" target=\"_blank\">"
                else:
                    bookmarkmins = int(bookmarkpos / 60)
                    bookmarksecs = int(bookmarkpos % 60)
                    bookmarkplot += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(bookmarkmins) + "m" + str(bookmarksecs) + "s\" target=\"_blank\">"
                # Ensure that if the next bookmark overlaps, it is visible
                if (bmcurrent + 2) < bmtotal:
                    if bookmark[1] > bookmarks[bmcurrent+1][0]:
                        bookmark[1] = bookmarks[bmcurrent+1][0]
                bookmarkplot += "<div class=\"bmgradient\" style=\"background-color: #FF6633; float: left; opacity: 0.6; height: 40px; width: " + str(int((bookmark[1]-bookmark[0])*bmsecondwidth)) + "px; filter:alpha(opacity=40)\"></div></a>"
                if bmcurrent == (bmtotal - 1) and bookmark[1] != progend:
                    bookmarkplot += "<div style=\"float: left; cursor: pointer; background-color: #FFFFFF; height: 40px; width: " + str(int((progend - bookmark[1])*bmsecondwidth)) + "px\"></div>"
                bmcurrent += 1
            output += "<div style=\"width= " + str(len(minuteitems)*slicewidth+3) + "px;overflow: hidden;height: 40px;\">" + bookmarkplot + "</div>"
            output += "<div style=\"font-size: 8pt; padding: 2px 0px 2px 4px; background-color: #009933; opacity: 0.8; color: #FFFFFF; filter:alpha(opacity=30)\">Raw Data</div>"
            output += "<div style=\"width= " + str(len(minuteitems)*slicewidth+3) + "px;overflow: hidden;height: 40px;\">" + rawtweetplot + "</div>"

            output += "</div>"
        else:
            output += "No data found to generate graphs.<br />"
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

def rawtweetsv2(request,pid,timestamp,aggregated=False):
    output = header
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later
    progdata = programmes.objects.filter(pid=pid).all()
    timestamp = int(timestamp)
    if len(progdata) == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
    else:
        output += """<style type="text/css">
                            .xmpl { padding: 10px 15px 10px 15px !important; }
                            ul.xmpl { padding: 5px 15px 5px 30px !important; }
                            .xmpl li { z-index: 0 !important; }
                            ul.xmpl, ol.xmpl { height: 100px; overflow: hidden; padding: 0px !important; }
                        </style>
                        <script type=\"text/javascript\" src=\"/media/jquery/jquery.tagcloud.min.js\"></script>
                        <script type=\"text/javascript\" src=\"/media/jquery/jquery.tinysort.min.js\"></script>"""
        output += """<script type=\"text/javascript\">
                            $(document).ready(function() {
                            if ((document.cloudopts.keyword.checked == true) | (document.cloudopts.entity.checked == true) | (document.cloudopts.common.checked == true)) {
                                updateCloud();
                            } else {
                                $('#tagcloud').tagcloud({type:"list",sizemin:15,sizemax:30,colormin:"3399FF",colormax:"339900"}).find("li").tsort();
                            }
                            });
                            function updateCloud() {
                                urlappender = "/data/tagcloud/""" + pid + """/""" + str(timestamp)
        if aggregated == "aggregated":
            output += "/aggregated\";"
        else:
            output += "\";"
        output += """           if ((document.cloudopts.keyword.checked == true) | (document.cloudopts.entity.checked == true) | (document.cloudopts.common.checked == true)) {
                                    urlappender += "/";
                                }
                                if (document.cloudopts.keyword.checked == true) {
                                    urlappender += "k";
                                }
                                if (document.cloudopts.entity.checked == true) {
                                    urlappender += "e";
                                }
                                if (document.cloudopts.common.checked == true) {
                                    urlappender += "c";
                                }
                                urlappender += '?randval='+Math.random();
                                $('#cloudcontainer').html('<span style="font-size: 10pt">Loading...</span>');
                                $.get(urlappender, function(data) {
                                    $('#cloudcontainer').html(data);
                                    $('#tagcloud').tagcloud({type:"list",sizemin:15,sizemax:30,colormin:"3399FF",colormax:"339900"}).find("li").tsort();
                                });
                            }</script>"""
        if aggregated == "aggregated":
            output += "<br /><strong>" + master.title + "</strong><br /><br />"
            progpos = timestamp*60
            endstamp = progpos + 60
            # In this case the 'timestamp' is actually the programme position
            rawtweetdict = dict()
            for row in progdata:
                rawtweets = rawdata.objects.filter(pid=pid,programme_position__gte=progpos,programme_position__lt=endstamp).order_by('timestamp').all()
                for tweet in rawtweets:
                    if rawtweetdict.has_key(int(tweet.programme_position)):
                        rawtweetdict[int(tweet.programme_position)].append("<br /><strong>" + str(datetime.utcfromtimestamp(tweet.timestamp + row.utcoffset)) + ":</strong> " + "@" + tweet.user + ": " + tweet.text)
                    else:
                        rawtweetdict[int(tweet.programme_position)] = ["<br /><strong>" + str(datetime.utcfromtimestamp(tweet.timestamp + row.utcoffset)) + ":</strong> " + "@" + tweet.user + ": " + tweet.text]
            tweetitems = rawtweetdict.items()
            tweetitems.sort()
            output += "<form name=\"cloudopts\" style=\"font-size: 9pt\">Hide Keywords: <input type=\"checkbox\" value=\"keyword\" name=\"keyword\" onClick=\"updateCloud();\">&nbsp; Hide Twitter Entities: <input type=\"checkbox\" value=\"entity\" name=\"entity\" onClick=\"updateCloud();\">&nbsp; Hide Common Words: <input type=\"checkbox\" value=\"common\" name=\"common\" onClick=\"updateCloud();\"></form><div id=\"cloudcontainer\">"
            output += tagcloud(False,pid,timestamp,"aggregated",False)
            #TODO For this to support non-JS browsers, the URL scheme will need to include elements for rawtweets directly
            output += "</div><br />"
            output += "Raw tweet output between " + str(timestamp) + " minutes and " + str(timestamp + 1) + " minutes through the programme<br />"
            output += "<div id=\"rawtweets\" style=\"font-size: 9pt\">"
            for minute in tweetitems:
                for tweet in minute[1]:
                    output += tweet
            output += "</div>"
        else:
            endstamp = timestamp + 60
            channel = progdata[0].channel
            output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
            progdate = datetime.utcfromtimestamp(progdata[0].timestamp) + timedelta(seconds=progdata[0].utcoffset)
            starttime = datetime.utcfromtimestamp(timestamp) + timedelta(seconds=progdata[0].utcoffset)
            endtime = datetime.utcfromtimestamp(endstamp) + timedelta(seconds=progdata[0].utcoffset)
            output += str(progdate.strftime("%d/%m/%Y")) + "<br />"
            output += "<strong>" + master.title + "</strong><br /><br />"
            output += "<form name=\"cloudopts\" style=\"font-size: 9pt\">Hide Keywords: <input type=\"checkbox\" value=\"keyword\" name=\"keyword\" onClick=\"updateCloud();\">&nbsp; Hide Twitter Entities: <input type=\"checkbox\" value=\"entity\" name=\"entity\" onClick=\"updateCloud();\">&nbsp; Hide Common Words: <input type=\"checkbox\" value=\"common\" name=\"common\" onClick=\"updateCloud();\"></form><div id=\"cloudcontainer\">"
            output += tagcloud(False,pid,timestamp,False,False)
            #TODO For this to support non-JS browsers, the URL scheme will need to include elements for rawtweets directly
            output += "</div><br />"
            output += "Raw tweet output between " + str(starttime.strftime("%H:%M:%S")) + " and " + str(endtime.strftime("%H:%M:%S")) + "<br />"
            rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=endstamp).order_by('timestamp').all()
            output += "<div id=\"rawtweets\" style=\"font-size: 9pt\">"
            for tweet in rawtweets:
                output += "<br /><strong>" + str(datetime.utcfromtimestamp(tweet.timestamp + progdata[0].utcoffset)) + ":</strong> " + "@" + tweet.user + ": " + tweet.text
            output += "</div><br /><br />"
            output += "Tweets: <a href=\"/api/" + pid + "/" + str(timestamp) + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(timestamp) + ".xml\" target=\"_blank\">XML</a><br />"
    output += footer
    return HttpResponse(output)

def tagcloud(request,pid,timestamp,params=False,wrapper=True):
    output = ""
    if params:
        if "/" in params:
            params = params.split("/")
            aggregated = params[0]
            elements = params[1]
        else:
            if params == "aggregated":
                aggregated = params
                elements = False
            else:
                aggregated = False
                elements = params
    else:
        aggregated = False
        elements = False
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later
    progdata = programmes.objects.filter(pid=pid).all()
    timestamp = int(timestamp)
    if len(progdata) == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
    else:
        output += "<ul id=\"tagcloud\" class=\"xmpl\" style=\"width: 700px; height: auto; position: static; list-style: none outside none; margin: 0px; padding: 0px\">"
        if aggregated == "aggregated":
            progpos = timestamp*60
            # In this case the 'timestamp' is actually the programme position
            analysedwords = dict()
            for row in progdata:
                searchstamp = row.timestamp-row.timediff+progpos
                if elements:
                    if "k" in elements and "e" in elements and "c" in elements:
                        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp,is_keyword=0,is_entity=0,is_common=0).order_by('-count').all()
                    elif "k" in elements and "e" in elements:
                        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp,is_keyword=0,is_entity=0).order_by('-count').all()
                    elif "k" in elements and "c" in elements:
                        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp,is_keyword=0,is_common=0).order_by('-count').all()
                    elif "c" in elements and "e" in elements:
                        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp,is_entity=0,is_common=0).order_by('-count').all()
                    elif "k" in elements:
                        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp,is_keyword=0).order_by('-count').all()
                    elif "c" in elements:
                        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp,is_common=0).order_by('-count').all()
                    elif "e" in elements:
                        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp,is_entity=0).order_by('-count').all()
                else:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=searchstamp).order_by('-count').all()
                for word in newanalysis:
                    if analysedwords.has_key(word.word):
                        analysedwords[word.word] += int(word.count)
                    else:
                        analysedwords[word.word] = int(word.count)
            worditems = [[v, k] for k, v in analysedwords.items()]
            worditems.sort(reverse=True)
            currenttag = 0
            for word in worditems:
                if currenttag >= 100:
                    break
                output += "<li style=\"cursor: pointer\" title=\"" + word[1] + "\" value=\"" + str(word[0]) + "\"><a title=\"" + str(word[0]) + "\">" + word[1] + " </a></li>"
                currenttag += 1
        else:
            # The below seems horribly overcomplicated, but I'm failing to see an easier way given Django's API TODO
            if elements:
                if "k" in elements and "e" in elements and "c" in elements:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp,is_keyword=0,is_entity=0,is_common=0).order_by('-count').all()
                elif "k" in elements and "e" in elements:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp,is_keyword=0,is_entity=0).order_by('-count').all()
                elif "k" in elements and "c" in elements:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp,is_keyword=0,is_common=0).order_by('-count').all()
                elif "c" in elements and "e" in elements:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp,is_entity=0,is_common=0).order_by('-count').all()
                elif "k" in elements:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp,is_keyword=0).order_by('-count').all()
                elif "c" in elements:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp,is_common=0).order_by('-count').all()
                elif "e" in elements:
                    newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp,is_entity=0).order_by('-count').all()
            else:
                newanalysis = wordanalysis.objects.filter(pid=pid,timestamp=timestamp).order_by('-count').all()
            currenttag = 0
            for entry in newanalysis:
                if currenttag >= 100:
                    break
                #output += "<br />" + entry.word + ": " + str(entry.count) + " " + str(entry.is_keyword) + " " + str(entry.is_entity) + " " + str(entry.is_common)
                output += "<li style=\"cursor: pointer\" title=\"" + entry.word + "\" value=\"" + str(entry.count) + "\"><a title=\"" + str(entry.count) + "\">" + entry.word + " </a></li>"
                currenttag += 1
        output += "</ul>"
    if wrapper:
        return HttpResponse(output)
    else:
        return output
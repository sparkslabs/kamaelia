# Create your views here.
from django.http import HttpResponse
from bookmarks.output.models import programmes,analyseddata,rawdata
from datetime import date,timedelta,datetime
from pygooglechart import SimpleLineChart, Axis #lc
import time
import cjson
import string
import re
from django.core.exceptions import ObjectDoesNotExist
#TODO: Replace ugly meta refresh tags with AJAX

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]
            
radiochannels = ["radio1","1xtra","radio2","radio3","radio4","5live","sportsextra","6music","radio7","asiannetwork","worldservice"]

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

    output += "<h2>Note:</h2><p>- Some programme durations are currently identified incorrectly. Despite this, all data for the period will have been collected.</p><div style=\"display: inline; position: relative\"><h2>TV</h2>"
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
                output += "No Data</div>"
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
                output += "No Data</div>"
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
                endtimestamp = starttimestamp + 86400
                data = programmes.objects.filter(channel__exact=channel,timestamp__gte=starttimestamp,timestamp__lt=endtimestamp).order_by('timestamp').all()
                for programme in data:
                    progdate = datetime.utcfromtimestamp(programme.timestamp) + timedelta(seconds=programme.utcoffset)
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
                endtimestamp = starttimestamp + 86400
                data = programmes.objects.filter(channel__exact=channel,timestamp__gte=starttimestamp,timestamp__lt=endtimestamp).order_by('timestamp').all()
                for programme in data:
                    progdate = datetime.utcfromtimestamp(programme.timestamp) + timedelta(seconds=programme.utcoffset)

                    if programme.totaltweets > 0:

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

                        #TODO: Fix the bad labelling!
                        graph.set_title("Tweets per minute")
                        left_axis = ['',int(maxy/4),int(maxy/2),int(3*maxy/4),int(maxy)]
                        bottom_axis = [0,int(maxx/8),int(maxx/4),int(3*maxx/8),int(maxx/2),int(5*maxx/8),int(3*maxx/4),int(7*maxx/8),int(maxx)]
                        graph.set_axis_labels(Axis.LEFT,left_axis)
                        graph.set_axis_labels(Axis.BOTTOM,bottom_axis)
                        output += "<br /><img src=\"" + graph.get_url() + "\"><br />"

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

def programme(request,pid):
    # Now that this is live, would be clever to use AJAX to refresh graphs etc every minute whilst still unanalysed?

    output = header
    data = programmes.objects.filter(pid=pid).all()
    if len(data) == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    elif len(data) == 1:
        if data[0].analysed == 0:
            output += "<meta http-equiv='refresh' content='30'>"
        channel = data[0].channel
        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
        progdate = datetime.utcfromtimestamp(data[0].timestamp) + timedelta(seconds=data[0].utcoffset)
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
                        try:
                            wfdata = cjson.decode(minute.wordfrequnexpected)
                            unexpecteditems = [(v,k) for k, v in wfdata.items()]
                            unexpecteditems.sort(reverse=True)
                            if len(unexpecteditems) > 0:
                                # Find most popular keyword
                                keyword = unexpecteditems[0][1]
                                # Now look at each previous minute until it's no longer the top keyword
                                topkeyword = keyword
                                currentstamp = minute.timestamp
                                while topkeyword == keyword:
                                    currentstamp -= 60
                                    try:
                                        dataset = analyseddata.objects.get(pid=pid,timestamp=currentstamp)
                                    except ObjectDoesNotExist:
                                        break
                                    wfdata = cjson.decode(dataset.wordfrequnexpected)
                                    unexpecteditems = [(v,k) for k, v in wfdata.items()]
                                    unexpecteditems.sort(reverse=True)
                                    if len(unexpecteditems) > 0:
                                        # Find most popular keyword
                                        topkeyword = unexpecteditems[0][1]

                                startstamp = currentstamp
                                endstamp = currentstamp + 60
                                
                                # Investigate the previous minute
                                tweetset = False
                                rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=startstamp,timestamp__lt=endstamp).order_by('timestamp').all()
                                for tweet in rawtweets:
                                    tweettext = string.lower(tweet.text)
                                    for items in """!"#$%&(),:;?@~[]'`{|}""":
                                        tweettext = string.replace(tweettext,items,"")
                                    try:
                                        if str(keyword) in tweettext:
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
                                            if str(keyword) in tweettext:
                                                bookmarkstest.append(tweet.timestamp)
                                                break
                                        except UnicodeEncodeError:
                                            break
                        except cjson.DecodeError, e:
                            # Data is too old - no word freq data
                            pass
                        except AttributeError, e:
                            # As above
                            pass

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

            #TODO: Fix the bad labelling!
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
                    output += "<br /><a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(playertimemin) + "m" + str(playertimesec) + "s\" target=\"_blank\">http://bbc.co.uk/i/" + pid + "/?t=" + str(playertimemin) + "m" + str(playertimesec) + "s</a>"
        else:
            output += "<br />Not enough data to generate statistics.<br />"

        output += "<br /><br />API: <a href=\"/api/" + data[0].pid + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + data[0].pid + ".xml\" target=\"_blank\">XML</a>"
        # Reveal tweets is temporary - will allow selection and viewing of single minutes once the database has been redesigned.
        output += "<br /><br /><a href=\"/channel-graph/" + data[0].channel + "/" + str(progdate.strftime("%Y/%m/%d")) + "/\">Back to channel page</a> - <a href=\"http://www.bbc.co.uk/programmes/" + data[0].pid + "\" target=\"_blank\">View BBC /programmes page</a>"

    else:
        output += "<br />Database consistency error - somehow a primary key appears twice. The world may have ended."
        output += "<br /><br /><a href=\"/\">Back to index</a>"

    output += footer
    return HttpResponse(output)

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
        analysedtweets = analyseddata.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=endstamp).all()
        output += "<br /><b>Testing:</b>"
        for entry in analysedtweets:
            output += "<br />" + entry.wordfreqexpected + "<br />" + entry.wordfrequnexpected
        output += "<br />"
        rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=endstamp).order_by('timestamp').all()
        output += "<div id=\"rawtweets\" style=\"font-size: 9pt\">"
        #tweetseccount = dict()
        for tweet in rawtweets:
        #    if tweetseccount.has_key(tweet.timestamp):
        #        tweetseccount[tweet.timestamp] += 1
        #    else:
        #        tweetseccount[tweet.timestamp] = 1
            output += "<br /><strong>" + str(datetime.utcfromtimestamp(tweet.timestamp + progdata[0].utcoffset)) + ":</strong> " + "@" + tweet.user + ": " + tweet.text
        output += "</div>"
        #if len(tweetseccount) > 0:
        #    tweetseccount = [(v,k) for k, v in tweetseccount.items()]
        #    tweetseccount.sort(reverse=True)
        #    output += "<br />" + str(tweetseccount)
    output += footer
    return HttpResponse(output)
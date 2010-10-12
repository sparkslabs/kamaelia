# Create your views here.
from django.http import HttpResponse
from bookmarks.output.models import programmes,analyseddata,rawdata
from datetime import date,timedelta,datetime
from dateutil.parser import parse
from pygooglechart import SimpleLineChart, Axis #lc
#TODO: Replace ugly meta refresh tags with AJAX

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]
            
radiochannels = ["radio1","1xtra","radio2","radio3","radio4","5live","sportsextra","6music","radio7","asiannetwork","worldservice"]

allchannels = tvchannels + radiochannels

header = '<html><head><title>Social Bookmarks</title><script type="text/javascript" src="/media/jquery/jquery.min.js"></script>\
            </head><body style="margin: 0px"><div style="background-color: #FFFFFF; position: absolute; width: 100%; height: 100%">\
            <div style="width: 100%; overflow: hidden; height: 80px; font-family: Arial, Helvetica, sans-serif; position: absolute; background-color: #A9D0F5">\
            <div style="padding-left: 10px"><h1>Social Bookmarks</h1></div></div><div style="position: absolute; top: 80px; font-family: Arial, Helvetica, sans-serif; padding: 10px">'

footer = '</div></div></body></html>'

def index(request):
    # TODO: This page is now horribly inefficient - ugh
    currentdate = date.today()
    output = header
    output += "<meta http-equiv='refresh' content='30'>"
    output += "<style type=\"text/css\">.box a:link, .box a:visited, .box a:active, .box a:hover { color: inherit; }</style>"
    # Prevent division by zero later on...
    #maxtweets = 1
    largeststdev = 1

    # Identify the total tweets for each current programme (provided the grabber is still running)
    for channel in allchannels:
        data = programmes.objects.filter(channel=channel).order_by('-expectedstart')
        if len(data) > 0:
            progdate = parse(data[0].expectedstart)
            progdate = progdate.replace(tzinfo=None)
            progdate = progdate + timedelta(seconds=data[0].duration)
            datenow = datetime.now()
            #if data[0].totaltweets > maxtweets and datenow <= progdate:
            #    maxtweets = data[0].totaltweets
            if data[0].stdevtweets > largeststdev and datenow <= progdate:
                largeststdev = data[0].stdevtweets

    #normaliser = 1/float(maxtweets)
    normaliser = 1/float(largeststdev)

    output += "<div style=\"display: inline; position: relative\"><h2>TV</h2>"
    for channel in tvchannels:
        data = programmes.objects.filter(channel=channel).order_by('-expectedstart')
        if len(data) > 0:
            progdate = parse(data[0].expectedstart)
            tz = progdate.tzinfo
            offset = datetime.strptime(str(tz.utcoffset(progdate)),"%H:%M:%S")
            offset = timedelta(hours=offset.hour)
            progdate = progdate.replace(tzinfo=None)
            progend = progdate + timedelta(seconds=data[0].duration - data[0].timediff)
            datenow = datetime.utcnow() + offset
            if datenow <= progend:
                opacity = normaliser * data[0].stdevtweets
                #fontval = str(int(255 * opacity))
                if opacity < 0.5:
                    fontcolour = "#000000"
                else:
                    fontcolour = "#FFFFFF"
                bgval = str(int(255 - (255 * opacity)))
                #fontcolour = "rgb(" + fontval + "," + fontval + "," + fontval + ")"
                bgcolour = "rgb(" + bgval + "," + bgval + "," + bgval + ")"
                output += "<div style=\"float: left; margin-right: 5px;\"><a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "<div id=\"" + channel + "\" class=\"box\" style=\"width: 77px; background-color: " + bgcolour + "; color: " + fontcolour + "; text-align: center;\"><a href=\"/programmes/" + data[0].pid + "/\" style=\"text-decoration: none\">" + str(data[0].totaltweets) + "</a></div></div>"
            else:
                output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "No Data</div>"
        else:
            output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
            output += "No Data</div>"

    output += "<br /><br /></div><br /><br /><div style=\"display: inline; position: relative\"><h2>Radio</h2>"
    for channel in radiochannels:
        data = programmes.objects.filter(channel=channel).order_by('-expectedstart')
        if len(data) > 0:
            progdate = parse(data[0].expectedstart)
            tz = progdate.tzinfo
            offset = datetime.strptime(str(tz.utcoffset(progdate)),"%H:%M:%S")
            offset = timedelta(hours=offset.hour)
            progdate = progdate.replace(tzinfo=None)
            progend = progdate + timedelta(seconds=data[0].duration - data[0].timediff)
            datenow = datetime.utcnow() + offset
            if datenow <= progend:
                opacity = normaliser * data[0].stdevtweets
                #fontval = str(int(255 * opacity))
                if opacity < 0.5:
                    fontcolour = "#000000"
                else:
                    fontcolour = "#FFFFFF"
                bgval = str(int(255 - (255 * opacity)))
                #fontcolour = "rgb(" + fontval + "," + fontval + "," + fontval + ")"
                bgcolour = "rgb(" + bgval + "," + bgval + "," + bgval + ")"
                output += "<div style=\"float: left; margin-right: 5px;\"><a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "<div id=\"" + channel + "\" class=\"box\" style=\"width: 77px; background-color: " + bgcolour + "; color: " + fontcolour + "; text-align: center;\"><a href=\"/programmes/" + data[0].pid + "/\" style=\"text-decoration: none\">" + str(data[0].totaltweets) + "</a></div></div>"
            else:
                output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
                output += "No Data</div>"
        else:
            output += "<div style=\"float: left; margin-right: 5px; text-align: center\"><a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
            output += "No Data</div>"
        
    output += "<br /><br /></div><br />API: <a href=\"/api/summary.json\" target=\"_blank\">JSON</a> - <a href=\"/api/summary.xml\" target=\"_blank\">XML</a>" + footer

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
                datecomp = year + "-" + month + "-" + day
                output += "<br />Currently viewing shows for " + day + "/" + month + "/" + year + "<br />"
                data = programmes.objects.filter(channel__exact=channel,expectedstart__contains=datecomp).order_by('expectedstart').all()
                for programme in data:
                    progdate = parse(programme.expectedstart)
                    progdate = progdate.replace(tzinfo=None)
                    output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "\">" + programme.title + "</a>"
                if len(data) < 1:
                    output += "<br />No data for this date - please select another from the picker above.<br />"
            else:
                output += "<br />Please select a date from the picker above.<br />"
        output += "<br /><br /><a href=\"/\">Back to index</a>"

    output += footer
    return HttpResponse(output)

def programme(request,pid):
    # When doing API in json/RDF? look at 'Outputting CSV with Django' online.
    # Now that this is live, would be clever to use AJAX to refresh graphs etc every minute whilst still unanalysed?

    output = header
    output += "<script type=\"text/javascript\">"
    output += "function revealTweets() {"
    output += "if (document.getElementById('rawtweets').style.display == 'none') {"
    output += "document.getElementById('rawtweets').style.display = 'inline';"
    output += "} else {"
    output += "document.getElementById('rawtweets').style.display = 'none';"
    output += "}}</script>"

    data = programmes.objects.filter(pid=pid).all()
    if len(data) == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    elif len(data) == 1:
        if data[0].analysed == 0:
            output += "<meta http-equiv='refresh' content='30'>"
        channel = data[0].channel
        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
        progdate = parse(data[0].expectedstart)
        tz = progdate.tzinfo
        progdate = progdate.replace(tzinfo=None)
        actualstart = progdate - timedelta(seconds=data[0].timediff)
        minutedata = analyseddata.objects.filter(pid=pid).order_by('datetime').all()
        output += str(progdate.strftime("%d/%m/%Y")) + "<br />"
        output += "<strong>" + data[0].title + "</strong><br />"
        output += "Expected show times: " + str(progdate.strftime("%H:%M:%S")) + " to " + str((progdate + timedelta(seconds=data[0].duration)).strftime("%H:%M:%S")) + "<br />"
        output += "Actual show times (estimated): " + str(actualstart.strftime("%H:%M:%S")) + " to " + str((actualstart + timedelta(seconds=data[0].duration)).strftime("%H:%M:%S")) + "<br />"
        #if data[0].imported == 0:
        #    output += "<br />Data for this programme has not been flagged as imported."
        #    output += "<br />- This may indicate that the programme is yet to finish."
        #    output += "<br />- If the programme finished over 5 minutes ago, you may need to set the flag manually."
        #elif data[0].analysed == 0:
        #    output += "<br />Data for this programme has been imported but is awaiting analysis."
        #else:
            # Still need to add some form of chart or charts here - looking at Google Chart API first.
            # Would be worth caching charts if poss to avoid too many API calls.
        if 1:
            tweetmins = dict()
            appender = ""
            lastwasbookmark = False
            bookmarks = list()
            bookmarkcont = list()
            for minute in minutedata:
                # This isn't the most elegant BST solution, but it appears to work
                offset = datetime.strptime(str(tz.utcoffset(parse(minute.datetime))),"%H:%M:%S")
                offset = timedelta(hours=offset.hour)
                tweettime = parse(minute.datetime) + offset
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
                appender += "<br />" + str(tweettime.strftime("%H:%M")) + ": <a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(playertimemin) + "m" + str(playertimesec) + "s\" target=\"_blank\">" + str(minute.totaltweets) + "</a>"
                if minute.totaltweets > (1.5*data[0].stdevtweets+data[0].meantweets):
                    if lastwasbookmark == True:
                        appender += " cont'd..."
                        bookmarkcont.append(playertimemin)
                    else:
                        if minute.totaltweets > (2.2*data[0].stdevtweets+data[0].meantweets):
                            appender += " BOOKMARK!"
                            lastwasbookmark = True
                            bookmarks.append(playertimemin)
                        else:
                            lastwasbookmark = False
                else:
                    lastwasbookmark = False
                if not tweetmins.has_key(str(playertimemin)):
                    tweetmins[str(playertimemin)] = int(minute.totaltweets)
            if len(tweetmins) > 0:
                output += "<br />Tweets per minute - Mean: " + str(round(data[0].meantweets,2)) + " - Median: " + str(data[0].mediantweets) + " - Mode: " + str(data[0].modetweets) + " - STDev: " + str(round(data[0].stdevtweets,2)) + "<br />"
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
                blockgraph = "<div style=\"border-top: 1px #CCCCCC solid; border-left: 1px #CCCCCC solid; border-right: 1px #CCCCCC solid; height: 100px; width: " + str(mainwidth) + "px\">"
                width = int(1000/(maxx+1))
                for min in xlist:
                    if tweetmins.has_key(str(min)):
                        opacity = float(tweetmins[str(min)]) / maxy
                    else:
                        opacity = 0
                    blockgraph += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(min) + "m" + str(playertimesec) + "s\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 100px; float: left; background-color: #000000; opacity: " + str(opacity) + "; filter:alpha(opacity=" + str(int(opacity * 100)) + ")\"></div></a>"
                blockgraph += "</div>"

                blockgraph2 = "<div style=\"border-bottom: 1px #CCCCCC solid; border-left: 1px #CCCCCC solid; border-right: 1px #CCCCCC solid; height: 20px; width: " + str(mainwidth) + "px\">"
                for min in xlist:
                    if min in bookmarks and max(tweetmins.values()) > 9: # Arbitrary value chosen for now - needs experimentation - was 9
                        blockgraph2 += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(min) + "m" + str(playertimesec) + "s\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #888888\"></div></a>"
                        lastbookmark = min
                    elif min in bookmarkcont and max(tweetmins.values()) > 9: # Arbitrary value chosen for now - needs experimentation - was 9
                        blockgraph2 += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(lastbookmark) + "m" + str(playertimesec) + "s\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #888888\"></div></a>"
                    else:
                        blockgraph2 += "<div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #FFFFFF\"></div>"
                blockgraph2 += "</div>"

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
                output += "<br /><img src=\"" + graph.get_url() + "\"><br /><br />"
                output += blockgraph
                output += blockgraph2
                #output += appender
            else:
                output += "<br />Not enough data to generate statistics.<br />"

        output += "<br /><br />API: <a href=\"/api/" + data[0].pid + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + data[0].pid + ".xml\" target=\"_blank\">XML</a>"
        # Reveal tweets is temporary - will allow selection and viewing of single minutes once the database has been redesigned.
        output += "<br /><br /><a href=\"/channels/" + data[0].channel + "/" + str(progdate.strftime("%Y/%m/%d")) + "/\">Back to channel page</a> - <a href=\"javascript:revealTweets()\">View all / hide all tweets</a> - <a href=\"http://www.bbc.co.uk/programmes/" + data[0].pid + "\" target=\"_blank\">View BBC /programmes page</a>"

        # The below is a lesser of two evils solution - Ideally tweets for individual minutes would be grabbed via AJAX upon request.
        # This can't be added without significant pain until the database has been restructured slightly to use better format dates and times for raw tweets
        rawtweets = rawdata.objects.filter(pid=pid).all()
        output += "<br /><br /><div id=\"rawtweets\" style=\"display: none; font-size: 9pt\">"
        for tweet in rawtweets:
            output += "<br /><strong>" + tweet.datetime + ":</strong> " + tweet.text
        output += "</div>"
    else:
        output += "<br />Database consistency error - somehow a primary key appears twice. The world may have ended."
        output += "<br /><br /><a href=\"/\">Back to index</a>"

    output += footer
    return HttpResponse(output)
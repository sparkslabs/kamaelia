# Create your views here.
from django.http import HttpResponse
from bookmarks.output.models import programmes,analyseddata
from datetime import date,timedelta,datetime
from dateutil.parser import parse
from pygooglechart import SimpleLineChart, Axis #lc

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]
            
radiochannels = ["radio1","1xtra","radio2","radio3","radio4","radio5","sportsextra","6music","radio7","asiannetwork","worldservice"]

header = '<html><head><title>Social Bookmarks</title><script type="text/javascript" src="/media/jquery/jquery.min.js"></script></head><body><h1>Social Bookmarks</h1>'

footer = '</body></html>'

def index(request):
    currentdate = date.today()
    output = header

    output += "<br />Notice the severe lack of CSS<br />"

    output += "<h2>TV</h2>"
    for channel in tvchannels:
        output += "<a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a> "
    output += "<br /><h2>Radio</h2>"
    for channel in radiochannels:
        output += "<a href=\"/channels/" + channel + "/" + str(currentdate.strftime("%Y/%m/%d")) + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a> "
        
    output += footer
    return HttpResponse(output)

def channel(request,channel,year=0,month=0,day=0):
    output = header
    data = programmes.objects.filter(channel=channel)
    if channel not in radiochannels and channel not in tvchannels:
        output += "Invalid channel supplied."
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
        
        output += "<a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
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
    output = header

    data = programmes.objects.filter(pid=pid).all()
    if len(data) == 0:
        output += "Invalid pid supplied or no data has yet been captured for this programme."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    elif len(data) == 1:
        channel = data[0].channel
        output += "<a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
        progdate = parse(data[0].expectedstart)
        tz = progdate.tzinfo
        progdate = progdate.replace(tzinfo=None)
        actualstart = progdate + timedelta(seconds=data[0].timediff)
        minutedata = analyseddata.objects.filter(pid=pid).order_by('datetime').all()
        output += str(progdate.strftime("%d/%m/%Y")) + "<br />"
        output += "<strong>" + data[0].title + "</strong><br />"
        output += "Expected show times: " + str(progdate.strftime("%H:%M:%S")) + " to " + str((progdate + timedelta(seconds=data[0].duration)).strftime("%H:%M:%S")) + "<br />"
        output += "Actual show times (estimated): " + str(actualstart.strftime("%H:%M:%S")) + " to " + str((actualstart + timedelta(seconds=data[0].duration)).strftime("%H:%M:%S")) + "<br />"
        if data[0].imported == 0:
            output += "<br />Data for this programme has not been flagged as imported."
            output += "<br />- This may indicate that the programme is yet to finish."
            output += "<br />- If the programme finished over 5 minutes ago, you may need to set the flag manually."
        elif data[0].analysed == 0:
            output += "<br />Data for this programme has been imported but is awaiting analysis."
        else:
            # Still need to add some form of chart or charts here - looking at Google Chart API first.
            # Would be worth caching charts if poss to avoid too many API calls.            
            tweetmins = dict()
            appender = ""
            for minute in minutedata:
                # This isn't the most elegant BST solution, but it appears to work
                offset = datetime.strptime(str(tz.utcoffset(parse(minute.datetime))),"%H:%M:%S")
                offset = timedelta(hours=offset.hour)
                tweettime = parse(minute.datetime) + offset
                proghour = tweettime.hour - actualstart.hour
                progmin = tweettime.minute - actualstart.minute
                progsec = tweettime.second - actualstart.second
                playertime = (((proghour * 60) + progmin) * 60) + progsec
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
                if not tweetmins.has_key(str(playertimemin)):
                    tweetmins[str(playertimemin)] = int(minute.totaltweets)

            if len(tweetmins) > 0:
                output += "<br />Tweets per minute - Mean: " + str(round(data[0].meantweets,2)) + " - Median: " + str(data[0].mediantweets) + " - Mode: " + str(data[0].modetweets) + "<br />"
                xlist = range(0,data[0].duration/60)
                ylist = list()
                for min in xlist:
                    if tweetmins.has_key(str(min)):
                        ylist.append(tweetmins[str(min)])
                    else:
                        ylist.append(0)

                maxy = max(ylist)
                maxx = max(xlist)
                graph = SimpleLineChart(750,300,y_range=[0,maxy])
                graph.add_data(ylist)

                #TODO: Fix the bad labelling!
                graph.set_title("Tweets per minute (with bad labelling)")
                left_axis = ['',int(maxy/4),int(maxy/2),int(3*maxy/4),int(maxy)]
                bottom_axis = [0,int(maxx/8),int(maxx/4),int(3*maxx/8),int(maxx/2),int(5*maxx/8),int(3*maxx/4),int(7*maxx/8),int(maxx)]
                graph.set_axis_labels(Axis.LEFT,left_axis)
                graph.set_axis_labels(Axis.BOTTOM,bottom_axis)
                output += "<br /><img src=\"" + graph.get_url() + "\"><br />"
                output += appender
            else:
                output += "<br />Not enough data to generate statistics.<br />"

        output += "<br /><br /><a href=\"/channels/" + data[0].channel + "/" + str(progdate.strftime("%Y/%m/%d")) + "/\">Back to channel page</a> - <a href=\"http://www.bbc.co.uk/programmes/" + data[0].pid + "\" target=\"_blank\">View BBC /programmes page</a>"
    else:
        output += "Database consistency error - somehow a primary key appears twice..."
        output += "<br /><br /><a href=\"/\">Back to index</a>"

    output += footer
    return HttpResponse(output)
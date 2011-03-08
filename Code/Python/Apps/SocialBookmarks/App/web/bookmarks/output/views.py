from django.http import HttpResponse
from bookmarks.output.models import programmes,analyseddata,rawdata,wordanalysis,programmes_unique
from datetime import date,timedelta,datetime
from pygooglechart import SimpleLineChart, Axis #lc (line chart)
from django.core.exceptions import ObjectDoesNotExist
import time
import string
import math
#TODO: Replace ugly meta refresh tags with AJAX in index

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
    '''
    Main index page for social bookmarks
    '''
    output = header
    # Ajax refresh code for divs
    scripting = """<script>
                        jQuery.noConflict();
                        jQuery(document).ready(function() {
                            var refreshId = setInterval(function() {
                                jQuery('#tv').load('/data/index/tv?randval='+Math.random());
                                jQuery('#radio').load('/data/index/radio?randval='+Math.random());}, 20000);
                });
                </script>"""

    output += scripting

    # Allowance for non-JS browsers
    output += "<noscript><meta http-equiv='refresh' content='60'></noscript>"
    output += "<style type=\"text/css\">.box a:link, .box a:visited, .box a:active, .box a:hover { color: inherit; }</style>"

    # Display all TV channels
    output += "<div style=\"display: inline; position: relative\" id=\"tv\">"
    output += indexdata(False,"tv",False)

    # Display all radio channels
    output += "</div><br /><br /><div style=\"display: inline; position: relative\" id=\"radio\">"
    output += indexdata(False,"radio",False)

    # Print API links
    output += "</div><br /><br />API: <a href=\"/api/summary.json\" target=\"_blank\">JSON</a> - <a href=\"/api/summary.xml\" target=\"_blank\">XML</a>" + footer

    return HttpResponse(output)

def indexdata(request,channelgroup,wrapper=True):
    '''
    Data generator for index page for AJAX
    '''

    output = ""

    currentdate = date.today()
    # Prevent division by zero later on...
    largeststdev = 1

    # Find the largest standard deviation recorded for a current programme to act as a normaliser
    for channel in allchannels:
        data = programmes.objects.filter(channel=channel).latest('timestamp')
        if isinstance(data,object):
            if data.stdevtweets > largeststdev and data.imported==0:
                largeststdev = data.stdevtweets

    normaliser = 1/float(largeststdev)

    if channelgroup == "tv":
        output += "<h2>TV</h2>"
        for channel in tvchannels:
            data = programmes.objects.filter(channel=channel).latest('timestamp')
            if isinstance(data,object):
                if data.imported==0:
                    # Generate a colour (opacity) based on this channel's standard deviation and the normaliser
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
    elif channelgroup == "radio":
        output += "<h2>Radio</h2>"
        for channel in radiochannels:
            data = programmes.objects.filter(channel=channel).latest('timestamp')
            if isinstance(data,object):
                if data.imported==0:
                    # Generate a colour (opacity) based on this channel's standard deviation and the normaliser
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

    output += "<br /><br />"
    if wrapper:
        return HttpResponse(output)
    else:
        return output

def channel(request,channel,year=0,month=0,day=0):
    '''
    Channel page, accessible via /channels/bbcone etc
    '''
    output = header
    data = programmes.objects.filter(channel=channel)
    if channel not in radiochannels and channel not in tvchannels:
        output += "<br />Invalid channel supplied."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    else:
        # Print the date picker (requires up to dat jQuery - included)
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

        # Print channel logo
        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
        if len(data) < 1:
            output += "<br />Please note: No data has yet been captured for this channel."
        else:
            output += '<br /><div id="inlineDatepicker"></div>'
            if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
                output += "<br />Currently viewing shows for " + day + "/" + month + "/" + year + "<br />"
                starttimestamp = time.mktime(datetime(int(year),int(month),int(day),0,0,0,0).timetuple())
                # Work out (roughly) whether or not the iPlayer programme will have expired - if so, show redux
                if starttimestamp + (86400 * 8) < time.time():
                    redux = True
                else:
                    redux = False
                endtimestamp = starttimestamp + 86400
                data = programmes.objects.filter(channel__exact=channel,timestamp__gte=starttimestamp,timestamp__lt=endtimestamp).order_by('timestamp').all()
                for programme in data:
                    try:
                        master = programmes_unique.objects.get(pid=programme.pid)
                    except ObjectDoesNotExist, e:
                        pass # This is handled later
                    progdate = datetime.utcfromtimestamp(programme.timestamp) + timedelta(seconds=programme.utcoffset)
                    # For each programme on the day specified, print the time and link to the programme's page
                    if redux:
                        output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "/redux\">" + master.title + "</a>"
                    else:
                        output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "\">" + master.title + "</a>"
                if len(data) < 1:
                    output += "<br />No data for this date - please select another from the picker above.<br />"
            else:
                output += "<br />Please select a date from the picker above.<br />"
        output += "<br /><br /><a href=\"/\">Back to index</a> - <a href=\"/channel-graph/" + channel + "/" + str(year) + "/" + str(month) + "/" + str(day) + "\">Graphical view</a>"

    output += footer
    return HttpResponse(output)

def channelgraph(request,channel,year=0,month=0,day=0):
    '''
    Channel graph page, accessible via /channel-graph/bbcone etc
    '''
    output = header
    data = programmes.objects.filter(channel=channel)
    if channel not in radiochannels and channel not in tvchannels:
        output += "<br />Invalid channel supplied."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    else:
        # Print date picker - must use jQuery with noConflict option to avoid conflict with Prototype JS namespace
        output += '<style type="text/css">@import "/media/jquery/jquery.datepick.css";</style>\n \
                    <script type="text/javascript" src="/media/jquery/jquery.datepick.js"></script>\n'
        output += "<script type=\"text/javascript\">\n \
                        jQuery.noConflict();\
                        jQuery(function() {\n "
        if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
            output += "jQuery('#inlineDatepicker').datepick({onSelect: showDate, defaultDate: '" + month + "/" + day + "/" + year + "', selectDefaultDate: true});\n"
        else:
            output += "jQuery('#inlineDatepicker').datepick({onSelect: showDate});\n "
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
        # Include prototype JS for graph generation
        output += """<!--[if IE]><script type=\"text/javascript\" src=\"/media/prototypejs/excanvas.js\"></script><![endif]-->
                <script type=\"text/javascript\" src=\"/media/prototypejs/prototype.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/base64.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/canvas2image.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/canvastext.js\"></script>
                <script type=\"text/javascript\" src=\"/media/prototypejs/flotr.js\"></script>"""

        output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br />"
        if len(data) < 1:
            output += "<br />Please note: No data has yet been captured for this channel."
        else:
            output += '<br /><div id="inlineDatepicker"></div>'
            if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
                output += "<br />Currently viewing shows for " + day + "/" + month + "/" + year + "<br />"
                starttimestamp = time.mktime(datetime(int(year),int(month),int(day),0,0,0,0).timetuple())
                # Roughly identify if the iPlayer programmes have expired - if so show redux instead
                if starttimestamp + (86400 * 8) < time.time():
                    redux = True
                else:
                    redux = False
                endtimestamp = starttimestamp + 86400
                data = programmes.objects.filter(channel__exact=channel,timestamp__gte=starttimestamp,timestamp__lt=endtimestamp).order_by('timestamp').all()
                for programme in data:
                    # Cycle through each programme printing its name and time along with a graph
                    progdate = datetime.utcfromtimestamp(programme.timestamp) + timedelta(seconds=programme.utcoffset)
                    try:
                        master = programmes_unique.objects.get(pid=programme.pid)
                    except ObjectDoesNotExist, e:
                        pass # This is handled later
                    if programme.totaltweets > 0:
                        # Only print the graph if there is actually some data
                        if redux:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "/redux\">" + master.title + "</a> (see below)"
                        else:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "\">" + master.title + "</a> (see below)"

                        # Use the data generating function to get the graph
                        output += programmev2data(False,"graphs-channel",programme.pid,programme.timestamp,redux,False)

                    else:
                        # No data so don't print a graph
                        if redux:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "/redux\">" + master.title + "</a>"
                        else:
                            output += "<br />" + str(progdate.strftime("%H:%M")) + ": <a href=\"/programmes/" + programme.pid + "\">" + master.title + "</a>"
                        output += " - No data available<br />"

                if len(data) < 1:
                    output += "<br />No data for this date - please select another from the picker above.<br />"
            else:
                output += "<br />Please select a date from the picker above.<br />"
        output += "<br /><br /><a href=\"/\">Back to index</a> - <a href=\"/channels/" + channel + "/" + str(year) + "/" + str(month) + "/" + str(day) + "\">Textual view</a>"

    output += footer
    return HttpResponse(output)

def programme(request,pid,redux=False):
    '''
    This is a deprecated version of the /programmes/pid page
    Doesn't handle cases where a PID has been broadcast more than one - simply displays an error in this case
    Accessible via /programmes-old/pid
    '''
    output = header
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later
    data = programmes.objects.filter(pid=pid).all()
    if len(data) == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    elif len(data) == 1:
        # Only display data if the programme has a single recorded broadcast
        if data[0].analysed == 0:
            # If the programme is still running (or rather hasn't been fully analysed) keep refreshing the page
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
        output += "<strong>" + master.title + "</strong><br />"
        output += "Expected show times: " + str(progdate.strftime("%H:%M:%S")) + " to " + str((progdate + timedelta(seconds=master.duration)).strftime("%H:%M:%S")) + "<br />"
        output += "Actual show times (estimated): " + str(actualstart.strftime("%H:%M:%S")) + " to " + str((actualstart + timedelta(seconds=master.duration)).strftime("%H:%M:%S")) + "<br />"
        output += "<br />Total tweets: " + str(data[0].totaltweets)
        tweetmins = dict()
        tweetstamps = dict()
        lastwasbookmark = False
        # Bookmarks is a list containing the starting minute for identified bookmarks
        bookmarks = list()
        # Should bookmarks span more than one minute, they are added to bookmarkcont
        bookmarkcont = list()
        # New version bookmarks including some word frequency analysis are held in bookmarkstest
        bookmarkstest = list()
        for minute in minutedata:
            tweettime = datetime.utcfromtimestamp(minute.timestamp) + timedelta(seconds=data[0].utcoffset)
            proghour = tweettime.hour - actualstart.hour
            progmin = tweettime.minute - actualstart.minute
            progsec = tweettime.second - actualstart.second
            # Identify where in the programme the tweets occurred - not needed in the new version of /programmes
            playertime = (((proghour * 60) + progmin) * 60) + progsec - 90 # needs between 60 and 120 secs removing to allow for tweeting time - using 90 for now
            if playertime > (master.duration - 60):
                playertimemin = (master.duration/60) - 1
                playertimesec = playertime%60
            elif playertime > 0:
                playertimemin = playertime/60
                playertimesec = playertime%60
            else:
                playertimemin = 0
                playertimesec = 0
            # Identify where bookmarks should occur by comparing the standard deviation to the mean
            if minute.totaltweets > (1.5*data[0].stdevtweets+data[0].meantweets):
                if lastwasbookmark == True:
                    bookmarkcont.append(playertimemin)
                else:
                    if minute.totaltweets > (2.2*data[0].stdevtweets+data[0].meantweets) and minute.totaltweets > 9: # Arbitrary value chosen for now - needs experimentation - was 9
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
            # The below xlist and ylist variables allow for the generation of the data points to be passed to the Google Chart API
            xlist = range(0,master.duration/60)
            ylist = list()
            for min in xlist:
                if tweetmins.has_key(str(min)):
                    ylist.append(tweetmins[str(min)])
                else:
                    ylist.append(0)

            maxy = max(ylist)
            maxx = max(xlist)

            mainwidth = int(1000/(maxx+1)) * (maxx + 1)
            # blockgraph = main gradient based output with iPlayer links
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
                        blockgraph3 += "<a href=\"/programmes-old/" + pid + "/" + str(tweetstamps[str(min)]) + "/\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #000000; opacity: " + str(opacity) + "\"></div></a>"
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
                        blockgraph3 += "<a href=\"/programmes-old/" + pid + "/" + str(tweetstamps[str(min)]) + "/\" target=\"_blank\"><div style=\"width: " + str(width) + "px; height: 20px; cursor: pointer; float: left; background-color: #000000; opacity: " + str(opacity) + "\"></div></a>"
                    else:
                        blockgraph3 += "<div style=\"width: " + str(width) + "px; height: 20px; float: left; background-color: #000000; opacity: " + str(opacity) + "\"></div>"
            blockgraph += "</div>"
            blockgraph2 += "</div>"
            blockgraph3 += "</div>"

            if mainwidth > 1000:
                mainwidth = 1000

            graph = SimpleLineChart(mainwidth,300,y_range=[0,maxy])
            graph.add_data(ylist)

            # Labelling on these graphs is poor (in terms of what numbers are shown where) - Flotr handles this better in the new /programmes
            graph.set_title("Tweets per minute")
            left_axis = ['',int(maxy/4),int(maxy/2),int(3*maxy/4),int(maxy)]
            bottom_axis = [0,int(maxx/8),int(maxx/4),int(3*maxx/8),int(maxx/2),int(5*maxx/8),int(3*maxx/4),int(7*maxx/8),int(maxx)]
            graph.set_axis_labels(Axis.LEFT,left_axis)
            graph.set_axis_labels(Axis.BOTTOM,bottom_axis)
            output += "<br /><img src=\"" + graph.get_url() + "\"><br /><br /><!--[if lte IE 8]><strong>Note:</strong> It looks like you're using Internet Explorer - until a code bug is fixed, you won't be able to see the last minute(s) of programmes in the plot below.<br /><br /><![endif]-->"
            output += blockgraph
            output += blockgraph2
            output += blockgraph3
            if len(bookmarkstest) > 0:
                output += "<br /><b>New Bookmark Testing</b>"
                for entry in bookmarkstest:
                    tweettime = datetime.utcfromtimestamp(entry) + timedelta(seconds=data[0].utcoffset)
                    proghour = tweettime.hour - actualstart.hour
                    progmin = tweettime.minute - actualstart.minute
                    progsec = tweettime.second - actualstart.second
                    playertime = (((proghour * 60) + progmin) * 60) + progsec - 80 # needs between 60 and 120 secs removing to allow for tweeting time - using 90 for now
                    if playertime > (master.duration - 60):
                        playertimemin = (master.duration/60) - 1
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
        if redux == "redux":
            output += "<br /><br />API: <a href=\"/api/" + data[0].pid + "/redux/stats.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + data[0].pid + "/redux/stats.xml\" target=\"_blank\">XML</a>"
        else:
            output += "<br /><br />API: <a href=\"/api/" + data[0].pid + "/stats.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + data[0].pid + "/stats.xml\" target=\"_blank\">XML</a>"
        output += "<br />Tweets: <a href=\"/api/" + data[0].pid + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + data[0].pid + ".xml\" target=\"_blank\">XML</a>"
        # Reveal tweets is temporary - will allow selection and viewing of single minutes once the database has been redesigned.
        output += "<br /><br /><a href=\"/channel-graph/" + data[0].channel + "/" + str(progdate.strftime("%Y/%m/%d")) + "/\">Back to channel page</a> - <a href=\"http://www.bbc.co.uk/programmes/" + data[0].pid + "\" target=\"_blank\">View BBC /programmes page</a>"

    else:
        output += "<br />Database consistency error - This pid has been broadcast more than once and hence is only compatible with the new /programmes views."
        output += "<br /><br /><a href=\"/\">Back to index</a>"

    output += footer
    return HttpResponse(output)

def programmev2(request,pid,timestamp=False,redux=False):
    '''
    Main programme viewing output, accessible via /programmes/pid
    Where a show has been broadcast before, its individual broadcasts can be viewed via /programmes/pid/timestamp
    '''
    output = header

    # 206 here (partial content) means the programme hasn't finished being analysed
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

    # Graph generation JS
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
        data = programmes.objects.filter(pid=pid).order_by('-timestamp').all()
        # Viewing all instances (inc repeats etc) - shows the same as the timestamp case if only one row found
    rowcount = len(data)
    if rowcount == 0:
        output += "<br />Invalid pid supplied or no data has yet been captured for this programme."
        output += "<br /><br /><a href=\"/\">Back to index</a>"
    else:
        if rowcount == 1:
            # If there has only been one broadcast of this programme, we can include show times, otherwise we can only show the duration
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

        # Print statistics and graphs in references divs so they can be refreshed
        output += "<br /><div id=\"statistics\">"
        output += programmev2data(False,"statistics",pid,timestamp,redux,False)
        output += "</div>"
        output += "<br /><div id=\"graphs\">"
        output += programmev2data(False,"graphs",pid,timestamp,redux,False)
        output += "</div>"

        if rowcount > 1:
            # Print links to each individual broadcast if there has been more than one
            output += "<br /><br /><strong>Broadcasts</strong>"
            for row in data:
                output += "<br /><a href=\"/programmes/" + pid + "/" + str(int(row.timestamp))
                if redux == "redux":
                    output += "/redux"
                output += "\">"
                progdatetime = datetime.utcfromtimestamp(row.timestamp)
                progdate = progdatetime + timedelta(seconds=row.utcoffset)
                output += str(progdate.strftime("%d/%m/%Y %H:%M:%S")) + " (" + str(row.channel) + ")"
                output += "</a>"
        output += "<br /><br />"
        # Print API links to general stats and the raw tweets
        if rowcount > 1:
            if redux == "redux":
                output += "API: <a href=\"/api/" + pid + "/redux/stats.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/redux/stats.xml\" target=\"_blank\">XML</a>"
            else:
                output += "API: <a href=\"/api/" + pid + "/stats.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/stats.xml\" target=\"_blank\">XML</a>"
            output += "<br />Tweets: <a href=\"/api/" + pid + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + ".xml\" target=\"_blank\">XML</a><br /><br />"
        else:
            if redux == "redux":
                output += "API: <a href=\"/api/" + pid + "/" + str(int(data[0].timestamp)) + "/redux/stats.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(int(data[0].timestamp)) + "/redux/stats.xml\" target=\"_blank\">XML</a>"
            else:
                output += "API: <a href=\"/api/" + pid + "/" + str(int(data[0].timestamp)) + "/stats.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(int(data[0].timestamp)) + "/stats.xml\" target=\"_blank\">XML</a>"
            output += "<br />Tweets: <a href=\"/api/" + pid + "/" + str(int(data[0].timestamp)) + ".json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(int(data[0].timestamp)) + ".xml\" target=\"_blank\">XML</a><br /><br />"
        # TODO The channel linked to here won't necessarily be the right one
        #output += <a href=\"/channel-graph/" + row.channel + "/" + str(progdate.strftime("%Y/%m/%d")) + "/\">Back to channel page</a> -
        output += "<a href=\"javascript:history.go(-1)\">Back to previous page</a> - "
        output += "<a href=\"http://www.bbc.co.uk/programmes/" + pid + "\" target=\"_blank\">View BBC /programmes page</a>"

    output += footer
    return HttpResponse(output)

def programmev2data(request,element,pid,timestamp=False,redux=False,wrapper=True):
    '''
    Data output for /programmes pages AJAX - accessible via /data/element/pid etc
    '''
    output = "" # Initialise output buffer
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later
    if timestamp:
        data = programmes.objects.filter(pid=pid,timestamp=timestamp).all()
    else:
        data = programmes.objects.filter(pid=pid).all()
    elemitem = "all"
    # Splitter used by /channel-graph to get the first graph rather than the block plot
    if "-" in element and "graphs" in element:
        splitter = element.split("-")
        element = splitter[0]
        elemitem = splitter[1]
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
                    minutegroups[group] += int(line.totaltweets)
                    totaltweets += int(line.totaltweets)

        minuteitems = minutegroups.items()
        minuteitems.sort()

        if len(data) == 1:
            meantweets = data[0].meantweets
            mediantweets = data[0].mediantweets
            modetweets = data[0].modetweets
            stdevtweets = data[0].stdevtweets
        else:
            meantweets = totaltweets / float(master.duration / 60)
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
        #TODO should really create an automatic saved cache of graphs that won't change again - avoids the need to javascript too
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

            if elemitem == "channel":
                containername = "container-" + progchannel + "-" + str(progtimestamp)
            else:
                containername = "container"

            output += "<div style=\"width: 990px; text-align: center; margin-left: 20px\"><strong>Tweets Per Minute vs. Programme Position</strong></div><div id=\"" + containername + "\" style=\"width: 990px; height: 300px\"></div>"

            output += "<script type=\"text/javascript\">var data = " + jsminlist + "; var f =  Flotr.draw($('" + containername + "'),[data],{label: 'test label', lines: {lineWidth: 1}});</script>"

            if elemitem != "channel":
            #if 1:
                # Not a channel page so print the slice plots too
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

                    # Work out where the bookmarks should be
                    #TODO: Bookmarks for aggregated programme pages haven't been done yet
                    # Need adding to the API when done
                    if minute[1] > (2.2*stdevtweets+meantweets) and minute[1] > 9: # Arbitrary value chosen for now - needs experimentation - was 9
                        
                        wfdata = None
                        for row in data:
                            wfdatatemp = wordanalysis.objects.filter(timestamp=row.timestamp-row.timediff+(minute[0]*60),pid=pid,is_keyword=0,is_common=0).order_by('-count').all()
                            if wfdata is None:
                                wfdata = wfdatatemp
                            else:
                                # TODO: Modify this to merge the data properly
                                wfdata = wfdata | wfdatatemp

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
                            minstamp = progtimestamp-progtimediff
                            minutediff = minute[0]*60
                            topkeyword = keyword
                            while topkeyword == keyword:
                                currentstamp -= 60
                                minutediff -= 60
                                if currentstamp < minstamp:
                                    break
                                try:
                                    dataset = None
                                    for row in data:
                                        datasettemp = wordanalysis.objects.filter(timestamp=row.timestamp-row.timediff+minutediff,pid=pid,is_keyword=0,is_common=0).order_by('-count').all()
                                        if dataset is None:
                                            dataset = datasettemp
                                        else:
                                            # TODO: Modify this to merge the data properly
                                            dataset = dataset | datasettemp
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
                            rawtweets = None
                            for row in data:
                                rawtweetstemp = rawdata.objects.filter(pid=pid,timestamp__gte=row.timestamp-row.timediff+minutediff,timestamp__lt=row.timestamp-row.timediff+minutediff+60).order_by('timestamp').all()
                                if rawtweets is None:
                                    rawtweets = rawtweetstemp
                                else:
                                    rawtweets = rawtweets | rawtweetstemp
                            for tweet in rawtweets:
                                tweettext = string.lower(tweet.text)
                                for items in """!"#$%&(),:;?@~[]'`{|}""":
                                    tweettext = string.replace(tweettext,items,"")
                                try:
                                    if str(keyword).lower() in tweettext:
                                        bookmarkstart = int(tweet.programme_position)
                                        tweetset = True
                                        break
                                except UnicodeEncodeError:
                                    break

                            if not tweetset:
                                rawtweets = None
                                for row in data:
                                    rawtweetstemp = rawdata.objects.filter(pid=pid,timestamp__gte=row.timestamp-row.timediff+minutediff+60,timestamp__lt=row.timestamp-row.timediff+minutediff+120).order_by('timestamp').all()
                                    if rawtweets is None:
                                        rawtweets = rawtweetstemp
                                    else:
                                        rawtweets = rawtweets | rawtweetstemp
                                for tweet in rawtweets:
                                    tweettext = string.lower(tweet.text)
                                    for items in """!"#$%&(),:;?@~[]'`{|}""":
                                        tweettext = string.replace(tweettext,items,"")
                                    try:
                                        if str(keyword).lower() in tweettext:
                                            bookmarkstart = int(tweet.programme_position)
                                            break
                                    except UnicodeEncodeError:
                                        break

                            # Now look at each next minute until it's no longer the top keyword
                            currentstamp = progtimestamp-progtimediff+(minute[0]*60)
                            maxstamp = progtimestamp-progtimediff+master.duration
                            minutediff = minute[0]*60
                            topkeyword = keyword
                            while topkeyword == keyword:
                                currentstamp += 60
                                minutediff += 60
                                if currentstamp > maxstamp:
                                    break
                                try:
                                    dataset = None
                                    for row in data:
                                        # TODO: Modify this to merge the data properly
                                        datasettemp = wordanalysis.objects.filter(timestamp=row.timestamp-row.timediff+minutediff,pid=pid,is_keyword=0,is_common=0).order_by('-count').all()
                                        if dataset is None:
                                            dataset = datasettemp
                                        else:
                                            dataset = dataset | datasettemp
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
                            rawtweets = None
                            for row in data:
                                rawtweetstemp = rawdata.objects.filter(pid=pid,timestamp__gte=row.timestamp-row.timediff+minutediff,timestamp__lt=row.timestamp-row.timediff+minutediff+60).order_by('timestamp').all()
                                if rawtweets is None:
                                    rawtweets = rawtweetstemp
                                else:
                                    rawtweets = rawtweets | rawtweetstemp
                            for tweet in rawtweets:
                                tweettext = string.lower(tweet.text)
                                for items in """!"#$%&(),:;?@~[]'`{|}""":
                                    tweettext = string.replace(tweettext,items,"")
                                try:
                                    if str(keyword).lower() in tweettext:
                                        bookmarkend = int(tweet.programme_position)
                                        tweetset = True
                                        break
                                except UnicodeEncodeError:
                                    break

                            if not tweetset:
                                rawtweets = None
                                for row in data:
                                    rawtweetstemp = rawdata.objects.filter(pid=pid,timestamp__gte=row.timestamp-row.timediff+minutediff+60,timestamp__lt=row.timestamp-row.timediff+minutediff+120).order_by('timestamp').all()
                                    if rawtweets is None:
                                        rawtweets = rawtweetstemp
                                    else:
                                        rawtweets = rawtweets | rawtweetstemp
                                for tweet in rawtweets:
                                    tweettext = string.lower(tweet.text)
                                    for items in """!"#$%&(),:;?@~[]'`{|}""":
                                        tweettext = string.replace(tweettext,items,"")
                                    try:
                                        if str(keyword).lower() in tweettext:
                                            bookmarkend = int(tweet.programme_position)
                                            break
                                    except UnicodeEncodeError:
                                        break

                            if (bookmarkstart and bookmarkend) and (bookmarkstart != bookmarkend):
                                if bookmarkstart < 0:
                                    bookmarkstart = 0
                                if bookmarkend > master.duration:
                                    bookmarkend = master.duration
                                # Only bookmark worthy if it creates 'buzz' for 60 seconds or more
                                if (len(bookmarks) > 0):
                                    # Check if the bookmarks should be merged, allowing a slight overlap time of 20 seconds in case of a sudden lack of tweets
                                    checkkeyword = bookmarks[len(bookmarks)-1][3]
                                    originalkeyword = keyword
                                    # TODO Fix this so that two bookmarks aren't identified instead of one if 'Ha' and 'ha' are identified as the keywords respectively
                                    # Need to take account of the fact there could be some unicode here
                                    #try:
                                    #    checkkeyword = string.lower(checkkeyword)
                                    #    originalkeyword = string.lower(originalkeyword)
                                    #except UnicodeEncodeError:
                                    #    pass
                                    if bookmarks[len(bookmarks)-1][1] >= (bookmarkstart - 20) and checkkeyword == originalkeyword:
                                        bookmarks[len(bookmarks)-1][1] = bookmarkend
                                        continue
                                if (bookmarkend - bookmarkstart) > 60:
                                    #output += "<br />" + str(bookmarkstart) + " " + str(bookmarkend) + " " + str(bookmarkstart-80) + " " + keyword
                                    bookmarks.append([bookmarkstart,bookmarkend,bookmarkstart-80,keyword])

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
                    elif bmcurrent > 0 and bmcurrent < bmtotal:
                        if bookmarks[bmcurrent-1][1] < bookmark[0]:
                            bookmarkplot += "<div style=\"float: left; background-color: #FFFFFF; height: 40px; width: " + str(int((bookmark[0]-bookmarks[bmcurrent-1][1])*bmsecondwidth)) + "px\"></div>"
                    bookmarkpos = bookmark[2] - progstart
                    # Need to check having taken some time off the bookmark to allow for tweeting that it doesn't underrun
                    if bookmarkpos < 0:
                        bookmarkpos = 0
                    if redux == "redux":
                        # Any channel will work fine for redux but iPlayer needs the most recent
                        bookmarkplot += "<a href=\"http://g.bbcredux.com/programme/" + reduxchannel + "/" + progdatestring + "/" + progtimestring + "?start=" + str(int(bookmarkpos)) + "\" title=\"Caused by: " + bookmark[3] + "\" target=\"_blank\">"
                    else:
                        bookmarkmins = int(bookmarkpos / 60)
                        bookmarksecs = int(bookmarkpos % 60)
                        bookmarkplot += "<a href=\"http://bbc.co.uk/i/" + pid + "/?t=" + str(bookmarkmins) + "m" + str(bookmarksecs) + "s\" title=\"Caused by: " + bookmark[3] + "\" target=\"_blank\">"
                    # Ensure that if the next bookmark overlaps, it is visible
                    if (bmcurrent + 2) < bmtotal:
                        if bookmark[1] > bookmarks[bmcurrent+1][0]:
                            bookmark[1] = bookmarks[bmcurrent+1][0]
                    bookmarkplot += "<div class=\"bmgradient\" style=\"background-color: #FF6633; cursor: pointer; float: left; opacity: 0.6; height: 40px; width: " + str(int((bookmark[1]-bookmark[0])*bmsecondwidth)) + "px; filter:alpha(opacity=40)\"></div></a>"
                    if bmcurrent == (bmtotal - 1) and bookmark[1] != progend:
                        bookmarkplot += "<div style=\"float: left; background-color: #FFFFFF; height: 40px; width: " + str(int((progend - bookmark[1])*bmsecondwidth)) + "px\"></div>"
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
    '''
    Deprecated raw tweet output available via /programmes-old/pid/timestamp
    '''
    output = header
    progdata = programmes.objects.filter(pid=pid).all()
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later
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
        output += "<strong>" + master.title + "</strong><br />"
        output += "Raw tweet output between " + str(starttime.strftime("%H:%M:%S")) + " and " + str(endtime.strftime("%H:%M:%S")) + "<br />"
        rawtweets = rawdata.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=endstamp).order_by('timestamp').all()
        output += "<div id=\"rawtweets\" style=\"font-size: 9pt\">"
        for tweet in rawtweets:
            output += "<br /><strong>" + str(datetime.utcfromtimestamp(tweet.timestamp + progdata[0].utcoffset)) + ":</strong> " + "@" + tweet.user + ": " + tweet.text
        output += "</div><br /><br />"
        output += "Tweets: <a href=\"/api/" + pid + "/" + str(timestamp) + "/tweets.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(timestamp) + "/tweets.xml\" target=\"_blank\">XML</a><br />"
        newanalysis = wordanalysis.objects.filter(pid=pid,timestamp__gte=timestamp,timestamp__lt=endstamp,is_common=0).order_by('-count').all()
        for entry in newanalysis:
            output += "<br />" + entry.word + ": " + str(entry.count) + " " + str(entry.is_keyword) + " " + str(entry.is_entity) + " " + str(entry.is_common)
    output += footer
    return HttpResponse(output)

def rawtweetsv2(request,pid,timestamp,aggregated=False):
    '''
    New raw tweet output accessible via /raw/pid/timestamp, or /raw/pid/progpos/aggregated for cases of multiple showings
    '''
    output = header
    try:
        master = programmes_unique.objects.get(pid=pid)
    except ObjectDoesNotExist, e:
        pass # This is handled later
    if aggregated:
        progdata = programmes.objects.filter(pid=pid).all()
    else:
        progdata = programmes.objects.filter(pid=pid,timestamp__lte=timestamp).order_by('-timestamp').all()
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
        # Tag cloud JS
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
        # Handling Ajax request for tag cloud refresh when new parameters selected from checkboxes
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
            progpos = timestamp*60
            endstamp = progpos + 60
            output += "<br /><strong>" + master.title + "</strong><br /><br />"
            # Allow skipping from this minute to the next and previous
            if timestamp > 0:
                # Print previous button
                output += "<a href=\"/raw/" + pid + "/" + str(timestamp - 1) + "/aggregated\"><- Previous</a>"
            else:
                output += "<- Previous"
            output += " - "
            if timestamp < ((master.duration / 60)-1):
                # Print 'next' button
                output += "<a href=\"/raw/" + pid + "/" + str(timestamp + 1) + "/aggregated\">Next -></a>"
            else:
                output += "Next ->"
            output += "<br /><br />"
            # In this case the 'timestamp' is actually the programme position
            rawtweetdict = dict()
            rawtweets = rawdata.objects.filter(pid=pid,programme_position__gte=progpos,programme_position__lt=endstamp).order_by('timestamp').all()
            for tweet in rawtweets:
                if rawtweetdict.has_key(int(tweet.programme_position)):
                    rawtweetdict[int(tweet.programme_position)].append("<br /><strong>" + str(timestamp) + "m" + str(int(tweet.programme_position)-timestamp*60) + "s:</strong> " + "@" + tweet.user + ": " + tweet.text)
                else:
                    rawtweetdict[int(tweet.programme_position)] = ["<br /><strong>" + str(timestamp) + "m" + str(int(tweet.programme_position)-timestamp*60) + "s:</strong> " + "@" + tweet.user + ": " + tweet.text]
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
            output += "</div><br />"
            output += "Tweets: <a href=\"/api/" + pid + "/" + str(timestamp) + "/aggregated/tweets.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(timestamp) + "/aggregated/tweets.xml\" target=\"_blank\">XML</a><br />"
        else:
            endstamp = timestamp + 60
            channel = progdata[0].channel
            output += "<br /><a href=\"http://www.bbc.co.uk/" + channel + "\" target=\"_blank\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a><br /><br />"
            progdate = datetime.utcfromtimestamp(progdata[0].timestamp) + timedelta(seconds=progdata[0].utcoffset)
            starttime = datetime.utcfromtimestamp(timestamp) + timedelta(seconds=progdata[0].utcoffset)
            endtime = datetime.utcfromtimestamp(endstamp) + timedelta(seconds=progdata[0].utcoffset)
            output += str(progdate.strftime("%d/%m/%Y")) + "<br />"
            output += "<strong>" + master.title + "</strong><br /><br />"
            if timestamp > (progdata[0].timestamp - progdata[0].timediff):
                # Print previous button
                output += "<a href=\"/raw/" + pid + "/" + str(timestamp - 60) + "\"><- Previous</a>"
            else:
                output += "<- Previous"
            output += " - "
            if (progdata[0].timestamp - progdata[0].timediff + master.duration) > endstamp:
                # Print 'next' button
                output += "<a href=\"/raw/" + pid + "/" + str(timestamp + 60) + "\">Next -></a>"
            else:
                output += "Next ->"
            output += "<br /><br />"
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
            output += "Tweets: <a href=\"/api/" + pid + "/" + str(timestamp) + "/tweets.json\" target=\"_blank\">JSON</a> - <a href=\"/api/" + pid + "/" + str(timestamp) + "/tweets.xml\" target=\"_blank\">XML</a><br />"
    output += footer
    return HttpResponse(output)

def tagcloud(request,pid,timestamp,params=False,wrapper=True):
    '''
    Tag cloud generation - accessible via /data/tagcloud/pid/progpos/aggregated or /data/tagcloud/pid/timestamp
    '''
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
        starttag = "<ul id=\"tagcloud\" class=\"xmpl\" style=\"width: 700px; height: auto; position: static; list-style: none outside none; margin: 0px; padding: 0px\">"
        endtag = "</ul>"
        output += starttag
        if aggregated == "aggregated":
            progpos = timestamp*60
            # In this case the 'timestamp' is actually the programme position
            analysedwords = dict()
            for row in progdata:
                searchstamp = row.timestamp-row.timediff+progpos
                # Identify which elements to show in the tag cloud based on the parameters specified
                # Overcomplicated number of queries - could be simplified I expect TODO
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
                # Print an <li> for each tag, which will be converted by JS into a cloud
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
                output += "<li style=\"cursor: pointer\" title=\"" + entry.word + "\" value=\"" + str(entry.count) + "\"><a title=\"" + str(entry.count) + "\">" + entry.word + " </a></li>"
                currenttag += 1
        if output == starttag:
            output += "<div style=\"font-size: 9pt\">No tweets recorded / this data uses an old timestamp format that doesn't support generation of tag clouds</div>"
        output += endtag
    if wrapper:
        return HttpResponse(output)
    else:
        return output

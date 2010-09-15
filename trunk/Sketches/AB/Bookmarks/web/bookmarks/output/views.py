# Create your views here.
from django.http import HttpResponse
from bookmarks.output.models import programmes,analyseddata
from datetime import date

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament"]
            
radiochannels = ["radio1","1xtra","radio2","radio3","radio4","radio5","sportsextra","6music","radio7","asiannetwork","worldservice"]

header = '<html><head><title>Social Bookmarks</title><script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script></head><body><h1>Social Bookmarks</h1>'

footer = '</body></html>'

def index(request):
    currentdate = date.today()
    currentyear = str(currentdate.year)
    currentmonth = str(currentdate.month)
    currentday = str(currentdate.day)
    if len(currentmonth) < 2:
        currentmonth = "0" + currentmonth
    if len(currentday) < 2:
        currentday = "0" + currentday
    output = header

    output += "<br />Notice the severe lack of CSS<br />"

    output += "<h2>TV</h2>"
    for channel in tvchannels:
        output += "<a href=\"/channels/" + channel + "/" + currentyear + "/" + currentmonth + "/" + currentday + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a> "
    output += "<br /><h2>Radio</h2>"
    for channel in radiochannels:
        output += "<a href=\"/channels/" + channel + "/" + currentyear + "/" + currentmonth + "/" + currentday + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a> "
        
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
        
        output += "<img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"><br />"
        if len(data) < 1:
            output += "<br />Please note: No data has yet been captured for this channel."
        else:
            output += '<br /><br /><div id="inlineDatepicker"></div>'
            if len(str(day)) == 2 and len(str(month)) == 2 and len(str(year)) == 4:
                datecomp = year + "-" + month + "-" + day
                data = programmes.objects.filter(channel__exact=channel,expectedstart__contains=datecomp).order_by('expectedstart').all()
                for programme in data:
                    output += "<br />" + programme.expectedstart + " <a href=\"/programmes/" + programme.pid + "\">" + programme.title + "</a>"
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
        minutedata = analyseddata.objects.filter(pid=pid)
        output += data[0].title + "<br />"
        output += data[0].expectedstart + "<br />"
        output += str(data[0].duration)
        output += "<br /><br /><a href=\"/\">Back to channel page</a>" #TODO - get data from database
    else:
        output += "Database consistency error - somehow a primary key appears twice..."
        output += "<br /><br /><a href=\"/\">Back to index</a>"

    output += footer
    return HttpResponse(output)
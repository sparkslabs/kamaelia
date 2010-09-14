# Create your views here.
from django.http import HttpResponse

tvchannels = ["bbcone","bbctwo","bbcthree","bbcfour","cbbc","cbeebies","bbcnews","bbcparliament","bbchd"]
            
radiochannels = ["radio1","1xtra","radio2","radio3","radio4","radio5","sportsextra","6music","radio7","asiannetwork","worldservice"]

def index(request):
    output = '' # TODO Fix serious lack of formatting here

    output += "<h1>Social Bookmarks</h1>"
    output += "<h2>TV</h2>"
    for channel in tvchannels:
        output += "<a href=\"/channels/" + channel + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a> "
    output += "<br /><h2>Radio</h2>"
    for channel in radiochannels:
        output += "<a href=\"/channels/" + channel + "/\"><img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"></a> "
    return HttpResponse(output)

def channel(request,channel,year=0,month=0,day=0):
    if day != 0 and month != 0 and year != 0:
        output = "<img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"><br />"
        output += "<p>Hello, world. You're at the bookmarks index for channel " + channel + " on " + day + "/" + month + "/" + year + ".</p>"
        return HttpResponse(output)
    elif month != 0 and year != 0:
        output = "<img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"><br />"
        output += "Hello, world. You're at the bookmarks index for channel " + channel + " in " + month + "/" + year + "."
        return HttpResponse(output)
    elif year != 0:
        output = "<img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"><br />"
        output += "Hello, world. You're at the bookmarks index for channel " + channel + " in " + year + "."
        return HttpResponse(output)
    else:
        output = "<img src=\"/media/channels/" + channel + ".gif\" style=\"border: none\"><br />"
        output += "Hello, world. You're at the bookmarks index for channel " + channel + "."
        return HttpResponse(output)

def programme(request,pid):
    return HttpResponse("Hello, world. You're at the bookmarks index for pid %s." % pid)
from piston.handler import BaseHandler
from bookmarks.output.models import programmes, keywords

class ProgrammesHandler(BaseHandler):
    allowed_methods = ('GET',)
    #fields = ('pid', 'channel', 'title', 'expectedstart', 'timediff', 'duration', 'imported', 'analysed', 'totaltweets', 'meantweets', 'mediantweets', 'modetweets', 'stdevtweets')
    #model = programmes

    def read(self, request, pid):
        retdata = dict()
        data = programmes.objects.filter(pid=pid)
        if len(data) == 1:
            retdata['status'] = "OK"
            retdata['pid'] = data[0].pid
            retdata['title'] = data[0].title
            retdata['expectedstart'] = data[0].expectedstart
            retdata['timediff'] = data[0].timediff
            retdata['duration'] = data[0].duration
            retdata['imported'] = data[0].imported
            retdata['analysed'] = data[0].analysed
            retdata['totaltweets'] = data[0].totaltweets
            retdata['meantweets'] = data[0].meantweets
            retdata['mediantweets'] = data[0].mediantweets
            retdata['modetweets'] = data[0].modetweets
            retdata['stdevtweets'] = data[0].stdevtweets
            kwdata = keywords.objects.filter(pid=pid).all()
            retdata['keywords'] = list()
            for row in kwdata:
                retdata['keywords'].append({'keyword' : row.keyword, 'type' : row.type})
        else:
            retdata['status'] = "ERROR"
        return retdata
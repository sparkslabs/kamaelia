from django.conf.urls.defaults import *
from piston.resource import Resource
from bookmarks.api.handlers import ProgrammesHandler, SummaryHandler, TimestampHandler, TweetHandler

programmes_handler = Resource(ProgrammesHandler)
summary_handler = Resource(SummaryHandler)
timestamp_handler = Resource(TimestampHandler)
tweet_handler = Resource(TweetHandler)

urlpatterns = patterns('',
   # Summary pages
   url(r'^summary.json', summary_handler, { 'emitter_format': 'json' }),
   url(r'^summary.xml', summary_handler, { 'emitter_format': 'xml' }),
   # The below handle raw tweet output for minute periods within programmes
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<aggregated>\D+)/tweets.json', timestamp_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<aggregated>\D+)/tweets.xml', timestamp_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/tweets.json', timestamp_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/tweets.xml', timestamp_handler, { 'emitter_format': 'xml' }),
   # The below handle programme stats either aggregated or for a single programme
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<redux>\D+)/stats.json', programmes_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<redux>\D+)/stats.xml', programmes_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+)/(?P<redux>\D+)/stats.json', programmes_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/(?P<redux>\D+)/stats.xml', programmes_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/stats.json', programmes_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+)/stats.xml', programmes_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+)/stats.json', programmes_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/stats.xml', programmes_handler, { 'emitter_format': 'xml' }),
   # The below handle raw tweet output for single programmes or aggregated one (whole programme duration)
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+).json', tweet_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+).xml', tweet_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+).json', tweet_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+).xml', tweet_handler, { 'emitter_format': 'xml' }),
)

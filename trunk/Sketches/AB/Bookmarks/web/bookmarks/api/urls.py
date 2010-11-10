from django.conf.urls.defaults import *
from piston.resource import Resource
from bookmarks.api.handlers import ProgrammesHandler, SummaryHandler, TimestampHandler, TweetHandler

programmes_handler = Resource(ProgrammesHandler)
summary_handler = Resource(SummaryHandler)
timestamp_handler = Resource(TimestampHandler)
tweet_handler = Resource(TweetHandler)

urlpatterns = patterns('',
   url(r'^summary.json', summary_handler, { 'emitter_format': 'json' }),
   url(r'^summary.xml', summary_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+).json', timestamp_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/(?P<timestamp>\d+).xml', timestamp_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+)/tweets.json', tweet_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+)/tweets.xml', tweet_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+).json', programmes_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+).xml', programmes_handler, { 'emitter_format': 'xml' }),
)

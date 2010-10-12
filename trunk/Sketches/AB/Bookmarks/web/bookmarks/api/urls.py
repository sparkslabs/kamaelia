from django.conf.urls.defaults import *
from piston.resource import Resource
from bookmarks.api.handlers import ProgrammesHandler, SummaryHandler

programmes_handler = Resource(ProgrammesHandler)
summary_handler = Resource(SummaryHandler)

urlpatterns = patterns('',
   url(r'^summary.json', summary_handler, { 'emitter_format': 'json' }),
   url(r'^summary.xml', summary_handler, { 'emitter_format': 'xml' }),
   url(r'^(?P<pid>\w+).json', programmes_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+).xml', programmes_handler, { 'emitter_format': 'xml' }),
)

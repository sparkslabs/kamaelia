from django.conf.urls.defaults import *
from piston.resource import Resource
from bookmarks.api.handlers import ProgrammesHandler

programmes_handler = Resource(ProgrammesHandler)

urlpatterns = patterns('',
   url(r'^(?P<pid>\w+).json', programmes_handler, { 'emitter_format': 'json' }),
   url(r'^(?P<pid>\w+).xml', programmes_handler, { 'emitter_format': 'xml' }),
)

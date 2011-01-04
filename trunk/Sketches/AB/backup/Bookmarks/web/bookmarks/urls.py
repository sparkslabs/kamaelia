from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^bookmarks/', include('bookmarks.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),

    (r'^programmes-old/(?P<pid>\w+)/(?P<timestamp>\d+)/$', 'bookmarks.output.views.rawtweets'),
    (r'^programmes-old/(?P<pid>\w+)/(?P<redux>\D+)$', 'bookmarks.output.views.programme'),
    (r'^programmes-old/(?P<pid>\w+)/$', 'bookmarks.output.views.programme'),
    (r'^raw/(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<aggregated>\D+)$', 'bookmarks.output.views.rawtweetsv2'),
    (r'^raw/(?P<pid>\w+)/(?P<timestamp>\d+)$', 'bookmarks.output.views.rawtweetsv2'),
    (r'^programmes/(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<redux>\D+)$', 'bookmarks.output.views.programmev2'),
    (r'^programmes/(?P<pid>\w+)/(?P<timestamp>\d+)$', 'bookmarks.output.views.programmev2'),
    (r'^programmes/(?P<pid>\w+)/(?P<redux>\D+)$', 'bookmarks.output.views.programmev2'),
    (r'^programmes/(?P<pid>\w+)/$', 'bookmarks.output.views.programmev2'),
    (r'^data/index/(?P<channelgroup>\D+)$', 'bookmarks.output.views.indexdata'),
    (r'^data/tagcloud/(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<params>\D+)$', 'bookmarks.output.views.tagcloud'),
    (r'^data/tagcloud/(?P<pid>\w+)/(?P<timestamp>\d+)$', 'bookmarks.output.views.tagcloud'),
    (r'^data/(?P<element>\D+)/(?P<pid>\w+)/(?P<timestamp>\d+)/(?P<redux>\D+)$', 'bookmarks.output.views.programmev2data'),
    (r'^data/(?P<element>\D+)/(?P<pid>\w+)/(?P<timestamp>\d+)$', 'bookmarks.output.views.programmev2data'),
    (r'^data/(?P<element>\D+)/(?P<pid>\w+)/(?P<redux>\D+)$', 'bookmarks.output.views.programmev2data'),
    (r'^data/(?P<element>\D+)/(?P<pid>\w+)/$', 'bookmarks.output.views.programmev2data'),
    (r'^channels/(?P<channel>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'bookmarks.output.views.channel'),
    (r'^channels/(?P<channel>\w+)/(?P<year>\d+)/(?P<month>\d+)/$', 'bookmarks.output.views.channel'),
    (r'^channels/(?P<channel>\w+)/(?P<year>\d+)/$', 'bookmarks.output.views.channel'),
    (r'^channels/(?P<channel>\w+)/$', 'bookmarks.output.views.channel'),
    (r'^channel-graph/(?P<channel>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'bookmarks.output.views.channelgraph'),
    (r'^channel-graph/(?P<channel>\w+)/(?P<year>\d+)/(?P<month>\d+)/$', 'bookmarks.output.views.channelgraph'),
    (r'^channel-graph/(?P<channel>\w+)/(?P<year>\d+)/$', 'bookmarks.output.views.channelgraph'),
    (r'^channel-graph/(?P<channel>\w+)/$', 'bookmarks.output.views.channelgraph'),
    (r'^api/', include('bookmarks.api.urls')),
    (r'^$', 'bookmarks.output.views.index'),
)

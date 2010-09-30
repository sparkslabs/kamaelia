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

    (r'^programmes/(?P<pid>\w+)/$', 'bookmarks.output.views.programme'),
    (r'^channels/(?P<channel>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'bookmarks.output.views.channel'),
    (r'^channels/(?P<channel>\w+)/(?P<year>\d+)/(?P<month>\d+)/$', 'bookmarks.output.views.channel'),
    (r'^channels/(?P<channel>\w+)/(?P<year>\d+)/$', 'bookmarks.output.views.channel'),
    (r'^channels/(?P<channel>\w+)/$', 'bookmarks.output.views.channel'),
    (r'^api/', include('bookmarks.api.urls')),
    (r'^$', 'bookmarks.output.views.index'),
)

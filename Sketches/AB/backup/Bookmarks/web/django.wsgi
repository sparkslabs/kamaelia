import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'bookmarks.settings'

sys.path.append('/home/andrewbo/kamaelia/trunk/Sketches/AB/Bookmarks/web')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

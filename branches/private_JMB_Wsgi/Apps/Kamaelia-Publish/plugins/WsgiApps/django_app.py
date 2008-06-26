import os, sys
from static import static_app

import django.core.handlers.wsgi

_paths_set = set([])

def application(environ = {}, start_response = None):
    if not environ['kp.project_path'] in _paths_set:
        _paths_set.add(environ['kp.project_path'])
        sys.path.append(environ['kp.project_path'])
        
    
    if environ['PATH_INFO'].startswith('/media'):
        return static_app(environ, start_response)
        
    #django doesn't handle PATH_INFO or SCRIPT_NAME variables properly in the current version
    if environ.get('kp.django_path_handling', False):
        environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        
    from pprint import pprint
    pprint(environ)
    
    os.environ['DJANGO_SETTINGS_MODULE'] = environ['kp.django_settings_module']
    _application = django.core.handlers.wsgi.WSGIHandler()
    return _application(environ, start_response)

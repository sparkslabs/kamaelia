import os, sys

import django.core.handlers.wsgi

_paths_set = set([])

def application(environ, start_response):
    if not environ['kp.project_path'] in _paths_set:
        _paths_set.add(environ['kp.project_path'])
        sys.path.append(environ['kp.project_path'])
        
    _application = django.core.handlers.wsgi.WSGIHandler()
    return _application(environ, start_response)

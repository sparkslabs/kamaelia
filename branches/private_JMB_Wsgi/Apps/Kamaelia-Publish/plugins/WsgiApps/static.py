from support.la_static import Cling
import os

def static_app(environ, start_response):
    environ['kp.static_path'] = os.path.expanduser(environ['kp.static_path'])
    return Cling(environ['kp.static_path'], index_file=environ['kp.index_file']) (environ, start_response)

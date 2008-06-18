from support.la_static import Cling
import pdb

def static_app(environ, start_response):
    return Cling(environ['kp.static_path'], index_file=environ['kp.index_file']) (environ, start_response)

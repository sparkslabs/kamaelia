from paste.deploy import loadapp
import os
os.environ['PYTHON_EGG_CACHE'] = '~/kp/.eggs'

__app_objs__ = {}

def application(environ, start_response):
    if __app_objs__.get(environ['kp.paste_source']):
        app = __app_objs__[environ['kp.paste_source']]
    else:
        app = loadapp(environ['kp.paste_source'])
        
    return app(environ, start_response)

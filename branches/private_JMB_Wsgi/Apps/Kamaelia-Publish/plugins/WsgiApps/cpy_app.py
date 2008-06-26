import cherrypy

def application(environ, start_response):
    mod = importModule(environ['kp.cpy_import_path'])
    root = getattr(mod, environ['kp.cpy_root_attribute'])
    
    from pprint import pprint
    pprint(environ)
    
    return cherrypy.tree.mount(root(), environ['kp.cpy_http_path'])(environ, start_response)

def importModule(name):
    """
    Just a copy/paste of the example my_import function from here:
    http://docs.python.org/lib/built-in-funcs.html
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

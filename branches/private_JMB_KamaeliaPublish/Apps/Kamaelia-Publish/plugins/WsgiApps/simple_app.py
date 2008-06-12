def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type','text/html'),('Pragma','no-cache')]
    write = start_response(status, response_headers)
    writable = environ['wsgi.errors']
    writable.write('Writing to log!\n')

    yield '<P> My Own Hello World!\n'
    write('<p>Hello from the write callable!</p>')
    for i in sorted(environ.keys()):
        yield "<li>%s: %s\n" % (i, environ[i])
    yield "<li> wsgi.input:<br/><br/><kbd>"
    for line in environ['wsgi.input'].readlines():
        yield "%s<br/>" % (line)
    yield "</kbd>"
    writable = environ['wsgi.errors']
    writable.writelines(['Writing to log!'])
    writable.flush()
    yield 'done!'

from Kamaelia.Protocol.HTTP import ErrorPages
from Kamaelia.Protocol.HTTP.HTTPServer import MapStatusCodeToText

def application(environ, start_response):
    """
    This is just a plain old error page serving application.
    """
    error = 404

    status = MapStatusCodeToText[str(error)]
    response_headers = [('Content-type', 'text/html')]

    start_response(status, response_headers)

    ErrorPage = ErrorPages.getErrorPage(error)['data']
    yield ErrorPage

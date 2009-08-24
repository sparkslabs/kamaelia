from Kamaelia.Support.Protocol.HTTP import PopURI, PopWsgiURI, PopKamaeliaURI
from pprint import pformat, pprint

print """
Popping URIs allows you to move "down" a level in
a server's URI setup given a request dictionary.
These functions also allow you to specify what keys
to use in that request dictionary.

For example, assume that we have a WSGI environment
dictionary and we want to move down a level in the
URI path, we coud do this:

"""

request = {'SCRIPT_NAME' : '/a', 'PATH_INFO' : '/path/to/page'}

print '    request = %s\n    PopWsgiURI(request)' % pformat(request)
PopWsgiURI(request)
print '    print request'

print '\nThis gives these results:'
print '    %s' % pformat(request)

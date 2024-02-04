---
pagename: Developers/Projects/KamaeliaPublish/RequestReference
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
HTTP request dictionary reference 
=================================

This is a reference to the various fields that the HTTPServer will
include in the request dictionary.  In considering these items, I\'ll
use the following example request URI:

  http://www.foo.com:8080/index.html?foo=bar\

-   bad - This is used internally by the HTTPParser to know if there is
    a problem with the HTTP request.  You probably shouldn\'t worry
    about this variable.\
-   body - Ignore this.  The body will be forwarded to the resource
    handler by the HTTPRequestHandler component.
-   headers - This is a dictionary containing all of the HTTP headers.\
-   localip - The IP address for the computer the server is running on.\
-   localport - The port the HTTP request came in on.
-   method - GET, POST, PUT, etc.\
-   peer - The IP address of the requestor.\
-   peerport - The port the requestor sent the request to us through.\
-   protocol - This is always HTTP.
-   raw-uri - the unprocessed URI. The above example URI would translate
    into /index.html?foo=bar\
-   uri-prefix-trigger - This is roughly equivalent to the CGI
    environment variable \'SCRIPT\_NAME\'.  This lets the handler know
    its virtual \"location\" within the server.  It represents the
    portion of the URI that is consumed getting to the point it is at. 
    The value of this variable will vary depending on how the URL
    routing is set up, but in this example, it will probably be \'/\'
    since it appears we are looking at the root of the URI.\
-   uri-protocol - This will be the protocol as specified in the URI. 
    Will be empty if this data is not available.\
-   uri-server - This is the server\'s address.  Using the example URI,
    this variable will be \'www.foo.com:8080\'\
-   uri-suffix - This is roughly equivalent to the CGI environment
    variable \'PATH\_INFO\'.  This tells the handler the virtual
    \"location\" of its target.  It basically represents the portion of
    the URI that has yet to be consumed.  Again, this is dependent on
    the server\'s URL routing, but in the example above, the uri-suffix
    would probably be \'index.html?foo=bar\'.\
-   version - The version of HTTP the request was sent as.  This is
    dependent upon the browser the requestor is using, but will most
    likely be \'1.1\' for most browsers.

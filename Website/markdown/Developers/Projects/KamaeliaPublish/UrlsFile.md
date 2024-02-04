---
pagename: Developers/Projects/KamaeliaPublish/UrlsFile
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
What is a URL file and how do I make one?
-----------------------------------------

\
A URL file is a standard INI file for routing web content.  It is
designed to route a web request to the proper WSGI application.  It is
divided up into sections and each section is further subdivided into
options.  An example is this section for the built-in WSGI application
simple\_app:\
\
\
\[simple\_app\]\
regex: simple\
import\_path: Kamaelia.Apps.WSGI.Simple\
app\_object: simple\_app\
\
\
This demonstrates the three most important settings in the URL file: 
the regex, the import\_path, and the app\_object.  Except in the
instance of the 404 handler, the section heading (the part in brackets)
is mostly irrelevant.\
\
**regex -** This is the regex that is used to determine if a URL matches
this application.  It is only tested against the first directory in the
URI.  Therefore, this regex would match www.domain.com/simple but not
www.domain.com/blah/simple.  Please note that a regex **should not** be
entered for the 404 handler.  It is assumed to be \".\*\"\
\
**import\_path -** This is the path to import the module containing the
WSGI application object.\
\
**app\_object - ** This is the name of the application object within the
module represented by import\_path.  Thus, for this example, the server
would pull the function simple\_app out of
plugins.WsgiApps.simple\_app.  If this is omitted, it is assumed to be
\"application\".\
\
Please also note that order *is* important in the URL file.  The
application listed first will be the first one that is evaluated.\
\
Every URLs file must also have a 404 handler.  It will be automatically
assigned a regex of \".\*\".  It will be evaluated last in the URL
routing no matter what position it is put in the list, but it is
typically a good idea to put it last in the URL list anyway.\
\
Any option in the URLs file will be passed to the WSGI application as an
environment variable and will be prepended with \"kp\" to distinct them
as Kamaelia Publish specific settings (although this will be present in
Kamaelia WebServe).  Thus, some applications require their own custom
settings.  Take for instance the built-in Paste application handler
(assuming that you want to serve a paste system described by a config
file config.ini):\
\
\[paste\_app\]\
regex: paste\
import\_path:  Kamaelia.Apps.WSGI.PasteApp\
paste\_source: config:/path/to/config.ini\
\
The custom keys \'kp.regex\', \'kp.import\_path\', and
\'kp.paste\_source\' will be passed to the application with the values
\'paste\', \'Kamaelia.Apps.WSGI.Paste\', and \'/path/to/config.ini\',
respectively.\

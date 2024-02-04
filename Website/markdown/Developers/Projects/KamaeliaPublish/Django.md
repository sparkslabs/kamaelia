---
pagename: Developers/Projects/KamaeliaPublish/Django
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
How do I get Django working with Kamaelia Publish?
--------------------------------------------------

\
It is possible to get Django working with Kamaelia Publish, however
Django support is highly experimental (as is Django\'s WSGI support). 
Kamaelia Publish includes a built in application for serving Django
applications located at plugins.WsgiApps.django\_app.  This app
(probably) requires two variables to be set in the urls file: 
project\_path and django\_path\_handling.\
\

-   project\_path is essentially the directory that contains your django
    project
-   django\_path\_handling is just a boolean value.  What you set it to
    isn\'t really important (I just use \"True\"), just as long as it is
    set to something other than an empty string.  This setting exists
    because django\'s path handling isn\'t very WSGI-centric.  It will
    essentially prepend the WSGI SCRIPT\_NAME environment variable to
    the beginning of the WSGI PATH\_INFO variable and store the result
    in PATH\_INFO.

### Please note that django support is still experimental (more so than integration with other frameworks) and as such probably won\'t work right for your purposes. 

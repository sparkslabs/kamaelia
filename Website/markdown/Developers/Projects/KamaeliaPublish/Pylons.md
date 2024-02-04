---
pagename: Developers/Projects/KamaeliaPublish/Pylons
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
How do I get Pylons working with Kamaelia Publish?
--------------------------------------------------

Kamaelia Publish includes a built-in application for serving Pylons and
Paste content.  This file is plugins.WsgiApps.paste\_app and the app
object is application.  The paste\_source custom attribute is also
required to be specified with the URI for either your config file or
egg.\
\

### Please note that Pylons support is still experimental and may very well break. 

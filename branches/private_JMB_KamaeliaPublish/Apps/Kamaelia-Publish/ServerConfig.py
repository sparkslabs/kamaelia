import os

#Server configuration info
PORT = 8082

#File structuring info
WsgiDir = '/WsgiApps'
WsgiAppLog = os.environ['HOME'] + '/kamaelia-publish-wsgi.log'
URL_LIST_LOCATION = '~/urls'

#This dictionary is used to configure various elements of the WsgiHandler
WsgiConfig ={
#-------------------
#General server info
#-------------------
'SERVER_SOFTWARE' : "Kamaelia Publish v 0.0.1",
'SERVER_ADMIN' : "jason.baker@ttu.edu",
'WSGI_VER' : (1,0),
'URI-FILE' : '~/.uris'
}

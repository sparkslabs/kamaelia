import os

#Server configuration info
PORT = 8082

#File structuring info
WsgiDir = '/WsgiApps'
WsgiAppLog = os.environ['HOME'] + '/kamaelia-publish-wsgi.log'

#This dictionary is used to configure various elements of the WsgiHandler
WsgiConfig ={
#-------------------
#General server info
#-------------------
'SERVER_SOFTWARE' : "Descartes prototype",
'SERVER_ADMIN' : "jason.baker@ttu.edu",
'WSGI_VER' : (1,0),
'URI-FILE' : '~/.uris'
}

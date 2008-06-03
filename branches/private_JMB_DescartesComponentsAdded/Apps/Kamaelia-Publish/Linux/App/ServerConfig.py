#general server configuration
PORT = 8082

#File structuring
WSGI_DIR = '/etc/WsgiApps'
WSGI_APP_LOG = WSGI_DIR + 'wsgi.log'

#This dictionary is used to configure various elements of the WsgiHandler
WsgiConfig ={
#-------------------
#General server info
#-------------------
'SERVER_SOFTWARE' : "Descartes prototype",
'SERVER_ADMIN' : "jason.baker@ttu.edu",
'WSGI_VER' : (1,0),
}

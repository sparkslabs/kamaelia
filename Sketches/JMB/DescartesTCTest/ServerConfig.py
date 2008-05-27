PORT = 8082

#This dictionary is used to configure various elements of the WsgiHandler
WsgiConfig ={
#-------------------
#General server info
#-------------------
'SERVER_SOFTWARE' : "Descartes prototype",
'SERVER_ADMIN' : "jason.baker@ttu.edu",
'WSGI_VER' : (1,0),


#------------------
#WSGI Directory info
#------------------
'WSGI_DIRECTORY' : 'Wsgi',
'APPS_SUBDIR' : 'Apps',
'LOG_NAME' : 'Apps.log',
}

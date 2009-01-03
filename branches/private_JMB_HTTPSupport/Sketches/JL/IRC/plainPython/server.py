#! /usr/bin/python
#server
#Can only accept one client.

import socket
import string 

def acceptClient(sock):
    client, address = sock.accept()
    nickInfo = client.recv(1000) #assumes that NICK is the first message received
    userInfo = client.recv(1000) #assumes that USER is the second message received
    nick = nickInfo.split()[1]
    userSplit = userInfo.split()
    username = userSplit[1]
    hostname = userSplit[2]
    servername = userSplit[3]
    realname = string.join(userSplit[4:], ' ')
    entry = {'nick': nick, 'uname': username, 'address': address,
             'hostname':hostname, 'servername':servername,
             'realname':realname}
    print entry
    table[client] = entry
    
    
def receive(client):
    print "Waiting for data"
    data = client.recv(1000)
    print data
    return data

def createSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((network, port))
    sock.listen(1)
    return sock

port = 6667
network = '127.0.0.1'
table = dict()

sock = createSocket()

print "Waiting for client to connect"
acceptClient(sock)

done = False
while not done:
    keys = table.keys()
    for one_key in keys:
        data = receive(one_key)
        if data == 'quit':
            done = True
        if 'JOIN' in data:
            info = table[one_key]
            one_key.send(':%s!n=%s@%s.%s JOIN %s' % (info['nick'], info['uname'],
                                                   info['hostname'],
                                                   info['servername'],
                                                   data[data.find('JOIN') + 5:]))

    
sock.close()


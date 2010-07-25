#! /usr/bin/python
# -*- coding: utf-8 -*-
#server
#Can only accept one client.
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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


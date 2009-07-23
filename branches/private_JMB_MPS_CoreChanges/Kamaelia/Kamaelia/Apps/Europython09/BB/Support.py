#!/usr/bin/python

import os
import cjson

class Folder(object):
    def __init__(self, folder="messages"):
        super(Folder, self).__init__()
        self.folder = folder
        try:
            f = open(self.folder + "/.meta")
            raw_meta = f.read()
            f.close()
            meta = cjson.decode(raw_meta)
        except IOError:
            meta = {"maxid": 0}
        self.meta = meta

    def getMessage(self, messageid):
        try:
            f = open(self.folder + "/" + str(messageid))
            message = f.read()
            f.close()
            message = cjson.decode(message)
            return message
        except IOError:
            return None

    def getMessages(self):
        messages = []
        for i in os.listdir(self.folder):
            if i[:1] == ".":
                continue
            messages.append(self.getMessage(i))
        return messages

def readUsers(path="users.passwd"):
    f = open(path)
    users = f.read()
    f.close()
    users = cjson.decode(users)
    return users

if __name__ == "__main__":
    users = readUsers()

#!/usr/bin/python

import inspect
import re

class Fail(Exception): pass

class Shardable(object):
    def __init__(self):
        super(Shardable,self).__init__()
        print "Initialising Shardable"
        self.IShards = {}

    def addMethod(self, name, method):
        self.__dict__[name] = lambda *args: method(self,*args)

    def addIShard(self, name, method):
        self.IShards[name] = method

    def initialShards(self, initial_shards):
        for name in initial_shards:
            self.addIShard(name, initial_shards[name])

    def checkDependencies(self):
        missing_methods = []
        missing_ishards = []
        for i in self.requires_methods:
            try:
                x = self.__getattribute__(i)
            except AttributeError, e:
                missing_methods.append(i)

        for i in self.requires_ishards:
            try:
                x = self.IShards[i]
            except KeyError, e:
                missing_ishards.append(i)

        if missing_methods != [] or missing_ishards != []:
            print "Class", self.__class__.__name__, "requires the following dependencies"
            print "   Missing Methods:", missing_methods
            print "   Missing IShards:", missing_ishards
            print
            raise Fail(missing_methods+missing_ishards)

    def getIShard(self, code_object_name, backup=""):
        try:
            IShard = inspect.getsource(self.IShards[code_object_name])
        except KeyError:
            IShard = ":\n"+backup
        IShard = IShard[re.search(":.*\n",IShard).end():] # strip def.*
        lines = []
        indent = -1
        for line in IShard.split("\n"):
            if indent == -1:
                r = line.strip()
                indent = len(line) - len(r)
                lines.append(r)
            else:
                lines.append(line[indent:])
        IShard = "\n".join(lines)
        return IShard

#!/usr/bin/python


import os

def isPythonFile(Path, File):
    FullEntry = os.path.join(Path, File)
    if os.path.isfile(FullEntry):
        if len(File) > 3:
            if File[-3:] == ".py":
                return True
    return False

def parseComponentLine(Line):
    components = [ x for x in Line[Line.find("(")+1:Line.rfind(")")].replace(" ", "").split(",") if x != ""]
    return components

def ComponentMeta(File):
    F = open(File)
    contents = F.readlines()
    F.close()
    meta = [ X for X in contents if "__kamaelia_components__" in X ]
    if meta != []:
        if len(meta)>1:
            print "WARNING: 2 component lines(!)"
            return []
        meta = parseComponentLine(meta[0])
    return meta

def SearchComponents(baseDirectory, Base):
    Entries = os.listdir(baseDirectory)
    result = {}
    for Entry in Entries:
        FullEntry = os.path.join(baseDirectory, Entry)
        if isPythonFile(baseDirectory, Entry):

            meta = ComponentMeta(FullEntry)
            Entry = Entry[:-3]
            if meta:
                result[ tuple( Base+[ Entry ] ) ] = meta
        elif os.path.isdir(FullEntry):
            subtree = SearchComponents(FullEntry, Base+[Entry])
            result.update(subtree)
    return result

def GetAllKamaeliaComponents():
    import Kamaelia
    installbase = os.path.dirname(Kamaelia.__file__)
    return SearchComponents(installbase, ["Kamaelia"])

import pprint
pprint.pprint(GetAllKamaeliaComponents(),None,4)

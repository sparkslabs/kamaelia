#!/bin/python


import os

def slurp(filename,binary=False):
    # print("OPEN:", filename)
    f = open(filename, "rb")
    x = f.read()
    if not binary:
        x = x.decode("utf-8")
    f.close()
    return x

def store(filename, contents, binary=False):
    if not binary:
        f = open(filename, "w")
    else:
        f = open(filename, "wb")
    f.write(contents)
    f.close()

def find(basedir, t="file"):
    if t != "file":
        raise NotImplementedError()
    #
    for i in os.listdir(basedir):
        p = os.path.join(basedir, i)
        if os.path.isdir(p):
            for j in find(p, t):
                yield j
        else:
            yield p


source = "markdown"
target = "auto-site"
pagetemplate = slurp("site-resources/page-template.html")

def copy(source, dest):
    data = slurp(source, binary=True)
    store(dest, data, binary=True)
    
destdir = os.path.join(target, "site-resources")
try:
    os.makedirs(destdir)
except FileExistsError:
    pass

for entry in find("site-resources"):
    filename = os.path.basename(entry)
    tfilename = os.path.join(destdir, filename)
    print(entry, tfilename)
    copy(entry, tfilename)

def head(count, gen):
    for i in range(count):
        yield next(gen)

for entry in find(source): #cd markdown; find -type f |while read filename; do
    filename = entry.replace("markdown/","")
    print(filename)                           # echo $filename
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)        # D=$(dirname $filename)
    tdirname = os.path.join(target, dirname)
    try:
        os.makedirs(tdirname)                # cd ../auto-site/ ; mkdir -p $D
    except FileExistsError:
        pass
    print("os.makedirs(tdirname)", tdirname) 
    corename = basename[:-3]                  # basename=`echo $filename | sed -e "s/.md$//g" ` # strip ".md"
    tfilename = os.path.join(tdirname, corename)+".html"
    command = 'pandoc %s -o %s' % (entry, tfilename)
    print(command)
    os.system(command)
    print()

    sourcepage = slurp(tfilename)
    newpage = pagetemplate.replace("%CONTENT GOES HERE%", sourcepage)
    store(tfilename, newpage)
